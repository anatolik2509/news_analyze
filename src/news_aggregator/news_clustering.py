from math import exp
import spacy
from sklearn.cluster import DBSCAN

from news_db.news_repository import NewsRepository
from news_db.topic_repository import TopicRepository
from news_db.model import Event, ArticleToEvent
import re


CLEANR = re.compile('<.*?>') 
EMOJI_PATTERN = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                           "]+", flags=re.UNICODE)

named_entities_count = {}

def add_entities(vector):
  used_entities = set()
  for e in vector.ents:
    if e.lemma_ in used_entities:
      continue
    if e.lemma_ in named_entities_count:
      named_entities_count[e.lemma_] += 1
    else:
      named_entities_count[e.lemma_] = 1
    used_entities.add(e.lemma_)


def cleantext(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  cleantext = re.sub(EMOJI_PATTERN, '', cleantext)
  return cleantext


def named_entity_equal(ne1, ne2):
  return ne1 in ne2 or ne2 in ne1


def named_entity_similarity(vector1, vector2):
  named_entities1 = set()
  named_entities2 = set()
  for ne1 in vector1.ents:
    named_entities1.add(ne1.lemma_)
  for ne2 in vector2.ents:
    named_entities2.add(ne2.lemma_)
  
  total = 0
  all_entities = named_entities1.union(named_entities2)
  for ne in all_entities:
    total += 1 / named_entities_count[ne]
  
  if total == 0:
    return 0
  
  similarity = 0
  for ne1 in named_entities1:
    for ne2 in named_entities2:
      if named_entity_equal(ne1, ne2):
        similarity += 1 / named_entities_count[ne1]
        if ne1 != ne2:
          similarity += 1 / named_entities_count[ne2]
        break
  return similarity / total

def run_clustering():
  news_repositry = NewsRepository()
  topic_repository = TopicRepository()
  news = news_repositry.get_all_articles_sorted_by_date()
  news_texts = [cleantext(article.text) for article in news]

  model = spacy.load('ru_core_news_md')
  news_vectors = [model(text) for text in news_texts]
  for v in news_vectors:
    add_entities(v)
  
  def print_entities(vector):
    for e in vector.ents:
      print(e.lemma_, e.label_, end=' ')
    print()

  print(len(news_vectors))

  groupped_news = set()
  news_groups = []
  similarities = []
  named_entities = []

  for i in range(len(news_vectors)):
      named_entities.append((news[i].id, news_vectors[i].ents))
      if i in groupped_news:
          continue
      groupped_news.add(i)
      news_group = [news[i]]
      for j in range(i+1, len(news_vectors)):
          if j in groupped_news:
              continue
          vector_similarity = news_vectors[i].similarity(news_vectors[j])
          ner_similarity = named_entity_similarity(news_vectors[i], news_vectors[j])
          similarities.append((news[i].id, news[j].id, vector_similarity, ner_similarity))
          if vector_similarity > 0.95 and ner_similarity > 0.2 or ner_similarity > 0.8:
              groupped_news.add(j)
              news_group.append(news[j])
              print(f"Vector similarity is {vector_similarity}")
              print("NER similarity is", ner_similarity)
              print(f"{news[i].id} {news_texts[i]}")
              print_entities(news_vectors[i])
              print('==============')
              print(f"{news[j].id} {news_texts[j]}")
              print_entities(news_vectors[j])
              print()
      news_groups.append(news_group)

  for i, news_group in enumerate(news_groups):
      print(f"Group {i}: length {len(news_group)}")

  # write news groups to one file
  with open('news_groups.txt', 'w') as f:
      for news_group in news_groups:
          for news in news_group:
              f.write(f"{news.id} {news.text}\n")
          f.write('\n')
      f.write('\n')
      for similarity in similarities:
          f.write(f"{similarity[0]} {similarity[1]} {similarity[2]} {similarity[3]}\n")
      f.write('\n')
      for named_entity in named_entities:
          f.write(f"{named_entity}\n")
  
  for i, news_group in enumerate(news_groups):
     event = Event(id = None, name=f"Группа новостей {i}")
     event_id = topic_repository.save_event(event)
     for news in news_group:
         article_to_event = ArticleToEvent(id=None, article_id=news.id, event_id=event_id)
         topic_repository.create_article_to_event(article_to_event)
