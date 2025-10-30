# Prydwen Scraper - Getting Started

## What We Built

A character build data scraper for HSR (Honkai Star Rail) that extracts information from Prydwen.gg and formats it into structured JSON.

## Project Structure

```
HsrMetaScrape/
├── metaScape/          # Original scraping scripts
│   ├── accurate_scraper.py
│   ├── all_modes_scraper.py
│   └── ... (all existing files moved here)
└── dataScape/          # New Prydwen.gg scraper
    ├── prydwen_scraper.py              # Selenium version (requires browser)
    ├── prydwen_scraper_simple.py       # Simple version (requests only) ✓
    ├── prydwen_kafka_build.json        # Example output
    ├── prydwen_kafka_page.html         # Saved page for debugging
    └── README.md                       # Documentation
```

## Output Format

The scraper generates JSON in this format:

```json
{
  "characterId": "kafka",
  "lightCones": [
    {
      "name": "Patience Is All You Need",
      "notes": "Best in slot for DoT damage"
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
    "subStats": ["CRIT Rate", "CRIT DMG", "ATK%", "Speed", "Break Effect"]
  }
}
```

## How to Use

### Option 1: Simple Version (Recommended for now)

The simple version uses `requests` and `BeautifulSoup` - no browser required!

```powershell
cd dataScape
python prydwen_scraper_simple.py
```

**Status:** ✅ Working! Successfully extracted:
- ✓ Character ID
- ✓ Relic sets (4 found for Kafka)
- ✓ Main stats (body, rope)
- ✓ Sub-stats (6 found)
- ⚠ Light cones (needs improvement - page is JS-rendered)
- ⚠ Planar sets (needs improvement)

### Option 2: Selenium Version (Full Power)

Requires Chrome or Edge browser installed:

```powershell
cd dataScape
python prydwen_scraper.py
```

**Status:** ⚠ Requires browser installation
- Needs Chrome or Microsoft Edge to be properly installed
- Will auto-detect and use available browser
- Better for JavaScript-heavy pages

## Current Results

### Test Run: Kafka

**Command:**
```powershell
python prydwen_scraper_simple.py
```

**Results:**
- ✓ Successfully scraped from https://www.prydwen.gg/star-rail/characters/kafka
- ✓ Extracted 4 relic sets: Prisoner in Deep Confinement, Pioneer Diver of Dead Waters, Band of Sizzling Thunder, Eagle of Twilight Line
- ✓ Extracted sub-stats: CRIT Rate, CRIT DMG, ATK%, Speed, Effect Hit Rate, Break Effect
- ⚠ Light cones need manual review (page uses JavaScript rendering)
- ⚠ Planar sets need manual review

## Next Steps

### To Improve Extraction:

1. **Install Chrome/Edge** for the Selenium version:
   - Download: https://www.google.com/chrome/
   - Or use Edge (pre-installed on Windows)
   - Run: `python prydwen_scraper.py`

2. **Customize for Other Characters:**
   Edit the character name in either script:
   ```python
   character_name = "raiden"  # or "acheron", "feixiao", etc.
   ```

3. **Batch Scraping:**
   Create a list of characters and loop through them:
   ```python
   characters = ["kafka", "raiden", "acheron", "feixiao"]
   for char in characters:
       data = scraper.scrape_character(char)
       scraper.save_to_json(data, f"prydwen_{char}_build.json")
   ```

### To Fix Light Cones & Planar Sets:

The simple version struggles with these because Prydwen.gg uses JavaScript to render the content. Two solutions:

1. **Use Selenium version** (requires browser):
   - Renders JavaScript
   - Can click on "Build and Teams" tab
   - Better extraction accuracy

2. **Improve selectors** in simple version:
   - Analyze the saved HTML file: `prydwen_kafka_page.html`
   - Find unique identifiers for light cones and planar sets
   - Update the extraction methods

## Files Created

- ✅ `prydwen_scraper.py` - Full Selenium version
- ✅ `prydwen_scraper_simple.py` - Simple requests version (working!)
- ✅ `prydwen_kafka_build.json` - Example output
- ✅ `prydwen_kafka_page.html` - Saved page for debugging
- ✅ `README.md` - Documentation
- ✅ `GETTING_STARTED.md` - This file!

## Dependencies Installed

```
selenium>=4.15.0
webdriver-manager>=4.0.0
```

(Also using existing: `requests`, `beautifulsoup4`, `lxml`, `pandas`)

## Tips

1. **Check the saved HTML files** to understand page structure
2. **Start with simple version** - it's working for most data!
3. **Manual review** the JSON output for accuracy
4. **Customize character names** by editing the script
5. **Use Selenium version** when you need 100% accuracy

## Questions?

- Review the `README.md` in dataScape for more details
- Check the saved HTML files to understand what's being scraped
- Look at the example JSON output to verify format

---

**Status:** ✅ Scraper is functional and producing structured JSON output!

**Next:** Install Chrome/Edge for improved extraction, or refine the simple version's selectors.
