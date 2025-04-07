CREATE TABLE source (
    id bigserial primary key,
    source_key varchar(20) not null,
    source_name varchar(1000) not null,
    latest_publication_date timestamp,
    earliest_publication_date timestamp,
    tg_channel varchar(100)
);

CREATE TABLE article (
    id bigserial primary key,
    article_name varchar(1000) not null,
    article_text text not null,
    publication_date timestamp not null,
    source_id bigint references source(id),
    article_hash varchar(32) not null
);

INSERT INTO source(source_key, source_name, tg_channel) VALUES 
('ria_news_tg',     'РИА Новости (Telegram)',               '@rian_ru'),
('kommersant_tg',   'Коммерсант (Telegram)',                '@kommersant'),
('mash_tg',         'Mash (Telegram)',                      '@mash'),
('news_efir_tg',    'Прямой Эфир (Telegram)',               '@novosti_efir'),
('ranshe_vseh_tg',  'Раньше всех. Ну почти. (Telegram)',    '@bbbreaking');
