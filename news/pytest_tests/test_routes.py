from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('pk_news')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:home', None)
    ),
)
@pytest.mark.django_db
def test_pages_for_anonymous(client, name, args):
    """
    Главная страница, страница отдельной записи,
    страницы регистрации пользователей, входа в 
    учётную запись и выхода из неё доступны 
    анонимным пользователям.
    """
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_author_can_edit_and_delete_comment(
        author_client,
        comment,
        name):
    """
    Страницы удаления и редактирования 
    комментария доступны автору комментария.
    """
    url = reverse(name, args=(comment.id, ))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_anonymous_user_edit_and_delete_comment(
        client,
        comment,
        name):
    """
    При попытке перейти на страницу редактирования
    или удаления комментария анонимный пользователь 
    перенаправляется на страницу авторизации.
    """
    url = reverse(name, args=(comment.id, ))
    response = client.get(url)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_not_author_edit_and_delete_comment(
        not_author_client,
        comment,
        name):
    """
    Авторизованный пользователь не может зайти на страницы 
    редактирования или удаления чужих комментариев
    (возвращается ошибка 404).
    """
    url = reverse(name, args=(comment.id,))
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
