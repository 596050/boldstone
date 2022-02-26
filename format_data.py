#!/usr/bin/envpython3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 19:34:31 2022

https://business.facebook.com/business/help/120325381656392?id=725943027795860
https://www.facebook.com/business/help/526764014610932?id=725943027795860
https://business.facebook.com/commerce/catalogs/1638438493182970/feeds/351548610213919/overview?business_id=2380586078685156
https://www.facebook.com/business/help/1535453216800644

https://business.facebook.com/commerce/326960679342026/shops?business_id=2380586078685156

@author: pricet
"""

import pandas as pd
from bs4 import BeautifulSoup

catalog_products = pd.read_csv('catalog_products.csv', skiprows=[0, 2])
products_export = pd.read_csv('products_export.csv')
products_export_filtered = products_export.dropna(subset=['Variant SKU'])

new_catalog_products = catalog_products.copy()

#print('catalog_products', catalog_products)
#print('products_export', products_export.head(0))

product_base_url = 'https://boldstone.co.uk/products'

mapping = {
 "id": 'Variant SKU',
 "title": 'Title',
 "price": 'Variant Price', # GBP
 "image_link": 'Image Src',
 "description": 'Body (HTML)',
# "availability": 'in stock',
# "condition": 'new',
 "availability": '',
 "condition": '',
 "link": 'Handle',
 "brand": '',
# "brand": 'Boldstone',
 "google_product_category": '',
 "fb_product_category": '',
"quantity_to_sell_on_facebook": '',
# "quantity_to_sell_on_facebook": '1',
 "sale_price": 'Variant Price', # GBP
 "sale_price_effective_date": '',
 "item_group_id": '',
 "gender": '',
 "color": '',
 "size": '',
 "age_group": '',
 "material": '',
 "pattern": '',
 "shipping": '',
 "shipping_weight": 'Variant Grams',
 "style[0]": ''
}

for column in catalog_products:
    if mapping[column] != '':
        new_catalog_products[column] = products_export_filtered[mapping[column]]

new_catalog_products['quantity_to_sell_on_facebook'] = '1'
new_catalog_products['brand'] = 'Boldstone'
new_catalog_products['condition'] = 'new'
new_catalog_products['availability'] = 'in stock'

for index, row in new_catalog_products.iterrows():
    soup = BeautifulSoup(row['description'])
    new_catalog_products.loc[index,'description' ] = soup.get_text()
    new_catalog_products.loc[index,'price' ] = str(new_catalog_products.loc[index,'price' ]) + " " + "GBP"
    new_catalog_products.loc[index,'sale_price' ] = str(new_catalog_products.loc[index,'sale_price' ]) + " " + "GBP"
    if (new_catalog_products.loc[index,'shipping_weight' ] > 100):
        new_catalog_products.loc[index,'shipping_weight' ] = str(new_catalog_products.loc[index,'shipping_weight']/1000)  + " " + "kg"
    else:
        new_catalog_products.loc[index,'shipping_weight' ] = str(new_catalog_products.loc[index,'shipping_weight' ]) + " " + "g"
    new_catalog_products.loc[index,'link' ] = product_base_url + "/" + str(new_catalog_products.loc[index,'link' ])



### Fields to add:
#additional_image_link
#google_product_category
#fb_product_category


compression_opts = dict(method=None, archive_name='boldstone_facebook_products.csv')  
new_catalog_products.to_csv('boldstone_facebook_products.csv', index=False) 
