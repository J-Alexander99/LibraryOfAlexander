"""
HTML Structure Analyzer - Find the pattern for tier assignments
"""

from bs4 import BeautifulSoup
import re
import json


def analyze_structure():
    with open('tier_list_debug.html', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')
    
    # Find the main tier list container
    tier_list = soup.find('div', class_='custom-tier-list-hsr')
    
    if not tier_list:
        print("Could not find custom-tier-list-hsr")
        return
    
    print("Found HSR tier list container\n")
    
    # Find all tier rows
    tier_rows = tier_list.find_all('div', class_=re.compile(r'tier-row|custom-tier-burst'))
    print(f"Found {len(tier_rows)} potential tier rows\n")
    
    # Look for tier labels (T0, T1, etc.)
    tier_labels = tier_list.find_all(string=re.compile(r'\bT\d(?:\.\d)?\b'))
    print(f"Found {len(tier_labels)} tier label strings:")
    for i, label in enumerate(tier_labels[:10]):
        parent = label.parent
        print(f"  {i+1}. '{label.strip()}' in <{parent.name} class='{parent.get('class')}'>")
    
    print("\n" + "="*80)
    print("Looking for role-tier structure...")
    print("="*80 + "\n")
    
    # Try to find role sections
    role_sections = tier_list.find_all('div', class_='custom-tier-container')
    print(f"Found {len(role_sections)} role sections\n")
    
    for i, section in enumerate(role_sections[:2]):  # Just first 2 for analysis
        print(f"\n--- Role Section {i+1} ---")
        
        # Find role header
        header = section.find('div', class_=re.compile(r'custom-header|burst-type'))
        if header:
            role_text = header.get_text(strip=True)
            print(f"Role: {role_text}")
        
        # Find tier bursts (groups of characters per tier)
        bursts = section.find_all('div', class_='custom-tier-burst')
        print(f"Tier bursts in this role: {len(bursts)}")
        
        for j, burst in enumerate(bursts[:3]):  # First 3 tiers
            # Look for tier label
            tier_label_elem = burst.find('div', class_='tier-label')
            if tier_label_elem:
                tier = tier_label_elem.get_text(strip=True)
                print(f"\n  Tier {j+1}: {tier}")
                
                # Find characters in this tier
                chars = burst.find_all('a', href=re.compile(r'/characters/'))
                print(f"  Characters ({len(chars)}):")
                for char_link in chars[:5]:  # First 5 chars
                    char_name = char_link.find('span')
                    if char_name:
                        print(f"    - {char_name.get_text(strip=True)}")


if __name__ == "__main__":
    analyze_structure()
