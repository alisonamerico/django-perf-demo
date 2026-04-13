"""
Tests for N+1 ForeignKey problem.
"""

from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_books_fk_slow_returns_200(client):
    """Test that slow endpoint returns 200."""
    response = client.get(reverse('store:books_slow'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_books_fk_slow_triggers_n_plus_1(client, books_with_authors):
    """Test that slow version triggers N+1 queries."""
    response = client.get(reverse('store:books_slow'))
    assert response.context['query_count'] >= 10


@pytest.mark.django_db
def test_books_fk_fast_returns_200(client):
    """Test that fast endpoint returns 200."""
    response = client.get(reverse('store:books_fast'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_books_fk_fast_uses_single_query(client, books_with_authors):
    """Test that fast version uses only 1 query with JOIN."""
    response = client.get(reverse('store:books_fast'))
    assert response.context['query_count'] == 1
