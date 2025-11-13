# %%
import requests
from bs4 import BeautifulSoup
import re

# une seule page
CATEGORY_URL = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"

# plusieurs pages
# CATEGORY_URL = "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"

def get_books_url():
    site = requests.get("https://books.toscrape.com/index.html")
    home_page = BeautifulSoup(site.content, 'html.parser')
    category_books_url = []

    categories_infos = home_page.find_all('a', href=re.compile("books/"))
    return categories_infos
    
def transform_cat(categories_infos):
    categories = []
    for a in categories_infos:
        category = {}
        category['name'] = a.get_text().strip()
        category['url'] = a.get('href').strip()
        categories.append(category)
    return categories
            
def scrap_category():
    categories_infos = get_all_cat()
    transform_cat(categories_infos)

scrap_category()
# %%
