from news_fetching import telegram_fetcher
from datetime import UTC, datetime, timedelta

if  __name__ == "__main__":
    telegram_fetcher.fetch_earlier_messages(datetime.now(tz=UTC) - timedelta(hours=8))
