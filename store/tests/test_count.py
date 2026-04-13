"""
Tests for len() vs count() problem.
"""

from http import HTTPStatus

import pytest
from django.urls import reverse

from store.factories import BookFactory


@pytest.mark.django_db
def test_count_slow_returns_200(client):
    """Test that slow endpoint returns 200."""
    response = client.get(reverse('store:count_slow'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_count_fast_returns_200(client):
    """Test that fast endpoint returns 200."""
    response = client.get(reverse('store:count_fast'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_count_fast_uses_two_queries(client):
    """Test that fast version uses 2 queries (COUNT + list)."""
    BookFactory.create_batch(5)
    response = client.get(reverse('store:count_fast'))
    assert response.context['query_count'] == 2
