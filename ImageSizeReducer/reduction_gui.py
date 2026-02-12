import os
import threading
import random
import time
import math
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import queue


class GlitchLabel(Label):
    """Label with glitch animation effect"""
    def __init__(self, master, **kwargs):
        self.original_text = kwargs.get('text', '')
        super().__init__(master, **kwargs)
        self.glitch_chars = "!@#$%^&*()_+-=[]{}|;':,.<>?/~`"
        self.is_glitching = False
        
    def glitch_effect(self, duration=300):
        if self.is_glitching:
            return
        self.is_glitching = True
        original = self.original_text
        
        def animate(step=0):
            if step < 8:
                # Create glitchy text
                glitched = ''.join(
                    random.choice(self.glitch_chars) if random.random() < 0.3 else c
                    for c in original
                )
                self.config(text=glitched)
                self.after(30, lambda: animate(step + 1))
            else:
                self.config(text=original)
                self.is_glitching = False
        
        animate()


class HexagonCanvas(Canvas):
    """Canvas with animated hexagonal pattern background"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.hexagons = []
        self.animation_running = False
        
    def draw_hexagons(self):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1:
            return
        
        hex_size = 30
        for y in range(-hex_size, height + hex_size, int(hex_size * 1.7)):
            for x in range(-hex_size, width + hex_size, int(hex_size * 1.5)):
                offset = hex_size * 0.75 if (y // int(hex_size * 1.7)) % 2 else 0
                opacity = random.randint(1, 3)
                color = f"#1a1a1a" if opacity == 1 else "#0a0a0a"
                self.create_hexagon(x + offset, y, hex_size, color)
    
    def create_hexagon(self, x, y, size, color):
        # Simplified hexagon
        hex_points = [
            x, y - size//2,
            x + size//2, y - size//4,
            x + size//2, y + size//4,
            x, y + size//2,
            x - size//2, y + size//4,
            x - size//2, y - size//4
        ]
        self.create_polygon(hex_points, fill=color, outline="#222222", width=1)


class ImageReducerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("◢ IMAGE COMPRESSION PROTOCOL ◣")
        self.root.geometry("900x750")
        self.root.resizable(False, False)
        self.root.configure(bg="#0a0a0a")
        
        # Set custom cursor for entire window
        self.root.config(cursor="crosshair")
        
        # Variables
        self.input_folder = StringVar()
        self.output_folder = StringVar()
        self.quality = IntVar(value=85)
        self.resize_enabled = BooleanVar(value=False)
        self.max_width = IntVar(value=1920)
        self.max_height = IntVar(value=1080)
        self.convert_png_to_jpg = BooleanVar(value=True)
        self.processing = False
        self.progress_queue = queue.Queue()
        
        # Animation variables
        self.scan_line_position = 0
        self.boot_sequence_complete = False
        self.stats_blink = False
        
        # Set default folders
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_folder.set(os.path.join(script_dir, "input"))
        self.output_folder.set(os.path.join(script_dir, "output"))
        
        self.setup_ui()
        self.start_boot_sequence()
        self.check_queue()
        self.animate_scanline()
    
    def setup_ui(self):
        # Hexagon background
        self.hex_canvas = HexagonCanvas(self.root, bg="#0a0a0a", highlightthickness=0)
        self.hex_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.after(100, self.hex_canvas.draw_hexagons)
        
        # Main container with border glow effect
        container = Frame(self.root, bg="#0a0a0a")
        container.place(relx=0.5, rely=0.5, anchor=CENTER, width=860, height=710)
        
        # Outer glow frame
        glow_frame = Frame(container, bg="#1a1a1a", highlightthickness=2, 
                          highlightbackground="#d4af37", highlightcolor="#d4af37")
        glow_frame.pack(fill=BOTH, expand=True, padx=2, pady=2)
        
        # Inner frame
        inner_frame = Frame(glow_frame, bg="#0f0f0f", highlightthickness=1,
                           highlightbackground="#3a3a3a")
        inner_frame.pack(fill=BOTH, expand=True, padx=3, pady=3)
        
        # Title Header with glitch effect
        title_frame = Frame(inner_frame, bg="#0a0a0a", height=80)
        title_frame.pack(fill=X)
        title_frame.pack_propagate(False)
        
        # Decorative corner elements
        corner_left = Label(title_frame, text="◢◤", font=("Consolas", 20, "bold"), 
                           bg="#0a0a0a", fg="#d4af37")
        corner_left.place(x=10, y=25)
        
        corner_right = Label(title_frame, text="◥◣", font=("Consolas", 20, "bold"), 
                            bg="#0a0a0a", fg="#d4af37")
        corner_right.place(relx=1.0, x=-50, y=25)
        
        # Main title with glitch effect
        self.title_label = GlitchLabel(title_frame, 
                                       text="IMAGE COMPRESSION PROTOCOL", 
                                       font=("Consolas", 20, "bold"), 
                                       bg="#0a0a0a", fg="#d4af37")
        self.title_label.original_text = "IMAGE COMPRESSION PROTOCOL"
        self.title_label.pack(pady=10)
        
        subtitle = Label(title_frame, text="[ SYSTEM INITIALIZED - AWAITING INPUT ]", 
                        font=("Consolas", 9), bg="#0a0a0a", fg="#00d4aa")
        subtitle.pack()
        
        # Scanline effect
        self.scanline = Frame(title_frame, bg="#d4af37", height=2)
        self.scanline.place(x=0, y=0, relwidth=1)
        
        # Main content frame
        main_frame = Frame(inner_frame, bg="#0f0f0f", padx=25, pady=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Folder Selection Section
        folder_frame = LabelFrame(main_frame, text="  ▶ DIRECTORY CONFIGURATION  ", 
                                 font=("Consolas", 10, "bold"), padx=15, pady=15,
                                 bg="#0f0f0f", fg="#d4af37", 
                                 highlightthickness=1, highlightbackground="#d4af37")
        folder_frame.pack(fill=X, pady=(0, 12))
        
        # Input folder
        Label(folder_frame, text="INPUT:", font=("Consolas", 9, "bold"), 
              bg="#0f0f0f", fg="#00d4aa").grid(row=0, column=0, sticky=W, pady=8)
        input_entry = Entry(folder_frame, textvariable=self.input_folder, width=55, state="readonly",
                           font=("Consolas", 9), bg="#1a1a1a", fg="#d4af37",
                           readonlybackground="#1a1a1a", relief=FLAT, 
                           insertbackground="#d4af37", highlightthickness=1,
                           highlightbackground="#3a3a3a", highlightcolor="#d4af37")
        input_entry.grid(row=0, column=1, padx=10, pady=8)
        self.add_entry_hover_effect(input_entry)
        
        btn_input = Button(folder_frame, text="◢ SCAN ◣", command=self.browse_input, width=12,
                          font=("Consolas", 9, "bold"), bg="#1a1a1a", fg="#d4af37",
                          activebackground="#d4af37", activeforeground="#0a0a0a",
                          relief=FLAT, cursor="target", highlightthickness=1,
                          highlightbackground="#d4af37")
        btn_input.grid(row=0, column=2, pady=8)
        self.add_hover_effect(btn_input, "#d4af37", "#1a1a1a")
        
        # Output folder
        Label(folder_frame, text="OUTPUT:", font=("Consolas", 9, "bold"),
              bg="#0f0f0f", fg="#00d4aa").grid(row=1, column=0, sticky=W, pady=8)
        output_entry = Entry(folder_frame, textvariable=self.output_folder, width=55, state="readonly",
                            font=("Consolas", 9), bg="#1a1a1a", fg="#d4af37",
                            readonlybackground="#1a1a1a", relief=FLAT,
                            insertbackground="#d4af37", highlightthickness=1,
                            highlightbackground="#3a3a3a", highlightcolor="#d4af37")
        output_entry.grid(row=1, column=1, padx=10, pady=8)
        self.add_entry_hover_effect(output_entry)
        
        btn_output = Button(folder_frame, text="◢ SCAN ◣", command=self.browse_output, width=12,
                           font=("Consolas", 9, "bold"), bg="#1a1a1a", fg="#d4af37",
                           activebackground="#d4af37", activeforeground="#0a0a0a",
                           relief=FLAT, cursor="target", highlightthickness=1,
                           highlightbackground="#d4af37")
        btn_output.grid(row=1, column=2, pady=8)
        self.add_hover_effect(btn_output, "#d4af37", "#1a1a1a")
        
        # Settings Section
        settings_frame = LabelFrame(main_frame, text="  ▶ COMPRESSION PARAMETERS  ", 
                                   font=("Consolas", 10, "bold"), padx=15, pady=15,
                                   bg="#0f0f0f", fg="#d4af37",
                                   highlightthickness=1, highlightbackground="#d4af37")
        settings_frame.pack(fill=X, pady=(0, 12))
        
        # Quality slider
        quality_frame = Frame(settings_frame, bg="#0f0f0f")
        quality_frame.pack(fill=X, pady=8)
        
        Label(quality_frame, text="QUALITY LEVEL:", font=("Consolas", 9, "bold"),
              bg="#0f0f0f", fg="#00d4aa").pack(side=LEFT)
        
        self.quality_label = Label(quality_frame, text="[085]", font=("Consolas", 11, "bold"), 
                                   bg="#0f0f0f", fg="#d4af37", width=6)
        self.quality_label.pack(side=RIGHT, padx=5)
        
        # Custom styled slider
        quality_slider_frame = Frame(quality_frame, bg="#0f0f0f")
        quality_slider_frame.pack(side=LEFT, fill=X, expand=True, padx=15)
        
        quality_slider = Scale(quality_slider_frame, from_=1, to=100, orient=HORIZONTAL, 
                              variable=self.quality, showvalue=0,
                              command=self.update_quality_display,
                              bg="#1a1a1a", fg="#d4af37", troughcolor="#0a0a0a",
                              highlightthickness=0, sliderrelief=FLAT,
                              activebackground="#d4af37", relief=FLAT, bd=0, cursor="target")
        quality_slider.pack(fill=X)
        self.add_slider_hover_effect(quality_slider)
        
        Label(settings_frame, text="// OPTIMAL RANGE: 75-90 | HIGHER VALUES = INCREASED FIDELITY", 
              font=("Consolas", 7), bg="#0f0f0f", fg="#3a3a3a").pack(anchor=W, pady=(0, 8))
        
        # Convert PNG to JPG option with custom checkbox styling
        check_frame = Frame(settings_frame, bg="#0f0f0f")
        check_frame.pack(anchor=W, pady=5)
        
        convert_check = Checkbutton(check_frame, text="◢ CONVERT PNG → JPG", 
                   variable=self.convert_png_to_jpg, font=("Consolas", 9, "bold"),
                   bg="#0f0f0f", fg="#00d4aa", selectcolor="#1a1a1a",
                   activebackground="#0f0f0f", activeforeground="#d4af37",
                   highlightthickness=0, cursor="hand2")
        convert_check.pack(side=LEFT)
        self.add_checkbox_hover_effect(convert_check)
        
        # Resize Section
        resize_frame = LabelFrame(main_frame, text="  ▶ DIMENSIONAL CONSTRAINTS  ", 
                                 font=("Consolas", 10, "bold"), padx=15, pady=15,
                                 bg="#0f0f0f", fg="#d4af37",
                                 highlightthickness=1, highlightbackground="#d4af37")
        resize_frame.pack(fill=X, pady=(0, 12))
        
        enable_frame = Frame(resize_frame, bg="#0f0f0f")
        enable_frame.pack(anchor=W, pady=(0, 10))
        
        enable_resize = Checkbutton(enable_frame, text="◢ ENABLE DIMENSIONAL OVERRIDE", 
                                   variable=self.resize_enabled, 
                                   command=self.toggle_resize,
                                   font=("Consolas", 9, "bold"),
                                   bg="#0f0f0f", fg="#00d4aa", selectcolor="#1a1a1a",
                                   activebackground="#0f0f0f", activeforeground="#d4af37",
                                   highlightthickness=0, cursor="hand2")
        enable_resize.pack(side=LEFT)
        self.add_checkbox_hover_effect(enable_resize)
        self.add_checkbox_hover_effect(enable_resize)
        
        dimension_frame = Frame(resize_frame, bg="#0f0f0f")
        dimension_frame.pack(fill=X)
        
        self.dimension_label_width = Label(dimension_frame, text="WIDTH:", 
                                          font=("Consolas", 9, "bold"),
                                          bg="#0f0f0f", fg="#00d4aa", state=DISABLED)
        self.dimension_label_width.grid(row=0, column=0, sticky=W, padx=(0, 8))
        
        self.width_entry = Spinbox(dimension_frame, from_=100, to=7680, textvariable=self.max_width, 
                                   width=12, font=("Consolas", 10, "bold"), state=DISABLED,
                                   bg="#1a1a1a", fg="#d4af37", buttonbackground="#1a1a1a",
                                   readonlybackground="#1a1a1a", relief=FLAT,
                                   highlightthickness=1, highlightbackground="#3a3a3a",
                                   insertbackground="#d4af37")
        self.width_entry.grid(row=0, column=1, padx=8)
        
        self.dimension_label_height = Label(dimension_frame, text="HEIGHT:", 
                                           font=("Consolas", 9, "bold"),
                                           bg="#0f0f0f", fg="#00d4aa", state=DISABLED)
        self.dimension_label_height.grid(row=0, column=2, sticky=W, padx=(25, 8))
        
        self.height_entry = Spinbox(dimension_frame, from_=100, to=4320, textvariable=self.max_height, 
                                    width=12, font=("Consolas", 10, "bold"), state=DISABLED,
                                    bg="#1a1a1a", fg="#d4af37", buttonbackground="#1a1a1a",
                                    readonlybackground="#1a1a1a", relief=FLAT,
                                    highlightthickness=1, highlightbackground="#3a3a3a",
                                    insertbackground="#d4af37")
        self.height_entry.grid(row=0, column=3, padx=8)
        
        Label(resize_frame, text="// PROPORTIONAL SCALING ALGORITHM ACTIVE", 
              font=("Consolas", 7), bg="#0f0f0f", fg="#3a3a3a").pack(anchor=W, pady=(8, 0))
        
        # Progress Section
        progress_frame = LabelFrame(main_frame, text="  ▶ OPERATION STATUS  ", 
                                   font=("Consolas", 10, "bold"), padx=15, pady=15,
                                   bg="#0f0f0f", fg="#d4af37",
                                   highlightthickness=1, highlightbackground="#d4af37")
        progress_frame.pack(fill=BOTH, expand=True, pady=(0, 12))
        
        # Progress bar container
        progress_container = Frame(progress_frame, bg="#0a0a0a", highlightthickness=1,
                                  highlightbackground="#d4af37")
        progress_container.pack(fill=X, pady=(0, 10))
        
        self.progress_var = DoubleVar()
        
        # Custom style for progress bar
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Custom.Horizontal.TProgressbar",
                       troughcolor='#0a0a0a',
                       bordercolor='#d4af37',
                       background='#d4af37',
                       lightcolor='#ffd700',
                       darkcolor='#d4af37',
                       thickness=20)
        
        self.progress_bar = ttk.Progressbar(progress_container, variable=self.progress_var, 
                                           maximum=100, mode='determinate',
                                           style="Custom.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=X, padx=2, pady=2)
        
        # Status text with glitch
        status_frame = Frame(progress_frame, bg="#0f0f0f")
        status_frame.pack(fill=X, pady=(0, 8))
        
        Label(status_frame, text=">>", font=("Consolas", 10, "bold"),
              bg="#0f0f0f", fg="#d4af37").pack(side=LEFT, padx=(0, 8))
        
        self.status_label = GlitchLabel(status_frame, text="SYSTEM READY - AWAITING COMMAND", 
                                       font=("Consolas", 9, "bold"), bg="#0f0f0f", fg="#00d4aa")
        self.status_label.original_text = "SYSTEM READY - AWAITING COMMAND"
        self.status_label.pack(side=LEFT, anchor=W)
        
        # Log text area with scrollbar (terminal style)
        log_frame = Frame(progress_frame, bg="#0a0a0a", highlightthickness=1,
                         highlightbackground="#d4af37")
        log_frame.pack(fill=BOTH, expand=True)
        
        scrollbar = Scrollbar(log_frame, bg="#1a1a1a", troughcolor="#0a0a0a",
                             activebackground="#d4af37")
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.log_text = Text(log_frame, height=6, wrap=WORD, font=("Consolas", 8), 
                            yscrollcommand=scrollbar.set, bg="#0a0a0a", fg="#00d4aa",
                            insertbackground="#d4af37", selectbackground="#d4af37",
                            selectforeground="#0a0a0a", relief=FLAT, padx=8, pady=8)
        self.log_text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Configure text tags for colored output
        self.log_text.tag_config("success", foreground="#00d4aa")
        self.log_text.tag_config("error", foreground="#ff4444")
        self.log_text.tag_config("warning", foreground="#ffa500")
        self.log_text.tag_config("info", foreground="#d4af37")
        
        # Action Buttons
        button_frame = Frame(main_frame, bg="#0f0f0f")
        button_frame.pack(fill=X, pady=(5, 0))
        
        # Main execute button with enhanced styling
        execute_container = Frame(button_frame, bg="#0a0a0a", highlightthickness=2,
                                  highlightbackground="#d4af37")
        execute_container.pack(side=LEFT, fill=X, expand=True, padx=(0, 8))
        
        self.process_button = Button(execute_container, 
                                     text="◢◤ EXECUTE COMPRESSION SEQUENCE ◥◣", 
                                     command=self.start_processing, 
                                     bg="#1a1a1a", fg="#d4af37", 
                                     font=("Consolas", 12, "bold"), 
                                     height=2, cursor="target", relief=FLAT,
                                     activebackground="#d4af37", 
                                     activeforeground="#0a0a0a",
                                     highlightthickness=0)
        self.process_button.pack(fill=BOTH, expand=True, padx=2, pady=2)
        self.add_button_pulse_effect(self.process_button, execute_container)
        
        # Clear log button
        clear_container = Frame(button_frame, bg="#0a0a0a", highlightthickness=2,
                               highlightbackground="#3a3a3a")
        clear_container.pack(side=LEFT, fill=X, expand=True)
        
        clear_btn = Button(clear_container, text="[ CLEAR LOG ]", command=self.clear_log, 
               bg="#1a1a1a", fg="#3a3a3a", font=("Consolas", 10, "bold"), 
               height=2, cursor="target", relief=FLAT,
               activebackground="#3a3a3a", activeforeground="#0a0a0a",
               highlightthickness=0)
        clear_btn.pack(fill=BOTH, expand=True, padx=2, pady=2)
        self.add_hover_effect(clear_btn, "#00d4aa", "#1a1a1a")
    
    def update_quality_display(self, value):
        """Update quality label with formatted value"""
        val = int(float(value))
        self.quality_label.config(text=f"[{val:03d}]")
    
    def start_boot_sequence(self):
        """Animated boot sequence"""
        boot_messages = [
            "INITIALIZING COMPRESSION PROTOCOLS...",
            "LOADING NEURAL MATRIX...",
            "CALIBRATING IMAGE PROCESSORS...",
            "SYSTEM READY"
        ]
        
        def show_message(index=0):
            if index < len(boot_messages):
                self.status_label.config(text=boot_messages[index])
                self.status_label.original_text = boot_messages[index]
                if index < len(boot_messages) - 1:
                    self.root.after(400, lambda: show_message(index + 1))
                else:
                    self.boot_sequence_complete = True
                    self.root.after(500, lambda: self.status_label.config(
                        text="SYSTEM READY - AWAITING COMMAND"))
                    self.status_label.original_text = "SYSTEM READY - AWAITING COMMAND"
        
        self.root.after(100, show_message)
    
    def animate_scanline(self):
        """Animate the scanline effect"""
        if hasattr(self, 'scanline'):
            self.scan_line_position = (self.scan_line_position + 5) % 900
            self.scanline.place(x=self.scan_line_position, y=0, width=100, height=2)
        self.root.after(50, self.animate_scanline)
    
    def add_hover_effect(self, widget, hover_bg, normal_bg, hover_fg=None, normal_fg=None):
        """Add hover glow effect to widgets"""
        original_bg = widget.cget('bg')
        original_fg = widget.cget('fg')
        
        def on_enter(e):
            widget.config(bg=hover_bg, fg=normal_bg if hover_fg is None else hover_fg)
            # Add glow effect by updating parent frame
            if hasattr(widget.master, 'config'):
                try:
                    widget.master.config(highlightbackground=hover_bg, highlightthickness=3)
                except:
                    pass
        
        def on_leave(e):
            widget.config(bg=normal_bg, fg=original_fg if normal_fg is None else normal_fg)
            # Remove glow
            if hasattr(widget.master, 'config'):
                try:
                    widget.master.config(highlightthickness=2)
                except:
                    pass
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def add_button_pulse_effect(self, button, container):
        """Add pulsing glow effect to main button"""
        original_bg = button.cget('bg')
        original_fg = button.cget('fg')
        
        def on_enter(e):
            # Start pulse animation
            self.pulse_button(button, container, 0)
            button.is_hovering = True
        
        def on_leave(e):
            button.is_hovering = False
            button.config(bg=original_bg, fg=original_fg)
            container.config(highlightbackground="#d4af37", highlightthickness=2)
        
        button.is_hovering = False
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
    
    def pulse_button(self, button, container, step):
        """Create pulsing animation"""
        if not hasattr(button, 'is_hovering') or not button.is_hovering:
            return
        
        # Calculate pulse intensity
        intensity = abs(math.sin(step * 0.2)) * 0.5 + 0.5
        
        # Interpolate colors
        base_color = int(0x1a * intensity + 0x0a * (1 - intensity))
        glow_color = int(0xd4 * intensity + 0xff * (1 - intensity))
        
        button.config(bg=f"#{base_color:02x}{base_color:02x}{base_color:02x}")
        container.config(highlightthickness=int(2 + intensity * 2))
        
        # Continue animation
        self.root.after(50, lambda: self.pulse_button(button, container, step + 1))
    
    def add_entry_hover_effect(self, entry):
        """Add hover effect to entry widgets"""
        def on_enter(e):
            entry.config(highlightbackground="#00d4aa", highlightcolor="#00d4aa", highlightthickness=2)
        
        def on_leave(e):
            entry.config(highlightbackground="#3a3a3a", highlightthickness=1)
        
        entry.bind('<Enter>', on_enter)
        entry.bind('<Leave>', on_leave)
    
    def add_slider_hover_effect(self, slider):
        """Add hover effect to slider widgets"""
        def on_enter(e):
            slider.config(troughcolor="#1a1a1a", activebackground="#00d4aa")
        
        def on_leave(e):
            slider.config(troughcolor="#0a0a0a", activebackground="#d4af37")
        
        slider.bind('<Enter>', on_enter)
        slider.bind('<Leave>', on_leave)
    
    def add_checkbox_hover_effect(self, checkbox):
        """Add hover effect to checkbox widgets"""
        original_fg = checkbox.cget('fg')
        
        def on_enter(e):
            checkbox.config(fg="#d4af37")
        
        def on_leave(e):
            checkbox.config(fg=original_fg)
        
        checkbox.bind('<Enter>', on_enter)
        checkbox.bind('<Leave>', on_leave)
    
    def toggle_resize(self):
        state = NORMAL if self.resize_enabled.get() else DISABLED
        self.width_entry.config(state=state)
        self.height_entry.config(state=state)
        self.dimension_label_width.config(state=state)
        self.dimension_label_height.config(state=state)
    
    def browse_input(self):
        folder = filedialog.askdirectory(title="Select Input Folder", 
                                        initialdir=self.input_folder.get())
        if folder:
            self.input_folder.set(folder)
    
    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder", 
                                        initialdir=self.output_folder.get())
        if folder:
            self.output_folder.set(folder)
    
    def clear_log(self):
        self.log_text.delete(1.0, END)
    
    def log(self, message, tag="info"):
        """Log message with color coding"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(END, formatted_message, tag)
        self.log_text.see(END)
        self.root.update_idletasks()
    
    def start_processing(self):
        if self.processing:
            messagebox.showwarning("Processing", "Already processing images!")
            return
        
        input_folder = self.input_folder.get()
        output_folder = self.output_folder.get()
        
        if not input_folder or not output_folder:
            messagebox.showerror("Error", "Please select both input and output folders!")
            return
        
        if not os.path.exists(input_folder):
            messagebox.showerror("Error", f"Input folder does not exist:\n{input_folder}")
            return
        
        # Check if there are any images in the input folder
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        image_files = [f for f in os.listdir(input_folder) 
                      if os.path.isfile(os.path.join(input_folder, f)) 
                      and os.path.splitext(f)[1].lower() in supported_formats]
        
        if not image_files:
            messagebox.showwarning("No Images", "No supported images found in the input folder!")
            return
        
        self.processing = True
        self.process_button.config(state=DISABLED, 
                                  text="◢◤ PROCESSING... ◥◣", 
                                  bg="#0a0a0a", fg="#ff4444")
        self.progress_var.set(0)
        self.clear_log()
        self.title_label.glitch_effect()
        self.status_label.config(text="COMPRESSION SEQUENCE INITIATED")
        self.status_label.original_text = "COMPRESSION SEQUENCE INITIATED"
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_images, daemon=True)
        thread.start()
    
    def process_images(self):
        try:
            input_folder = self.input_folder.get()
            output_folder = self.output_folder.get()
            quality = self.quality.get()
            max_size = (self.max_width.get(), self.max_height.get()) if self.resize_enabled.get() else None
            convert_png = self.convert_png_to_jpg.get()
            
            # Create output folder
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            
            supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
            
            # Get list of image files
            image_files = [f for f in os.listdir(input_folder) 
                          if os.path.isfile(os.path.join(input_folder, f)) 
                          and os.path.splitext(f)[1].lower() in supported_formats]
            
            total_files = len(image_files)
            processed_count = 0
            total_original_size = 0
            total_reduced_size = 0
            
            self.progress_queue.put(('status', f'PROCESSING {total_files} TARGETS...'))
            self.progress_queue.put(('log', f"{'='*70}", 'info'))
            self.progress_queue.put(('log', f"COMPRESSION PROTOCOL INITIATED", 'info'))
            self.progress_queue.put(('log', f"QUALITY PARAMETER: {quality} | DIMENSIONAL OVERRIDE: {max_size or 'DISABLED'}", 'info'))
            self.progress_queue.put(('log', f"PNG→JPG CONVERSION: {'ENABLED' if convert_png else 'DISABLED'}", 'info'))
            self.progress_queue.put(('log', f"{'='*70}\n", 'info'))
            
            for idx, filename in enumerate(image_files):
                file_path = os.path.join(input_folder, filename)
                file_ext = os.path.splitext(filename)[1].lower()
                
                try:
                    with Image.open(file_path) as img:
                        # Convert RGBA to RGB if saving as JPEG
                        if img.mode == 'RGBA' and (file_ext in {'.jpg', '.jpeg'} or convert_png):
                            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                            rgb_img.paste(img, mask=img.split()[3])
                            img = rgb_img
                        elif img.mode not in ('RGB', 'L'):
                            img = img.convert('RGB')
                        
                        # Resize if enabled
                        if max_size:
                            img.thumbnail(max_size, Image.Resampling.LANCZOS)
                        
                        # Prepare output path
                        output_path = os.path.join(output_folder, filename)
                        
                        # Convert PNG to JPG if option is enabled
                        if file_ext == '.png' and convert_png:
                            output_path = os.path.splitext(output_path)[0] + '.jpg'
                        
                        # Save with optimization
                        if file_ext in {'.jpg', '.jpeg'} or (file_ext == '.png' and convert_png):
                            img.save(output_path, 'JPEG', quality=quality, optimize=True)
                        elif file_ext == '.png':
                            img.save(output_path, 'PNG', optimize=True)
                        else:
                            img.save(output_path, optimize=True)
                        
                        # Track sizes
                        original_size = os.path.getsize(file_path)
                        reduced_size = os.path.getsize(output_path)
                        total_original_size += original_size
                        total_reduced_size += reduced_size
                        
                        reduction_percent = ((original_size - reduced_size) / original_size) * 100 if original_size > 0 else 0
                        
                        status = "COMPRESSED" if reduction_percent > 0 else "OPTIMIZED"
                        self.progress_queue.put(('log', 
                            f"[✓] {filename}", 'success'))
                        self.progress_queue.put(('log',
                            f"    {original_size/1024:.1f}KB → {reduced_size/1024:.1f}KB | {status}: {abs(reduction_percent):.1f}%", 'info'))
                        processed_count += 1
                        
                except Exception as e:
                    self.progress_queue.put(('log', f"[✗] ERROR: {filename} - {str(e)}", 'error'))
                
                # Update progress
                progress = ((idx + 1) / total_files) * 100
                self.progress_queue.put(('progress', progress))
            
            # Summary
            self.progress_queue.put(('log', f"\n{'='*70}", 'info'))
            self.progress_queue.put(('log', f"OPERATION COMPLETE", 'success'))
            self.progress_queue.put(('log', f"{'='*70}", 'info'))
            self.progress_queue.put(('log', f"PROCESSED: {processed_count}/{total_files} TARGETS", 'success'))
            self.progress_queue.put(('log', f"ORIGINAL SIZE: {total_original_size/1024/1024:.2f} MB", 'info'))
            self.progress_queue.put(('log', f"COMPRESSED SIZE: {total_reduced_size/1024/1024:.2f} MB", 'info'))
            
            if total_original_size > 0:
                total_reduction = ((total_original_size - total_reduced_size) / total_original_size) * 100
                saved_mb = (total_original_size - total_reduced_size) / 1024 / 1024
                self.progress_queue.put(('log', f"REDUCTION EFFICIENCY: {total_reduction:.1f}%", 'success'))
                self.progress_queue.put(('log', f"SPACE RECOVERED: {saved_mb:.2f} MB", 'success'))
            
            self.progress_queue.put(('log', f"{'='*70}", 'info'))
            self.progress_queue.put(('status', f'MISSION COMPLETE | {processed_count} TARGETS PROCESSED'))
            self.progress_queue.put(('done', True))
            self.progress_queue.put(('glitch', True))
            
        except Exception as e:
            self.progress_queue.put(('log', f"\n[✗] FATAL ERROR: {str(e)}", 'error'))
            self.progress_queue.put(('status', 'CRITICAL SYSTEM ERROR'))
            self.progress_queue.put(('done', False))
            self.progress_queue.put(('glitch', True))
    
    def check_queue(self):
        try:
            while True:
                msg = self.progress_queue.get_nowait()
                
                if len(msg) == 2:
                    msg_type, value = msg
                    tag = "info"
                else:
                    msg_type, value, tag = msg if len(msg) == 3 else (msg[0], msg[1], "info")
                
                if msg_type == 'log':
                    self.log(value, tag)
                elif msg_type == 'status':
                    self.status_label.config(text=value)
                    self.status_label.original_text = value
                elif msg_type == 'progress':
                    self.progress_var.set(value)
                elif msg_type == 'glitch':
                    self.title_label.glitch_effect()
                    self.status_label.glitch_effect()
                elif msg_type == 'done':
                    self.processing = False
                    self.process_button.config(state=NORMAL, 
                                             text="◢◤ EXECUTE COMPRESSION SEQUENCE ◥◣", 
                                             bg="#1a1a1a", fg="#d4af37")
                    if value:
                        # Create custom success dialog
                        self.show_completion_message("MISSION ACCOMPLISHED", 
                                                    "Compression sequence completed successfully.\nAll targets have been processed.")
                    else:
                        self.show_completion_message("SYSTEM ERROR", 
                                                    "An error occurred during the compression sequence.\nCheck the operation log for details.",
                                                    error=True)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)
    
    def show_completion_message(self, title, message, error=False):
        """Custom styled message box"""
        dialog = Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x200")
        dialog.configure(bg="#0a0a0a")
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Frame with border
        frame = Frame(dialog, bg="#0f0f0f", highlightthickness=2,
                     highlightbackground="#d4af37" if not error else "#ff4444")
        frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_color = "#ff4444" if error else "#d4af37"
        Label(frame, text=title, font=("Consolas", 14, "bold"),
              bg="#0f0f0f", fg=title_color).pack(pady=(20, 10))
        
        # Message
        Label(frame, text=message, font=("Consolas", 10),
              bg="#0f0f0f", fg="#00d4aa", justify=CENTER).pack(pady=10)
        
        # Button
        btn_frame = Frame(frame, bg="#0a0a0a", highlightthickness=1,
                         highlightbackground=title_color)
        btn_frame.pack(pady=(20, 20))
        
        ack_btn = Button(btn_frame, text="[ ACKNOWLEDGE ]", command=dialog.destroy,
               bg="#1a1a1a", fg=title_color, font=("Consolas", 10, "bold"),
               relief=FLAT, cursor="target", padx=20, pady=10,
               activebackground=title_color, activeforeground="#0a0a0a")
        ack_btn.pack(padx=2, pady=2)
        self.add_hover_effect(ack_btn, title_color, "#1a1a1a")
        self.add_hover_effect(ack_btn, title_color, "#1a1a1a")


def main():
    root = Tk()
    app = ImageReducerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
