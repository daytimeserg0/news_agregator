from flask import Flask, render_template, request, jsonify, send_file
import psycopg2
from config import host, user, password, db_name

def fetchall():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        )
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM news ORDER BY news_time DESC")
    news_data = cursor.fetchall()
    connection.close()
    return news_data

news_data = fetchall()

app = Flask(__name__)


@app.route('/')
def main():
    return send_file('templates/index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    news_data = fetchall()
    return jsonify(news_data)


@app.route('/search-results')
def search_results():
    news_data = fetchall()
    # Получение значения запроса из строки параметров URL
    original_search_query = request.args.get('query', '')
    search_query = original_search_query.lower()

    news_counter = 0
    for news_item in news_data:
        news = []
        for tag in news_item[3]:
            tag_words = tag.lower().split()
            for tag_word in tag_words:
                if tag_word.lower().startswith(search_query.lower()):
                    if news_item not in news:
                        news.append(news_item)
                        news_counter += 1

    return render_template('search-results.html', news=news_data, search_query=search_query,
                           or_search_query=original_search_query, found_news=news_counter)

@app.route('/tag-news')
def tags():
    news_data = fetchall()
    tag_query = request.args.get('tag', '')
    news_counter = 0
    for news_item in news_data:
        for tag in news_item[3]:
            if tag == tag_query:
                news_counter += 1

    return render_template('tag-news.html', news=news_data, tag_query=tag_query, found_news=news_counter)

if __name__ == '__main__':
    app.run(debug=True)
