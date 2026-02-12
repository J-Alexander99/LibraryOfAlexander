"""
Endfield Stock Tracker - Main GUI Application
Track market prices and get buy/sell recommendations
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
from PIL import Image, ImageTk
from data_manager import DataManager
from analyzer import StockAnalyzer
from ocr_handler import PriceOCR
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StockTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Endfield Stock Tracker")
        self.root.geometry("1200x800")
        
        # Initialize data manager and analyzer
        self.dm = DataManager("stock_data.json")
        self.analyzer = StockAnalyzer(self.dm)
        self.ocr = PriceOCR()
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Status bar (create before tabs since they use it)
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor='w')
        status_bar.pack(side='bottom', fill='x')
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_price_entry_tab()
        self.create_import_tab()
        self.create_portfolio_tab()
        self.create_recommendations_tab()
        self.create_transactions_tab()
        self.create_statistics_tab()
    
    def create_price_entry_tab(self):
        """Tab for entering daily prices"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Price Entry")
        
        # Top frame for new item
        top_frame = ttk.LabelFrame(tab, text="Add New Item", padding=10)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(top_frame, text="Item Name:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.new_item_entry = ttk.Entry(top_frame, width=40)
        self.new_item_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(top_frame, text="Add Item", command=self.add_new_item).grid(row=0, column=2, padx=5, pady=5)
        
        # Middle frame for price entry
        middle_frame = ttk.LabelFrame(tab, text="Update Prices", padding=10)
        middle_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create scrollable frame
        canvas = tk.Canvas(middle_frame)
        scrollbar = ttk.Scrollbar(middle_frame, orient="vertical", command=canvas.yview)
        self.price_entries_frame = ttk.Frame(canvas)
        
        self.price_entries_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.price_entries_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bottom frame for bulk update
        bottom_frame = ttk.Frame(tab)
        bottom_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(bottom_frame, text="Refresh Price List", command=self.refresh_price_entries).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="Update All Prices", command=self.update_all_prices).pack(side='left', padx=5)
        
        self.price_entries = {}
        self.refresh_price_entries()
    
    def create_import_tab(self):
        """Tab for importing prices from screenshots via OCR"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Import (OCR)")
        
        # Check OCR availability
        ocr_available, ocr_engine = self.ocr.is_available()
        
        if not ocr_available:
            warning_frame = ttk.LabelFrame(tab, text="OCR Not Available", padding=10)
            warning_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Get detailed error info
            error_details = self.ocr.get_error_messages()
            
            warning_text = """OCR functionality requires additional packages.

Install one of the following:

1. EasyOCR (Recommended):
   pip install pillow easyocr

2. Tesseract:
   pip install pillow pytesseract
   (Also requires Tesseract-OCR installation on your system)

After installation, restart the application.

