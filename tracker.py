import requests
from bs4 import BeautifulSoup
import smtplib
import re

URL = 'https://www.etsy.com/nz/listing/884020481/anklet-bracelet-gold-chain-anklet-thick?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sc_gallery-1-2&plkey=811b0d827e70a34e51d0455890ae256faf698715%3A884020481&pro=1'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}

def check_price():
    page = requests.get(URL, headers = headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find("h2", class_="wt-screen-reader-only").get_text()
    price = soup.find("p", class_="wt-text-title-03 wt-mr-xs-2").get_text()
    saved = soup.find("p", class_="wt-text-caption wt-text-slime")
    price = re.findall('\d+\.\d+', price)
    if (saved == None):
        saved = 'Not on sale'
    else:
        saved = saved.get_text()
        saved = saved.strip()

    converted_price = float(price[0])

    if (converted_price < 35):
        send_mail(saved)
    print(saved)

def send_mail(saved):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    #### unique to you for sending to your own email 
    server.login('xx', 'xx')
    subject = 'Item has dropped in price'
    body =  saved

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'xx',
        'xx',
        msg
    )

    print("sent")

    server.quit()

check_price()