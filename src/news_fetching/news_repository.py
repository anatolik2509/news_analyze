import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv
from model import Article, Source

class NewsRepository:
    def __init__(self, connection_params=None, env_file=None):
        """
        Initialize the repository with database connection parameters.
        
        Args:
            connection_params (dict, optional): Dictionary with connection parameters 
                                              (host, database, user, password, etc.)
            env_file (str, optional): Path to .env file to load connection parameters from
        """
        if env_file:
            # Load environment variables from the specified .env file
            load_dotenv(env_file)
            self.connection_params = {
                "host": os.getenv("POSTGRES_HOST", "localhost"),
                "database": os.getenv("POSTGRES_DB"),
                "user": os.getenv("POSTGRES_USER"),
                "password": os.getenv("POSTGRES_PASSWORD"),
                "port": os.getenv("POSTGRES_PORT", "5432")
            }
        else:
            self.connection_params = connection_params or {}
    

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
    

    def get_source_by_key(self, source_key: str) -> Source:
        """
        Get a source by its key.
        
        Args:
            source_key (str): The key of the source to retrieve
            
        Returns:
            Source: The source object if found, None otherwise
        """
        query = "SELECT id, source_key, source_name, latest_publication_date, earliest_publication_date FROM source WHERE source_key = %s"
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (source_key,))
                    result = cursor.fetchone()
                    
                    if result:
                        return Source(id=result[0], key=result[1], name=result[2], 
                                      latest_publication_date=result[3], earliest_publication_date=result[4])
                    return None
        except Exception as e:
            print(f"Error getting source: {e}")
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
    