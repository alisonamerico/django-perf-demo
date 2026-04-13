"""
Models for the Django Performance Demo application.

This module contains the database models used to demonstrate
performance problems in Django applications:

- Author: Represents a book author
- Tag: Represents tags for books (ManyToMany)
- Book: Represents a book with ForeignKey to Author and ManyToMany to Tag
- Review: Represents reviews for books (reverse ForeignKey)
"""

from django.db import models


class Author(models.Model):
    """Represents an author of a book."""

    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    born_year = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Represents a tag that can be assigned to books."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=300)
    # ForeignKey - alvo principal do select_related
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='books'
    )
    # ManyToMany - alvo principal do prefetch_related
    tags = models.ManyToManyField(Tag, blank=True, related_name='books')
    published_year = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    # "heavy" field - useful for demonstrating only()/defer()
    synopsis = models.TextField(blank=True)

    class Meta:
        ordering = ['title']
        # db_index is automatic in ForeignKey; we add an extra index
        # on published_year to demonstrate performance difference
        indexes = [
            models.Index(fields=['published_year'], name='book_year_idx'),
        ]

    def __str__(self):
        return self.title


class Review(models.Model):
    # Reverse FK - demonstrates prefetch_related on related manager
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='reviews'
    )
    reviewer_name = models.CharField(max_length=100)
    rating = models.SmallIntegerField()  # 1–5
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.reviewer_name} → {self.book.title} ({self.rating}★)'
