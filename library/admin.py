from django.contrib import admin
from .models import Category, Author, Book, Borrowing, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "icon")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "publication_year", "total_copies", "created_at")
    list_filter = ("category", "language", "publication_year")
    search_fields = ("title", "author__name", "category__name")
    ordering = ("-created_at",)


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "book", "borrowed_at", "expected_return_at", "returned_at", "is_late")
    list_filter = ("returned_at",)
    search_fields = ("student__username", "book__title")
    ordering = ("-borrowed_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "student", "stars", "created_at")
    list_filter = ("stars",)
    search_fields = ("book__title", "student__username")
    ordering = ("-created_at",)
