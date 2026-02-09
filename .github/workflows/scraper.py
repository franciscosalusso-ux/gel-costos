import requests
from bs4 import BeautifulSoup
import json
import html
import pandas as pd
from datetime import datetime
import os

# ------------------ PRODUCTOS ------------------
product_urls = [
    {'name': 'Nipagin Metilparabeno', 'url': 'https://puraquimica.com.ar/producto/nipagin-metilparabeno-x-kg/'},
    {'name': 'Carbopol Acrypol 940', 'url': 'https://puraquimica.com.ar/producto/carbopol-acrypol-940-x-kg/'},
    {'name': 'Trietanolamina 85%', 'url': 'https://puraquimica.com.ar/producto/trietanolamina-85-x-kg-x-kilos/'},
    {'name': 'Glicerina Refinada Alimenticia', 'url': 'https://puraquimica.com.ar/producto/glicerina-refinada-alimenticia-x-kg-vegetal/'}
]

headers = {'User-Agent': 'Mozilla/5.0'}

results = []

# ------------------ SCRAPING ------------------
for product_info in product_urls:
    product_name = product_info['name']
    url = product_info['url']
    price_1kg = 'N/A'

    print(f"Procesando {product_name}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        lines = response.text.splitlines()

        target_line = None
        for line in lines:
            if '<form class="variations_form' in line:
                target_line = line
                break

        if target_line:
            soup = BeautifulSoup(target_line, 'html.parser')
            form_tag = so_

