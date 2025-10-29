"""
Prydwen.gg Star Rail Tier List Scraper
Extracts tier list data and converts to numerical ratings (1-10)
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from typing import Dict, List, Optional
from datetime import datetime


class TierListScraper:
    """
    Scraper specifically for Prydwen.gg tier lists.
    Converts tier ratings to numerical scores (1-10).
    """
    
    BASE_URL = "https://www.prydwen.gg/star-rail"
    TIER_LIST_URL = f"{BASE_URL}/tier-list"
    
    # Tier to rating conversion
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
    
    # Game mode identifiers
    GAME_MODES = {
        'moc': 'Memory of Chaos',
        'pf': 'Pure Fiction',
        'as': 'Apocalyptic Shadow'
    }
    
    def __init__(self, delay: float = 2.0, use_selenium: bool = False):
        """
        Initialize the scraper.
        
        Args:
            delay: Delay in seconds between requests
            use_selenium: Whether to use Selenium for dynamic content
        """
        self.delay = delay
        self.use_selenium = use_selenium
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def _make_request(self, url: str) -> Optional[str]:
        """
        Make a request and return HTML content.
        
        Args:
            url: URL to request
            
        Returns:
            HTML content or None if request fails
        """
        try:
            print(f"Requesting: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            time.sleep(self.delay)
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def _extract_character_name(self, text: str) -> str:
        """
        Extract clean character name from text.
        Removes eidolon info, element, and tags.
        
        Args:
            text: Raw text from character link
            
        Returns:
            Clean character name
        """
        # Remove eidolon info (E0, E6, etc.)
        text = re.sub(r'\s*E\d+\s*', ' ', text)
        
        # Split by common separators and take the first part (character name)
        # This handles cases like "Acheron E0 Lightning DEBUFF"
        parts = text.strip().split()
        
        # Character names can have special characters like "•" or multiple words
        # We'll need to be smart about this
        name_parts = []
        for part in parts:
            # Stop at element keywords or common tags
            if part.upper() in ['PHYSICAL', 'FIRE', 'ICE', 'LIGHTNING', 'WIND', 
                               'QUANTUM', 'IMAGINARY', 'DEBUFF', 'SP-FRIENDLY', 
                               'SP-UNFRIENDLY', 'PARTNER', 'ADVANCE', 'BREAK', 
                               'BUFF', 'DOT', 'DPS']:
                break
            # Skip eidolon markers
            if re.match(r'^E\d+$', part):
                continue
            name_parts.append(part)
        
        return ' '.join(name_parts).strip()
    
    def _parse_tier_section(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """
        Parse tier list HTML and extract character-tier mappings.
        
        Args:
            soup: BeautifulSoup object of tier list page
            
        Returns:
            Dictionary mapping tier names to lists of character names
        """
        tier_data = {}
        
        # Try to find tier sections
        # The structure might be: tier label (T0, T1, etc.) followed by character links
        
        # Look for patterns like "T0", "T1", etc. in the HTML
        html_text = soup.get_text()
        
        # Find all anchor tags that link to characters
        character_links = soup.find_all('a', href=re.compile(r'/star-rail/characters/'))
        
        print(f"Found {len(character_links)} character links")
        
        # For now, let's try a different approach
        # Look for tier indicators in the text
        tier_pattern = re.compile(r'\b(T\d(?:\.\d)?)\b')
        
        # Get all text nodes and links together
        # This is a simplified approach - we'll need to refine based on actual HTML structure
        
        # Debug: Print some of the page structure
        print("\nPage structure sample:")
        for i, link in enumerate(character_links[:5]):
            print(f"  Link {i}: {link.get_text()[:100]}")
            print(f"    href: {link.get('href')}")
            # Check parent elements for tier info
            parent = link.parent
            if parent:
                print(f"    Parent: {parent.name} - {parent.get_text()[:50]}")
        
        return tier_data
    
    def scrape_tier_list(self, save_raw_html: bool = False) -> Dict[str, Dict[str, float]]:
        """
        Scrape tier list for all three game modes.
        
        Args:
            save_raw_html: Whether to save raw HTML for debugging
            
        Returns:
            Dictionary mapping character names to their ratings in each mode
            Format: {
                'Character Name': {
                    'moc': 8.0,
                    'pf': 9.0,
                    'as': 7.0
                }
            }
        """
        html_content = self._make_request(self.TIER_LIST_URL)
        
        if not html_content:
            print("Failed to fetch tier list page")
            return {}
        
        if save_raw_html:
            with open('tier_list_raw.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("Saved raw HTML to tier_list_raw.html")
        
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Parse the tier list
        tier_data = self._parse_tier_section(soup)
        
        # Convert tier data to ratings
        character_ratings = {}
        
        for tier, characters in tier_data.items():
            rating = self.TIER_RATINGS.get(tier, 0)
            for char in characters:
                if char not in character_ratings:
                    character_ratings[char] = {}
                # For now, apply same rating to all modes
                # We'll need to parse mode-specific data later
                character_ratings[char]['moc'] = rating
        
        return character_ratings
    
    def scrape_with_selenium(self) -> Dict[str, Dict[str, float]]:
        """
        Scrape tier list using Selenium for dynamic content.
        This is more reliable but requires chromedriver.
        
        Returns:
            Dictionary mapping character names to their ratings
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.options import Options
            
            print("Using Selenium to scrape tier list...")
            
            options = Options()
            options.add_argument('--headless')  # Run in background
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument(f'user-agent={self.session.headers["User-Agent"]}')
            
            driver = webdriver.Chrome(options=options)
            character_ratings = {}
            
            try:
                # Load each mode's tier list
                for mode_key, mode_name in self.GAME_MODES.items():
                    print(f"\nScraping {mode_name} tier list...")
                    driver.get(self.TIER_LIST_URL)
                    
                    # Wait for page to load
                    time.sleep(3)
                    
                    # TODO: Click on the correct tab for each mode
                    # This depends on how the tabs are structured in the HTML
                    
                    # Extract tier data
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, 'lxml')
                    
                    # Find tier sections and characters
                    # This is where we need to inspect the actual HTML structure
                    
                    print(f"Page title: {driver.title}")
                    
                    time.sleep(self.delay)
                
            finally:
                driver.quit()
            
            return character_ratings
            
        except ImportError:
            print("Selenium not installed. Install with: pip install selenium webdriver-manager")
            return {}
        except Exception as e:
            print(f"Error using Selenium: {e}")
            return {}
    
    def export_to_json(self, data: Dict, filename: str = "tier_ratings.json") -> None:
        """
        Export tier ratings to JSON file.
        
        Args:
            data: Character ratings data
            filename: Output filename
        """
        output = {
            'timestamp': datetime.now().isoformat(),
            'source': self.TIER_LIST_URL,
            'tier_mapping': self.TIER_RATINGS,
            'characters': data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\nData exported to {filename}")
        print(f"Total characters: {len(data)}")
    
    def export_to_csv(self, data: Dict, filename: str = "tier_ratings.csv") -> None:
        """
        Export tier ratings to CSV file.
        
        Args:
            data: Character ratings data
            filename: Output filename
        """
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Character', 'Memory of Chaos', 'Pure Fiction', 'Apocalyptic Shadow'])
            
            for char, ratings in sorted(data.items()):
                writer.writerow([
                    char,
                    ratings.get('moc', 'N/A'),
                    ratings.get('pf', 'N/A'),
                    ratings.get('as', 'N/A')
                ])
        
        print(f"Data exported to {filename}")


def main():
    """Main function to run the tier list scraper."""
    print("=== Prydwen.gg Star Rail Tier List Scraper ===\n")
    
    scraper = TierListScraper(delay=2.0)
    
    print("Scraping tier list data...")
    print("This will save the raw HTML for inspection.\n")
    
    # Scrape with requests first (save HTML for inspection)
    data = scraper.scrape_tier_list(save_raw_html=True)
    
    if data:
        scraper.export_to_json(data)
        scraper.export_to_csv(data)
    else:
        print("\nNo data extracted with requests method.")
        print("The page likely uses JavaScript to load content.")
        print("\nTrying Selenium method...")
        
        # Try Selenium
        data = scraper.scrape_with_selenium()
        if data:
            scraper.export_to_json(data)
            scraper.export_to_csv(data)
    
    print("\n=== Next Steps ===")
    print("1. Inspect tier_list_raw.html to understand the page structure")
    print("2. Update the parsing logic based on the actual HTML structure")
    print("3. Test with a small subset before running full scrape")


if __name__ == "__main__":
    main()
