import time
import json
import os
import bs4

from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.firefox.service import Service

from bs4 import BeautifulSoup

url_drop = input('URL: ' )
currency = float(input('Curr: '))

def get_page_source(url):
    s = Service("E:\\VS_CODE\\Avito\\geckodriver.exe")
    useragent = UserAgent()

    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", useragent.opera)
    options.set_preference('intl.accept_languages', 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7')

    driver = webdriver.Firefox(service=s, options=options)

    try:
        driver.get(url=url)
        time.sleep(5)
        driver.implicitly_wait(10)
        items = driver.page_source
        with open('index1.html', "w", encoding="utf-8") as file:
            file.write(items)
        # print(items)
    except Exception as ex:
        print(ex)

    driver.close()
    driver.quit()

def get_price(sticker):
    with open('index1.html', 'r', encoding="utf-8") as file:
        page = file.read()

    soup = BeautifulSoup(page, "html.parser")

    span = soup.find(class_='market_table_value normal_price')
    price = span.find(class_='normal_price').text.split('$')
    price = price[1].split(' ')
    price = float(price[0])
    price_ru = currency * price 

    print('Стоимость стикера ' + sticker + ': ' + "%.2f" % price_ru + ' руб.')

def get_sticker_url():
    with open('index1.html', 'r', encoding="utf-8") as file:
        page = file.read()

    soup = BeautifulSoup(page, "html.parser")

    div = soup.find(id="sticker_info")
    stick = div.find('br')

    text = ''

    while(stick):
        stick = stick.next_sibling
        if isinstance(stick, bs4.element.Tag):
            text += stick.get_text()
        elif isinstance(stick, bs4.element.NavigableString):
            text += stick

    text = text.split(',')
    print(f'Стикеров на оружии: {len(text)}')
    for stick in text:
        if 'Наклейка:' in stick:
            stick = stick.split('Наклейка:')[1]
        
        sticker = stick
        print(f'Стикер {stick}')

        stick = stick.split(' ')
        if '|' in stick:
            stick.remove('|')
        if '' in stick:
            stick.remove('')
        length = len(stick)

        if length == 1:
            url = f'https://steamcommunity.com/market/search?q=Наклейка+{stick[0]}'
        elif length == 2:
            url = f'https://steamcommunity.com/market/search?q=Наклейка+%7C+{stick[0]}+{stick[1]}'
        elif length == 3:
            url = f'https://steamcommunity.com/market/search?q=Наклейка+%7C+{stick[0]}+{stick[1]}+{stick[2]}'
        elif length == 4:
            url = f'https://steamcommunity.com/market/search?q=Наклейка+%7C+{stick[0]}+{stick[1]}+{stick[2]}+{stick[3]}'
        elif length == 5:
            url = f'https://steamcommunity.com/market/search?q=Наклейка+%7C+{stick[0]}+{stick[1]}+{stick[2]}+{stick[3]}+{stick[4]}'

        print(url)
        get_page_source(url)
        get_price(sticker)
    return url

get_page_source(url_drop)
get_sticker_url()
