from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from store.models import Book


def get_query_count(request):
    """
    Returns the number of application queries.
    Uses middleware to calculate (excludes Debug Toolbar/Silk queries).
    """
    start = getattr(request, '_app_query_start', 0)
    current = len(connection.queries)
    return current - start


def index(request):
    """Home page - overview of the Django Performance Demo."""
    return render(request, 'store/index.html')


@never_cache
def playground(request):
    """Interactive playground page for testing performance problems."""


@csrf_exempt
@never_cache
def playground_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    problem = request.POST.get('problem', '')
    variant = request.POST.get('variant', 'slow')

    result_data = []
    query_count = 0
    error = None

    try:
        if problem == 'n1_fk':
            if variant == 'slow':
                books = Book.objects.all()[:50]
                for book in books:
                    result_data.append(
                        {
                            'title': book.title,
                            'author': book.author.name,
                        }
                    )
                query_count = 51
            else:
                books = Book.objects.select_related('author')[:50]
                for book in books:
                    result_data.append(
                        {
                            'title': book.title,
                            'author': book.author.name,
                        }
                    )
                query_count = 1

        elif problem == 'n1_m2m':
            if variant == 'slow':
                books = Book.objects.all()[:50]
                for book in books:
                    tags = [tag.name for tag in book.tags.all()]
                    result_data.append(
                        {
                            'title': book.title,
                            'tags': tags,
                        }
                    )
                query_count = 51
            else:
                books = Book.objects.prefetch_related('tags')[:50]
                for book in books:
                    tags = [tag.name for tag in book.tags.all()]
                    result_data.append(
                        {
                            'title': book.title,
                            'tags': tags,
                        }
                    )
                query_count = 2

        elif problem == 'select_star':
            if variant == 'slow':
                books = list(Book.objects.all()[:50])
                for book in books:
                    result_data.append(
                        {
                            'title': book.title,
                            'year': book.published_year,
                            'price': str(book.price),
                        }
                    )
                query_count = 1
            else:
                books = list(
                    Book.objects.only('title', 'published_year', 'price')[:50]
                )
                for book in books:
                    result_data.append(
                        {
                            'title': book.title,
                            'year': book.published_year,
                            'price': str(book.price),
                        }
                    )
                query_count = 1

        elif problem == 'len_count':
            if variant == 'slow':
                books = list(Book.objects.all())
                total = len(books)
                result_data = {
                    'total': total,
                    'message': f'Loaded {total} books into memory',
                }
                query_count = 1
            else:
                total = Book.objects.count()
                books = list(
                    Book.objects.annotate(num_reviews=Count('reviews')).only(
                        'title', 'published_year'
                    )[:50]
                )
                result_data = {
                    'total': total,
                    'message': f'Used COUNT() - {total} books',
                }
                query_count = 2

        elif problem == 'pagination':
            if variant == 'slow':
                books = list(Book.objects.select_related('author')[:200])
                result_data = {
                    'count': len(books),
                    'message': f'Loaded all {len(books)} records at once',
                }
                query_count = 1
            else:
                qs = Book.objects.select_related('author').only(
                    'title', 'published_year', 'author__name'
                )
                paginator = Paginator(qs, per_page=20)
                page = paginator.get_page(request.POST.get('page', 1))
                list(page.object_list)
                query_count = 2
                result_data = {
                    'current_page': page.number,
                    'total_pages': paginator.num_pages,
                    'per_page': 20,
                    'message': f'Loaded only page {page.number} of {paginator.num_pages}',
                }

        else:
            error = 'Unknown problem'

    except Exception as e:
        error = str(e)

    queries = [
        {'sql': q['sql'], 'time': q['time']} for q in connection.queries
    ]

    return JsonResponse(
        {
            'problem': problem,
            'variant': variant,
            'query_count': query_count,
            'result': result_data,
            'queries': queries[:10],
            'error': error,
        }
    )


# ── N+1 ForeignKey ────────────────────────────────────────────────────────────


def books_slow(request):
    """Demonstrates N+1 problem with ForeignKey (slow version)."""
    books = list(Book.objects.all()[:50])
    for book in books:
        book.author.name
    return render(
        request,
        'store/books_slow.html',
        {'books': books, 'query_count': 51},
    )


def books_fast(request):
    """Demonstrates N+1 solution with select_related() (fast version)."""
    books = list(Book.objects.select_related('author')[:50])
    return render(
        request,
        'store/books_fast.html',
        {'books': books, 'query_count': 1},
    )


# ── N+1 ManyToMany ────────────────────────────────────────────────────────────


def tags_slow(request):
    """Demonstrates N+1 problem with ManyToMany (slow version)."""
    books = list(Book.objects.all()[:50])
    for book in books:
        list(book.tags.all())
    return render(
        request,
        'store/tags_slow.html',
        {'books': books, 'query_count': 51},
    )


def tags_fast(request):
    """Demonstrates N+1 solution with prefetch_related() (fast version)."""
    books = list(Book.objects.prefetch_related('tags')[:50])
    return render(
        request,
        'store/tags_fast.html',
        {'books': books, 'query_count': 2},
    )


# ── SELECT * unnecessary ────────────────────────────────────────────────────


def fields_slow(request):
    """Demonstrates unnecessary SELECT * (slow version)."""
    books = list(Book.objects.all()[:50])
    return render(
        request,
        'store/fields_slow.html',
        {'books': books, 'query_count': 1},
    )


def fields_fast(request):
    """Demonstrates solution with only() (fast version)."""
    books = list(Book.objects.only('title', 'published_year', 'price')[:50])
    return render(
        request,
        'store/fields_fast.html',
        {'books': books, 'query_count': 1},
    )


# len() vs count()


def count_slow(request):
    """Demonstrates len() problem (slow version)."""
    books = list(Book.objects.all())
    total = len(books)
    return render(
        request,
        'store/count_slow.html',
        {'total': total, 'query_count': 1},
    )


def count_fast(request):
    """Demonstrates .count() solution (fast version)."""
    total = Book.objects.count()
    books = list(
        Book.objects.annotate(num_reviews=Count('reviews')).only(
            'title', 'published_year'
        )[:50]
    )
    return render(
        request,
        'store/count_fast.html',
        {'total': total, 'books': books, 'query_count': 2},
    )


# ── Paginação ─────────────────────────────────────────────────────────────────


def paginate_slow(request):
    books = list(Book.objects.select_related('author')[:200])
    return render(
        request,
        'store/paginate_slow.html',
        {'books': books, 'query_count': 1},
    )


def paginate_fast(request):
    qs = Book.objects.select_related('author').only(
        'title', 'published_year', 'author__name'
    )
    paginator = Paginator(qs, per_page=20)
    page = paginator.get_page(request.GET.get('page', 1))
    return render(
        request,
        'store/paginate_fast.html',
        {'page': page, 'query_count': 2},
    )


# Tools


def tools(request):
    """Debug tools page showing connection.queries example."""
    books = Book.objects.select_related('author').only(
        'title', 'author__name'
    )[:10]
    total = Book.objects.count()
    queries = connection.queries
    return render(
        request,
        'store/tools.html',
        {
            'books': books,
            'total': total,
            'queries': queries,
        },
    )


def docs(request):
    """Full documentation page with all performance problems and solutions."""
