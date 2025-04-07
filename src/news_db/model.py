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
    def __init__(self, id, name, text, publication_date, source_id):
        self.id = id
        self.name = name
        self.text = text
        self.publication_date = publication_date
        self.source_id = source_id
        hash_object = hashlib.md5()
        hash_object.update((name + text + str(publication_date)).encode('utf-8'))
        self.article_hash = hash_object.hexdigest();

    def __repr__(self) -> str:
        return f"Article(id={self.id}, name='{self.name}', source_id={self.source_id})"
