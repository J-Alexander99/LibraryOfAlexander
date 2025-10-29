from bs4 import BeautifulSoup
import json
import re

with open('tier_list_debug.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')

# Look for script tags with JSON data
scripts = soup.find_all('script', type='application/json')
print(f"Found {len(scripts)} JSON script tags\n")

for i, script in enumerate(scripts[:5]):
    content = script.string
    if content and len(content) < 5000:  # Only print if not too long
        print(f"=== Script {i} ===")
        print(content[:500])
        print()

# Look for data attributes
print("\n=== Looking for data attributes ===")
elements_with_data = soup.find_all(attrs={'data-tier': True})
print(f"Elements with data-tier: {len(elements_with_data)}")

# Check if there's a __GATSBY or __NEXT_DATA__ or similar
all_scripts = soup.find_all('script')
print(f"\nTotal script tags: {len(all_scripts)}")

for script in all_scripts:
    if script.string and ('__GATSBY' in script.string or 'pageContext' in script.string or 'tierList' in script.string):
        print(f"Found interesting script:")
        print(script.string[:1000])
        break
