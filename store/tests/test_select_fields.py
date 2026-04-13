"""
Tests for SELECT * unnecessary problem.
"""

from http import HTTPStatus

import pytest
from django.urls import reverse

from store.factories import BookFactory


@pytest.mark.django_db
def test_fields_slow_returns_200(client):
    """Test that slow endpoint returns 200."""
    response = client.get(reverse('store:fields_slow'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_fields_fast_returns_200(client):
    """Test that fast endpoint returns 200."""
    response = client.get(reverse('store:fields_fast'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_fields_fast_uses_single_query(client):
    """Test that fast version uses only 1 query."""
    BookFactory.create_batch(5)
    response = client.get(reverse('store:fields_fast'))
    assert response.context['query_count'] == 1
