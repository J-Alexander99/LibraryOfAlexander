from bs4 import BeautifulSoup

with open('tier_list_debug.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')

tier_list = soup.find('div', class_='custom-tier-list-hsr')
role_sections = tier_list.find_all('div', class_='custom-tier-container')

print(f"Total role sections: {len(role_sections)}")

for i, section in enumerate(role_sections[:3]):
    print(f"\n--- Section {i} ---")
    bursts = section.find_all('div', class_='custom-tier-burst')
    print(f"Bursts with class 'custom-tier-burst': {len(bursts)}")
    
    # Try finding by recursive=False
    direct_bursts = section.find_all('div', class_='custom-tier-burst', recursive=False)
    print(f"Direct child bursts: {len(direct_bursts)}")
    
    # Find tier labels
    labels = section.find_all('div', class_='tier-label')
    print(f"Tier labels found: {len(labels)}")
    
    if labels:
        for j, label in enumerate(labels[:3]):
            print(f"  Label {j}: {label.get_text()}")
    
    # Print structure
    children = list(section.children)
    print(f"Direct children: {len([c for c in children if c.name])}")
    for j, child in enumerate([c for c in children if c.name][:5]):
        print(f"  Child {j}: <{child.name} class='{child.get('class')}'>")
