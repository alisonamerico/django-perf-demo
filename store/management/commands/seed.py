"""
Management command to populate the database with test data.

Usage:
    python manage.py seed # default: 20 authors, 100 books, 5 tags, 3 reviews/book
    python manage.py seed --books 200 --reviews 5
"""

from django.core.management.base import BaseCommand

from store.factories import (
    AuthorFactory,
    BookFactory,
    ReviewFactory,
    TagFactory,
)
from store.models import Author, Book, Review, Tag


class Command(BaseCommand):
    help = 'Populates the database with fake data for performance testing'

    def add_arguments(self, parser):
        parser.add_argument('--authors', type=int, default=20)
        parser.add_argument('--books', type=int, default=100)
        parser.add_argument('--tags', type=int, default=15)
        parser.add_argument('--reviews', type=int, default=3)
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clears the database before inserting',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing database...')
            Review.objects.all().delete()
            Book.objects.all().delete()
            Author.objects.all().delete()
            Tag.objects.all().delete()

        self.stdout.write(f'Creating {options["tags"]} tags...')
        tags = [TagFactory() for _ in range(options['tags'])]

        self.stdout.write(f'Creating {options["authors"]} authors...')
        AuthorFactory.create_batch(options['authors'])

        self.stdout.write(
            f'Creating {options["books"]} books (with random tags)...'
        )
        books = BookFactory.create_batch(options['books'])

        reviews_total = options['books'] * options['reviews']
        self.stdout.write(f'Creating ~{reviews_total} reviews...')
        for book in books:
            ReviewFactory.create_batch(options['reviews'], book=book)

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Seed complete:'
                f'\n  • {Tag.objects.count()} tags'
                f'\n  • {Author.objects.count()} authors'
                f'\n  • {Book.objects.count()} books'
                f'\n  • {Review.objects.count()} reviews'
            )
        )
