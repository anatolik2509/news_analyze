import os
import psycopg2
from dotenv import load_dotenv


class DatabaseConfig:
    def __init__(self, env_path: str = '.env'):
        load_dotenv(env_path)
        self.connection_params = {
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "database": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "port": os.getenv("POSTGRES_PORT", "5432")
        }

    def create_connection(self) -> psycopg2.extensions.connection:
        try:
            return psycopg2.connect(**self.connection_params)
        except psycopg2.Error as e:
            raise Exception(f"Error connecting to database: {e}")
