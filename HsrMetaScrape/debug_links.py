from bs4 import BeautifulSoup
import re

html = open('tier_list_debug.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'lxml')

links = soup.find_all('a', href=re.compile(r'/characters/'))
print(f'Total links: {len(links)}\n')

for i, link in enumerate(links[2:7]):
    print(f"=== Link {i+2} ===")
    print(f"href: {link.get('href')}")
    print(f"Text: |{link.get_text().strip()}|")
    print(f"Has span: {link.find('span') is not None}")
    if link.find('span'):
        print(f"Span text: |{link.find('span').get_text().strip()}|")
    print()
