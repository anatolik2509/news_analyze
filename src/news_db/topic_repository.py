from news_db.db_config import DatabaseConfig
from news_db.model import Topic, Event, ArticleToEvent, Article


class TopicRepository:
    def __init__(self, env_file='.env'):
        """
        Initialize the repository with database connection parameters.
        
        Args:
            env_file (str, optional): Path to .env file to load connection parameters from
        """
        self.db_config = DatabaseConfig(env_file)
    

    def get_connection(self):
        """Create and return a database connection."""
        return self.db_config.create_connection()
    

    def save_event(self, event: Event):
        """
        Create a new event in the database.

        Args:
            event (Event): The event object to be created

        Returns:
            int: The ID of the newly created event
        """
        insert_query = """
            INSERT INTO event (name, summary, topic_id)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        update_query = """
            UPDATE event SET name=%s, summary=%s, topic_id=%s
            WHERE id=%s
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    if event.id:
                        cursor.execute(update_query, (event.name, event.summary, event.topic_id, event.id))
                        return event.id
                    else:
                        cursor.execute(
                            insert_query,
                            (event.name, event.summary, event.topic_id)
                        )
                        event_id = cursor.fetchone()[0]
                        return event_id
        except Exception as e:
            print(f"Error creating event: {e}")
            return None
    

    def save_topic(self, topic: Topic):
        """
        Save a topic to the database.
        Args:
            topic (Topic): The topic object to be saved
        """
        insert_query = """
            INSERT INTO topic (name, description)
            VALUES (%s, %s)
            RETURNING id
        """
        update_query = """
            UPDATE topic SET name=%s, description=%s
            WHERE id=%s
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    if topic.id:
                        cursor.execute(update_query, (topic.name, topic.description, topic.id))
                        return topic.id
                    else:
                        cursor.execute(
                            insert_query,
                            (topic.name, topic.description)
                        )
                        topic_id = cursor.fetchone()[0]
                        return topic_id
        except Exception as e:
            print(f"Error saving topic: {e}")
            return None
    

    def create_article_to_event(self, article_to_event: ArticleToEvent):
        """
        Create a new article_to_event entry in the database.
        Args:
            article_id (int): The ID of the article
            event_id (int): The ID of the event
        """
        insert_query = """
            INSERT INTO article_to_event (article_id, event_id)
            VALUES (%s, %s) ON CONFLICT DO NOTHING
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(insert_query, (article_to_event.article_id, article_to_event.event_id))
        except Exception as e:
            print(f"Error creating article_to_event: {e}")
            raise
    

    def get_events_with_topic_and_articles(self):
        """
        Get all events with their associated topics and articles.
        Returns:
            list: A list of dictionaries containing event information
        """
        select_event_query = """
            SELECT e.id, e.name, e.summary, t.id, t.name AS topic_name
            FROM event e
            LEFT JOIN topic t ON e.topic_id = t.id
        """
        select_articles_for_event_query = """
            SELECT a.id, a.article_name, a.article_text, a.publication_date, a.source_id
            FROM article a
            JOIN article_to_event a2e ON a.id = a2e.article_id
            WHERE a2e.event_id = %s
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(select_event_query)
                    events = []
                    for row in cursor.fetchall():
                        event = Event(
                            id = row[0],
                            name = row[1],
                            summary = row[2],
                            topic_id = row[3]
                        )
                        topic = Topic(
                            id = row[3],
                            name = row[4]
                        )
                        articles = []
                        cursor.execute(select_articles_for_event_query, (event.id,))
                        for article_row in cursor.fetchall():
                            article = Article(
                                id = article_row[0],
                                name = article_row[1],
                                text = article_row[2],
                                publication_date = article_row[3],
                                source_id = article_row[4]
                            )
                            articles.append(article)
                        events.append((event, topic, articles))
                    return events
        except Exception as e:
            print(f"Error getting events with topics and articles: {e}")
            raise
    

    def get_all_topic(self):
        """
        Get all topics from the database.
        Returns:
            list: A list of Topic objects
        """
        select_query = """
            SELECT id, name, description
            FROM topic
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(select_query)
                    topics = []
                    for row in cursor.fetchall():
                        topic = Topic(
                            id = row[0],
                            name = row[1],
                            description = row[2]
                        )
                        topics.append(topic)
                    return topics
        except Exception as e:
            print(f"Error getting topics: {e}")
            raise
    

    def get_topic_by_id(self, topic_id: int):
        """
        Get a topic by its ID.
        Args:
            topic_id (int): The ID of the topic
        Returns:
            Topic: The Topic object
        """
        select_query = """
            SELECT id, name, description
            FROM topic
            WHERE id = %s
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(select_query, (topic_id,))
                    row = cursor.fetchone()
                    if row:
                        topic = Topic(
                            id = row[0],
                            name = row[1],
                            description = row[2]
                        )
                        return topic
                    else:
                        return None
        except Exception as e:
            print(f"Error getting topic by ID: {e}")
            raise
    

    def get_event_by_id(self, event_id: int):
        """
        Get an event by its ID.
        Args:
            event_id (int): The ID of the event
        Returns:
            Event: The Event object
        """
        select_query = """
            SELECT id, name, summary, topic_id
            FROM event
            WHERE id = %s
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(select_query, (event_id,))
                    row = cursor.fetchone()
                    if row:
                        event = Event(
                            id = row[0],
                            name = row[1],
                            summary = row[2],
                            topic_id = row[3]
                        )
                        return event
                    else:
                        return None
        except Exception as e:
            print(f"Error getting event by ID: {e}")
            raise
