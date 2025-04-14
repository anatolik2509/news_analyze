from flask import Flask, render_template, redirect, request, jsonify, url_for
import sys
import os
from news_db.news_repository import NewsRepository
from news_explorer.topic_service import TopicService


app = Flask(__name__)
topic_service = TopicService()


@app.route('/')
def index():
    return redirect('/articles')


@app.route('/articles')
def articles():
    news_repository = NewsRepository()
    articles = news_repository.get_all_articles_sorted_by_date()
    
    for article in articles:
        article.formatted_date = article.publication_date.strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template('index.html', articles=articles)


@app.route('/api/topics', methods=['POST'])
def create_topic():
    """REST метод для создания нового топика"""
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Название топика обязательно'}), 400
    
    topic_id = topic_service.create_topic(
        name=data['name'],
        description=data.get('description')
    )
    
    if topic_id:
        return jsonify({'id': topic_id, 'name': data['name']}), 201
    else:
        return jsonify({'error': 'Не удалось создать топик'}), 500


@app.route('/api/events', methods=['POST'])
def create_event():
    """REST метод для создания нового события"""
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Название события обязательно'}), 400
    
    event_id = topic_service.create_event(
        name=data['name'],
        summary=data.get('summary'),
        topic_id=data.get('topic_id'),
        article_ids=data.get('article_ids', [])
    )
    
    if event_id:
        return jsonify({
            'id': event_id, 
            'name': data['name'],
            'topic_id': data.get('topic_id'),
            'article_ids': data.get('article_ids', [])
        }), 201
    else:
        return jsonify({'error': 'Не удалось создать событие'}), 500


@app.route('/events/<int:event_id>/articles', methods=['POST'])
def add_article_to_event(event_id):
    data = request.form
    if not data or 'article_id' not in data:
        return jsonify({'error': 'Идентификатор статьи обязателен'}), 400
    article_id = data['article_id']
    topic_service.add_article_to_event(event_id, article_id)
    return redirect(url_for('events_page'))
    

@app.route('/events')
def events_page():
    """Страница для отображения событий"""
    events_data = topic_service.get_events_with_details()
    
    # Форматируем даты для отображения
    for _, _, articles in events_data:
        for article in articles:
            article.formatted_date = article.publication_date.strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template('events.html', events_data=events_data)


@app.route('/topics')
def topics_page():
    """Страница для отображения всех топиков"""
    # Получаем все топики из базы данных
    # Для этого нужно добавить метод в TopicService
    topics = topic_service.get_all_topic()
    return render_template('topics.html', topics=topics)


@app.route('/topics/new', methods=['GET', 'POST'])
def new_topic():
    """Страница с формой для создания нового топика"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            return render_template('topic_form.html', error='Название топика обязательно')
        
        topic_id = topic_service.create_topic(name=name, description=description)
        
        if topic_id:
            return redirect(url_for('topics_page'))
        else:
            return render_template('topic_form.html', error='Не удалось создать топик')
    
    return render_template('topic_form.html')


@app.route('/topics/edit/<int:topic_id>', methods=['GET', 'POST'])
def edit_topic(topic_id):
    """Страница с формой для редактирования топика"""
    topic = topic_service.get_topic_by_id(topic_id)
    
    if not topic:
        return redirect(url_for('new_topic'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            return render_template('topic_form.html', topic=topic, error='Название топика обязательно')
        
        topic.name = name
        topic.description = description
        topic_service.save_topic(topic)
        
        return redirect(url_for('topics_page'))
    
    return render_template('topic_form.html', topic=topic)


@app.route('/events/new', methods=['GET', 'POST'])
def new_event():
    """Страница с формой для создания нового события"""
    topic_service = TopicService()
    
    # Получаем все топики для выпадающего списка
    topics = topic_service.get_all_topic()
    
    if request.method == 'POST':
        name = request.form.get('name')
        summary = request.form.get('summary')
        topic_id = request.form.get('topic_id')
        
        if not name:
            return render_template('event_form.html', 
                                  topics=topics, 
                                  error='Название события обязательно')
        
        # Преобразуем строковые ID в целые числа
        if topic_id:
            topic_id = int(topic_id)
        
        event_id = topic_service.create_event(
            name=name,
            summary=summary,
            topic_id=topic_id
        )
        
        if event_id:
            return redirect(url_for('events_page'))
        else:
            return render_template('event_form.html', 
                                  topics=topics,
                                  error='Не удалось создать событие')
    
    return render_template('event_form.html', topics=topics, articles=articles)


@app.route('/events/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    """Страница с формой для редактирования события"""
    topic_service = TopicService()
    
    # Получаем событие по ID
    event = topic_service.get_event_by_id(event_id)
    
    if not event:
        return redirect(url_for('events_page'))
    
    # Получаем все топики для выпадающего списка
    topics = topic_service.get_all_topic()
    
    if request.method == 'POST':
        name = request.form.get('name')
        summary = request.form.get('summary')
        topic_id = request.form.get('topic_id')
        
        if not name:
            return render_template('event_form.html', 
                                  event=event,
                                  topics=topics,
                                  error='Название события обязательно')
        
        # Преобразуем строковые ID в целые числа
        if topic_id:
            topic_id = int(topic_id)
        
        # Обновляем событие
        event.name = name
        event.summary = summary
        event.topic_id = topic_id
        topic_service.save_event(event)
        
        return redirect(url_for('events_page'))
    
    return render_template('event_form.html', 
                          event=event,
                          topics=topics)


@app.route('/events/<int:event_id>/articles', methods=['GET'])
def add_article_to_event_form(event_id):
    """Страница с формой для добавления статьи к событию"""
    topic_service = TopicService()
    
    # Получаем событие по ID
    event = topic_service.get_event_by_id(event_id)
    
    if not event:
        return redirect(url_for('events_page'))
    
    return render_template('add_article_form.html', event=event)

