CREATE TABLE source (
    id bigserial primary key,
    source_key varchar(20) not null,
    source_name varchar(1000) not null,
    latest_publication_date timestamp,
    earliest_publication_date timestamp
);

CREATE TABLE source_to_tg_channel (
    id bigserial primary key,
    source_id bigint references source(id) unique,
    tg_channel varchar(100) not null
)

CREATE TABLE article (
    id bigserial primary key,
    article_name varchar(1000) not null,
    article_text text not null,
    publication_date timestamp not null,
    source_id bigint references source(id),
    article_hash varchar(32) not null
);

INSERT INTO source(source_key, source_name) VALUES ('kommersant', 'Коммерсант');
INSERT INTO source(source_key, source_name) VALUES ('ria_news_tg', 'РИА Новости (Telegram)');
INSERT INTO source_to_tg_channel(source_id, tg_channel) SELECT id, '@rian_ru' FROM source WHERE source_key = 'ria_news_tg';