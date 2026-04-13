from django.contrib import admin

from store.models import Author, Book, Review, Tag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'born_year']
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_year', 'price']
    list_select_related = ['author']
    search_fields = ['title']
    filter_horizontal = ['tags']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer_name', 'book', 'rating', 'created_at']
    list_select_related = ['book']
