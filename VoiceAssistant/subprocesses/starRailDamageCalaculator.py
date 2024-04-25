def calculate_damage(attacker_level, dmg_reduction_1, dmg_reduction_2, character_stats):
    # Unpack character stats
    skill_multiplier, extra_multiplier, scaling_attribute, extra_dmg, \
    elemental_dmg_percent, all_type_dmg_percent, def_multiplier, \
    res_percent, res_pen_percent, dmg_taken_percent, toughness_multiplier, weaken_percent = character_stats

    # Calculate Base DMG
    base_dmg = (skill_multiplier + extra_multiplier) * scaling_attribute + extra_dmg

    # Calculate DMG% Multiplier
    dmg_percent_multiplier = 100 + elemental_dmg_percent + all_type_dmg_percent

    # Calculate DEF Multiplier
    def_multiplier = 100 - (def_multiplier / (def_multiplier + 200 + 10 * attacker_level))

    # Calculate RES Multiplier
    res_multiplier = 100 - (res_percent - res_pen_percent)

    # Calculate DMG Taken Multiplier
    dmg_taken_multiplier = 100 + dmg_taken_percent

    # Calculate Universal DMG Reduction Multiplier
    universal_dmg_reduction_multiplier = 100 * (1 - dmg_reduction_1) * (1 - dmg_reduction_2)

    # Calculate Weaken Multiplier
    weaken_multiplier = 100 - weaken_percent

    # Calculate Expected DMG
    expected_dmg = (
        base_dmg
        * dmg_percent_multiplier / 100
        * def_multiplier / 100
        * res_multiplier / 100
        * dmg_taken_multiplier / 100
        * universal_dmg_reduction_multiplier / 100
        * weaken_multiplier / 100
    )

    return round(expected_dmg)


# Example inputs for a generic character
attacker_level = 50  # Set the attacker's level
dmg_reduction_1 = 0.1  # Example value for dmg_reduction_1
dmg_reduction_2 = 0.2  # Example value for dmg_reduction_2

character_stats = (
    60,  # skill_multiplier
    0,   # extra_multiplier
    1062,  # scaling_attribute
    0,    # extra_dmg
    25.8,  # elemental_dmg_percent
    10,   # all_type_dmg_percent
    50,   # def_multiplier
    80,   # res_percent
    0,    # res_pen_percent
    0,    # dmg_taken_percent
    90,   # toughness_multiplier
    0,    # weaken_percent
)

# Calculate expected damage for the generic character
expected_dmg = calculate_damage(attacker_level, dmg_reduction_1, dmg_reduction_2, character_stats)

# Display result
print("Expected Damage for the Generic Character:", expected_dmg)
