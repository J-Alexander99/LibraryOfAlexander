# HSR Tier List Scraper - All Modes Complete ✅

## Success Summary

Successfully implemented **multi-mode tier list scraping** using Selenium to extract data from all three game modes:

### Results:
- ✅ **Memory of Chaos (MoC)**: 77 characters extracted
- ✅ **Pure Fiction (PF)**: 77 characters extracted  
- ✅ **Apocalyptic Shadow (AS)**: 77 characters extracted
- 📊 **Total entries**: 231 (77 characters × 3 modes)

## Technical Implementation

### Method:
1. **Selenium WebDriver** - Automated Chrome browser to handle JavaScript tabs
2. **Tab Clicking** - Clicked through `.tier-list-switcher.hsr .option` divs (3 tabs)
3. **Div-Based Extraction** - Used proven accurate_scraper.py logic for each mode
4. **Multi-Mode Export** - Combined data with mode labels

### Key Features:
- Headless browser mode (no GUI)
- 2-second wait between tab clicks for content loading
- Preserved working div class extraction logic (tier-0, tier-05, etc.)
- Automatic tier → rating conversion (T0=10, T1=8, T2=6, etc.)
- Role detection (DPS, Support, Sustain, etc.)

## Output Files

### 1. hsr_tier_ratings_all_modes.csv
**Structure:**
```
Mode, Mode Name, Character, Tier, Rating, Role, URL
MoC, Memory of Chaos, Acheron, T1, 8.0, DPS, /star-rail/characters/acheron
PF, Pure Fiction, Acheron, T0.5, 9.0, DPS, /star-rail/characters/acheron
AS, Apocalyptic Shadow, Acheron, T1, 8.0, DPS, /star-rail/characters/acheron
```

**Features:**
- 231 rows (77 chars × 3 modes)
- Mode column for filtering (MoC, PF, AS)
- 1-10 rating scale
- Character roles and URLs

### 2. hsr_tier_ratings_all_modes.json
**Structure:**
```json
{
  "MoC": {
    "mode": "Memory of Chaos",
    "count": 77,
    "characters": {
      "Acheron": {
        "tier": "T1",
        "rating": 8.0,
        "role": "DPS",
        "url": "/star-rail/characters/acheron"
      },
      ...
    }
  },
  "PF": { ... },
  "AS": { ... }
}
```

## Sample Data

### T0 Characters by Mode:

**Memory of Chaos (13 T0 chars):**
- Anaxa, Archer, Castorice, Cerydra, Dan Heng • Imbibitor Lunae, Hyacine, Hysilens, Kafka, March 7th (Evernight), Phainon, Sunday, Trailblazer (Remembrance), Tribbie

**Pure Fiction (9 T0 chars):**
- Castorice, Hyacine, Hysilens, Jade, Jing Yuan, March 7th (Evernight), Phainon, The Herta, Tribbie

**Apocalyptic Shadow (12 T0 chars):**
- Aglaea, Anaxa, Castorice, Cerydra, Feixiao, Firefly, Hyacine, Lingsha, March 7th (Evernight), Phainon, Tribbie, Yunli

### Tier Distribution Example (MoC):
- T0: 13 characters (Rating 10)
- T0.5: 14 characters (Rating 9)
- T1: 11 characters (Rating 8)
- T1.5: 7 characters (Rating 7)
- T2: 6 characters (Rating 6)
- T3: 4 characters (Rating 4)
- T4: 6 characters (Rating 2)
- T5: 16 characters (Rating 1)

## Usage

### Run the Scraper:
```powershell
python all_modes_scraper.py
```

### Load CSV Data:
```python
import pandas as pd
df = pd.read_csv('hsr_tier_ratings_all_modes.csv')

# Filter by mode
moc = df[df['Mode'] == 'MoC']
pf = df[df['Mode'] == 'PF']
as_mode = df[df['Mode'] == 'AS']

# Find T0 DPS characters in Pure Fiction
t0_pf_dps = df[(df['Mode'] == 'PF') & (df['Tier'] == 'T0') & (df['Role'] == 'DPS')]
```

### Load JSON Data:
```python
import json
with open('hsr_tier_ratings_all_modes.json', encoding='utf-8') as f:
    data = json.load(f)

# Access specific mode
moc_chars = data['MoC']['characters']
acheron_moc = moc_chars['Acheron']
print(f"Acheron in MoC: {acheron_moc['tier']} ({acheron_moc['rating']}/10)")
```

## Files

### Production Files:
- ✅ `all_modes_scraper.py` - Selenium-based multi-mode scraper
- ✅ `accurate_scraper.py` - Original single-mode scraper (still works)
- ✅ `hsr_tier_ratings_all_modes.csv` - Multi-mode CSV export
- ✅ `hsr_tier_ratings_all_modes.json` - Multi-mode JSON export
- ✅ `requirements.txt` - Dependencies

### Dependencies:
```
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
pandas>=2.0.0
selenium>=4.15.0
```

## Notes

- **Chrome driver auto-installed** by Selenium 4.15+
- **Headless mode** runs without browser window (can disable by setting `headless=False`)
- **Tab detection** automatically finds all 3 mode tabs
- **Character count** may vary if Prydwen updates their tier list
- **Same characters appear in all modes** but with different tier assignments

## Comparison: Mode-Specific Differences

Characters can have **different tier ratings** depending on game mode:

**Example - Acheron:**
- MoC: T1 (Rating 8)
- PF: T0.5 (Rating 9)
- AS: T1 (Rating 8)

This reflects how character performance varies across different endgame content types!

---

**Status**: ✅ **COMPLETE** - All three game modes successfully scraped and exported!
