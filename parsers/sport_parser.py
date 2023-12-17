from parsers.modules import get_page, get_hashtags, db_insert, get_img, img_writer, sport_all_news
from datetime import datetime
from babel.dates import format_datetime
import time
import locale

locale.setlocale(locale.LC_TIME, 'ru_RU')


def sport_parser():
    url = "https://www.sport.ru/news/"
    soup = get_page(url)
    end_time = ''
    all_news = sport_all_news(soup)

    for news_item in all_news:
        process_news(*news_item, end_time)

    time.sleep(120)  # менять время ожидания здесь
    while True:
        soup = get_page(url)
        print(datetime.now().time())
        end_time = all_news[0][2]
        all_news = sport_all_news(soup)

        for news_item in all_news:
            stopper = process_news(*news_item, end_time)
            if stopper == -1:
                break
        time.sleep(120)  # менять время ожидания здесь


def process_news(news_title, news_href, time_check, end_time):
    if time_check == end_time:
        return -1

    soup = get_page(news_href)

    # ДАТА И ВРЕМЯ ПОМЕНЯТЬ ФОРМАТ
    news_date = soup.find(class_="article-date").text.strip()
    news_date = datetime.strptime(news_date, "%d.%m.%Y, %H:%M")
    news_date = format_datetime(news_date, "d MMMM y, HH:mm", locale='ru_RU')

    # ТЭГИ
    news_hashtags = soup.find_all(class_="atag")
    hashtags = get_hashtags(news_hashtags)

    # КАРТИНКА
    img_href = "https://www.sport.ru" + soup.find(class_="article-image article-image-large").find('img')["src"]
    img = get_img(img_href)
    img_title = img_writer(img, news_title)

    # БАЗА ДАННЫХ
    db_insert(news_title, news_href, hashtags, news_date, img_title)
