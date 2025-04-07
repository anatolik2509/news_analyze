import os
from news_db.news_repository import NewsRepository
from news_db.model import Article, Source
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from datetime import datetime
import markdown


def fetch_earlier_messages(news_repository: NewsRepository = NewsRepository(), batch_size: int = 50):
    load_dotenv('.env')
    TELEGRAM_API_ID = int(os.getenv('TELEGRAM_API_ID'))
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
    TELEGRAM_USERNAME = os.getenv('TELEGRAM_USERNAME')
    client = TelegramClient(TELEGRAM_USERNAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
    __fetch_and_save_messages_for_sources(news_repository, batch_size, client)


def __fetch_and_save_messages_for_sources(news_repository: NewsRepository, batch_size, client):
    sources = news_repository.get_sources()
    with client:
        print(client.get_me())
        for source in sources:
            __process_source(news_repository, source, client, batch_size)
    

def __process_source(news_repository, source, client, batch_size):
    tg_channel_alias = source.tg_channel
    if not tg_channel_alias:
        return
    channel = client.get_input_entity(tg_channel_alias)
    messages = client.iter_messages(channel, limit=batch_size, offset_date=source.earliest_publication_date)
    for message in messages:
        process_message(news_repository, source, message)
    news_repository.update_source(source)


def process_message(news_repository, source: Source, message):
    if message.text:
        article = Article(
                    id=None,
                    name=source.name,
                    text=markdown.markdown(message.text),
                    publication_date=message.date,
                    source_id=source.id
                )
        __add_date_for_source(source, message.date)
        id = news_repository.add_article(article)
        print(id)


def __add_date_for_source(source: Source, date: datetime):
    date = date.replace(tzinfo=None)
    if not source.latest_publication_date or date > source.latest_publication_date:
        source.latest_publication_date = date
    if not source.earliest_publication_date or date < source.earliest_publication_date:
        source.earliest_publication_date = date
