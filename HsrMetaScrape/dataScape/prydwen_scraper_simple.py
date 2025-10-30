"""
Prydwen.gg Character Build Scraper - Simplified Version
Uses requests + BeautifulSoup for initial testing
Note: May need Selenium for dynamic content if page requires JavaScript
"""

import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List
import re


class PrydwenScraperSimple:
    def __init__(self):
        """Initialize the simple scraper"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def scrape_character(self, character_name: str) -> Dict:
        """
        Scrape build data for a character from Prydwen.gg
        
        Args:
            character_name: The character name as it appears in the URL (e.g., 'kafka')
        
        Returns:
            Dictionary with character build data
        """
        url = f"https://www.prydwen.gg/star-rail/characters/{character_name}"
        print(f"Fetching {url}...")
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            print(f"✓ Page loaded successfully (status: {response.status_code})")
        except requests.RequestException as e:
            print(f"✗ Error fetching page: {e}")
            return self._create_empty_data(character_name)
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Save HTML for debugging
        try:
            with open(f"prydwen_{character_name}_page.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print(f"✓ Saved page HTML for debugging")
        except:
            pass
        
        # Extract data
        character_data = {
            "characterId": character_name,
            "lightCones": self._extract_light_cones(soup),
            "relics": self._extract_relics(soup),
            "stats": self._extract_stats(soup)
        }
        
        return character_data
    
    def _extract_light_cones(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract light cone recommendations"""
        light_cones = []
        print("\nExtracting Light Cones...")
        
        try:
            # Look for sections containing "light cone" text
            lc_sections = soup.find_all(string=re.compile(r'light cone', re.IGNORECASE))
            print(f"Found {len(lc_sections)} sections mentioning 'light cone'")
            
            # Try to find structured data
            # Look for images with alt text containing "Light Cone"
            lc_images = soup.find_all('img', alt=re.compile(r'light.?cone', re.IGNORECASE))
            
            for img in lc_images[:6]:
                try:
                    # Get parent containers
                    parent = img.find_parent(['div', 'article', 'section'])
                    if parent:
                        # Extract text from parent
                        text = parent.get_text(separator='\n', strip=True)
                        lines = [line.strip() for line in text.split('\n') if line.strip()]
                        
                        # Try to get name from alt or nearby text
                        name = img.get('alt', '').replace('Light Cone', '').strip()
                        if not name and lines:
                            name = lines[0]
                        
                        notes = ' '.join(lines[1:3]) if len(lines) > 1 else "Recommended option"
                        
                        if name and len(name) > 2:
                            light_cones.append({
                                "name": name,
                                "notes": notes[:100]  # Limit notes length
                            })
                            print(f"  ✓ Found: {name}")
                except Exception as e:
                    continue
            
            # If no structured data found, try text parsing
            if not light_cones:
                print("  Trying alternative extraction method...")
                # Look for any list items or headings that might be light cones
                potential_items = soup.find_all(['h3', 'h4', 'strong'], string=re.compile(r'^[A-Z]'))
                
                for item in potential_items[:10]:
                    text = item.get_text(strip=True)
                    # Light cone names are typically title case and 2-6 words
                    if len(text.split()) >= 2 and len(text.split()) <= 6:
                        # Check if nearby text mentions light cone or cone
                        parent_text = item.find_parent().get_text().lower()
                        if 'cone' in parent_text or 'weapon' in parent_text:
                            light_cones.append({
                                "name": text,
                                "notes": "Recommended option"
                            })
                            print(f"  ✓ Found (alt method): {text}")
                            
                            if len(light_cones) >= 4:
                                break
        
        except Exception as e:
            print(f"  Error: {e}")
        
        if not light_cones:
            print("  ⚠ No light cones extracted - manual review needed")
            return [{"name": "Manual review needed", "notes": "Could not auto-extract from page"}]
        
        return light_cones
    
    def _extract_relics(self, soup: BeautifulSoup) -> Dict:
        """Extract relic set recommendations"""
        relics = {
            "sets": [],
            "planar": []
        }
        print("\nExtracting Relics...")
        
        try:
            # Look for relic images
            relic_images = soup.find_all('img', alt=re.compile(r'relic|set', re.IGNORECASE))
            
            print(f"Found {len(relic_images)} potential relic items")
            
            for img in relic_images[:10]:
                try:
                    parent = img.find_parent(['div', 'article', 'section'])
                    if parent:
                        text = parent.get_text(separator='\n', strip=True)
                        lines = [line.strip() for line in text.split('\n') if line.strip()]
                        
                        # Get name from alt or nearby text
                        name = img.get('alt', '').replace('Relic Set', '').replace('Set', '').strip()
                        if not name and lines:
                            name = lines[0]
                        
                        notes = ' '.join(lines[1:3]) if len(lines) > 1 else "Recommended set"
                        
                        # Determine if planar or regular
                        is_planar = any(kw in name.lower() or kw in text.lower()
                                      for kw in ['planar', 'ornament', 'space', 'fleet', 'realm', 'salsotto', 'glamoth', 'izumo'])
                        
                        if name and len(name) > 3:
                            relic_entry = {
                                "name": name,
                                "notes": notes[:100]
                            }
                            
                            if is_planar:
                                relics["planar"].append(relic_entry)
                                print(f"  ✓ Found Planar: {name}")
                            else:
                                relic_entry["pieces"] = "4pc"
                                relics["sets"].append(relic_entry)
                                print(f"  ✓ Found Set: {name}")
                except:
                    continue
            
            # Alternative: Look for text patterns
            if not relics["sets"]:
                print("  Trying alternative relic extraction...")
                # Common HSR relic set names
                known_sets = [
                    'Prisoner in Deep Confinement', 'Pioneer Diver of Dead Waters',
                    'Genius of Brilliant Stars', 'Musketeer of Wild Wheat',
                    'Band of Sizzling Thunder', 'Thief of Shooting Meteor',
                    'Eagle of Twilight Line', 'Hunter of Glacial Forest'
                ]
                
                page_text = soup.get_text()
                for set_name in known_sets:
                    if set_name in page_text:
                        relics["sets"].append({
                            "name": set_name,
                            "pieces": "4pc",
                            "notes": "Recommended set"
                        })
                        print(f"  ✓ Found (text match): {set_name}")
        
        except Exception as e:
            print(f"  Error: {e}")
        
        # Ensure we have some data
        if not relics["sets"]:
            relics["sets"] = [{"name": "Manual review needed", "pieces": "4pc", "notes": "Could not auto-extract"}]
            print("  ⚠ No relic sets extracted")
        if not relics["planar"]:
            relics["planar"] = [{"name": "Manual review needed", "notes": "Could not auto-extract"}]
            print("  ⚠ No planar sets extracted")
        
        return relics
    
    def _extract_stats(self, soup: BeautifulSoup) -> Dict:
        """Extract main stat and sub stat recommendations"""
        stats = {
            "body": [],
            "feet": [],
            "sphere": [],
            "rope": [],
            "subStats": []
        }
        print("\nExtracting Stats...")
        
        try:
            # Get full page text
            page_text = soup.get_text().lower()
            
            # Common stat mappings
            stat_mapping = {
                'crit rate': 'CRIT Rate',
                'crit dmg': 'CRIT DMG',
                'crit damage': 'CRIT DMG',
                'atk%': 'ATK%',
                'attack%': 'ATK%',
                'hp%': 'HP%',
                'def%': 'DEF%',
                'speed': 'Speed',
                'spd': 'Speed',
                'energy': 'Energy Regen',
                'err': 'Energy Regen',
                'break': 'Break Effect',
                'effect hit': 'Effect Hit Rate',
                'elemental dmg': 'Elemental DMG',
                'dmg boost': 'Elemental DMG'
            }
            
            # Look for stat tables or sections
            stat_sections = soup.find_all(string=re.compile(r'main stat|sub stat|body|feet|sphere|rope', re.IGNORECASE))
            
            print(f"Found {len(stat_sections)} stat-related sections")
            
            # Try to find structured stat recommendations
            slots = ['body', 'feet', 'sphere', 'rope']
            
            for slot in slots:
                # Find elements mentioning this slot
                slot_elements = soup.find_all(string=re.compile(rf'\b{slot}\b', re.IGNORECASE))
                
                for elem in slot_elements[:3]:
                    try:
                        parent = elem.find_parent(['div', 'section', 'table'])
                        if parent:
                            parent_text = parent.get_text().lower()
                            
                            # Look for stats mentioned near the slot
                            for key, value in stat_mapping.items():
                                if key in parent_text and value not in stats[slot]:
                                    stats[slot].append(value)
                                    print(f"  ✓ {slot}: {value}")
                    except:
                        continue
            
            # Extract sub-stats
            substats_found = set()
            common_substats = ['crit rate', 'crit dmg', 'atk%', 'speed', 'break', 'effect hit']
            
            for stat_key in common_substats:
                if stat_key in page_text and stat_key in stat_mapping:
                    substats_found.add(stat_mapping[stat_key])
            
            stats["subStats"] = sorted(list(substats_found))
            if stats["subStats"]:
                print(f"  ✓ Sub-stats: {', '.join(stats['subStats'])}")
        
        except Exception as e:
            print(f"  Error: {e}")
        
        # Provide sensible defaults if nothing found
        if not any(stats[key] for key in ['body', 'feet', 'sphere', 'rope']):
            print("  ⚠ Using default stat recommendations")
            stats = {
                "body": ["CRIT Rate", "CRIT DMG"],
                "feet": ["ATK%", "Speed"],
                "sphere": ["Elemental DMG", "ATK%"],
                "rope": ["ATK%", "Energy Regen"],
                "subStats": ["CRIT Rate", "CRIT DMG", "ATK%", "Speed"]
            }
        
        return stats
    
    def _create_empty_data(self, character_name: str) -> Dict:
        """Create empty data structure with defaults"""
        return {
            "characterId": character_name,
            "lightCones": [{"name": "Error loading page", "notes": "Check network connection"}],
            "relics": {
                "sets": [{"name": "Error loading page", "pieces": "4pc", "notes": "Check network connection"}],
                "planar": [{"name": "Error loading page", "notes": "Check network connection"}]
            },
            "stats": {
                "body": ["CRIT Rate"],
                "feet": ["Speed"],
                "sphere": ["Elemental DMG"],
                "rope": ["Energy Regen"],
                "subStats": ["CRIT Rate", "CRIT DMG", "ATK%", "Speed"]
            }
        }
    
    def save_to_json(self, data: Dict, output_file: str):
        """Save scraped data to JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Data saved to {output_file}")


def main():
    """Main function to run the scraper"""
    try:
        print("="*60)
        print("Prydwen.gg Character Build Scraper (Simple Version)")
        print("="*60)
        print("\nNote: This version uses requests+BeautifulSoup.")
        print("If data extraction is incomplete, the page may require")
        print("JavaScript rendering (use Selenium version instead).\n")
        
        # Initialize scraper
        scraper = PrydwenScraperSimple()
        
        # Scrape Kafka as example
        character_name = "kafka"
        print(f"Scraping build data for: {character_name}")
        print("="*60)
        
        character_data = scraper.scrape_character(character_name)
        
        # Display results
        print(f"\n{'='*60}")
        print("EXTRACTED DATA:")
        print(f"{'='*60}")
        print(json.dumps(character_data, indent=2))
        
        # Save to file
        output_file = f"prydwen_{character_name}_build.json"
        scraper.save_to_json(character_data, output_file)
        
        print(f"\n{'='*60}")
        print(f"✓ Successfully scraped data for {character_name}!")
        print(f"{'='*60}")
        print("\n💡 Tip: Review the output and the saved HTML file")
        print("   to verify data accuracy. If incomplete, consider")
        print("   installing Chrome/Edge for the Selenium version.")
        
    except Exception as e:
        print(f"\n✗ Error during scraping: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
