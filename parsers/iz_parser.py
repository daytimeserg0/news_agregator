from parsers.modules import get_page, get_hashtags, db_insert, get_img, img_writer, iz_all_news
from datetime import datetime
import time


def iz_parser():
    url = 'https://iz.ru/feed'
    soup = get_page(url).find(id="block-purple-content")
    print(datetime.now().time())
    end_time = ''
    all_news = iz_all_news(soup)

    for news_item in all_news:
        process_news(*news_item, end_time)

    time.sleep(120)  # менять время ожидания здесь
    while True:
        soup = get_page(url).find(id="block-purple-content")
        print(datetime.now().time())
        end_time = all_news[0][2]
        all_news = iz_all_news(soup)

        for news_item in all_news:
            stopper = process_news(*news_item, end_time)
            if stopper == -1:
                break
        time.sleep(120)  # менять время ожидания здесь


def process_news(news_title, news_href, time_check, end_time):
    if time_check == end_time:
        return -1

    soup = get_page(news_href)

    # КАРТИНКА
    img_href = "https:" + soup.find(class_="owl-lazy")['data-src']

    c = 0
    while ("DefaultPic" in str(img_href)) and (c != 12):  # менять время ожидания здесь
        time.sleep(30)
        c += 1
        soup = get_page(news_href)
        img_href = "https:" + soup.find(class_="owl-lazy")['data-src']
        print("новость дополняется ", datetime.now().time())

    img = get_img(img_href)
    img_title = img_writer(img, news_title)

    # ДАТА И ВРЕМЯ
    news_date = soup.find('time').text

    # ТЭГИ
    news_hashtags = soup.find_all("div", itemprop='about')
    hashtags = get_hashtags(news_hashtags)

    # БАЗА ДАННЫХ
    db_insert(news_title, news_href, hashtags, news_date, img_title)

