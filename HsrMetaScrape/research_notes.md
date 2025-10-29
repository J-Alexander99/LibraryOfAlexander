# Prydwen.gg Star Rail Scraping Research

## Website Overview
- **Target URL**: https://www.prydwen.gg/star-rail
- **Purpose**: Scrape character data, tier lists, and meta information for Honkai: Star Rail

## Key Pages Identified

### 1. Main Page (https://www.prydwen.gg/star-rail)
- Active redemption codes
- Event timeline
- Quick links to guides and resources

### 2. Characters List (https://www.prydwen.gg/star-rail/characters)
- Shows 79 characters (as of October 2025)
- Filterable by:
  - Rarity (4★, 5★)
  - Element (Physical, Fire, Ice, Lightning, Wind, Quantum, Imaginary)
  - Path (Abundance, Destruction, Erudition, Harmony, Hunt, Nihility, Preservation, Remembrance)

### 3. Tier List (https://www.prydwen.gg/star-rail/tier-list)
- Three separate tier lists:
  - **Memory of Chaos (MoC)**: Blast and single target damage
  - **Pure Fiction (PF)**: AoE damage focused
  - **Apocalyptic Shadow (AS)**: Single target and Break potential
- Tier categories:
  - T0: Apex Characters
  - T1: Meta Characters
  - T2: (Visible in structure)
  - T3: Off-Meta Characters
  - T4: (Lower tier)
  - T5: The Forgotten Ones
- Character roles: DPS, SUPPORT DPS, AMPLIFIER, SUSTAIN
- Tags: DEBUFF, SP-FRIENDLY, SP-UNFRIENDLY, PARTNER, ADVANCE, BREAK, BUFF, DOT, etc.

### 4. Individual Character Pages
- Pattern: https://www.prydwen.gg/star-rail/characters/{character-name}
- Example: https://www.prydwen.gg/star-rail/characters/acheron

## Data Structure to Extract

### Character Data
- **Name**: Character name
- **Rarity**: 4★ or 5★
- **Element**: Physical, Fire, Ice, Lightning, Wind, Quantum, Imaginary
- **Path**: Abundance, Destruction, Erudition, Harmony, Hunt, Nihility, Preservation, Remembrance
- **Eidolon Level**: E0-E6 (for tier ratings)
- **Tags**: Various gameplay characteristics

### Tier List Data
- **Character Name**
- **Tier**: T0-T5
- **Category**: Apex, Meta, Off-Meta, Forgotten
- **Role**: DPS, Support DPS, Amplifier, Sustain
- **Mode Performance**: Separate ratings for MoC, PF, AS
- **Tags**: Gameplay modifiers and characteristics

## Technical Considerations

### Website Type
- Appears to be a modern JavaScript-based site (likely React/Gatsby based on structure)
- May require:
  - Selenium/Playwright for dynamic content
  - Or API endpoint discovery if they have a backend API
  - BeautifulSoup might work if content is server-side rendered

### Potential Challenges
1. **Dynamic Content Loading**: Character cards may load via JavaScript
2. **Anti-Scraping Measures**: Rate limiting, bot detection
3. **Data Updates**: Tier lists update regularly (last update: 15/10/2025)
4. **Pagination**: Check if character list is paginated

### Ethical Considerations
- Respect robots.txt
- Implement rate limiting (delay between requests)
- Cache data to minimize requests
- Consider reaching out for API access if available

## Next Steps

### Phase 1: Basic Scraping
1. Check robots.txt: https://www.prydwen.gg/robots.txt
2. Test with requests + BeautifulSoup
3. If that fails, try Selenium/Playwright

### Phase 2: Data Extraction
1. Extract character list with basic info
2. Extract tier list data for all three modes
3. Map characters to their tier ratings

### Phase 3: Individual Character Pages
1. Build scraper for detailed character information
2. Extract builds, light cones, relics recommendations
3. Extract skill descriptions and stats

### Phase 4: Data Storage
1. Design JSON/CSV structure for scraped data
2. Implement database if needed (SQLite?)
3. Add timestamp tracking for updates

## Required Libraries

```python
# Basic scraping
requests
beautifulsoup4
lxml

# Dynamic content (if needed)
selenium
webdriver-manager

# Alternative to Selenium
playwright

# Data handling
pandas
json
```

## Legal/Ethical Notes
- Always check and respect robots.txt
- Add User-Agent to requests
- Implement delays between requests (1-2 seconds minimum)
- Cache responses to avoid repeated requests
- Consider that this is community-maintained data
- Check if they have a public API or data export option
