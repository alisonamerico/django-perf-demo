"""
Tests for N+1 ManyToMany problem.
"""

from http import HTTPStatus

import pytest
from django.urls import reverse

from store.factories import BookFactory


@pytest.mark.django_db
def test_tags_m2m_slow_returns_200(client):
    """Test that slow endpoint returns 200."""
    response = client.get(reverse('store:tags_slow'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_tags_m2m_slow_triggers_n_plus_1(client):
    """Test that slow version triggers N+1 queries."""
    BookFactory.create_batch(5)
    response = client.get(reverse('store:tags_slow'))
    assert response.context['query_count'] >= 5


@pytest.mark.django_db
def test_tags_m2m_fast_returns_200(client):
    """Test that fast endpoint returns 200."""
    response = client.get(reverse('store:tags_fast'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_tags_m2m_fast_uses_two_queries(client):
    """Test that fast version uses 2 queries with prefetch."""
    BookFactory.create_batch(5)
    response = client.get(reverse('store:tags_fast'))
    assert response.context['query_count'] == 2
