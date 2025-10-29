from bs4 import BeautifulSoup
import re

with open('tier_list_debug.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')

tier_list = soup.find('div', class_='custom-tier-list-hsr')
role_sections = tier_list.find_all('div', class_='custom-tier-container')

section = role_sections[1]  # Pick second section which has bursts

bursts = section.find_all('div', class_='custom-tier-burst')
print(f"Found {len(bursts)} tier bursts\n")

for i, burst in enumerate(bursts):
    print(f"=== Burst {i} ===")
    
    # Look for tier label - might be in different places
    tier_span = burst.find('span', string=re.compile(r'\bT\d'))
    if tier_span:
        print(f"Tier (from span): {tier_span.get_text()}")
    
    # Try finding div with tier-row class
    tier_rows = burst.find_all('div', class_='tier-row')
    print(f"Tier rows: {len(tier_rows)}")
    
    for j, row in enumerate(tier_rows[:2]):
        print(f"\n  Row {j}:")
        # Look for tier label in row
        row_label = row.find('span', string=re.compile(r'\bT\d'))
        if row_label:
            print(f"    Tier: {row_label.get_text()}")
        
        # Look for characters
        chars = row.find_all('a', href=re.compile(r'/characters/'))
        print(f"    Characters: {len(chars)}")
        for char_link in chars[:3]:
            char_span = char_link.find('span')
            if char_span:
                print(f"      - {char_span.get_text().strip()}")
    
    print()
