import hashlib

class Source:
    def __init__(self, id, key, name, latest_publication_date=None, earliest_publication_date=None, tg_channel=None):
        self.id = id
        self.key = key
        self.name = name
        self.latest_publication_date = latest_publication_date
        self.earliest_publication_date = earliest_publication_date
        self.tg_channel = tg_channel


class Article:
    def __init__(self, id, name, text, publication_date, source_id, article_hash=None):
        self.id = id
        self.name = name
        self.text = text
        self.publication_date = publication_date
        self.source_id = source_id
        if article_hash is None:
            hash_object = hashlib.md5()
            hash_object.update((name + text + str(publication_date)).encode('utf-8'))
            article_hash = hash_object.hexdigest()
        self.article_hash = article_hash

    def __repr__(self) -> str:
        return f"Article(id={self.id}, name='{self.name}', source_id={self.source_id})"


class Topic:
    def __init__(self, id, name, description=None, parent_topic_id=None):
        self.id = id
        self.name = name
        self.description = description
        self.parent_topic_id = parent_topic_id

    def __repr__(self) -> str:
        return f"Topic(id={self.id}, name='{self.name}')"


class Event:
    def __init__(self, id, name, summary=None, topic_id=None):
        self.id = id
        self.name = name
        self.summary = summary
        self.topic_id = topic_id

    def __repr__(self) -> str:
        return f"Event(id={self.id}, name='{self.name}', topic={self.topic_id})"


class ArticleToEvent:
    def __init__(self, id, article_id, event_id):
        self.id = id
        self.article_id = article_id
        self.event_id = event_id

    def __repr__(self) -> str:
        return f"ArticleToEvent(id={self.id}, article_id={self.article_id}, event_id={self.event_id})"

