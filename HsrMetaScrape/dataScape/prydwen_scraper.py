"""
Prydwen.gg Character Build Scraper - Edge/Chrome Compatible
Extracts character build data (light cones, relics, stats) from Prydwen.gg
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import sys
from typing import Dict, List, Optional


class PrydwenScraper:
    def __init__(self, headless: bool = True, browser: str = "auto"):
        """
        Initialize the scraper with WebDriver
        
        Args:
            headless: Run browser in headless mode (no GUI)
            browser: "chrome", "edge", or "auto" (try both)
        """
        self.driver = None
        self.wait = None
        
        # Try to initialize browser
        if browser == "auto":
            self._init_auto(headless)
        elif browser == "edge":
            self._init_edge(headless)
        elif browser == "chrome":
            self._init_chrome(headless)
        else:
            raise ValueError(f"Unknown browser: {browser}")
        
        if not self.driver:
            raise RuntimeError("Failed to initialize any browser. Please install Chrome or Edge.")
        
        self.wait = WebDriverWait(self.driver, 15)
    
    def _init_auto(self, headless: bool):
        """Try Edge first (pre-installed on Windows), then Chrome"""
        print("Attempting to initialize browser (trying Edge, then Chrome)...")
        
        # Try Edge first (usually pre-installed on Windows)
        try:
            self._init_edge(headless)
            if self.driver:
                print("✓ Using Microsoft Edge")
                return
        except Exception as e:
            print(f"Edge not available: {e}")
        
        # Try Chrome as fallback
        try:
            self._init_chrome(headless)
            if self.driver:
                print("✓ Using Google Chrome")
                return
        except Exception as e:
            print(f"Chrome not available: {e}")
    
    def _init_edge(self, headless: bool):
        """Initialize Microsoft Edge"""
        edge_options = EdgeOptions()
        if headless:
            edge_options.add_argument("--headless")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--window-size=1920,1080")
        edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        try:
            service = EdgeService(EdgeChromiumDriverManager().install())
            self.driver = webdriver.Edge(service=service, options=edge_options)
        except Exception:
            raise
    
    def _init_chrome(self, headless: bool):
        """Initialize Google Chrome"""
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        try:
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception:
            raise
    
    def scrape_character(self, character_name: str) -> Dict:
        """
        Scrape build data for a character from Prydwen.gg
        
        Args:
            character_name: The character name as it appears in the URL (e.g., 'kafka')
        
        Returns:
            Dictionary with character build data
        """
        url = f"https://www.prydwen.gg/star-rail/characters/{character_name}"
        print(f"Navigating to {url}...")
        
        self.driver.get(url)
        time.sleep(3)  # Let initial page load
        
        # Click on "Build and Teams" tab
        print("Looking for 'Build and Teams' tab...")
        try:
            # Try different possible selectors for the tab
            build_tab = None
            possible_selectors = [
                "//button[contains(text(), 'Build')]",
                "//a[contains(text(), 'Build')]",
                "//div[contains(@class, 'tab')]//span[contains(text(), 'Build')]",
                "//*[contains(text(), 'Build and Teams')]",
                "//button[contains(., 'Build')]",
                "//*[@role='tab' and contains(., 'Build')]"
            ]
            
            for selector in possible_selectors:
                try:
                    build_tab = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"Found tab with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if build_tab:
                build_tab.click()
                time.sleep(3)  # Wait for tab content to load
                print("✓ Clicked 'Build and Teams' tab")
            else:
                print("⚠ Could not find 'Build and Teams' tab, proceeding with current page")
        
        except Exception as e:
            print(f"Error clicking tab: {e}")
            print("Proceeding to scrape from current page...")
        
        # Save page source for debugging
        try:
            with open("page_debug.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            print("✓ Saved page source to page_debug.html for debugging")
        except:
            pass
        
        # Extract data
        character_data = {
            "characterId": character_name,
            "lightCones": self._extract_light_cones(),
            "relics": self._extract_relics(),
            "stats": self._extract_stats()
        }
        
        return character_data
    
    def _extract_light_cones(self) -> List[Dict]:
        """Extract light cone recommendations"""
        light_cones = []
        print("\nExtracting Light Cones...")
        
        try:
            # Look for light cone section headers
            lc_headers = self.driver.find_elements(By.XPATH, 
                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'light cone')]")
            
            print(f"Found {len(lc_headers)} Light Cone headers")
            
            # Try multiple extraction strategies
            # Strategy 1: Look for structured cards/items
            lc_cards = self.driver.find_elements(By.XPATH,
                "//div[contains(@class, 'card') or contains(@class, 'item')]//img[contains(@alt, 'Light Cone') or contains(@src, 'light')]")
            
            for card in lc_cards[:6]:
                try:
                    parent = card.find_element(By.XPATH, "../..")
                    text = parent.text.strip()
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    
                    if lines:
                        name = lines[0]
                        notes = ' '.join(lines[1:]) if len(lines) > 1 else "Recommended option"
                        
                        if name and len(name) > 2:
                            light_cones.append({
                                "name": name,
                                "notes": notes
                            })
                            print(f"  ✓ Found: {name}")
                except:
                    continue
        
        except Exception as e:
            print(f"Error extracting light cones: {e}")
        
        if not light_cones:
            print("⚠ No light cones extracted - manual review needed")
            return [{"name": "Manual review needed", "notes": "Could not auto-extract from page"}]
        
        return light_cones
    
    def _extract_relics(self) -> Dict:
        """Extract relic set recommendations"""
        relics = {
            "sets": [],
            "planar": []
        }
        print("\nExtracting Relics...")
        
        try:
            # Look for relic sections
            relic_headers = self.driver.find_elements(By.XPATH,
                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'relic')]")
            
            print(f"Found {len(relic_headers)} Relic headers")
            
            # Try to find relic cards/items
            relic_cards = self.driver.find_elements(By.XPATH,
                "//div[contains(@class, 'card') or contains(@class, 'item')]//img[contains(@alt, 'Relic') or contains(@alt, 'Set') or contains(@src, 'relic')]")
            
            for card in relic_cards[:8]:
                try:
                    parent = card.find_element(By.XPATH, "../..")
                    text = parent.text.strip()
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    
                    if lines:
                        name = lines[0]
                        notes = ' '.join(lines[1:]) if len(lines) > 1 else "Recommended set"
                        
                        # Determine if planar or regular set
                        is_planar = any(kw in name.lower() or kw in text.lower()
                                      for kw in ['planar', 'ornament', 'space', 'fleet', 'realm', 'salsotto', 'glamoth'])
                        
                        if name and len(name) > 3:
                            relic_entry = {
                                "name": name,
                                "notes": notes
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
        
        except Exception as e:
            print(f"Error extracting relics: {e}")
        
        # Ensure we have some data
        if not relics["sets"]:
            relics["sets"] = [{"name": "Manual review needed", "pieces": "4pc", "notes": "Could not auto-extract"}]
            print("⚠ No relic sets extracted")
        if not relics["planar"]:
            relics["planar"] = [{"name": "Manual review needed", "notes": "Could not auto-extract"}]
            print("⚠ No planar sets extracted")
        
        return relics
    
    def _extract_stats(self) -> Dict:
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
                'dmg%': 'Elemental DMG'
            }
            
            # Get page text
            page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            
            # Look for stat recommendations
            slots = ['body', 'feet', 'sphere', 'rope']
            
            for slot in slots:
                # Find sections mentioning this slot
                slot_sections = self.driver.find_elements(By.XPATH,
                    f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{slot}')]")
                
                for section in slot_sections[:3]:  # Limit search
                    try:
                        parent_text = section.find_element(By.XPATH, "./../..").text.lower()
                        
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
            print(f"  ✓ Sub-stats: {', '.join(stats['subStats'])}")
        
        except Exception as e:
            print(f"Error extracting stats: {e}")
        
        # Provide sensible defaults if nothing found
        if not any(stats[key] for key in ['body', 'feet', 'sphere', 'rope']):
            print("⚠ Using default stat recommendations")
            stats = {
                "body": ["CRIT Rate", "CRIT DMG"],
                "feet": ["ATK%", "Speed"],
                "sphere": ["Elemental DMG", "ATK%"],
                "rope": ["ATK%", "Energy Regen"],
                "subStats": ["CRIT Rate", "CRIT DMG", "ATK%", "Speed"]
            }
        
        return stats
    
    def save_to_json(self, data: Dict, output_file: str):
        """Save scraped data to JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Data saved to {output_file}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("\n✓ Browser closed")


def main():
    """Main function to run the scraper"""
    scraper = None
    try:
        # Initialize scraper (will auto-detect Edge or Chrome)
        print("="*60)
        print("Prydwen.gg Character Build Scraper")
        print("="*60)
        
        scraper = PrydwenScraper(headless=False, browser="auto")  # Set headless=True to hide browser
        
        # Scrape Kafka as example
        character_name = "kafka"
        print(f"\nScraping build data for: {character_name}")
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
        
    except Exception as e:
        print(f"\n✗ Error during scraping: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if scraper:
            scraper.close()


if __name__ == "__main__":
    main()
