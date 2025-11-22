# %%
import requests
from bs4 import BeautifulSoup
import csv
import re
import time

HOME_URL = "https://books.toscrape.com/index.html"
CATEGORY_URL = "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"


WORDS_TO_NUMBER = {
    "Zero": 0,
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    }

def all_categories(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    link_list = soup.find_all('a', href=re.compile("category/books/"))
    cat_list = []    
    cat_base_url ='https://books.toscrape.com/'
    for link in link_list:
        cat = {}
        cat['name'] = link.get_text().strip()
        cat['url'] = f'{cat_base_url}{link['href']}'
        cat_list.append(cat)
    return cat_list

all_categories(HOME_URL)

def get_page(cat_index, soup):
    books_url_buffer = []
    url_container = soup.find_all('h3')
    for h3 in url_container:
        original_book_url = h3.find('a')['href']
        add_book_url = original_book_url.replace('../../..', '')
        base_book_url = 'https://books.toscrape.com/catalogue'
        book_full_url = f'{base_book_url}{add_book_url}'
        books_url_buffer.append(book_full_url)

    is_next = soup.find(class_='next')
    if is_next != None:
        next_page_number = is_next.find('a')['href']
        base_url = cat_index.replace('index.html', '')
        next_url = f'{base_url}{next_page_number}'
    else: next_url = None

    return books_url_buffer, next_url

def get_category(cat_index):

    category_books_url = []

    page = requests.get(cat_index)
    soup = BeautifulSoup(page.content, 'html.parser')

    books_url_buffer, next_page_url = get_page(cat_index, soup)
    category_books_url.extend(books_url_buffer)

    while next_page_url != None:
        next_page = requests.get(next_page_url)
        soup = BeautifulSoup(next_page.content, 'html.parser')
        books_url_buffer, next_page_url = get_page(cat_index, soup)
        category_books_url.extend(books_url_buffer)
    return category_books_url

def get_book_infos(url):
    book = requests.get(url)
    soup = BeautifulSoup(book.content, 'html.parser')
    
    return soup

def transform_book_info(url, soup):
    title = soup.find('h1').get_text()
    book_infos = soup.find_all('td')
    book_upc = soup.find_all('td')[0].get_text()
    book_price_incl = soup.find_all('td')[3].get_text()
    book_price_excl = soup.find_all('td')[2].get_text()
    book_description = soup.find('meta', attrs={'name':'description'})['content'].strip()
    book_category = soup.find_all('li')[2].get_text().strip()
    book_rating_str = soup.find('p', class_='star-rating')['class'][1]
    book_rating_int = WORDS_TO_NUMBER.get(book_rating_str)
    book_img_link = soup.find('img')['src']
    book_img_base_url = 'https://books.toscrape.com/'
    book_img_add_url = book_img_link.replace('../..', '')
    book_img_url = f'{book_img_base_url}{book_img_add_url}'
    print(book_img_url)
    raw = book_infos[5].get_text()
    book_quantity = ''.join(c for c in raw if c.isdigit())
    book_to_load = {
        'product_page_url': url,
        'universal_product_code (upc)': book_upc,
        'title': title,
        'price_including_tax': book_price_incl,
        'price_excluding_tax': book_price_excl,
        'number_available': book_quantity,
        'product_description': book_description,
        'category': book_category,
        'review_rating': book_rating_int,
        'image_url': book_img_url
    }

    img_data = requests.get(book_img_url).content
    with open(f'images/{book_upc}.jpg', "wb") as handler:
        handler.write(img_data)

    return book_to_load

def load_category(data, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        FIELDNAMES = [
            "product_page_url",
            "universal_product_code (upc)",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "review_rating",
            "image_url"
        ]
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)
        pass

def scrap_category(category_url, category_name):
    url_list = get_category(category_url)
    books_to_load = []
    for url in url_list:
        soup = get_book_infos(url)
        book_to_load = transform_book_info(url, soup)
        books_to_load.append(book_to_load)
    load_category(books_to_load, filename=f'csv/{category_name}.csv')
    pass

def scrap_all_books(url):
    cat_list = all_categories(url)
    for cat in cat_list:
        scrap_category(cat['url'], cat['name'])
        print(f'CSV {cat['name']} créé !')
    

start = time.time()
scrap_all_books(HOME_URL)
end = time.time()
print("Temps d'exécution :", round(end - start, 1), "secondes")

#%%