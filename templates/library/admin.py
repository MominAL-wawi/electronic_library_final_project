from django.contrib import admin
from .models import Category, Author, Book, Borrowing, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon')
    search_fields = ('name',)
    list_per_page = 20

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 20

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'total_copies', 'created_at')
    list_filter = ('category', 'author')
    search_fields = ('title', 'author__name')
    list_per_page = 20

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'book', 'borrowed_at', 'expected_return_at', 'returned_at')
    list_filter = ('returned_at',)
    search_fields = ('student__username', 'book__title')
    list_per_page = 25

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'student', 'stars', 'created_at')
    list_filter = ('stars',)
    search_fields = ('book__title', 'student__username')
    list_per_page = 25
