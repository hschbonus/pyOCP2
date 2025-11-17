# %%
import requests
from bs4 import BeautifulSoup
import csv

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
        original_book_url = h3.find('a')['href']
        add_book_url = original_book_url.replace('../../..', '')
        base_book_url = 'https://books.toscrape.com/catalogue'
        book_full_url = f'{base_book_url}{add_book_url}'
        category_books_url.append(book_full_url)

    is_next = soup.find(class_='next')
    
    while is_next != None:
        next_page_number = is_next.find('a')['href']
        base_url = url.replace('index.html', '')
        next_url = f'{base_url}{next_page_number}'
        next_page = requests.get(next_url)
        soup = BeautifulSoup(next_page.content, 'html.parser')

        url_container = soup.find_all('h3')
    
        for h3 in url_container:
            original_book_url = h3.find('a')['href']
            add_book_url = original_book_url.replace('../../..', '')
            base_book_url = 'https://books.toscrape.com/catalogue'
            book_full_url = f'{base_book_url}{add_book_url}'
            category_books_url.append(book_full_url)
        
        is_next = soup.find(class_='next')
    
    return category_books_url

words_to_numbers = {
    "Zero": 0,
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    }

def get_book_infos(url):
    book = requests.get(url)
    soup = BeautifulSoup(book.content, 'html.parser')
    return soup

def transform_book_info(url, soup):
    title = soup.find('h1').get_text()
    book_infos = soup.find_all('td')
    book_description = soup.find('meta', attrs={'name':'description'})['content'].strip()
    book_category = soup.find_all('li')[2].get_text().strip()
    book_rating_str = soup.find('p', class_='star-rating')['class'][1]
    book_rating_int = words_to_numbers.get(book_rating_str)
    book_imgurl = soup.find('img')['src']
    book_quantity = ''.join(c for c in book_infos[2] if c.isdigit())
    book_to_load = {
        'product_page_url': url,
        'universal_product_code (upc)': book_infos[0],
        'title': title,
        'price_including_tax': book_infos[3],
        'price_excluding_tax': book_infos[2],
        'number_available': book_quantity,
        'product_description': book_description,
        'category': book_category,
        'review_rating': book_rating_int,
        'image_url': book_imgurl
    }
    return book_to_load

def load_category(data, field_names, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names.keys())
        writer.writeheader()
        writer.writerow(data)

def scrap_category(category_url):
    url_list = get_books_url(category_url)
    books_to_load = []
    for url in url_list:
        soup = get_book_infos(url)
        book_to_load = transform_book_info(url, soup)
        books_to_load.append(book_to_load)
    load_category(books_to_load, book_to_load, filename='category.csv')

scrap_category(CATEGORY_URL)
# %%
