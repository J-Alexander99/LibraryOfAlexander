import requests
from bs4 import BeautifulSoup

html = requests.get('https://www.prydwen.gg/star-rail/tier-list').text
soup = BeautifulSoup(html, 'lxml')

# Find all character links
char_links = soup.find_all('a', href=lambda x: x and '/star-rail/characters/' in x)

print("Dan Heng variants found:")
for link in char_links:
    href = link.get('href')
    if 'dan-heng' in href.lower():
        # Try to get character name from the link
        img = link.find('img')
        name = img.get('alt', 'No name') if img else 'No name'
        print(f"  URL: {href}")
        print(f"  Name from img alt: {name}")
        print()
