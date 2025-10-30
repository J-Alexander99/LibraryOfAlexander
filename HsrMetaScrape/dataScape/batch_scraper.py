"""
Batch Prydwen Scraper
Scrapes multiple characters at once and combines into a single JSON file
"""

from prydwen_scraper_simple import PrydwenScraperSimple
import json
import time
from typing import Dict, List


def scrape_multiple_characters(characters: List[str], delay: float = 2.0) -> Dict:
    """
    Scrape multiple characters and combine into one JSON
    
    Args:
        characters: List of character names (as they appear in URLs)
        delay: Seconds to wait between requests (be nice to the server!)
    
    Returns:
        Dictionary with all character data
    """
    scraper = PrydwenScraperSimple()
    all_data = {}
    
    print(f"\n{'='*60}")
    print(f"Batch Scraping {len(characters)} Characters")
    print(f"{'='*60}\n")
    
    for i, character in enumerate(characters, 1):
        print(f"\n[{i}/{len(characters)}] Scraping: {character}")
        print("-" * 60)
        
        try:
            character_data = scraper.scrape_character(character)
            all_data[character] = character_data
            print(f"✓ Successfully scraped {character}")
            
            # Be nice to the server - add delay between requests
            if i < len(characters):
                print(f"⏳ Waiting {delay}s before next request...")
                time.sleep(delay)
        
        except Exception as e:
            print(f"✗ Error scraping {character}: {e}")
            all_data[character] = {
                "characterId": character,
                "error": str(e)
            }
    
    return all_data


def main():
    """Main batch scraping function"""
    
    # Characters to scrape (add more as needed!)
    characters = [
        "kafka",
        "acheron",
        "firefly",
        "feixiao",
        "aventurine",
        "robin",
        "ruan-mei",
        "black-swan",
        "sparkle",
        "silver-wolf"
    ]
    
    print("\n" + "="*60)
    print("Prydwen.gg Batch Character Scraper")
    print("="*60)
    print(f"\nQueued: {len(characters)} characters")
    print(f"Characters: {', '.join(characters)}")
    print("\n⚠ Note: This will take a few minutes to be respectful")
    print("   to Prydwen's servers (2s delay between requests)")
    
    input("\nPress Enter to start scraping...")
    
    # Scrape all characters
    all_data = scrape_multiple_characters(characters, delay=2.0)
    
    # Save combined data
    output_file = "prydwen_all_characters.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print("BATCH SCRAPING COMPLETE")
    print(f"{'='*60}")
    print(f"✓ Scraped: {len([k for k, v in all_data.items() if 'error' not in v])} characters")
    print(f"✗ Errors: {len([k for k, v in all_data.items() if 'error' in v])} characters")
    print(f"💾 Saved to: {output_file}")
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    for character, data in all_data.items():
        if 'error' in data:
            print(f"✗ {character:20} - ERROR: {data['error']}")
        else:
            lc_count = len(data.get('lightCones', []))
            relic_count = len(data.get('relics', {}).get('sets', []))
            print(f"✓ {character:20} - {lc_count} LCs, {relic_count} relics")
    
    print(f"\n{'='*60}")
    print("💡 Review the JSON file for detailed build data")
    print("💡 Edit this script to add/remove characters")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