---
Debug Information:
"""
            warning_text += error_details
            
            text_widget = tk.Text(warning_frame, wrap=tk.WORD, height=20, width=80)
            text_widget.insert('1.0', warning_text)
            text_widget.config(state='disabled')
            text_widget.pack(padx=10, pady=10, fill='both', expand=True)
            
            ttk.Button(warning_frame, text="Test Import Again", command=self.test_ocr_imports).pack(pady=10)
            return
        
        # OCR is available
        status_text = f"OCR Engine: {ocr_engine.upper()}"
        ttk.Label(tab, text=status_text, foreground='green', font=('Arial', 9, 'bold')).pack(pady=5)
        
        # Item selection frame
        select_frame = ttk.LabelFrame(tab, text="1. Select Item", padding=10)
        select_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(select_frame, text="Item:").pack(side='left', padx=5)
        self.import_item_var = tk.StringVar()
        self.import_item_combo = ttk.Combobox(select_frame, textvariable=self.import_item_var, width=40)
        self.import_item_combo.pack(side='left', padx=5)
        ttk.Button(select_frame, text="Refresh List", command=self.refresh_import_combo).pack(side='left', padx=5)
        
        # Image frame
        image_frame = ttk.LabelFrame(tab, text="2. Paste Screenshot from Clipboard", padding=10)
        image_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Image display
        self.import_image_label = ttk.Label(image_frame, text="No image loaded", relief='sunken')
        self.import_image_label.pack(fill='both', expand=True, padx=5, pady=5)
        
        button_frame = ttk.Frame(image_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="Paste from Clipboard", command=self.paste_screenshot).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Extract Prices (OCR)", command=self.extract_prices).pack(side='left', padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(tab, text="3. Confirm Extracted Prices", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Results display with scrollbar
        results_container = ttk.Frame(results_frame)
        results_container.pack(fill='both', expand=True)
        
        self.import_results_text = scrolledtext.ScrolledText(results_container, height=10, width=80)
        self.import_results_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Action buttons
        action_frame = ttk.Frame(results_frame)
        action_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(action_frame, text="Import All Prices", command=self.import_prices).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Clear", command=self.clear_import).pack(side='left', padx=5)
        
        # Store for extracted data
        self.current_image = None
        self.extracted_prices = []
        
        self.refresh_import_combo()
    
    def refresh_import_combo(self):
        """Refresh items combo in import tab"""
        items = sorted(self.dm.get_all_items())
        self.import_item_combo['values'] = items
        if items and not self.import_item_var.get():
            self.import_item_var.set(items[0])
    
    def paste_screenshot(self):
        """Paste image from clipboard"""
        image = self.ocr.get_clipboard_image()
        
        if image is None:
            messagebox.showerror("Error", "No image found in clipboard. Please copy a screenshot first.")
            return
        
        self.current_image = image
        
        # Display image (resize if too large)
        display_image = image.copy()
        max_width = 800
        max_height = 400
        
        if display_image.width > max_width or display_image.height > max_height:
            display_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(display_image)
        self.import_image_label.configure(image=photo, text="")
        self.import_image_label.image = photo  # Keep reference
        
        self.status_var.set(f"Image loaded: {image.width}x{image.height}")
    
    def extract_prices(self):
        """Extract prices from current image using OCR"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please paste an image first")
            return
        
        item = self.import_item_var.get()
        if not item:
            messagebox.showwarning("Warning", "Please select an item")
            return
        
        self.status_var.set("Extracting prices... (First time may take 30-60 seconds to load OCR models)")
        self.root.update()
        
        try:
            # Preprocess and extract
            processed_image = self.ocr.preprocess_image(self.current_image)
            self.extracted_prices = self.ocr.extract_numbers(processed_image)
        except Exception as e:
            messagebox.showerror("Error", f"OCR extraction failed: {str(e)}")
            self.status_var.set("OCR extraction failed")
            return
        
        # Display results
        if not self.extracted_prices:
            result_text = "No prices detected. Try:\n"
            result_text += "- Using a clearer screenshot\n"
            result_text += "- Ensuring prices are visible and not obstructed\n"
            result_text += "- Checking that the image contains numeric prices"
        else:
            result_text = f"Found {len(self.extracted_prices)} prices for '{item}':\n\n"
            
            # Group and count duplicates
            from collections import Counter
            price_counts = Counter(self.extracted_prices)
            
            for price, count in sorted(price_counts.items()):
                result_text += f"  {price:,}  (found {count}x)\n"
            
            result_text += f"\nTotal: {len(self.extracted_prices)} price entries\n"
            result_text += f"Average: {sum(self.extracted_prices) / len(self.extracted_prices):,.0f}\n"
            result_text += f"Min: {min(self.extracted_prices):,}  |  Max: {max(self.extracted_prices):,}"
        
        self.import_results_text.delete('1.0', tk.END)
        self.import_results_text.insert('1.0', result_text)
        
        self.status_var.set(f"Extracted {len(self.extracted_prices)} prices")
    
    def import_prices(self):
        """Import extracted prices to database"""
        if not self.extracted_prices:
            messagebox.showwarning("Warning", "No prices to import")
            return
        
        item = self.import_item_var.get()
        if not item:
            messagebox.showwarning("Warning", "Please select an item")
            return
        
        # Add all prices
        date = datetime.now().date().isoformat()
        for price in self.extracted_prices:
            self.dm.add_price_entry(item, price, date)
        
        messagebox.showinfo("Success", f"Imported {len(self.extracted_prices)} prices for {item}")
        
        self.status_var.set(f"Imported {len(self.extracted_prices)} prices for {item}")
        self.clear_import()
        self.refresh_price_entries()
    
    def clear_import(self):
        """Clear import data"""
        self.current_image = None
        self.extracted_prices = []
        self.import_image_label.configure(image='', text="No image loaded")
        self.import_results_text.delete('1.0', tk.END)
        self.status_var.set("Import cleared")
    
    def test_ocr_imports(self):
        """Test OCR imports and show results"""
        result = "Testing OCR imports...\n\n"
        
        # Test Pillow
        try:
            from PIL import Image, ImageGrab
            result += "✓ Pillow (PIL) is installed and working\n"
        except ImportError as e:
            result += f"✗ Pillow (PIL) import failed: {e}\n"
        
        # Test EasyOCR
        try:
            import easyocr
            result += "✓ EasyOCR is installed\n"
            try:
                reader = easyocr.Reader(['en'], gpu=False)
                result += "✓ EasyOCR initialized successfully\n"
            except Exception as e:
                result += f"✗ EasyOCR initialization failed: {e}\n"
        except ImportError as e:
            result += f"✗ EasyOCR import failed: {e}\n"
        
        # Test Tesseract
        try:
            import pytesseract
            result += "✓ pytesseract is installed\n"
        except ImportError as e:
            result += f"✗ pytesseract import failed: {e}\n"
        
        result += "\n---\nIf packages are missing, run:\npip install pillow easyocr\n"
        result += "\nThen restart the application."
        
        messagebox.showinfo("OCR Import Test", result)
    
    def create_portfolio_tab(self):
        """Tab for viewing portfolio"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Portfolio")
        
        # Summary frame
        summary_frame = ttk.LabelFrame(tab, text="Portfolio Summary", padding=10)
        summary_frame.pack(fill='x', padx=10, pady=10)
        
        self.portfolio_summary_text = tk.Text(summary_frame, height=4, width=80)
        self.portfolio_summary_text.pack(fill='x', padx=5, pady=5)
        
        # Holdings frame
        holdings_frame = ttk.LabelFrame(tab, text="Holdings", padding=10)
        holdings_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create treeview
        columns = ('Item', 'Owned', 'Avg Cost', 'Current Price', 'Value', 'Profit', 'Profit %')
        self.portfolio_tree = ttk.Treeview(holdings_frame, columns=columns, show='tree headings', height=15)
        
        # Column headings
        self.portfolio_tree.heading('#0', text='')
        self.portfolio_tree.column('#0', width=0, stretch=False)
        
        for col in columns:
            self.portfolio_tree.heading(col, text=col)
            if col == 'Item':
                self.portfolio_tree.column(col, width=200)
            else:
                self.portfolio_tree.column(col, width=100, anchor='e')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(holdings_frame, orient='vertical', command=self.portfolio_tree.yview)
        self.portfolio_tree.configure(yscrollcommand=scrollbar.set)
        
        self.portfolio_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Buttons
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Refresh", command=self.refresh_portfolio).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Record Transaction", command=self.open_transaction_dialog).pack(side='left', padx=5)
        
        self.refresh_portfolio()
    
    def create_recommendations_tab(self):
        """Tab for buy/sell recommendations"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Recommendations")
        
        # Buy recommendations
        buy_frame = ttk.LabelFrame(tab, text="Top Buying Opportunities", padding=10)
        buy_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.buy_recommendations_text = scrolledtext.ScrolledText(buy_frame, height=12, width=80, wrap=tk.WORD)
        self.buy_recommendations_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Sell recommendations
        sell_frame = ttk.LabelFrame(tab, text="Sell Recommendations (Owned Items)", padding=10)
        sell_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.sell_recommendations_text = scrolledtext.ScrolledText(sell_frame, height=12, width=80, wrap=tk.WORD)
        self.sell_recommendations_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Refresh Recommendations", command=self.refresh_recommendations).pack(side='left', padx=5)
        
        self.refresh_recommendations()
    
    def create_transactions_tab(self):
        """Tab for transaction history"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Transactions")
        
        # Transaction list
        columns = ('Date', 'Type', 'Item', 'Quantity', 'Price', 'Total')
        self.transactions_tree = ttk.Treeview(tab, columns=columns, show='tree headings', height=25)
        
        self.transactions_tree.heading('#0', text='')
        self.transactions_tree.column('#0', width=0, stretch=False)
        
        for col in columns:
            self.transactions_tree.heading(col, text=col)
            if col == 'Item':
                self.transactions_tree.column(col, width=250)
            elif col == 'Type':
                self.transactions_tree.column(col, width=80)
            else:
                self.transactions_tree.column(col, width=100, anchor='e')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=self.transactions_tree.yview)
        self.transactions_tree.configure(yscrollcommand=scrollbar.set)
        
        self.transactions_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Buttons
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Refresh", command=self.refresh_transactions).pack(side='left', padx=5)
        
        self.refresh_transactions()
    
    def create_statistics_tab(self):
        """Tab for item statistics"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Statistics")
        
        # Selection frame
        select_frame = ttk.Frame(tab)
        select_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(select_frame, text="Select Item:").pack(side='left', padx=5)
        self.stats_item_var = tk.StringVar()
        self.stats_item_combo = ttk.Combobox(select_frame, textvariable=self.stats_item_var, width=40)
        self.stats_item_combo.pack(side='left', padx=5)
        ttk.Button(select_frame, text="Show Statistics", command=self.show_statistics).pack(side='left', padx=5)
        
        # Create paned window for graph and text
        paned = ttk.PanedWindow(tab, orient='vertical')
        paned.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Graph frame
        graph_frame = ttk.LabelFrame(paned, text="Price History (Last 30 Days)", padding=10)
        paned.add(graph_frame, weight=1)
        
        # Create matplotlib figure
        self.stats_figure = Figure(figsize=(10, 4), dpi=100)
        self.stats_plot = self.stats_figure.add_subplot(111)
        self.stats_canvas = FigureCanvasTkAgg(self.stats_figure, graph_frame)
        self.stats_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Statistics text frame
        text_frame = ttk.LabelFrame(paned, text="Detailed Statistics", padding=10)
        paned.add(text_frame, weight=1)
        
        self.statistics_text = scrolledtext.ScrolledText(text_frame, height=15, width=80, wrap=tk.WORD)
        self.statistics_text.pack(fill='both', expand=True)
        
        self.refresh_statistics_combo()
    
    def add_new_item(self):
        """Add a new item to track"""
        item_name = self.new_item_entry.get().strip()
        if not item_name:
            messagebox.showwarning("Warning", "Please enter an item name")
            return
        
        self.dm.add_item(item_name)
        self.new_item_entry.delete(0, tk.END)
        self.refresh_price_entries()
        self.refresh_statistics_combo()
        self.status_var.set(f"Added item: {item_name}")
    
    def refresh_price_entries(self):
        """Refresh the price entry fields"""
        # Clear existing entries
        for widget in self.price_entries_frame.winfo_children():
            widget.destroy()
        
        self.price_entries = {}
        items = sorted(self.dm.get_all_items())
        
        # Header
        ttk.Label(self.price_entries_frame, text="Item Name", font=('Arial', 9, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self.price_entries_frame, text="Current Price", font=('Arial', 9, 'bold')).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.price_entries_frame, text="New Price", font=('Arial', 9, 'bold')).grid(row=0, column=2, padx=5, pady=5)
        
        # Create entry for each item
        for idx, item in enumerate(items, start=1):
            current_price = self.dm.get_latest_price(item)
            
            ttk.Label(self.price_entries_frame, text=item).grid(row=idx, column=0, padx=5, pady=2, sticky='w')
            ttk.Label(self.price_entries_frame, text=str(current_price) if current_price else "N/A").grid(row=idx, column=1, padx=5, pady=2)
            
            entry = ttk.Entry(self.price_entries_frame, width=15)
            entry.grid(row=idx, column=2, padx=5, pady=2)
            self.price_entries[item] = entry
        
        self.status_var.set(f"Loaded {len(items)} items")
    
    def update_all_prices(self):
        """Update all entered prices"""
        updated = 0
        for item, entry in self.price_entries.items():
            price_text = entry.get().strip()
            if price_text:
                try:
                    price = int(price_text)
                    self.dm.add_price(item, price)
                    entry.delete(0, tk.END)
                    updated += 1
                except ValueError:
                    messagebox.showerror("Error", f"Invalid price for {item}: {price_text}")
                    return
        
        self.refresh_price_entries()
        self.status_var.set(f"Updated {updated} prices")
        messagebox.showinfo("Success", f"Updated {updated} item prices")
    
    def refresh_portfolio(self):
        """Refresh portfolio display"""
        # Clear existing items
        for item in self.portfolio_tree.get_children():
            self.portfolio_tree.delete(item)
        
        # Get summary
        summary = self.analyzer.get_portfolio_summary()
        summary_text = f"""Total Items: {summary['items_owned']}
Total Invested: {summary['total_invested']:,}
Current Value: {summary['current_value']:,}
Total Profit: {summary['total_profit']:+,} ({summary['profit_percent']:+.2f}%)"""
        
        self.portfolio_summary_text.delete('1.0', tk.END)
        self.portfolio_summary_text.insert('1.0', summary_text)
        
        # Add portfolio items
        portfolio = self.dm.get_portfolio()
        for item_name, holdings in sorted(portfolio.items()):
            if holdings.get("owned", 0) > 0:
                current_price = self.dm.get_latest_price(item_name)
                if current_price:
                    owned = holdings["owned"]
                    avg_cost = holdings["average_cost"]
                    current_value = owned * current_price
                    profit = current_value - holdings["total_invested"]
                    profit_percent = (profit / holdings["total_invested"] * 100) if holdings["total_invested"] > 0 else 0
                    
                    values = (
                        item_name,
                        f"{owned}",
                        f"{avg_cost:.0f}",
                        f"{current_price}",
                        f"{current_value:,}",
                        f"{profit:+,.0f}",
                        f"{profit_percent:+.2f}%"
                    )
                    
                    # Color code by profit
                    tag = 'profit' if profit > 0 else 'loss' if profit < 0 else 'neutral'
                    item_id = self.portfolio_tree.insert('', 'end', values=values, tags=(tag,))
        
        # Configure tags
        self.portfolio_tree.tag_configure('profit', foreground='green')
        self.portfolio_tree.tag_configure('loss', foreground='red')
        self.portfolio_tree.tag_configure('neutral', foreground='black')
        
        self.status_var.set("Portfolio refreshed")
    
    def refresh_recommendations(self):
        """Refresh buy/sell recommendations"""
        # Buy recommendations
        buy_recs = self.analyzer.get_top_opportunities(10)
        buy_text = "TOP BUYING OPPORTUNITIES\n" + "="*80 + "\n\n"
        
        for i, rec in enumerate(buy_recs, 1):
            buy_text += f"{i}. {rec['item']}\n"
            buy_text += f"   Recommendation: {rec['recommendation'].upper().replace('_', ' ')}\n"
            buy_text += f"   Confidence: {rec['confidence']:.0f}%\n"
            buy_text += f"   Current Price: {rec['current_price']:,} (Avg: {rec['average_price']:.0f}, Min: {rec['min_price']})\n"
            buy_text += f"   Trend: {rec['trend'].capitalize()}\n"
            buy_text += "   Reasons:\n"
            for reason in rec['reasons']:
                buy_text += f"   • {reason}\n"
            buy_text += "\n"
        
        self.buy_recommendations_text.delete('1.0', tk.END)
        self.buy_recommendations_text.insert('1.0', buy_text)
        
        # Sell recommendations
        sell_text = "SELL RECOMMENDATIONS (OWNED ITEMS)\n" + "="*80 + "\n\n"
        
        portfolio = self.dm.get_portfolio()
        sell_recs = []
        
        for item_name, holdings in portfolio.items():
            if holdings.get("owned", 0) > 0:
                rec = self.analyzer.get_sell_recommendation(item_name)
                if rec["confidence"] > 0:
                    sell_recs.append(rec)
        
        sell_recs.sort(key=lambda x: x["confidence"], reverse=True)
        
        for i, rec in enumerate(sell_recs, 1):
            sell_text += f"{i}. {rec['item']}\n"
            sell_text += f"   Recommendation: {rec['recommendation'].upper().replace('_', ' ')}\n"
            sell_text += f"   Confidence: {rec['confidence']:.0f}%\n"
            sell_text += f"   Current Price: {rec['current_price']:,} (Bought at: {rec['average_cost']:.0f})\n"
            sell_text += f"   Profit: {rec['profit']:+,.0f} ({rec['profit_percent']:+.2f}%)\n"
            sell_text += f"   Trend: {rec['trend'].capitalize()}\n"
            sell_text += "   Reasons:\n"
            for reason in rec['reasons']:
                sell_text += f"   • {reason}\n"
            sell_text += "\n"
        
        if not sell_recs:
            sell_text += "No items owned or insufficient data for recommendations.\n"
        
        self.sell_recommendations_text.delete('1.0', tk.END)
        self.sell_recommendations_text.insert('1.0', sell_text)
        
        self.status_var.set("Recommendations refreshed")
    
    def refresh_transactions(self):
        """Refresh transaction history"""
        # Clear existing items
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
        
        # Get transactions (most recent first)
        transactions = self.dm.get_transactions()
        transactions.reverse()
        
        for trans in transactions:
            values = (
                trans['date'],
                trans['type'].upper(),
                trans['item'],
                trans['quantity'],
                f"{trans['price']:,}",
                f"{trans['total']:,}"
            )
            
            tag = 'buy' if trans['type'] == 'buy' else 'sell'
            self.transactions_tree.insert('', 'end', values=values, tags=(tag,))
        
        # Configure tags
        self.transactions_tree.tag_configure('buy', foreground='blue')
        self.transactions_tree.tag_configure('sell', foreground='green')
        
        self.status_var.set(f"Showing {len(transactions)} transactions")
    
    def show_statistics(self):
        """Show statistics for selected item"""
        item = self.stats_item_var.get()
        if not item:
            messagebox.showwarning("Warning", "Please select an item")
            return
        
        stats = self.analyzer.calculate_statistics(item)
        
        if "error" in stats:
            self.statistics_text.delete('1.0', tk.END)
            self.statistics_text.insert('1.0', f"No data available for {item}")
            # Clear graph
            self.stats_plot.clear()
            self.stats_plot.text(0.5, 0.5, 'No data available', 
                                ha='center', va='center', fontsize=12)
            self.stats_canvas.draw()
            return
        
        # Generate graph
        self.plot_price_history(item)
        
        # Format statistics text
        text = f"STATISTICS FOR: {item}\n"
        text += "="*80 + "\n\n"
        
        text += "CURRENT PRICES:\n"
        text += f"  Current Price: {stats['current_price']:,}\n"
        text += f"  Minimum Price: {stats['min_price']:,}\n"
        text += f"  Maximum Price: {stats['max_price']:,}\n"
        text += f"  Average Price: {stats['avg_price']:,.0f}\n"
        text += f"  Median Price: {stats['median_price']:,.0f}\n\n"
        
        text += "RELATIVE POSITION:\n"
        text += f"  vs. Average: {stats['vs_avg_percent']:+.2f}%\n"
        text += f"  vs. Minimum: {stats['vs_min_percent']:+.2f}%\n"
        text += f"  vs. Maximum: {stats['vs_max_percent']:+.2f}%\n\n"
        
        text += "VOLATILITY:\n"
        text += f"  Price Range: {stats['price_range']:,}\n"
        text += f"  Standard Deviation: {stats['volatility']:.2f}\n"
        text += f"  Data Points: {stats['data_points']}\n\n"
        
        # Price history
        history = self.dm.get_price_history(item)
        text += "RECENT PRICE HISTORY:\n"
        for entry in history[-20:]:
            if "prices" in entry:
                # Multiple prices per day
                avg_price = sum(entry["prices"]) / len(entry["prices"])
                min_price = min(entry["prices"])
                max_price = max(entry["prices"])
                text += f"  {entry['date']}: {avg_price:,.0f} avg ({len(entry['prices'])} entries: {min_price:,}-{max_price:,})\n"
            else:
                # Single price (old format)
                text += f"  {entry['date']}: {entry['price']:,}\n"
        
        self.statistics_text.delete('1.0', tk.END)
        self.statistics_text.insert('1.0', text)
        
        self.status_var.set(f"Statistics for {item}")
    
    def plot_price_history(self, item: str):
        """Plot price history graph for the last 30 days"""
        history = self.dm.get_price_history(item)
        
        if not history:
            return
        
        # Get last 30 days of data
        today = datetime.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        dates = []
        avg_prices = []
        min_prices = []
        max_prices = []
        
        for entry in history:
            entry_date = datetime.fromisoformat(entry['date']).date()
            
            if entry_date >= thirty_days_ago:
                dates.append(entry_date)
                
                if "prices" in entry:
                    # Multiple prices
                    avg_prices.append(sum(entry["prices"]) / len(entry["prices"]))
                    min_prices.append(min(entry["prices"]))
                    max_prices.append(max(entry["prices"]))
                else:
                    # Single price
                    price = entry["price"]
                    avg_prices.append(price)
                    min_prices.append(price)
                    max_prices.append(price)
        
        # Clear previous plot
        self.stats_plot.clear()
        
        if not dates:
            self.stats_plot.text(0.5, 0.5, 'No data in last 30 days', 
                                ha='center', va='center', fontsize=12)
        else:
            # Plot average prices as points connected by lines
            self.stats_plot.plot(dates, avg_prices, marker='o', linestyle='-', 
                                linewidth=2, markersize=6, label='Average Price', color='#2E86AB')
            
            # Add shaded area for min/max range if there are multiple prices per day
            if any(min_prices[i] != max_prices[i] for i in range(len(dates))):
                self.stats_plot.fill_between(dates, min_prices, max_prices, 
                                            alpha=0.2, color='#2E86AB', label='Price Range')
            
            self.stats_plot.set_xlabel('Date', fontsize=10)
            self.stats_plot.set_ylabel('Price', fontsize=10)
            self.stats_plot.set_title(f'Price History - {item}', fontsize=12, fontweight='bold')
            self.stats_plot.grid(True, alpha=0.3)
            self.stats_plot.legend(loc='best')
            
            # Format y-axis with commas
            self.stats_plot.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
                lambda x, p: f'{int(x):,}'
            ))
            
            # Rotate date labels for better readability
            self.stats_figure.autofmt_xdate()
        
        self.stats_canvas.draw()
    
    def refresh_statistics_combo(self):
        """Refresh the items combo box in statistics tab"""
        items = sorted(self.dm.get_all_items())
        self.stats_item_combo['values'] = items
        if items and not self.stats_item_var.get():
            self.stats_item_var.set(items[0])
    
    def open_transaction_dialog(self):
        """Open dialog to record a transaction"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Record Transaction")
        dialog.geometry("400x300")
        
        # Item selection
        ttk.Label(dialog, text="Item:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        item_var = tk.StringVar()
        item_combo = ttk.Combobox(dialog, textvariable=item_var, width=30)
        item_combo['values'] = sorted(self.dm.get_all_items())
        item_combo.grid(row=0, column=1, padx=10, pady=10)
        
        # Transaction type
        ttk.Label(dialog, text="Type:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        type_var = tk.StringVar(value="buy")
        ttk.Radiobutton(dialog, text="Buy", variable=type_var, value="buy").grid(row=1, column=1, sticky='w', padx=10)
        ttk.Radiobutton(dialog, text="Sell", variable=type_var, value="sell").grid(row=1, column=1, sticky='e', padx=10)
        
        # Quantity
        ttk.Label(dialog, text="Quantity:").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        quantity_entry = ttk.Entry(dialog, width=32)
        quantity_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Price
        ttk.Label(dialog, text="Price:").grid(row=3, column=0, padx=10, pady=10, sticky='w')
        price_entry = ttk.Entry(dialog, width=32)
        price_entry.grid(row=3, column=1, padx=10, pady=10)
        
        def save_transaction():
            item = item_var.get()
            trans_type = type_var.get()
            
            try:
                quantity = int(quantity_entry.get())
                price = int(price_entry.get())
                
                if not item:
                    messagebox.showwarning("Warning", "Please select an item")
                    return
                
                self.dm.record_transaction(item, trans_type, quantity, price)
                self.status_var.set(f"Recorded {trans_type}: {quantity}x {item} @ {price}")
                dialog.destroy()
                
                # Refresh displays
                self.refresh_portfolio()
                self.refresh_transactions()
                
            except ValueError as e:
                messagebox.showerror("Error", "Please enter valid numbers for quantity and price")
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save", command=save_transaction).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=10)


def main():
    root = tk.Tk()
    app = StockTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
