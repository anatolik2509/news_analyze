from flask import Flask, render_template
import sys
import os
from news_db.news_repository import NewsRepository

app = Flask(__name__)

@app.route('/')
def index():
    news_repository = NewsRepository()
    articles = news_repository.get_all_articles_sorted_by_date()
    
    for article in articles:
        article.formatted_date = article.publication_date.strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
