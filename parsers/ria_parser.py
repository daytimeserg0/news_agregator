from parsers.modules import get_page, get_hashtags, db_insert, get_img, img_writer, ria_all_news
from datetime import datetime
from babel.dates import format_datetime
import locale
import time

locale.setlocale(locale.LC_TIME, 'ru_RU')


def ria_parser():
    url = "https://ria.ru/lenta/"
    soup = get_page(url)
    print(datetime.now().time())
    end_time = ''
    all_news = ria_all_news(soup)

    for news_item in all_news:
        process_news(*news_item, end_time)

    time.sleep(120)
    while True:
        soup = get_page(url)
        print(datetime.now().time())
        end_time = all_news[0][2]
        all_news = ria_all_news(soup)

        for news_item in all_news:
            stopper = process_news(*news_item, end_time)
            if stopper == -1:
                break
        time.sleep(120)


def process_news(news_title, news_href, time_check, end_time):
    if time_check == end_time:
        return -1

    soup = get_page(news_href)

    # ДАТА И ВРЕМЯ
    news_date = soup.find(class_="article__info-date").find('a').text
    news_date = datetime.strptime(news_date, "%H:%M %d.%m.%Y")
    news_date = format_datetime(news_date, "d MMMM y, HH:mm", locale='ru_RU')

    # ТЭГИ
    news_hashtags = soup.find_all(class_="article__tags-item")
    hashtags = get_hashtags(news_hashtags)

    # КАРТИНКА
    img_href = soup.find("div", class_="photoview__open").img['src']
    img = get_img(img_href)
    img_title = img_writer(img, news_title)

    # БАЗА ДАННЫХ
    db_insert(news_title, news_href, hashtags, news_date, img_title)
