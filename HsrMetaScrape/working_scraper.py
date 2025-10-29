"""
Working Tier List Scraper for Prydwen.gg HSR Tier List
Extracts character tier ratings from all three game modes
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime
from typing import Dict, List


class HSRTierScraper:
    """
    Scraper for Honkai: Star Rail tier lists from Prydwen.gg
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
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def fetch_page(self) -> str:
        """Fetch the tier list page HTML"""
        print(f"Fetching {self.TIER_LIST_URL}...")
        response = self.session.get(self.TIER_LIST_URL, timeout=15)
        response.raise_for_status()
        time.sleep(1)  # Be respectful
        return response.text
    
    def clean_character_name(self, name: str) -> str:
        """Clean up character name"""
        # Fix encoding issues
        name = name.replace('â¢', '•').strip()
        return name
    
    def parse_tier_list_for_mode(self, soup: BeautifulSoup, mode: str) -> Dict[str, Dict]:
        """
        Parse tier list for a specific game mode.
        
        Args:
            soup: BeautifulSoup object
            mode: 'moc', 'pf', or 'as'
            
        Returns:
            Dict mapping character names to their tier info
        """
        character_tiers = {}
        
        # Find the HSR tier list container
        tier_list = soup.find('div', class_='custom-tier-list-hsr')
        
        if not tier_list:
            print(f"Could not find tier list container for {mode}")
            return character_tiers
        
        # Find all role sections (DPS, Support DPS, Amplifier, Sustain)
        role_sections = tier_list.find_all('div', class_='custom-tier-container')
        
        print(f"\nParsing {mode.upper()} tier list...")
        print(f"Found {len(role_sections)} role sections")
        
        for role_section in role_sections:
            # Get role name
            role_header = role_section.find('div', class_=re.compile(r'custom-header|burst-type'))
            role = "Unknown"
            if role_header:
                role = role_header.get_text(strip=True)
            
            # Find all tier bursts (groupings by tier)
            tier_bursts = role_section.find_all('div', class_='custom-tier-burst')
            
            for tier_burst in tier_bursts:
                # Find tier label
                tier_label_elem = tier_burst.find('div', class_='tier-label')
                if not tier_label_elem:
                    continue
                
                tier = tier_label_elem.get_text(strip=True)
                rating = self.TIER_RATINGS.get(tier, 0)
                
                # Find all characters in this tier
                char_links = tier_burst.find_all('a', href=re.compile(r'/characters/'))
                
                for char_link in char_links:
                    # Get character name
                    char_span = char_link.find('span')
                    if not char_span:
                        continue
                    
                    char_name = self.clean_character_name(char_span.get_text(strip=True))
                    
                    if not char_name:
                        continue
                    
                    # Store character tier info
                    if char_name not in character_tiers:
                        character_tiers[char_name] = {
                            'tier': tier,
                            'rating': rating,
                            'role': role,
                            'url': char_link.get('href', '')
                        }
        
        print(f"Extracted {len(character_tiers)} characters for {mode.upper()}")
        return character_tiers
    
    def scrape_all_modes(self) -> Dict[str, Dict[str, float]]:
        """
        Scrape tier lists for all three game modes.
        
        Returns:
            Dict mapping character names to ratings in each mode:
            {
                'Character Name': {
                    'moc': 8.0,
                    'pf': 9.0,
                    'as': 7.0
                }
            }
        """
        html = self.fetch_page()
        soup = BeautifulSoup(html, 'lxml')
        
        # For now, the page shows one mode at a time
        # The default view is Memory of Chaos
        # We'll need to handle this differently if we want all 3 modes
        
        # Parse the current mode (likely MoC)
        mode_chars = self.parse_tier_list_for_mode(soup, 'moc')
        
        # Create combined results
        results = {}
        for char_name, info in mode_chars.items():
            results[char_name] = {
                'moc': info['rating'],
                'pf': None,  # Would need to scrape different page states
                'as': None,  # Would need to scrape different page states
                'tier_moc': info['tier'],
                'role': info['role'],
                'url': info['url']
            }
        
        return results
    
    def export_to_json(self, data: Dict, filename: str = "hsr_tier_ratings.json"):
        """Export to JSON"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'source': self.TIER_LIST_URL,
            'tier_scale': self.TIER_RATINGS,
            'note': 'Currently only Memory of Chaos (MoC) ratings are scraped. PF and AS require different scraping approach.',
            'characters': data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\nExported to {filename}")
    
    def export_to_csv(self, data: Dict, filename: str = "hsr_tier_ratings.csv"):
        """Export to CSV"""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Character', 'MoC Rating', 'MoC Tier', 'Role', 'URL'])
            
            for char, info in sorted(data.items()):
                writer.writerow([
                    char,
                    info.get('moc', 'N/A'),
                    info.get('tier_moc', 'N/A'),
                    info.get('role', 'N/A'),
                    f"https://www.prydwen.gg{info.get('url', '')}"
                ])
        
        print(f"Exported to {filename}")


def main():
    print("="*80)
    print("HSR Tier List Scraper - Prydwen.gg")
    print("="*80)
    
    scraper = HSRTierScraper()
    
    # Scrape tier lists
    results = scraper.scrape_all_modes()
    
    if results:
        # Export results
        scraper.export_to_json(results)
        scraper.export_to_csv(results)
        
        # Print summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Total characters: {len(results)}")
        
        # Count by tier
        tier_counts = {}
        for char, info in results.items():
            tier = info.get('tier_moc', 'Unknown')
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        
        print("\nCharacters per tier (MoC):")
        for tier in sorted(tier_counts.keys(), key=lambda x: scraper.TIER_RATINGS.get(x, 0), reverse=True):
            print(f"  {tier}: {tier_counts[tier]} characters")
        
        # Show some examples
        print("\nSample characters:")
        for char in list(results.keys())[:5]:
            info = results[char]
            print(f"  {char}: {info['tier_moc']} ({info['moc']}/10) - {info['role']}")
    else:
        print("\nNo data extracted. Check the HTML structure.")
    
    print("\n" + "="*80)
    print("NOTE: This scraper currently only extracts Memory of Chaos ratings.")
    print("To get all 3 modes, you would need to use Selenium to click the tabs")
    print("or find the API endpoint that the website uses.")
    print("="*80)


if __name__ == "__main__":
    main()
