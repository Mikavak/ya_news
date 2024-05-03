from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from ..forms import BAD_WORDS, WARNING
from ..models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, form_data):
    """Анонимный пользователь не может отправить комментарий."""
    url = reverse('news:detail', args=(news.id, ))
    client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_author_user_can_create_comment(author_client, news, form_data):
    """Авторизованный пользователь может отправить комментарий."""
    url = reverse('news:detail', args=(news.id, ))
    author_client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 1


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client, news):
    """Если комментарий содержит запрещённые слова,
    он не будет опубликован, а форма вернёт ошибку."""
    url = reverse('news:detail', args=(news.id, ))
    form_data = {'text': BAD_WORDS[0]}
    response = author_client.post(url, data=form_data)
    assertFormError(response,
                    form='form',
                    field='text',
                    errors=WARNING
                    )


def test_author_can_delete_comment(author_client, comment, news):
    """Авторизованный пользователь может удалить коммент"""
    url = reverse('news:delete', args=(comment.id, ))
    response = author_client.delete(url)
    url_to_comments = reverse('news:detail', args=(news.id, ))
    url_2 = url_to_comments + '#comments'
    assertRedirects(response, url_2)


def test_not_author_cant_delete_comment(not_author_client, comment, news):
    """Аноним не может удалить коммент"""
    url = reverse('news:delete', args=(comment.id, ))
    response = not_author_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_can_edit_comment(author_client, comment, news, form_data):
    """Авторизованный пользователь может редактировать коммент"""
    url = reverse('news:edit', args=(comment.id, ))
    response = author_client.post(url, data=form_data)
    url_to_comments = reverse('news:detail', args=(news.id, ))
    url_2 = url_to_comments + '#comments'
    assertRedirects(response, url_2)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_not_author_cant_edit_comment_of_another_user(
        not_author_client, form_data, comment):
    """Аноним не может редактировать коммент"""
    url = reverse('news:edit', args=(comment.id, ))
    response = not_author_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text != form_data['text']


