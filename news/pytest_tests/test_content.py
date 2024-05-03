from django.urls import reverse
import pytest

@pytest.mark.django_db
def test_10_news(client, news_10):
    response = client.get(reverse('news:home'))
    obj = response.context['object_list']
    count = obj.count()
    assert count == 10

