from psycopg2 import pool
import requests
from bs4 import BeautifulSoup
from config import host, user, password, db_name
import hashlib

# Создание пула соединений
connection_pool = pool.SimpleConnectionPool(
    1,  # минимальное количество соединений в пуле
    10,  # максимальное количество соединений в пуле
    user=user,
    password=password,
    host=host,
    database=db_name
)


def get_page(media_url):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36"
    }
    url = media_url
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    return soup


def get_img(img_url):
    return requests.get(img_url)


def get_hashtags(news_hashtags):
    hashtags = "{"
    for j in range(len(news_hashtags)):
        tag = news_hashtags[j].text
        if ('"' in tag) or ("'" in tag):
            continue
        if j == len(news_hashtags) - 1:
            hashtags += f'"{tag}"'
        else:
            hashtags += f'"{tag}", '
    hashtags += "}"
    return hashtags


def db_insert(news_title, news_href, hashtags, news_date, img_title):
    query = "INSERT INTO news (news_title, news_href, news_tags, news_time, news_img) VALUES (%s, %s, %s, %s, %s)"

    # Получение соединения из пула
    connection = connection_pool.getconn()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (news_title, news_href, hashtags, news_date, f'static/media/{img_title}.jpg'))
        connection.commit()
    finally:
        # Возвращение соединения в пул
        connection_pool.putconn(connection)


def img_writer(img, news_title):
    img_title = hashlib.sha256(news_title.encode()).hexdigest()
    with open(f"static/media/{img_title}.jpg", "wb") as img_option:
        img_option.write(img.content)
    return img_title


def iz_all_news(soup):
    all_titles = soup.find_all(class_="lenta_news__day__list__item__title")
    all_news = []
    for item in all_titles:
        item_title = item.text.strip()
        item_href = "https://iz.ru" + item.parent.get('href')
        item_time = item.parent.find(class_="lenta_news__day__list__item__time small-gray").text
        all_news.append([item_title, item_href, item_time])
    return all_news


def ria_all_news(soup):
    all_titles = soup.find_all(class_="list-item")
    all_news = []
    for item in all_titles:
        item_title = item.find(class_="list-item__content").text.strip()
        item_href = item.find(class_="list-item__content").find('a')['href']
        item_time = item.find(class_="list-item__info").find(class_="list-item__date").text.strip()
        all_news.append([item_title, item_href, item_time])
    return all_news


def sport_all_news(soup):
    all_titles = soup.find_all(class_="articles-item articles-item-large")
    all_news = []
    for item in all_titles:
        item_title = item.find(class_="itm").text.strip()
        item_href = "https://www.sport.ru" + item.find(class_="itm").find('a')['href']
        item_time = item.find(class_="articles-item-info").text.strip()[-5:]
        all_news.append([item_title, item_href, item_time])
    return all_news
