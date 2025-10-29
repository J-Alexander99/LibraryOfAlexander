# HSR Meta Scraper

Automated scraper for Honkai: Star Rail tier list data from Prydwen.gg

## Purpose

This scraper automatically extracts character tier ratings from [Prydwen.gg's HSR tier list](https://www.prydwen.gg/star-rail/tier-list) and converts them to numerical ratings (1-10 scale). This allows you to automatically populate your app's character ratings without manual entry.

## Features

- ✅ Scrapes all 82+ characters from the tier list
- ✅ Converts tiers (T0, T0.5, T1... T5) to numerical ratings (10, 9, 8... 1)
- ✅ Extracts character roles (DPS, Support DPS, Amplifier, Sustain)
- ✅ Exports to both JSON and CSV formats
- ✅ Handles character name variations and encoding issues
- ✅ Respectful scraping with delays between requests

## Tier Rating Scale

| Tier | Rating | Description |
|------|--------|-------------|
| T0 | 10.0 | Apex Characters |
| T0.5 | 9.0 | High Apex |
| T1 | 8.0 | Meta Characters |
| T1.5 | 7.0 | High Meta |
| T2 | 6.0 | Viable |
| T2.5 | 5.0 | Niche |
| T3 | 4.0 | Off-Meta |
| T3.5 | 3.0 | Low Tier |
| T4 | 2.0 | Weak |
| T4.5 | 1.5 | Very Weak |
| T5 | 1.0 | The Forgotten Ones |

## Installation

### Requirements

```bash
pip install -r requirements.txt
```

Required packages:
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `lxml` - Fast parser
- `pandas` - Optional, for data manipulation

## Usage

### Quick Start

```bash
python accurate_scraper.py
```

This will:
1. Fetch the latest tier list from Prydwen.gg
2. Extract all character ratings using div class analysis
3. Generate `hsr_tier_ratings_accurate.json` and `hsr_tier_ratings_accurate.csv`

### Output Files

#### CSV Format (`hsr_tier_ratings_accurate.csv`)
```csv
Character,Tier,Rating (1-10),Role,URL
Acheron,T1,8.0,DPS,https://www.prydwen.gg/star-rail/characters/acheron
Aglaea,T0.5,9.0,DPS,https://www.prydwen.gg/star-rail/characters/aglaea
Anaxa,T0,10.0,DPS,https://www.prydwen.gg/star-rail/characters/anaxa
...
```

#### JSON Format (`hsr_tier_ratings_accurate.json`)
```json
{
  "timestamp": "2025-10-29T...",
  "source": "https://www.prydwen.gg/star-rail/tier-list",
  "tier_scale": {...},
  "characters": {
    "Acheron": {
      "tier": "T1",
      "rating": 8.0,
      "role": "DPS",
      "url": "/star-rail/characters/acheron"
    },
    ...
  }
}
```

### Programmatic Usage

```python
from accurate_scraper import HSRAccurateTierScraper

scraper = HSRAccurateTierScraper()

# Fetch and parse
html = scraper.fetch_page()
results = scraper.parse_tier_list(html)

# Access character data
for char_name, info in results.items():
    print(f"{char_name}: {info['rating']}/10 ({info['tier']}) - {info['role']}")

# Export
scraper.export_to_json(results, "my_ratings.json")
scraper.export_to_csv(results, "my_ratings.csv")
```

## Current Limitations

⚠️ **Important Notes:**

1. **Single Mode Only**: Currently scrapes only **Memory of Chaos (MoC)** ratings
   - Pure Fiction (PF) and Apocalyptic Shadow (AS) would require JavaScript interaction
   - The website uses tabs to switch between modes
   - Future enhancement: Use Selenium to automate tab clicks

2. **Static Snapshot**: Ratings are a point-in-time snapshot
   - Tier lists update regularly (check the timestamp in output)
   - Re-run the scraper to get latest data

3. **Accuracy**: Uses div class structure for high accuracy
   - Character tiers are determined by `custom-tier tier-X` div classes
   - Character names extracted from URL slugs for consistency

## Future Enhancements

### To scrape all 3 game modes:

1. **Option A: Selenium** - Click the mode tabs
   ```python
   # Install selenium
   pip install selenium webdriver-manager
   
   # Then use tier_scraper.py's scrape_with_selenium() method
   ```

2. **Option B: API Discovery** - Find if Prydwen has an API endpoint

3. **Option C: Multiple Page Loads** - Check if URL params can switch modes

## File Structure

```
HsrMetaScrape/
├── accurate_scraper.py              # ⭐ Main scraper (div-based, accurate)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── SOLUTION.md                      # Technical documentation
├── research_notes.md               # Initial research notes
├── hsr_tier_ratings_accurate.csv   # Output: CSV format
└── hsr_tier_ratings_accurate.json  # Output: JSON format
```

## Ethical Considerations

- ✅ Respects `robots.txt`
- ✅ Uses appropriate User-Agent headers
- ✅ Implements delays between requests (1 second)
- ✅ Minimal request frequency
- ✅ Gives credit to Prydwen.gg as data source

## Integration with Your App

Example: Update character ratings in bulk

```python
import csv

# Read the scraped data
with open('hsr_tier_ratings_accurate.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        char_name = row['Character']
        rating = float(row['Rating (1-10)'])
        tier = row['Tier']
        role = row['Role']
        
        # Update your app's database
        update_character_rating(char_name, 'moc', rating, tier, role)
```

## Troubleshooting

### No data extracted
- Check your internet connection
- Verify Prydwen.gg is accessible
- The website structure may have changed - check if div classes like `custom-tier tier-0` still exist

### Missing characters
- Some characters may not be rated yet
- Check the website manually to confirm

### Different tier counts than expected
- The scraper uses the div class structure (`tier-0`, `tier-05`, etc.)
- Verify the HTML structure hasn't changed using browser dev tools

## Credits

- Data source: [Prydwen.gg](https://www.prydwen.gg/star-rail/tier-list)
- Game: Honkai: Star Rail by HoYoverse

## License

This scraper is for personal/research use. Please respect Prydwen.gg's terms of service.
