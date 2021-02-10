import requests
from bs4 import BeautifulSoup
import smtplib
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

PATH = 'C:\Program Files (x86)\chromedriver.exe'
URL = 'https://www.etsy.com/nz/listing/884020481/anklet-bracelet-gold-chain-anklet-thick?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sc_gallery-1-2&plkey=811b0d827e70a34e51d0455890ae256faf698715%3A884020481&pro=1'

driver = webdriver.Chrome(PATH)
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}

def check_price():
    page = requests.get(URL, headers = headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find("h2", class_="wt-screen-reader-only").get_text()
    current_price = soup.find("p", class_="wt-text-title-03 wt-mr-xs-2").get_text()
    saved = soup.find("p", class_="wt-text-caption wt-text-slime")
    price = re.findall('\d+\.\d+', current_price)
    if (saved == None):
        saved = 'Not on sale'
    else:
        saved = saved.get_text()
        saved = saved.strip()

    if (float(price[0]) < 35):
        send_mail(saved, current_price)
        check_stock()

def send_mail(saved, current_price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    #### unique to you for sending to your own email 
    server.login('guistar9786@gmail.com', 'uojozsrfxskqctak')
    subject = 'Item has dropped in price'
    body =  'This item is currently : ' + current_price.strip() + ' ' + saved

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'guistar9786@gmail.com',
        'guistar9786@gmail.com',
        msg
    )

    print("sent")

    server.quit()

def check_stock(): 
    driver.get("https://www.etsy.com/nz")
    print(driver.title)

    search = driver.find_element_by_name("s")
    search.send_keys("test")
    search.send_keys(Keys.RETURN)

    try: 
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "main"))
        )
    except:
        driver.quit()

    main = driver.find_element_by_id()
    driver.quit()

check_price()