from math import sqrt
import tensorflow as tf
import tensorflow_hub as hub

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" 
model = hub.load(module_url)

from news_db.news_repository import NewsRepository
import re

CLEANR = re.compile('<.*?>') 


def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext


def squared_sum(x):
  """ return 3 rounded square rooted value """
 
  return round(sqrt(sum([a*a for a in x])),3)


def cos_similarity(x,y):
  """ return cosine similarity between two lists """
 
  numerator = sum(a*b for a,b in zip(x,y))
  denominator = squared_sum(x)*squared_sum(y)
  return round(numerator/float(denominator),3)


news_repositry = NewsRepository()
news = news_repositry.get_all_articles_sorted_by_date()
news_texts = [cleanhtml(article.text) for article in news]

news_vecors = model(news_texts).numpy()
print(len(news_vecors))

similarities = []
for i in range(len(news_vecors)):
    for j in range(i+1, len(news_vecors)):
        similarity = cos_similarity(news_vecors[i], news_vecors[j])
        similarities.append(similarity)
        if similarity > 0.95:
            print(f"Similarity is {similarity}")
            print(f"{news[i].id} {news_texts[i]}")
            print('==============')
            print(f"{news[j].id} {news_texts[j]}")
            print()
similarities = sorted(similarities, reverse=True)
print(similarities[50])
