"""
HSR Tier List Scraper - All Game Modes
Uses Selenium to click through tabs (MoC, PF, AS) and div-based extraction
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime
from typing import Dict, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class HSRAccurateTierScraper:
    """
    Accurate scraper that uses div tier classes to determine character ratings.
    Example: <div class="custom-tier tier-0 first"> contains T0 characters
    """
    
    TIER_LIST_URL = "https://www.prydwen.gg/star-rail/tier-list"
    
    # Tier to numerical rating (1-10 scale)
    TIER_RATINGS = {
        'T0': 10.0,
        'T0.5': 9.0,
        'T1': 8.0,
        'T1.5': 7.0,
        'T2': 6.0,
        'T2.5': 5.0,
        'T3': 4.0,
        'T3.5': 3.0,
        'T4': 2.0,
        'T4.5': 1.5,
        'T5': 1.0,
    }
    
    # Map div class names to tier names (based on actual HTML structure)
    DIV_CLASS_TO_TIER = {
        'tier-0': 'T0',
        'tier-05': 'T0.5',
        'tier-1': 'T1',
        'tier-15': 'T1.5',
        'tier-2': 'T2',
        'tier-25': 'T2.5',
        'tier-3': 'T3',
        'tier-35': 'T3.5',
        'tier-4': 'T4',
        'tier-45': 'T4.5',
        'tier-5': 'T5',
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_page(self) -> str:
        """Fetch tier list page HTML"""
        print(f"Fetching {self.TIER_LIST_URL}...")
        response = self.session.get(self.TIER_LIST_URL, timeout=15)
        response.raise_for_status()
        time.sleep(1)
        return response.text
    
    def extract_name_from_url(self, url: str) -> str:
        """
        Extract character name from URL slug.
        Example: /star-rail/characters/anaxa -> Anaxa
        """
        match = re.search(r'/characters/([^/]+)$', url)
        if not match:
            return ""
        
        slug = match.group(1)
        
        # Special cases for character name formatting
        special_cases = {
            'march-7th-swordmaster': 'March 7th (Swordmaster)',
            'march-7th-evernight': 'March 7th (Evernight)',
            'dan-heng-permansor-terrae': 'Dan Heng • Imbibitor Lunae',
            'imbibitor-lunae': 'Dan Heng • Imbibitor Lunae',
            'trailblazer-remembrance': 'Trailblazer (Remembrance)',
            'trailblazer-harmony': 'Trailblazer (Harmony)',
            'trailblazer-preservation': 'Trailblazer (Preservation)',
            'trailblazer-destruction': 'Trailblazer (Destruction)',
            'dr-ratio': 'Dr. Ratio',
        }
        
        if slug in special_cases:
            return special_cases[slug]
        
        # Convert slug to proper name: march-7th -> March 7th
        name = slug.replace('-', ' ').title()
        
        # Fix common issues
        name = name.replace('•', '•')  # Fix bullet point
        name = name.replace(' Of ', ' of ')  # Fix "of"
        name = name.replace(' The ', ' the ')  # Fix "the"
        
        return name
    
    def find_tier_and_role_for_link(self, link) -> tuple:
        """
        Find the tier and role for a character link.
        Traverses up the DOM to find tier div and role information.
        Returns: (tier, role) tuple
        """
        tier = None
        role = None
        
        # Traverse up to find tier div and role
        current = link
        depth = 0
        
        while current and depth < 10:
            # Check for tier class
            if not tier:
                classes = current.get('class', [])
                for cls in classes:
                    if cls in self.DIV_CLASS_TO_TIER:
                        tier = self.DIV_CLASS_TO_TIER[cls]
                        break
            
            # Check for role class
            if not role:
                classes = current.get('class', [])
                role_classes = ['dps', 'debuffer', 'support', 'sustain']
                for cls in classes:
                    if cls.lower() in role_classes:
                        role = cls.upper() if cls != 'debuffer' else 'SUPPORT DPS'
                        break
            
            if tier and role:
                break
            
            current = current.parent
            depth += 1
        
        return tier, role
    
    def parse_tier_list(self, html: str) -> Dict[str, Dict]:
        """
        Parse tier list by finding all character links and determining their tier
        from parent div classes.
        """
        soup = BeautifulSoup(html, 'lxml')
        characters = {}
        
        print("\nSearching for character links and their tier assignments...")
        
        # Find the main tier list container
        tier_list_container = soup.find('div', class_='custom-tier-list-hsr')
        
        if not tier_list_container:
            print("⚠ Could not find custom-tier-list-hsr container")
            return characters
        
        # Find all character links within the tier list
        char_links = tier_list_container.find_all('a', href=re.compile(r'/star-rail/characters/'))
        
        print(f"Found {len(char_links)} character links")
        
        for link in char_links:
            url = link.get('href', '')
            char_name = self.extract_name_from_url(url)
            
            if not char_name:
                continue
            
            # Find tier and role for this character
            tier, role = self.find_tier_and_role_for_link(link)
            
            if not tier:
                continue
            
            rating = self.TIER_RATINGS.get(tier, 0)
            
            # Store character (only if not already stored or if this is a better tier)
            if char_name not in characters or rating > characters[char_name]['rating']:
                characters[char_name] = {
                    'tier': tier,
                    'rating': rating,
                    'role': role or 'Unknown',
                    'url': url
                }
        
        print(f"\nExtracted {len(characters)} unique characters")
        
        # Print tier distribution
        tier_counts = {}
        for char, info in characters.items():
            tier = info['tier']
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        
        print("\nCharacters per tier:")
        for tier in sorted(tier_counts.keys(), key=lambda x: self.TIER_RATINGS.get(x, 0), reverse=True):
            print(f"  {tier}: {tier_counts[tier]} characters")
        
        return characters
    
    def export_to_json(self, data: Dict, filename: str = "hsr_tier_ratings_accurate.json"):
        """Export to JSON"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'source': self.TIER_LIST_URL,
            'tier_scale': self.TIER_RATINGS,
            'note': 'Tier ratings scraped using div class analysis for accuracy',
            'characters': data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Exported to {filename}")
    
    def export_to_csv(self, data: Dict, filename: str = "hsr_tier_ratings_accurate.csv"):
        """Export to CSV"""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Character', 'Tier', 'Rating (1-10)', 'Role', 'URL'])
            
            for char, info in sorted(data.items()):
                writer.writerow([
                    char,
                    info.get('tier', 'N/A'),
                    info.get('rating', 'N/A'),
                    info.get('role', 'Unknown'),
                    f"https://www.prydwen.gg{info.get('url', '')}"
                ])
        
        print(f"✓ Exported to {filename}")


