"""
Enhanced scraper for Prydwen.gg HSR Tier List - All Game Modes
Uses Selenium to click through tabs and the accurate div-based extraction method
"""

import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Mapping from div classes to tier labels
DIV_CLASS_TO_TIER = {
    'tier-0': 'T0',
    'tier-05': 'T0.5',
    'tier-1': 'T1',
    'tier-15': 'T1.5',
    'tier-2': 'T2',
    'tier-25': 'T2.5',
    'tier-3': 'T3',
    'tier-35': 'T3.5',
    'tier-4': 'T4',
    'tier-45': 'T4.5',
    'tier-5': 'T5',
}

TIER_TO_RATING = {
    'T0': 10,
    'T0.5': 9,
    'T1': 8,
    'T1.5': 7,
    'T2': 6,
    'T2.5': 5,
    'T3': 4,
    'T3.5': 3,
    'T4': 2,
    'T4.5': 1.5,
    'T5': 1,
}

GAME_MODES = {
    0: {'key': 'MoC', 'name': 'Memory of Chaos'},
    1: {'key': 'PF', 'name': 'Pure Fiction'},
    2: {'key': 'AS', 'name': 'Apocalyptic Shadow'}
}

print("File created successfully")
