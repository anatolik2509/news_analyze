CREATE TABLE topic (
    id bigserial primary key,
    name varchar(255) not null,
    description text,
    parent_topic_id bigint references topic(id)
);

CREATE TABLE event (
    id bigserial primary key,
    name varchar(255) not null,
    summary text,
    topic_id bigint not null references topic(id)
);

CREATE TABLE article_to_event (
    id bigserial primary key,
    article_id bigint not null references article(id),
    event_id bigint not null references event(id),
    UNIQUE (article_id, event_id)
);


