from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.all_books, name='books'),
    path('book/<int:id>/', views.book_details, name='book_details'),
    path('categories/', views.categories, name='categories'),
    path('authors/', views.authors, name='authors'),
    path('contact/', views.contact, name='contact'),

    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('my-books/', views.my_books, name='my_books'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),

    path('book/<int:id>/review/', views.add_review, name='add_review'),
]
