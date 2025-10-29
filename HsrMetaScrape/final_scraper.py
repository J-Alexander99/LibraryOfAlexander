"""
HSR Tier List Scraper - Text-based parsing approach
Parses the text content from the fetch_webpage results
"""

import requests
import re
import json
from datetime import datetime
from typing import Dict, List
import time


class HSRTierTextScraper:
    """
    Scraper that works with the text content of the tier list page.
    """
    
    TIER_LIST_URL = "https://www.prydwen.gg/star-rail/tier-list"
    
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
    
    # Role keywords
    ROLES = ['DPS', 'SUPPORT DPS', 'AMPLIFIER', 'SUSTAIN']
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_page(self) -> str:
        """Fetch tier list page"""
        print(f"Fetching {self.TIER_LIST_URL}...")
        response = self.session.get(self.TIER_LIST_URL, timeout=15)
        response.raise_for_status()
        time.sleep(1)
        return response.text
    
    def extract_name_from_url(self, url: str) -> str:
        """Extract character name from URL slug"""
        # Extract slug from URL like /star-rail/characters/march-7th-evernight
        match = re.search(r'/characters/([^/]+)$', url)
        if not match:
            return ""
        
        slug = match.group(1)
        # Convert slug to title case name
        # Replace hyphens with spaces and capitalize
        name = slug.replace('-', ' ').title()
        return name
    
    def clean_character_name(self, name: str, url: str = "") -> str:
        """Clean character name"""
        # Fix encoding issues
        name = name.replace('â¢', '•').strip()
        
        # Remove eidolon info like E0, E6 at the start
        name = re.sub(r'^E\d+\s*', '', name)
        
        # Remove element/tag keywords and everything after them
        keywords = ['PHYSICAL', 'FIRE', 'ICE', 'LIGHTNING', 'WIND', 'QUANTUM', 'IMAGINARY',
                   'DEBUFF', 'SP-FRIENDLY', 'SP-UNFRIENDLY', 'PARTNER', 'ADVANCE', 
                   'BREAK', 'BUFF', 'DOT', 'DPS', 'ENERGY', 'DELAY']
        
        words = name.strip().split()
        clean_words = []
        
        for word in words:
            # Stop at element/tag keywords
            if word.upper() in keywords:
                break
            # Skip standalone eidolon markers
            if re.match(r'^E\d+$', word):
                continue
            # Stop at patterns like "E0Advance" which start with E0
            if re.match(r'^E\d+[A-Z]', word):
                break
            clean_words.append(word)
        
        result = ' '.join(clean_words).strip()
        
        # If result is empty or still looks like tags, extract from URL
        if not result or (result and all(word.upper() in keywords or ',' in result for word in result.split())):
            if url:
                result = self.extract_name_from_url(url)
        
        return result
    
    def parse_tier_list_text(self, html: str) -> Dict[str, Dict]:
        """
        Parse tier list from HTML text content.
        Uses pattern matching on the visible text.
        """
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        
        # Get all text content
        text_content = soup.get_text()
        
        characters = {}
        
        # Pattern: Find tier markers followed by role, then character links
        # Example from earlier: "T0   DPS Anaxa E0 Wind DEBUFF Archer E0 Quantum..."
        
        # Find all character links first
        char_links = soup.find_all('a', href=re.compile(r'/star-rail/characters/'))
        
        print(f"Found {len(char_links)} character links total")
        
        # Try to find pattern: look for sections with tier headers
        # Pattern: APEX CHARACTERS or META CHARACTERS etc., followed by T0, T1 etc.
        
        tier_sections = re.findall(
            r'(APEX CHARACTERS|META CHARACTERS|OFF-META CHARACTERS|THE FORGOTTEN ONES)',
            text_content
        )
        
        print(f"Found tier category sections: {tier_sections}")
        
        # Alternative: directly find "TX " patterns in text followed by role and characters
        # Let me try a simpler approach - find all instances of character names near tier labels
        
        # Get text around each character link
        for link in char_links:
            # Get character name directly from link text
            raw_name = link.get_text(strip=True)
            url = link.get('href', '')
            
            if not raw_name:
                continue
                
            char_name = self.clean_character_name(raw_name, url)
            
            if not char_name:
                continue
            
            # Look for tier information in parent elements
            current = link
            tier_found = None
            role_found = None
            
            # Traverse up the tree looking for tier/role info
            for _ in range(10):  # Max 10 levels up
                if not current:
                    break
                
                parent_text = ''
                if hasattr(current, 'get_text'):
                    parent_text = current.get_text()
                
                # Look for tier pattern
                tier_match = re.search(r'\b(T\d(?:\.\d)?)\b', parent_text)
                if tier_match and not tier_found:
                    tier_found = tier_match.group(1)
                
                # Look for role
                for role in self.ROLES:
                    if role in parent_text and not role_found:
                        role_found = role
                        break
                
                if tier_found and role_found:
                    break
                
                current = current.parent
            
            # Store character
            if char_name not in characters:
                characters[char_name] = {
                    'tier': tier_found,
                    'rating': self.TIER_RATINGS.get(tier_found, 0) if tier_found else None,
                    'role': role_found,
                    'url': link.get('href', '')
                }
        
        print(f"\nExtracted {len(characters)} unique characters")
        
        # Count how many have tier info
        with_tier = sum(1 for c in characters.values() if c['tier'])
        print(f"Characters with tier info: {with_tier}")
        
        return characters
    
    def export_to_json(self, data: Dict, filename: str = "hsr_tier_ratings_final.json"):
        """Export to JSON"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'source': self.TIER_LIST_URL,
            'tier_scale': self.TIER_RATINGS,
            'note': 'Memory of Chaos tier ratings scraped from Prydwen.gg',
            'characters': data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\nExported to {filename}")
    
    def export_to_csv(self, data: Dict, filename: str = "hsr_tier_ratings_final.csv"):
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
                    info.get('role', 'N/A'),
                    f"https://www.prydwen.gg{info.get('url', '')}"
                ])
        
        print(f"Exported to {filename}")


def main():
    print("="*80)
    print("HSR Tier List Scraper (Text-based)")
    print("="*80)
    
    scraper = HSRTierTextScraper()
    
    # Fetch and parse
    html = scraper.fetch_page()
    results = scraper.parse_tier_list_text(html)
    
    if results:
        # Export
        scraper.export_to_json(results)
        scraper.export_to_csv(results)
        
        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Total characters: {len(results)}")
        
        # Count by tier
        tier_counts = {}
        for char, info in results.items():
            tier = info.get('tier', 'Unknown')
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        
        print("\nCharacters per tier:")
        for tier in sorted([t for t in tier_counts.keys() if t and t != 'Unknown'], 
                          key=lambda x: scraper.TIER_RATINGS.get(x, 0), reverse=True):
            print(f"  {tier}: {tier_counts[tier]} characters (Rating: {scraper.TIER_RATINGS[tier]}/10)")
        
        if 'Unknown' in tier_counts:
            print(f"  Unknown tier: {tier_counts['Unknown']} characters")
        
        # Show examples
        print("\nSample characters:")
        count = 0
        for char in sorted(results.keys()):
            info = results[char]
            if info['tier']:
                print(f"  {char}: {info['tier']} ({info['rating']}/10) - {info['role']}")
                count += 1
                if count >= 10:
                    break
    else:
        print("\nNo data extracted.")


if __name__ == "__main__":
    main()
