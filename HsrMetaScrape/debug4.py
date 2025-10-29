from bs4 import BeautifulSoup

with open('tier_list_debug.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')

tier_list = soup.find('div', class_='custom-tier-list-hsr')
role_sections = tier_list.find_all('div', class_='custom-tier-container')

section = role_sections[1]  # Pick second section
bursts = section.find_all('div', class_='custom-tier-burst')

if bursts:
    burst = bursts[0]
    print("First burst content:")
    print(burst.prettify()[:2000])
