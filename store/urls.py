from django.urls import path

from store import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    # N+1 ForeignKey
    path('books/slow/', views.books_slow, name='books_slow'),
    path('books/fast/', views.books_fast, name='books_fast'),
    # N+1 ManyToMany
    path('tags/slow/', views.tags_slow, name='tags_slow'),
    path('tags/fast/', views.tags_fast, name='tags_fast'),
    # SELECT * unnecessary
    path('fields/slow/', views.fields_slow, name='fields_slow'),
    path('fields/fast/', views.fields_fast, name='fields_fast'),
    # len() vs count()
    path('count/slow/', views.count_slow, name='count_slow'),
    path('count/fast/', views.count_fast, name='count_fast'),
    # Pagination
    path('paginate/slow/', views.paginate_slow, name='paginate_slow'),
    path('paginate/fast/', views.paginate_fast, name='paginate_fast'),
    # Tools
    path('tools/', views.tools, name='tools'),
    # Documentation
    path('docs/', views.docs, name='docs'),
    # Interactive Playground
    path('playground/', views.playground, name='playground'),
    path('playground/api/', views.playground_api, name='playground_api'),
]
