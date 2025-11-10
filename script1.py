# %%
import requests
from bs4 import BeautifulSoup

one_book_url = "https://books.toscrape.com/catalogue/my-paris-kitchen-recipes-and-stories_910/index.html"

def scrap_book(url):
    book = requests.get(url)
    soup = BeautifulSoup(book.content, 'html.parser')
    titre = soup.find('h1').get_text()
    print(titre)

scrap_book(one_book_url)