"""
Analysis module for Endfield Stock Tracker
Provides price analysis, trend detection, and trading recommendations
"""
import statistics
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta


class StockAnalyzer:
    def __init__(self, data_manager):
        self.dm = data_manager
    
    def calculate_statistics(self, item_name: str) -> Dict:
        """Calculate price statistics for an item"""
        history = self.dm.get_price_history(item_name)
        
        if not history:
            return {"error": "No price history"}
        
        # Extract all prices (handle both old single price and new multiple prices format)
        all_prices = []
        for entry in history:
            if "prices" in entry:
                all_prices.extend(entry["prices"])
            elif "price" in entry:
                all_prices.append(entry["price"])
        
        if not all_prices:
            return {"error": "No price data"}
        
        stats = {
            "item": item_name,
            "current_price": all_prices[-1],
            "min_price": min(all_prices),
            "max_price": max(all_prices),
            "avg_price": statistics.mean(all_prices),
            "median_price": statistics.median(all_prices),
            "price_range": max(all_prices) - min(all_prices),
            "volatility": statistics.stdev(all_prices) if len(all_prices) > 1 else 0,
            "data_points": len(all_prices)
        }
        
        # Calculate percentage from average
        stats["vs_avg_percent"] = ((stats["current_price"] - stats["avg_price"]) / stats["avg_price"] * 100) if stats["avg_price"] > 0 else 0
        
        # Calculate percentage from min/max
        stats["vs_min_percent"] = ((stats["current_price"] - stats["min_price"]) / stats["min_price"] * 100) if stats["min_price"] > 0 else 0
        stats["vs_max_percent"] = ((stats["current_price"] - stats["max_price"]) / stats["max_price"] * 100) if stats["max_price"] > 0 else 0
        
        return stats
    
    def detect_trend(self, item_name: str, days: int = 7) -> str:
        """Detect price trend over recent days"""
        history = self.dm.get_price_history(item_name)
        
        if len(history) < 2:
            return "insufficient_data"
        
        recent = history[-min(days, len(history)):]
        
        # Extract all prices from recent entries
        all_prices = []
        for entry in recent:
            if "prices" in entry:
                all_prices.extend(entry["prices"])
            elif "price" in entry:
                all_prices.append(entry["price"])
        
        # Simple trend: compare first and last of period
        if len(all_prices) >= 2:
            change = (all_prices[-1] - all_prices[0]) / all_prices[0] * 100
            if change > 5:
                return "upward"
            elif change < -5:
                return "downward"
            else:
                return "stable"
        
        return "unknown"
    
    def calculate_profit_potential(self, item_name: str) -> Dict:
        """Calculate potential profit for owned items"""
        portfolio = self.dm.get_portfolio().get(item_name, {})
        current_price = self.dm.get_latest_price(item_name)
        
        if not portfolio or not current_price or portfolio.get("owned", 0) == 0:
            return {"error": "No position or price data"}
        
        owned = portfolio["owned"]
        avg_cost = portfolio["average_cost"]
        current_value = owned * current_price
        invested = portfolio["total_invested"]
        
        profit = current_value - invested
        profit_percent = (profit / invested * 100) if invested > 0 else 0
        
        return {
            "item": item_name,
            "owned": owned,
            "average_cost": avg_cost,
            "current_price": current_price,
            "total_invested": invested,
            "current_value": current_value,
            "profit": profit,
            "profit_percent": profit_percent
        }
    
    def get_buy_recommendation(self, item_name: str) -> Dict:
        """Generate buy recommendation for an item"""
        stats = self.calculate_statistics(item_name)
        
        if "error" in stats:
            return {"recommendation": "wait", "reason": "Insufficient data", "confidence": 0}
        
        current = stats["current_price"]
        avg = stats["avg_price"]
        min_price = stats["min_price"]
        trend = self.detect_trend(item_name)
        
        score = 0
        reasons = []
        
        # Price below average is good
        if current < avg * 0.9:
            score += 30
            reasons.append(f"Price is {abs(stats['vs_avg_percent']):.1f}% below average")
        elif current < avg * 0.95:
            score += 20
            reasons.append(f"Price is {abs(stats['vs_avg_percent']):.1f}% below average")
        elif current > avg * 1.1:
            score -= 30
            reasons.append(f"Price is {stats['vs_avg_percent']:.1f}% above average")
        
        # Near minimum price is good
        if current <= min_price * 1.05:
            score += 25
            reasons.append("Near historical minimum")
        
        # Downward trend might continue
        if trend == "downward":
            score -= 15
            reasons.append("Downward trend detected - might drop more")
        elif trend == "upward":
            score -= 10
            reasons.append("Upward trend detected")
        
        # Determine recommendation
        if score >= 40:
            recommendation = "strong_buy"
        elif score >= 20:
            recommendation = "buy"
        elif score >= -10:
            recommendation = "hold"
        else:
            recommendation = "wait"
        
        return {
            "item": item_name,
            "recommendation": recommendation,
            "confidence": min(100, max(0, score + 50)),
            "reasons": reasons,
            "current_price": current,
            "average_price": avg,
            "min_price": min_price,
            "trend": trend
        }
    
    def get_sell_recommendation(self, item_name: str) -> Dict:
        """Generate sell recommendation for owned item"""
        stats = self.calculate_statistics(item_name)
        profit = self.calculate_profit_potential(item_name)
        
        if "error" in stats or "error" in profit:
            return {"recommendation": "hold", "reason": "Insufficient data", "confidence": 0}
        
        current = stats["current_price"]
        avg = stats["avg_price"]
        max_price = stats["max_price"]
        trend = self.detect_trend(item_name)
        profit_percent = profit["profit_percent"]
        
        score = 0
        reasons = []
        
        # High profit is good
        if profit_percent >= 100:
            score += 40
            reasons.append(f"Excellent profit: {profit_percent:.1f}%")
        elif profit_percent >= 50:
            score += 30
            reasons.append(f"Good profit: {profit_percent:.1f}%")
        elif profit_percent >= 20:
            score += 20
            reasons.append(f"Decent profit: {profit_percent:.1f}%")
        elif profit_percent < 0:
            score -= 30
            reasons.append(f"Currently at a loss: {profit_percent:.1f}%")
        
        # Price above average is good for selling
        if current > avg * 1.1:
            score += 25
            reasons.append(f"Price is {stats['vs_avg_percent']:.1f}% above average")
        elif current > avg * 1.05:
            score += 15
            reasons.append(f"Price is {stats['vs_avg_percent']:.1f}% above average")
        
        # Near maximum price is good
        if current >= max_price * 0.95:
            score += 20
            reasons.append("Near historical maximum")
        
        # Downward trend suggests sell
        if trend == "downward":
            score += 15
            reasons.append("Downward trend - might drop further")
        elif trend == "upward":
            score -= 10
            reasons.append("Upward trend - might rise more")
        
        # Determine recommendation
        if score >= 50:
            recommendation = "strong_sell"
        elif score >= 30:
            recommendation = "sell"
        elif score >= 0:
            recommendation = "hold"
        else:
            recommendation = "keep_holding"
        
        return {
            "item": item_name,
            "recommendation": recommendation,
            "confidence": min(100, max(0, score + 40)),
            "reasons": reasons,
            "current_price": current,
            "average_cost": profit["average_cost"],
            "profit": profit["profit"],
            "profit_percent": profit_percent,
            "trend": trend
        }
    
    def get_top_opportunities(self, limit: int = 5) -> List[Dict]:
        """Get top buying opportunities across all items"""
        opportunities = []
        
        for item_name in self.dm.get_all_items():
            rec = self.get_buy_recommendation(item_name)
            if rec["confidence"] > 0:
                opportunities.append(rec)
        
        # Sort by confidence
        opportunities.sort(key=lambda x: x["confidence"], reverse=True)
        return opportunities[:limit]
    
    def get_portfolio_summary(self) -> Dict:
        """Generate summary of entire portfolio"""
        portfolio = self.dm.get_portfolio()
        
        total_invested = 0
        total_current_value = 0
        items_owned = 0
        
        for item_name, holdings in portfolio.items():
            if holdings.get("owned", 0) > 0:
                items_owned += 1
                total_invested += holdings["total_invested"]
                current_price = self.dm.get_latest_price(item_name)
                if current_price:
                    total_current_value += holdings["owned"] * current_price
        
        total_profit = total_current_value - total_invested
        profit_percent = (total_profit / total_invested * 100) if total_invested > 0 else 0
        
        return {
            "items_owned": items_owned,
            "total_invested": total_invested,
            "current_value": total_current_value,
            "total_profit": total_profit,
            "profit_percent": profit_percent
        }
