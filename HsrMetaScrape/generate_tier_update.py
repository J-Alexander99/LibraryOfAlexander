"""
Generate tierUpdate.json from hsr_tier_ratings_all_modes.json
Combines all three mode ratings into a single character list
"""

import json


def generate_tier_update():
    """
    Read all modes data and create condensed format with:
    - Single character list
    - MoC, PF, AS ratings for each character
    - Total rating (sum of all three)
    """
    
    print("📖 Reading hsr_tier_ratings_all_modes.json...")
    with open('hsr_tier_ratings_all_modes.json', 'r', encoding='utf-8') as f:
        all_modes_data = json.load(f)
    
    # Build character dictionary
    characters = {}
    
    for mode_key in ['MoC', 'PF', 'AS']:
        mode_data = all_modes_data[mode_key]
        mode_characters = mode_data['characters']
        
        print(f"  Processing {mode_key}: {len(mode_characters)} characters")
        
        for char_name, char_info in mode_characters.items():
            # Initialize character if first time seeing them
            if char_name not in characters:
                characters[char_name] = {
                    'name': char_name,
                    'MoC_rating': 0,
                    'PF_rating': 0,
                    'AS_rating': 0,
                    'total_rating': 0
                }
            
            # Add mode-specific data
            if mode_key == 'MoC':
                characters[char_name]['MoC_rating'] = char_info['rating']
            elif mode_key == 'PF':
                characters[char_name]['PF_rating'] = char_info['rating']
            elif mode_key == 'AS':
                characters[char_name]['AS_rating'] = char_info['rating']
    
    # Calculate total ratings
    for char_name, char_data in characters.items():
        char_data['total_rating'] = (
            char_data['MoC_rating'] + 
            char_data['PF_rating'] + 
            char_data['AS_rating']
        )
    
    # Convert to list sorted by total rating (descending)
    character_list = sorted(
        characters.values(), 
        key=lambda x: x['total_rating'], 
        reverse=True
    )
    
    # Create output structure
    output = {
        'generated_at': '2025-10-29',
        'total_characters': len(character_list),
        'characters': character_list
    }
    
    # Write to file
    print("\n💾 Writing tierUpdate.json...")
    with open('tierUpdate.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated tierUpdate.json with {len(character_list)} characters")
    
    # Show summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    print(f"Total characters: {len(character_list)}")
    
    # Show top 5 by total rating
    print("\nTop 5 characters by total rating:")
    for i, char in enumerate(character_list[:5], 1):
        print(f"  {i}. {char['name']}: {char['total_rating']:.1f} total")
        print(f"     MoC: {char['MoC_rating']}, PF: {char['PF_rating']}, AS: {char['AS_rating']}")
    
    # Show bottom 5
    print("\nBottom 5 characters by total rating:")
    for i, char in enumerate(character_list[-5:], len(character_list)-4):
        print(f"  {i}. {char['name']}: {char['total_rating']:.1f} total")
        print(f"     MoC: {char['MoC_rating']}, PF: {char['PF_rating']}, AS: {char['AS_rating']}")
    
    print("="*70)


if __name__ == "__main__":
    generate_tier_update()
