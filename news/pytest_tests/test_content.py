import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_10_news(client, news_10):
    """
    Количество новостей на главной странице — не более 10.
    """
    response = client.get(reverse('news:home'))
    obj = response.context['object_list']
    count = obj.count()
    assert count == 10


@pytest.mark.django_db
def test_10_news_ordering(client, news_10):
    """Новости отсортированы от самой свежей к самой старой.
    Свежие новости в начале списка.
    """
    response = client.get(reverse('news:home'))
    obj = response.context['object_list']
    all_dates = [news.date for news in obj]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comment_ordering(client, comments_10, news):
    """
    Комментарии на странице отдельной новости
    отсортированы в хронологическом порядке: старые в
    начале списка, новые — в конце.
    """
    url = reverse('news:detail', args=(news.id, ))
    response = client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps

@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news):
    """Анонимному пользователю недоступна форма комментария"""
    url = reverse('news:detail', args=(news.id, ))
    response = client.get(url)
    assert 'form' not in response.context
    

@pytest.mark.django_db
def test_author_client_has_form(author_client, news):
    """Пользователю доступна форма комментария"""
    url = reverse('news:detail', args=(news.id, ))
    response = author_client.get(url)
    assert 'form' in response.context
