# Endfield Stock Tracker

A comprehensive tool for tracking market prices and managing your investment portfolio in games with dynamic market systems.

## Features

- **Price Tracking**: Record daily prices for multiple items
- **OCR Import**: Paste screenshots and automatically extract prices from ~40 friends' listings
- **Portfolio Management**: Track your holdings, average costs, and profits
- **Transaction History**: Complete record of all buy/sell transactions
- **Smart Recommendations**: AI-powered buy/sell recommendations based on:
  - Price trends and patterns
  - Historical price data
  - Volatility analysis
  - Profit potential
- **Statistical Analysis**: Detailed statistics for each item including min/max/average prices, volatility, and more

## Installation

### 1. Install Python packages

```bash
pip install -r requirements.txt
```

This installs:
- **Pillow**: Image handling and clipboard access
- **EasyOCR**: Optical character recognition for price extraction

### 2. Run the application

```bash
python main.py
```

## Usage

### Tabs Overview

1. **Price Entry**: Manually add new items and update daily prices
2. **Import (OCR)**: Paste screenshots to automatically extract multiple prices
3. **Portfolio**: View your holdings and current profit/loss
4. **Recommendations**: Get buy/sell recommendations
5. **Transactions**: View complete transaction history
6. **Statistics**: Detailed analysis for individual items

### OCR Import Workflow

1. In the game, open the market and take a screenshot showing your friends' prices (Ctrl+PrintScreen or Snipping Tool)
2. Copy the screenshot to clipboard
3. Go to the **Import (OCR)** tab
4. Select the item you're importing prices for
5. Click **"Paste from Clipboard"** - the screenshot appears
6. Click **"Extract Prices (OCR)"** - the app reads all price numbers
7. Review the extracted prices (it shows you counts, min/max, average)
8. Click **"Import All Prices"** to add them to your database

The OCR can handle ~40 different prices from your friends list in one screenshot!

## How Recommendations Work

### Buy Recommendations
- **Strong Buy**: Price significantly below average, near historical minimum
- **Buy**: Price below average with favorable conditions
- **Hold**: Price near average
- **Wait**: Price above average or downward trend expected

### Sell Recommendations (for owned items)
- **Strong Sell**: High profit, price near maximum, or downward trend
- **Sell**: Good profit opportunity
- **Hold**: Wait for better conditions
- **Keep Holding**: Upward trend or not yet profitable

## Tips for Best Results

1. **Enter Data Consistently**: Update prices daily for better trend analysis
2. **Record All Transactions**: Keep accurate portfolio records
3. **Wait for Data**: Recommendations improve with more historical data
4. **Consider Market Context**: Use recommendations as guidance, not absolute rules
5. **Diversify**: Don't invest everything in one item

## Data Storage

All data is stored in `stock_data.json` in the same directory. You can back this up to preserve your data.

## Example Items (from screenshots)

- Ankhorilling Kitchenware
- Musbeast Scrimshaw Dangles
- Witchcraft Mining Drill
- Aggeloi War Tins
- Valley Hydroculture Fillets
- Unity Syrup
- Seagaman Knucklebones
- Originium Saplings
- Vigilant Pickaxes
- Astarron Crystals
- Hard Noggin Helmets
- Scrap Toy Blocks

## Technical Details

- Built with Python and Tkinter
- No external dependencies required beyond standard library
- JSON-based data storage for portability
- Statistical analysis using standard deviation for volatility
- Trend detection using price change analysis
