from news_db.topic_repository import TopicRepository
from news_db.model import Topic, Event, ArticleToEvent

class TopicService:
    def __init__(self):
        self.topic_repository = TopicRepository()
    

    def create_topic(self, name, description=None):
        """
        Создает новый топик
        
        Args:
            name (str): Название топика
            description (str, optional): Описание топика
            
        Returns:
            int: ID созданного топика
        """
        topic = Topic(id=None, name=name, description=description)
        return self.topic_repository.save_topic(topic)
    

    def create_event(self, name, summary=None, topic_id=None, article_ids=None):
        """
        Создает новое событие и привязывает к нему статьи
        
        Args:
            name (str): Название события
            summary (str, optional): Краткое описание события
            topic_id (int, optional): ID топика, к которому относится событие
            article_ids (list, optional): Список ID статей, связанных с событием
            
        Returns:
            int: ID созданного события
        """
        event = Event(id=None, name=name, summary=summary, topic_id=topic_id)
        event_id = self.topic_repository.save_event(event)
        
        if article_ids and event_id:
            for article_id in article_ids:
                article_to_event = ArticleToEvent(id=None, article_id=article_id, event_id=event_id)
                self.topic_repository.create_article_to_event(article_to_event)
        
        return event_id
    

    def get_events_with_details(self):
        """
        Получает все события с информацией о топиках и связанных статьях
        
        Returns:
            list: Список кортежей (event, topic, articles)
        """
        return self.topic_repository.get_events_with_topic_and_articles()
    

    def get_all_topic(self):
        """
        Получает все топики

        Returns:
            list: Список топиков
        """
        return self.topic_repository.get_all_topic()
    

    def get_topic_by_id(self, topic_id):
        """
        Получает топик по его ID
        Args:
            topic_id (int): ID топика

        Returns:
            Topic: Объект топика
        """
        return self.topic_repository.get_topic_by_id(topic_id)
    

    def get_event_by_id(self, event_id):
        """
        Получает событие по его ID
        Args:
            event_id (int): ID события
            Returns:
            Event: Объект события
        """
        return self.topic_repository.get_event_by_id(event_id)
    

    def add_article_to_event(self, event_id, article_id):
        """
        Добавляет статью к событию
        Args:
            event_id (int): ID события
            article_id (int): ID статьи
        """
        article_to_event = ArticleToEvent(id=None, article_id=article_id, event_id=event_id)
        self.topic_repository.create_article_to_event(article_to_event)
    

    def save_topic(self, topic: Topic):
        """
        Обновляет информацию о топике
        Args:
            topic_id (int): ID топика
            name (str): Новое название топика
            description (str, optional): Новое описание топика
        """
        self.topic_repository.save_topic(topic)
    

    def save_event(self, event: Event):
        """
        Обновляет информацию о событии
        Args:
            event_id (int): ID события
            name (str): Новое название события
            summary (str, optional): Новое краткое описание события
        """
        self.topic_repository.save_event(event)
