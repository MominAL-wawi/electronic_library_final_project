from django.shortcuts import render
from django.contrib.auth.models import User
from library.models import Book, Author

def home(request):
    recent_books = Book.objects.order_by('-created_at')[:6]
    top_books = sorted(Book.objects.all(), key=lambda b: b.avg_rating, reverse=True)[:3]

    stats = {
        'books_count': Book.objects.count(),
        'authors_count': Author.objects.count(),
        'students_count': User.objects.count(),
    }
    return render(request, 'core/home.html', {
        'recent_books': recent_books,
        'top_books': top_books,
        'stats': stats
    })
