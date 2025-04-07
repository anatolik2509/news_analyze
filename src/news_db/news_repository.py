from typing import List
import psycopg2
import os
from dotenv import load_dotenv
from news_db.model import Article, Source

class NewsRepository:
    def __init__(self, env_file='.env'):
        """
        Initialize the repository with database connection parameters.
        
        Args:
            env_file (str, optional): Path to .env file to load connection parameters from
        """
        # Load environment variables from the specified .env file
        load_dotenv(env_file)
        self.connection_params = {
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "database": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "port": os.getenv("POSTGRES_PORT", "5432")
        }
    

    def get_connection(self):
        """Create and return a database connection."""
        return psycopg2.connect(**self.connection_params)
    

    def add_article(self, article: Article):
        """
        Add a new article to the database.
        
        Args:
            article (Article): The article object to be added
            
        Returns:
            int: The ID of the newly inserted article
        """
        insert_query = """
            INSERT INTO article (article_name, article_text, publication_date, source_id, article_hash)
            SELECT %s, %s, %s, %s, %s WHERE NOT EXISTS (
                SELECT 1 FROM article WHERE article_hash = %s AND publication_date = %s AND source_id = %s
            )
            RETURNING id
        """
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        insert_query, 
                        (article.name, article.text, article.publication_date, article.source_id, article.article_hash,
                         article.article_hash, article.publication_date, article.source_id)
                    )
                    article_id = cursor.fetchone()
                    conn.commit()
                    if article_id:
                        return article_id[0]
                    return None
        except Exception as e:
            print(f"Error adding article: {e}")
            raise
    

    def update_source(self, source: Source):
        """
        Update an existing source in the database.

        Args:
            source (Source): The source object to be updated
        """
        update_query = """
            UPDATE source
            SET latest_publication_date = %s, earliest_publication_date = %s
            WHERE id = %s
        """

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(update_query, (source.latest_publication_date, source.earliest_publication_date, source.id))
                    conn.commit()
        except Exception as e:
            print(f"Error updating source: {e}")
            raise
    

    def get_source_tg_channel(self, source_id: int) -> str:
        """
        Get the Telegram channel associated with a source.

        Args:
            source_id (int): The ID of the source

        Returns:
            str: The Telegram channel associated with the source
        """
        query = "SELECT tg_channel FROM source_to_tg_channel WHERE source_id = %s"

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (source_id,))
                    result = cursor.fetchone()

                    if result:
                        return result[0]
                    return None
        except Exception as e:
            print(f"Error getting Telegram channel: {e}")
            raise
    
    def get_sources(self) -> List[Source]:
        """
        Get all sources from the database.
        Returns:
            List[Source]: A list of all sources
        """
        query = "SELECT id, source_key, source_name, latest_publication_date, earliest_publication_date, tg_channel FROM source"
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()

                    sources = []
                    for result in results:
                        sources.append(Source(id=result[0], key=result[1], name=result[2],
                                               latest_publication_date=result[3], earliest_publication_date=result[4], tg_channel=result[5]))
                    return sources
        except Exception as e:
            print(f"Error getting sources: {e}")
            raise
    

    def get_all_articles_sorted_by_date(self):
        """
        Retrieves all articles from the database sorted by publication date (newest first)
        
        Returns:
            list: List of Article objects sorted by publication date
        """
        query = """
            SELECT a.id, a.article_name, a.article_text, a.publication_date, a.source_id
            FROM article a
            ORDER BY a.publication_date DESC
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    articles = []
                    for row in cursor.fetchall():
                        article = Article(
                            id=row[0],
                            name=row[1],
                            text=row[2],
                            publication_date=row[3],
                            source_id=row[4]
                        )
                        articles.append(article)
                    return articles
        except Exception as e:
            print(f"Error getting sources: {e}")
            raise
        cursor = self.connection.cursor()
        

