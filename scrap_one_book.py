# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd

one_book_url = "https://books.toscrape.com/catalogue/my-paris-kitchen-recipes-and-stories_910/index.html"

words_to_numbers = {
    "Zero": 0,
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    }

def scrap_book(url):
    book = requests.get(url)
    soup = BeautifulSoup(book.content, 'html.parser')
    title = soup.find('h1').get_text()
    book_infos = soup.find_all('td')
    book_description = soup.find('meta', attrs={'name':'description'})['content'].strip()
    book_category = soup.find_all('li')[2].get_text().strip()
    book_rating_str = soup.find('p', class_='star-rating')['class'][1]
    book_rating_int = words_to_numbers.get(book_rating_str)
    book_imgurl = soup.find('img')['src']
    book_quantity = ''.join(c for c in book_infos[2] if c.isdigit())

    book_to_load = {
        'product_page_url': book_imgurl,
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

    # print(book_to_load)

    df = pd.DataFrame([book_to_load])
    df.to_csv("one_book_scraped.csv", index=False)


scrap_book(one_book_url)

# %%
