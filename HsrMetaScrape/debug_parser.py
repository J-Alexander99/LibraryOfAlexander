"""
Direct Tier List Parser
Uses BeautifulSoup to parse the tier list and extract character ratings.
This version will inspect the HTML structure and build a working parser.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from typing import Dict, List, Tuple
from datetime import datetime


class DirectTierParser:
    """
    Direct parser for Prydwen tier lists.
    Extracts character names and their tier ratings.
    """
    
    TIER_LIST_URL = "https://www.prydwen.gg/star-rail/tier-list"
    
    # Tier to numerical rating (1-10 scale)
    TIER_RATINGS = {
        'T0': 10,
        'T0.5': 9,
        'T1': 8,
        'T1.5': 7,
        'T2': 6,
        'T2.5': 5,
        'T3': 4,
        'T3.5': 3,
        'T4': 2,
        'T4.5': 1.5,
        'T5': 1,
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_page(self) -> str:
        """Fetch the tier list page HTML."""
        print(f"Fetching {self.TIER_LIST_URL}...")
        response = self.session.get(self.TIER_LIST_URL, timeout=10)
        response.raise_for_status()
        return response.text
    
    def clean_character_name(self, text: str) -> str:
        """
        Clean character name from link text.
        Examples:
            "Acheron E0 Lightning DEBUFF" -> "Acheron"
            "March 7th • Evernight E0 Ice BUFF, SP-FRIENDLY" -> "March 7th • Evernight"
        """
        # Remove eidolon markers
        text = re.sub(r'\s+E\d+\s+', ' ', text)
        
        # Common element/tag keywords to stop at
        stop_words = [
            'PHYSICAL', 'FIRE', 'ICE', 'LIGHTNING', 'WIND', 'QUANTUM', 'IMAGINARY',
            'DEBUFF', 'SP-FRIENDLY', 'SP-UNFRIENDLY', 'PARTNER', 'ADVANCE', 
            'BREAK', 'BUFF', 'DOT', 'DPS', 'SUPPORT'
        ]
        
        words = text.strip().split()
        name_parts = []
        
        for word in words:
            if word.upper() in stop_words or re.match(r'^E\d+$', word):
                break
            name_parts.append(word)
        
        return ' '.join(name_parts).strip()
    
    def inspect_html_structure(self, html: str) -> None:
        """
        Inspect the HTML structure to understand how to parse it.
        """
        soup = BeautifulSoup(html, 'lxml')
        
        print("\n=== HTML STRUCTURE ANALYSIS ===\n")
        
        # Find all character links
        char_links = soup.find_all('a', href=re.compile(r'/star-rail/characters/'))
        print(f"Total character links found: {len(char_links)}\n")
        
        # Sample some links
        print("Sample character links:")
        for i, link in enumerate(char_links[:10]):
            text = link.get_text(strip=True)
            href = link.get('href')
            char_name = self.clean_character_name(text)
            print(f"  {i+1}. Raw: '{text}'")
            print(f"      Cleaned: '{char_name}'")
            print(f"      URL: {href}")
            
            # Check parent structure
            parent = link.parent
            if parent:
                parent_text = parent.get_text(strip=True)[:100]
                print(f"      Parent ({parent.name}): {parent_text}")
            print()
        
        # Look for tier indicators
        print("\nSearching for tier indicators (T0, T1, etc.)...")
        tier_pattern = re.compile(r'\bT\d(?:\.\d)?\b')
        all_text = soup.get_text()
        tiers_found = tier_pattern.findall(all_text)
        print(f"Tiers mentioned: {set(tiers_found)}")
        
        # Try to find sections
        print("\nLooking for section headers...")
        for tag in ['h2', 'h3', 'h4', 'h5', 'div']:
            headers = soup.find_all(tag, class_=re.compile(r'tier|category|apex|meta', re.I))
            if headers:
                print(f"\n{tag.upper()} elements with tier-related classes:")
                for h in headers[:5]:
                    print(f"  - {h.get('class')}: {h.get_text(strip=True)[:80]}")
        
        # Save full HTML for manual inspection
        with open('tier_list_debug.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("\nFull HTML saved to tier_list_debug.html")
    
    def parse_tier_list_manual(self, html: str) -> Dict[str, Dict[str, float]]:
        """
        Manual parsing approach - looks for patterns in the HTML.
        This is a first attempt that may need refinement.
        """
        soup = BeautifulSoup(html, 'lxml')
        character_ratings = {}
        
        # Find all character links
        char_links = soup.find_all('a', href=re.compile(r'/star-rail/characters/'))
        
        print(f"\nProcessing {len(char_links)} character links...")
        
        # Extract character names
        for link in char_links:
            text = link.get_text(strip=True)
            char_name = self.clean_character_name(text)
            
            if char_name and char_name not in character_ratings:
                character_ratings[char_name] = {
                    'raw_text': text,
                    'url': link.get('href'),
                    'tier': None,
                    'rating': None
                }
        
        print(f"Extracted {len(character_ratings)} unique characters")
        
        return character_ratings
    
    def export_results(self, data: Dict, base_filename: str = "tier_list_output"):
        """Export parsed data to JSON and CSV."""
        
        # JSON export
        json_file = f"{base_filename}.json"
        output = {
            'timestamp': datetime.now().isoformat(),
            'source': self.TIER_LIST_URL,
            'tier_rating_scale': self.TIER_RATINGS,
            'characters': data
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nJSON exported to {json_file}")
        
        # CSV export for easy import
        csv_file = f"{base_filename}.csv"
        import csv
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Character', 'Tier', 'Rating', 'Raw Text', 'URL'])
            
            for char_name, info in sorted(data.items()):
                writer.writerow([
                    char_name,
                    info.get('tier', 'N/A'),
                    info.get('rating', 'N/A'),
                    info.get('raw_text', ''),
                    info.get('url', '')
                ])
        print(f"CSV exported to {csv_file}")


def main():
    """Run the direct tier parser."""
    print("=== Prydwen Tier List Direct Parser ===\n")
    
    parser = DirectTierParser()
    
    # Fetch the page
    html = parser.fetch_page()
    
    # Inspect structure
    parser.inspect_html_structure(html)
    
    # Try to parse
    print("\n=== PARSING TIER LIST ===")
    data = parser.parse_tier_list_manual(html)
    
    # Export results
    parser.export_results(data)
    
    print("\n=== Analysis Complete ===")
    print("Next steps:")
    print("1. Review tier_list_debug.html to see the page structure")
    print("2. Look for the pattern that associates characters with tiers")
    print("3. Update the parsing logic to extract tier information")


if __name__ == "__main__":
    main()
