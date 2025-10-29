# HSR Tier List Scraper - Final Solution

## ✅ Accurate Div-Based Scraper

The **`accurate_scraper.py`** is the recommended scraper that uses the div class structure to accurately determine character tiers.

### How It Works

The scraper identifies character tiers by examining the CSS classes on the divs containing character links:

```html
<!-- Example from the actual HTML -->
<div class="custom-tier tier-0 first">
  <a href="/star-rail/characters/anaxa">
    <!-- Character: Anaxa, Tier: T0 (10/10) -->
  </a>
</div>

<div class="custom-tier tier-05">
  <a href="/star-rail/characters/aglaea">
    <!-- Character: Aglaea, Tier: T0.5 (9/10) -->
  </a>
</div>
```

### Div Class to Tier Mapping

| Div Class | Tier | Rating |
|-----------|------|--------|
| `tier-0` | T0 | 10.0 |
| `tier-05` | T0.5 | 9.0 |
| `tier-1` | T1 | 8.0 |
| `tier-15` | T1.5 | 7.0 |
| `tier-2` | T2 | 6.0 |
| `tier-25` | T2.5 | 5.0 |
| `tier-3` | T3 | 4.0 |
| `tier-35` | T3.5 | 3.0 |
| `tier-4` | T4 | 2.0 |
| `tier-45` | T4.5 | 1.5 |
| `tier-5` | T5 | 1.0 |

## Usage

```bash
python accurate_scraper.py
```

### Output

**`hsr_tier_ratings_accurate.csv`**
```csv
Character,Tier,Rating (1-10),Role,URL
Anaxa,T0,10.0,DPS,https://www.prydwen.gg/star-rail/characters/anaxa
Aglaea,T0.5,9.0,DPS,https://www.prydwen.gg/star-rail/characters/aglaea
Acheron,T1,8.0,DPS,https://www.prydwen.gg/star-rail/characters/acheron
...
```

**`hsr_tier_ratings_accurate.json`**
```json
{
  "timestamp": "2025-10-29T...",
  "characters": {
    "Anaxa": {
      "tier": "T0",
      "rating": 10.0,
      "role": "DPS",
      "url": "/star-rail/characters/anaxa"
    },
    ...
  }
}
```

## Latest Results (Oct 29, 2025)

- **Total Characters**: 77
- **T0 (10/10)**: 13 characters - Anaxa, Archer, Castorice, Cerydra, Dan Heng • Imbibitor Lunae, Hyacine, Hysilens, Kafka, March 7th (Evernight), Phainon, Sunday, The Herta, Tribbie
- **T0.5 (9/10)**: 14 characters
- **T1 (8/10)**: 11 characters
- **T1.5 (7/10)**: 7 characters
- **T2 (6/10)**: 6 characters
- **T3 (4/10)**: 4 characters
- **T4 (2/10)**: 6 characters
- **T5 (1/10)**: 16 characters

## Advantages Over Previous Approach

1. **More Accurate**: Uses the actual tier structure from the HTML
2. **No Text Parsing**: Doesn't rely on parsing character names from text
3. **Cleaner Names**: Extracts names from URL slugs (more reliable)
4. **Role Detection**: Identifies character roles (DPS, Support, Sustain)
5. **Handles Duplicates**: Keeps highest tier if character appears multiple times

## Character Name Handling

The scraper converts URL slugs to proper character names:

| URL Slug | Character Name |
|----------|----------------|
| `anaxa` | Anaxa |
| `march-7th-evernight` | March 7th (Evernight) |
| `dan-heng-permansor-terrae` | Dan Heng • Imbibitor Lunae |
| `dr-ratio` | Dr. Ratio |

## Integration Example

```python
import csv

# Read the accurate tier ratings
with open('hsr_tier_ratings_accurate.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        character = row['Character']
        rating = float(row['Rating (1-10)'])
        tier = row['Tier']
        role = row['Role']
        
        print(f"{character}: {tier} ({rating}/10) - {role}")
        # Update your app database here
```

## Files

- **`accurate_scraper.py`** ⭐ - RECOMMENDED: Div-based accurate scraper
- **`hsr_tier_ratings_accurate.csv`** - CSV output from accurate scraper
- **`hsr_tier_ratings_accurate.json`** - JSON output from accurate scraper
- **`requirements.txt`** - Python dependencies
- **`README.md`** - User documentation
- **`SOLUTION.md`** - Technical documentation (this file)
- **`research_notes.md`** - Initial research notes

## Notes

- Currently scrapes **Memory of Chaos (MoC)** mode only
- To scrape Pure Fiction and Apocalyptic Shadow, would need Selenium to switch tabs
- Character names are standardized from URL slugs for consistency
- Roles are detected from div classes (DPS, SUPPORT DPS, SUPPORT, SUSTAIN)
