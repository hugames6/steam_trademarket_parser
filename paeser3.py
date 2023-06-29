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
price_list = []

def get_page_source(url):
    s = Service("\geckodriver.exe")
    useragent = UserAgent()

    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", useragent.opera)
    # options.set_preference('intl.accept_languages', 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7')

    driver = webdriver.Firefox(service=s, options=options)

    try:
        driver.get(url=url)
        time.sleep(5)
        driver.implicitly_wait(10)
        items = driver.page_source
        with open('index1.html', "w", encoding="utf-8") as file:
            file.write(items)

        soup = BeautifulSoup(items, "html.parser")

        div = soup.find(id="searchResultsTable")
        drop_price = div.find_all(class_="market_commodity_orders_header_promote")
        drop_price = drop_price[1].text
        drop_price = drop_price.split('$')
        drop_price = float(drop_price[1]) * currency
        print('Стоимость дропа: ' + "%.2f" % drop_price + ' руб.')
        # print(items)
    except Exception as ex:
        print(ex)

    driver.close()
    driver.quit()
    return(drop_price)

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
    price_list.append(price_ru)

def get_sticker():
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
        elif length == 6:
            url = f'https://steamcommunity.com/market/search?q=Наклейка+%7C+{stick[0]}+{stick[1]}+{stick[2]}+{stick[3]}+{stick[4]}+{stick[5]}'
            
        get_page_source(url)
        get_price(sticker)
    return url

def percent(drop_price):
    stickers_total_price = 0
    for price in price_list:
        stickers_total_price = stickers_total_price + price
    print(f'Стоимость всех стикеров: ' + "%.2f" % stickers_total_price + ' руб.')
    percent = stickers_total_price / drop_price
    percent = float('%.2f' % percent) 

    return percent

drop_price = get_page_source(url_drop)
get_sticker()
per = percent(drop_price)
print(f'Стоимость стикеров равнf {per * 100}% от стоимости дропа.')