"""
Data management module for Endfield Stock Tracker
Handles loading, saving, and managing stock data
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class DataManager:
    def __init__(self, data_file="stock_data.json"):
        self.data_file = data_file
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "items": {},
            "price_history": {},
            "transactions": [],
            "portfolio": {}
        }
    
    def save_data(self):
        """Save data to JSON file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def add_item(self, item_name: str, category: str = "Unknown"):
        """Add a new item to track"""
        if item_name not in self.data["items"]:
            self.data["items"][item_name] = {
                "name": item_name,
                "category": category,
                "added_date": datetime.now().isoformat()
            }
            self.data["price_history"][item_name] = []
            self.data["portfolio"][item_name] = {
                "owned": 0,
                "average_cost": 0,
                "total_invested": 0
            }
            self.save_data()
    
    def add_price(self, item_name: str, price: int, date: Optional[str] = None):
        """Add a price entry for an item (single price per day, replaces existing)"""
        if item_name not in self.data["items"]:
            self.add_item(item_name)
        
        if date is None:
            date = datetime.now().date().isoformat()
        
        # Check if price already exists for this date
        for entry in self.data["price_history"][item_name]:
            if entry["date"] == date and "prices" not in entry:
                entry["price"] = price
                self.save_data()
                return
        
        # Add new price entry
        self.data["price_history"][item_name].append({
            "date": date,
            "price": price,
            "timestamp": datetime.now().isoformat()
        })
        self.save_data()
    
    def add_price_entry(self, item_name: str, price: int, date: Optional[str] = None):
        """Add a price entry (allows multiple prices per day)"""
        if item_name not in self.data["items"]:
            self.add_item(item_name)
        
        if date is None:
            date = datetime.now().date().isoformat()
        
        # Find or create entry for this date
        entry = None
        for e in self.data["price_history"][item_name]:
            if e["date"] == date:
                entry = e
                break
        
        if entry is None:
            # Create new entry with prices list
            entry = {
                "date": date,
                "prices": [price],
                "timestamp": datetime.now().isoformat()
            }
            self.data["price_history"][item_name].append(entry)
        else:
            # Add to existing entry
            if "prices" not in entry:
                # Convert old format to new format
                entry["prices"] = [entry.pop("price", price)]
            entry["prices"].append(price)
        
        self.save_data()
    
    def record_transaction(self, item_name: str, transaction_type: str, 
                          quantity: int, price: int, date: Optional[str] = None):
        """Record a buy or sell transaction"""
        if date is None:
            date = datetime.now().date().isoformat()
        
        transaction = {
            "item": item_name,
            "type": transaction_type,  # "buy" or "sell"
            "quantity": quantity,
            "price": price,
            "total": quantity * price,
            "date": date,
            "timestamp": datetime.now().isoformat()
        }
        
        self.data["transactions"].append(transaction)
        
        # Update portfolio
        portfolio = self.data["portfolio"].get(item_name, {"owned": 0, "average_cost": 0, "total_invested": 0})
        
        if transaction_type == "buy":
            new_total = portfolio["total_invested"] + (quantity * price)
            new_quantity = portfolio["owned"] + quantity
            portfolio["total_invested"] = new_total
            portfolio["owned"] = new_quantity
            portfolio["average_cost"] = new_total / new_quantity if new_quantity > 0 else 0
        elif transaction_type == "sell":
            portfolio["owned"] -= quantity
            if portfolio["owned"] < 0:
                portfolio["owned"] = 0
            if portfolio["owned"] == 0:
                portfolio["total_invested"] = 0
                portfolio["average_cost"] = 0
        
        self.data["portfolio"][item_name] = portfolio
        self.save_data()
    
    def get_price_history(self, item_name: str) -> List[Dict]:
        """Get price history for an item"""
        return self.data["price_history"].get(item_name, [])
    
    def get_latest_price(self, item_name: str) -> Optional[int]:
        """Get the most recent price for an item (average if multiple prices)"""
        history = self.get_price_history(item_name)
        if history:
            last_entry = history[-1]
            if "prices" in last_entry:
                # Average of multiple prices
                return int(sum(last_entry["prices"]) / len(last_entry["prices"]))
            else:
                # Single price (old format)
                return last_entry.get("price")
        return None
    
    def get_price_range(self, item_name: str, date: Optional[str] = None) -> Optional[dict]:
        """Get price range for a specific date"""
        if date is None:
            date = datetime.now().date().isoformat()
        
        history = self.get_price_history(item_name)
        for entry in history:
            if entry["date"] == date:
                if "prices" in entry:
                    prices = entry["prices"]
                    return {
                        "min": min(prices),
                        "max": max(prices),
                        "avg": sum(prices) / len(prices),
                        "count": len(prices)
                    }
                elif "price" in entry:
                    price = entry["price"]
                    return {
                        "min": price,
                        "max": price,
                        "avg": price,
                        "count": 1
                    }
        return None
    
    def get_all_items(self) -> List[str]:
        """Get list of all tracked items"""
        return list(self.data["items"].keys())
    
    def get_portfolio(self) -> Dict:
        """Get current portfolio"""
        return self.data["portfolio"]
    
    def get_transactions(self, item_name: Optional[str] = None) -> List[Dict]:
        """Get transaction history, optionally filtered by item"""
        if item_name:
            return [t for t in self.data["transactions"] if t["item"] == item_name]
        return self.data["transactions"]
