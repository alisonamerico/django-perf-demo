"""
Tests for Pagination problem.
"""

from http import HTTPStatus

import pytest
from django.urls import reverse

from store.factories import BookFactory


@pytest.mark.django_db
def test_paginate_slow_returns_200(client):
    """Test that slow endpoint returns 200."""
    response = client.get(reverse('store:paginate_slow'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_paginate_slow_returns_all_records(client):
    """Test that slow version loads all records."""
    BookFactory.create_batch(30)
    response = client.get(reverse('store:paginate_slow'))
    assert len(response.context['books']) >= 30


@pytest.mark.django_db
def test_paginate_fast_returns_200(client):
    """Test that fast endpoint returns 200."""
    response = client.get(reverse('store:paginate_fast'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_paginate_fast_returns_single_page(client):
    """Test that fast version returns only one page."""
    BookFactory.create_batch(30)
    response = client.get(reverse('store:paginate_fast'))
    assert len(response.context['page'].object_list) == 20


@pytest.mark.django_db
def test_paginate_fast_page_2_works(client):
    """Test that pagination page 2 works."""
    BookFactory.create_batch(30)
    response = client.get(reverse('store:paginate_fast') + '?page=2')
    assert response.status_code == HTTPStatus.OK
    assert response.context['page'].number == 2


@pytest.mark.django_db
def test_paginate_fast_uses_two_queries(client):
    """Test that fast version uses 2 queries (COUNT + page)."""
    BookFactory.create_batch(5)
    response = client.get(reverse('store:paginate_fast'))
    assert response.context['query_count'] == 2
