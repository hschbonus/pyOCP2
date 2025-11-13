# %%
import requests
from bs4 import BeautifulSoup
import re

# une seule page
# CATEGORY_URL = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"

# plusieurs pages
CATEGORY_URL = "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"

def get_books_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    category_books_url = []
    url_container = soup.find_all('h3')
    
    for h3 in url_container:
        category_books_url.append(h3.find('a')['href'])

    is_next = soup.find(class_='next')
    
    while is_next != None:
        next_page_number = is_next.find('a')['href']
        base_url = url.replace('index.html', '')
        next_url = f'{base_url}{next_page_number}'
        next_page = requests.get(next_url)
        soup = BeautifulSoup(next_page.content, 'html.parser')

        url_container = soup.find_all('h3')
    
        for h3 in url_container:
            category_books_url.append(h3.find('a')['href'])
        
        is_next = soup.find(class_='next')
    
    print(category_books_url)

        



    
# def transform_cat(categories_infos):
#     categories = []
#     for a in categories_infos:
#         category = {}
#         category['name'] = a.get_text().strip()
#         category['url'] = a.get('href').strip()
#         categories.append(category)
#     return categories
            
def scrap_category(url):
    get_books_url(url)

scrap_category(CATEGORY_URL)
# %%
