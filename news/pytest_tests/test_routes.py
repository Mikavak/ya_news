from http import HTTPStatus
from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects
from ..models import Comment, News


# # Указываем в фикстурах встроенный клиент.
# def test_home_availability_for_anonymous_user(client):
#     # Адрес страницы получаем через reverse():
#     url = reverse('news:home')
#     response = client.get(url)
#     assert response.status_code == HTTPStatus.OK

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
def test_author_can_edit(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_author_can_edit_comment(author_client, comment):
    url = reverse('news:edit', args=(comment.id, ))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_author_can_delete_comment(author_client, comment):
    url = reverse('news:delete', args=(comment.id, ))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_anonymous_user_edit_comment(client, comment):
    url = reverse('news:edit', args=(comment.id, ))
    response = client.get(url)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)


def test_anonymous_user_delete_comment(client, comment):
    url = reverse('news:delete', args=(comment.id, ))
    response = client.get(url)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)


def test_not_author_edit_comment(not_author_client, comment):
    url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_not_author_delete_comment(not_author_client, comment):
    url = reverse('news:delete', args=(comment.id,))
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
