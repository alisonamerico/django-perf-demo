"""
Pytest configuration and fixtures for Django Performance Demo.
"""

import pytest

from store.factories import AuthorFactory, BookFactory


@pytest.fixture
def books_with_authors(db):
    """Create test data: 3 authors with 10 books each."""
    authors = AuthorFactory.create_batch(3)
    for author in authors:
        BookFactory.create_batch(10, author=author)
    return authors
