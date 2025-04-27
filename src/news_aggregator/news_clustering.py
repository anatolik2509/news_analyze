import spacy
from sklearn.cluster import DBSCAN

from news_db.news_repository import NewsRepository
import re
CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

news_repositry = NewsRepository()
news = news_repositry.get_all_articles_sorted_by_date()
news_texts = [cleanhtml(article.text) for article in news]

model = spacy.load('ru_core_news_md')
news_vecors = [model(text) for text in news_texts]

similarities = []
for i in range(len(news_vecors)):
    for j in range(i+1, len(news_vecors)):
        similarity = news_vecors[i].similarity(news_vecors[j])
        if similarity > 0.95:
            print(f"Similarity is {similarity}")
            print(f"{news[i].id} {news_texts[i]}")
            print('==============')
            print(f"{news[j].id} {news_texts[j]}")
            print()

# dbscan = DBSCAN(eps=0.4, min_samples=2)
# clusters = dbscan.fit_predict(news_vecors)
# print(clusters)
# text_by_cluster = {}
# for i, cluster in enumerate(clusters):
#     if cluster not in text_by_cluster:
#         text_by_cluster[cluster] = []
#     text_by_cluster[cluster].append(news_texts[i])

# for cluster, texts in text_by_cluster.items():
#     print(f"Cluster {cluster}:")
#     for text in texts:
#         print('------------')
#         print(text)
#     print('############')
