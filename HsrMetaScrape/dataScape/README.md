# dataScape - Prydwen.gg Build Data Scraper

This folder contains tools for scraping character build data from Prydwen.gg.

## Purpose

Extract detailed character build information including:
- Light Cone recommendations
- Relic set recommendations (both regular and planar)
- Main stat priorities (Body, Feet, Sphere, Rope)
- Sub-stat priorities

## Files

- `prydwen_scraper.py` - Main Selenium-based scraper for Prydwen.gg character pages

## Setup

1. Install dependencies:
   ```powershell
   pip install selenium webdriver-manager
   ```

2. Ensure Chrome browser is installed (Selenium uses ChromeDriver)

## Usage

### Basic Usage

Run the scraper for a specific character:

```powershell
cd dataScape
python prydwen_scraper.py
```

By default, it scrapes Kafka's build data from: `https://www.prydwen.gg/star-rail/characters/kafka`

### Customize Character

Edit the `main()` function in `prydwen_scraper.py` to change the character:

```python
character_name = "kafka"  # Change to: "raiden", "acheron", etc.
```

### Using in Code

```python
from prydwen_scraper import PrydwenScraper

scraper = PrydwenScraper(headless=True)
character_data = scraper.scrape_character("kafka")
scraper.save_to_json(character_data, "kafka_build.json")
scraper.close()
```

## Output Format

The scraper produces JSON in the following format:

```json
{
  "characterId": "kafka",
  "lightCones": [
    {
      "name": "Patience Is All You Need",
      "notes": "Best in slot"
    }
  ],
  "relics": {
    "sets": [
      {
        "name": "Prisoner in Deep Confinement",
        "pieces": "4pc",
        "notes": "Best for DoT damage"
      }
    ],
    "planar": [
      {
        "name": "Firmament Frontline: Glamoth",
        "notes": "High speed builds"
      }
    ]
  },
  "stats": {
    "body": ["CRIT Rate", "CRIT DMG"],
    "feet": ["ATK%", "Speed"],
    "sphere": ["Lightning DMG", "ATK%"],
    "rope": ["ATK%", "Energy Regen"],
    "subStats": ["CRIT Rate", "CRIT DMG", "ATK%", "Speed"]
  }
}
```

## Notes

- The scraper navigates to the "Build and Teams" tab automatically
- Headless mode can be enabled/disabled in the constructor
- If extraction fails, it provides sensible defaults for manual review
- Chrome browser window will open during scraping (unless headless=True)

## Troubleshooting

- **ChromeDriver errors**: Make sure Chrome browser is up to date
- **Timeout errors**: Increase wait time in `WebDriverWait` constructor
- **Missing data**: Prydwen.gg may have changed their HTML structure - check selectors
