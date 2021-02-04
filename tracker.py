import requests
from bs4 import BeautifulSoup
URL = 'https://www.aliexpress.com/item/1005002021945079.html?spm=2114.12010615.8148356.3.67a140e5QGAl4O&spm=a2g0o.store_home.hotSpots_6000568986382.0'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}

page = requests.get(URL, headers = headers)

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.find("h1", class_ = "product-title-text").text

print(title)