def scrape_with_selenium(headless=True):
    """
    Use Selenium to click through the three mode tabs and scrape each one.
    Returns dict with 'MoC', 'PF', 'AS' keys.
    """
    GAME_MODES = {
        0: {'key': 'MoC', 'name': 'Memory of Chaos'},
        1: {'key': 'PF', 'name': 'Pure Fiction'},
        2: {'key': 'AS', 'name': 'Apocalyptic Shadow'}
    }
    
    # Setup Chrome
    chrome_options = Options()
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    
    print("🌐 Initializing Chrome driver...")
    driver = webdriver.Chrome(options=chrome_options)
    
    all_data = {}
    scraper = HSRAccurateTierScraper()
    
    try:
        print(f"📡 Loading https://www.prydwen.gg/star-rail/tier-list")
        driver.get("https://www.prydwen.gg/star-rail/tier-list")
        
        # Wait for tier list
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'custom-tier-list-hsr')))
        print("✅ Page loaded\n")
        
        # Find tabs
        tabs = driver.find_elements(By.CSS_SELECTOR, '.tier-list-switcher.hsr .option')
        print(f"✅ Found {len(tabs)} mode tabs\n")
        
        # Click each tab and scrape
        for i, mode_info in GAME_MODES.items():
            if i >= len(tabs):
                continue
                
            mode_key = mode_info['key']
            mode_name = mode_info['name']
            
            print("=" * 70)
            print(f"📋 {mode_name} (Tab {i+1}/3)")
            print("=" * 70)
            
            try:
                # Re-find tabs (avoid stale reference)
                tabs = driver.find_elements(By.CSS_SELECTOR, '.tier-list-switcher.hsr .option')
                tab = tabs[i]
                
                # Click tab
                print(f"  🖱️  Clicking tab...")
                driver.execute_script("arguments[0].click();", tab)
                time.sleep(2)  # Wait for content update
                
                # Get HTML and parse
                html = driver.page_source
                print(f"  🔍 Parsing tier list...")
                results = scraper.parse_tier_list(html)
                
                all_data[mode_key] = {
                    'mode': mode_name,
                    'characters': results,
                    'count': len(results)
                }
                
                print(f"  ✅ Extracted {len(results)} characters\n")
                
            except Exception as e:
                print(f"  ❌ Error: {e}\n")
                all_data[mode_key] = {
                    'mode': mode_name,
                    'characters': {},
                    'count': 0,
                    'error': str(e)
                }
        
    finally:
        driver.quit()
        print("🔒 Browser closed\n")
    
    return all_data


def main():
    print("\n" + "="*80)
    print("🎮 HSR Tier List Scraper - All Game Modes")
    print("="*80)
    print("📌 Method: Selenium + Accurate div-based extraction")
    print("="*80 + "\n")
    
    # Scrape all modes
    all_data = scrape_with_selenium(headless=True)
    
    # Summary
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    
    total = 0
    for mode_key in ['MoC', 'PF', 'AS']:
        if mode_key in all_data:
            mode_data = all_data[mode_key]
            count = mode_data['count']
            total += count
            status = "✅" if count > 0 else "❌"
            print(f"{status} {mode_data['mode']}: {count} characters")
    
    print("=" * 80)
    
    if total > 0:
        # Export combined data
        print()
        
        # Export JSON
        with open('hsr_tier_ratings_all_modes.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        print("💾 JSON exported to hsr_tier_ratings_all_modes.json")
        
        # Export CSV
        import csv
        with open('hsr_tier_ratings_all_modes.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Mode', 'Mode Name', 'Character', 'Tier', 'Rating', 'Role', 'URL'])
            
            for mode_key in ['MoC', 'PF', 'AS']:
                mode_data = all_data[mode_key]
                for char_name, char_info in sorted(mode_data.get('characters', {}).items()):
                    writer.writerow([
                        mode_key,
                        mode_data['mode'],
                        char_name,
                        char_info['tier'],
                        char_info['rating'],
                        char_info['role'],
                        char_info['url']
                    ])
        
        print("💾 CSV exported to hsr_tier_ratings_all_modes.csv")
        print(f"📊 Total entries: {total * 3}")  # Each char appears in 3 modes
        print("\n✅ Scraping complete!")
    else:
        print("\n❌ No data scraped!")



if __name__ == "__main__":
    main()
