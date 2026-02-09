import requests
from bs4 import BeautifulSoup
import json
import html
import pandas as pd
from openpyxl import load_workbook

# ------------------ PRODUCTOS ------------------
product_urls = [
    {'name': 'Nipagin Metilparabeno', 'url': 'https://puraquimica.com.ar/producto/nipagin-metilparabeno-x-kg/'},
    {'name': 'Carbopol Acrypol 940', 'url': 'https://puraquimica.com.ar/producto/carbopol-acrypol-940-x-kg/'},
    {'name': 'Trietanolamina 85%', 'url': 'https://puraquimica.com.ar/producto/trietanolamina-85-x-kg-x-kilos/'},
    {'name': 'Glicerina Refinada Alimenticia', 'url': 'https://puraquimica.com.ar/producto/glicerina-refinada-alimenticia-x-kg-vegetal/'}
]

headers = {
    'User-Agent': 'Mozilla/5.0'
}

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
            form_tag = soup.find('form', class_='variations_form')

            if form_tag and 'data-product_variations' in form_tag.attrs:
                variations_json_encoded = form_tag['data-product_variations']
                variations_json_unescaped = html.unescape(variations_json_encoded).replace('\\/', '/')
                variations_data = json.loads(variations_json_unescaped)

                for variation in variations_data:
                    description = BeautifulSoup(variation.get('variation_description', ''), 'html.parser').get_text(strip=True)
                    if '1 kgs' in description:
                        price = variation.get('display_price')
                        if price:
                            price_1kg = float(price)
                        break

    except Exception as e:
        print("Error:", e)

    results.append({'Product': product_name, 'Price': price_1kg})

df_prices = pd.DataFrame(results)
print(df_prices)

# ------------------ GUARDAR HISTORIAL ------------------
from datetime import datetime
import os

df_prices["fecha"] = datetime.now()

archivo = "historial_precios.csv"

if not os.path.exists(archivo):
    df_prices.to_csv(archivo, index=False)
else:
    df_prices.to_csv(archivo, mode="a", header=False, index=False)

print("Historial guardado correctamente")

# Calcular costo por pote
precios = {row["Product"]: row["Price"] for _, row in df_prices.iterrows()}

costo_pote = (
    precios["Carbopol Acrypol 940"]/40 +
    precios["Nipagin Metilparabeno"]/200 +
    precios["Trietanolamina 85%"]/40 +
    precios["Glicerina Refinada Alimenticia"]/40
)

df_pote = pd.DataFrame([{
    "Product": "COSTO_POTE",
    "Price": costo_pote,
    "fecha": datetime.now()
}])

df_prices = pd.concat([df_prices, df_pote])
