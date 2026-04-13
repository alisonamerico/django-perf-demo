import factory
from factory.django import DjangoModelFactory
from faker import Faker

from store.models import Author, Book, Review, Tag

fake = Faker('pt_BR')


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.LazyFunction(fake.name)
    bio = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=4))
    country = factory.LazyFunction(fake.country)
    born_year = factory.LazyFunction(
        lambda: fake.random_int(min=1900, max=1990)
    )


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ('slug',)

    name = factory.Sequence(lambda n: f'tag-{n}')
    slug = factory.LazyAttribute(lambda o: o.name.lower().replace(' ', '-'))


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.LazyFunction(lambda: fake.sentence(nb_words=4).rstrip('.'))
    author = factory.SubFactory(AuthorFactory)
    published_year = factory.LazyFunction(
        lambda: fake.random_int(min=1950, max=2024)
    )
    price = factory.LazyFunction(
        lambda: round(fake.random.uniform(10, 150), 2)
    )
    synopsis = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=8))

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            # Adds between 1 and 4 random tags
            from random import randint, sample

            all_tags = list(Tag.objects.all())
            if all_tags:
                chosen = sample(all_tags, k=min(randint(1, 4), len(all_tags)))
                self.tags.set(chosen)


class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    book = factory.SubFactory(BookFactory)
    reviewer_name = factory.LazyFunction(fake.name)
    rating = factory.LazyFunction(lambda: fake.random_int(min=1, max=5))
    body = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=3))
