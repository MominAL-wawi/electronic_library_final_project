from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    icon = models.CharField(max_length=80, blank=True)  # مثل: "bi bi-book"

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=250)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    publication_year = models.PositiveIntegerField()
    pages = models.PositiveIntegerField()
    language = models.CharField(max_length=80)
    description = models.TextField()
    total_copies = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def borrowed_count(self):
        return self.borrowings.filter(returned_at__isnull=True).count()

    @property
    def available_copies(self):
        available = self.total_copies - self.borrowed_count
        return max(0, available)

    @property
    def is_available(self):
        return self.available_copies > 0

    @property
    def avg_rating(self):
        qs = self.reviews.all()
        if not qs.exists():
            return 0
        return round(sum(r.stars for r in qs) / qs.count(), 1)

class Borrowing(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    borrowed_at = models.DateTimeField(default=timezone.now)
    expected_return_at = models.DateTimeField()
    returned_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-borrowed_at']
        unique_together = ('student', 'book', 'returned_at')  # يمنع استعارة نفس الكتاب مرتين بنفس الوقت

    def __str__(self):
        return f"{self.student.username} -> {self.book.title}"

    @property
    def is_late(self):
        return self.returned_at is None and timezone.now() > self.expected_return_at

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    stars = models.PositiveIntegerField()  # 1..5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'student')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.book.title} - {self.stars}★ by {self.student.username}"
