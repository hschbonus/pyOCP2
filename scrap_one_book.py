# %%
import requests
from bs4 import BeautifulSoup
import csv

BOOK_URL = "https://books.toscrape.com/catalogue/my-paris-kitchen-recipes-and-stories_910/index.html"

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

def transform_book_info(soup):
    title = soup.find('h1').get_text()
    book_infos = soup.find_all('td')
    book_description = soup.find('meta', attrs={'name':'description'})['content'].strip()
    book_category = soup.find_all('li')[2].get_text().strip()
    book_rating_str = soup.find('p', class_='star-rating')['class'][1]
    book_rating_int = words_to_numbers.get(book_rating_str)
    book_imgurl = soup.find('img')['src']
    book_quantity = ''.join(c for c in book_infos[2] if c.isdigit())
    book_to_load = {
        'product_page_url': BOOK_URL,
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

def load_book(book_to_load, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=book_to_load.keys())
        writer.writeheader()
        writer.writerow(book_to_load)

def scrap_book(url):
    soup = get_book_infos(url)
    book_to_load = transform_book_info(soup)
    load_book(book_to_load, filename='one_book.csv')

scrap_book(BOOK_URL)

# %%
