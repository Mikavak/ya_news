# conftest.py
from datetime import datetime, timedelta

import pytest
# Импортируем класс клиента.
from django.test.client import Client
from django.utils import timezone

# Импортируем модель заметки, чтобы создать экземпляр.
from news.models import Comment, News


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):  # Вызываем фикстуру автора.
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
    return client


@pytest.fixture
def news():
    news = News.objects.create(  # Создаём объект заметки.
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        text='New Comments',
        author=author,
        news=news,
    )
    return comment


@pytest.fixture
def comments_10(author, news):
    now = timezone.now()
    return Comment.objects.bulk_create(
        Comment(author=author,
                news=news,
                text='Просто коммент',
                created=now + timedelta(days=index))
        for index in range(10)
    )


@pytest.fixture
# Фикстура запрашивает другую фикстуру создания заметки.
def pk_news(news):
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return (news.pk,)


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст'
    }


@pytest.fixture
# Фикстура запрашивает другую фикстуру создания заметки.
def news_10():
    today = datetime.today()
    return News.objects.bulk_create(
        News(title=f'Новость {index}',
             text='Просто текст.',
             date=today - timedelta(days=index))
        for index in range(11)
    )
