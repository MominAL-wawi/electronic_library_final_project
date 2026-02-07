from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import Book, Category, Author, Borrowing, Review
from .forms import ReviewForm, ContactForm

MAX_BORROW = 5
BORROW_DAYS = 7

def all_books(request):
    qs = Book.objects.select_related('author', 'category').all()

    search = request.GET.get('q', '').strip()
    cat = request.GET.get('cat', '').strip()
    sort = request.GET.get('sort', 'new')

    if search:
        qs = qs.filter(title__icontains=search) | qs.filter(author__name__icontains=search)

    if cat:
        qs = qs.filter(category__id=cat)

    if sort == 'new':
        qs = qs.order_by('-created_at')
    elif sort == 'old':
        qs = qs.order_by('created_at')
    elif sort == 'rate':
        qs = sorted(qs, key=lambda b: b.avg_rating, reverse=True)

    categories = Category.objects.all()
    paginator = Paginator(qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'library/books.html', {
        'page_obj': page_obj,
        'categories': categories,
        'search': search,
        'cat': cat,
        'sort': sort
    })

def book_details(request, id):
    book = get_object_or_404(Book, id=id)
    reviews = book.reviews.select_related('student').all()

    is_logged = request.user.is_authenticated
    has_current = False
    borrowed_before = False
    can_review = False

    if is_logged:
        has_current = Borrowing.objects.filter(student=request.user, book=book, returned_at__isnull=True).exists()
        borrowed_before = Borrowing.objects.filter(student=request.user, book=book, returned_at__isnull=False).exists()
        can_review = borrowed_before and not Review.objects.filter(student=request.user, book=book).exists()

    return render(request, 'library/book_details.html', {
        'book': book,
        'reviews': reviews,
        'has_current': has_current,
        'can_review': can_review,
    })

def categories(request):
    cats = Category.objects.all()
    return render(request, 'library/categories.html', {'cats': cats})

def authors(request):
    auths = Author.objects.all()
    return render(request, 'library/authors.html', {'authors': auths})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "تم إرسال رسالتك بنجاح.")
            return redirect('contact')
        messages.error(request, "تأكد من تعبئة البيانات بشكل صحيح.")
    else:
        form = ContactForm()
    return render(request, 'library/contact.html', {'form': form})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if not book.is_available:
        messages.error(request, "لا توجد نسخ متاحة حالياً.")
        return redirect('book_details', id=book.id)

    already = Borrowing.objects.filter(student=request.user, book=book, returned_at__isnull=True).exists()
    if already:
        messages.warning(request, "أنت مستعير هذا الكتاب حالياً.")
        return redirect('book_details', id=book.id)

    current_count = Borrowing.objects.filter(student=request.user, returned_at__isnull=True).count()
    if current_count >= MAX_BORROW:
        messages.error(request, f"لا يمكنك استعارة أكثر من {MAX_BORROW} كتب.")
        return redirect('book_details', id=book.id)

    expected = timezone.now() + timedelta(days=BORROW_DAYS)
    Borrowing.objects.create(student=request.user, book=book, expected_return_at=expected)

    messages.success(request, "تمت استعارة الكتاب بنجاح.")
    return redirect('my_books')

@login_required
def my_books(request):
    borrows = Borrowing.objects.select_related('book').filter(student=request.user, returned_at__isnull=True)
    return render(request, 'library/my_books.html', {'borrows': borrows})

@login_required
def return_book(request, borrow_id):
    b = get_object_or_404(Borrowing, id=borrow_id, student=request.user)
    if b.returned_at is None:
        b.returned_at = timezone.now()
        b.save()
        messages.success(request, "تم إرجاع الكتاب.")
    return redirect('my_books')

@login_required
def add_review(request, id):
    book = get_object_or_404(Book, id=id)

    borrowed_before = Borrowing.objects.filter(student=request.user, book=book, returned_at__isnull=False).exists()
    if not borrowed_before:
        messages.error(request, "لا يمكنك التقييم إلا بعد استعارة الكتاب سابقاً.")
        return redirect('book_details', id=book.id)

    if Review.objects.filter(student=request.user, book=book).exists():
        messages.warning(request, "قمت بتقييم هذا الكتاب سابقاً.")
        return redirect('book_details', id=book.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.student = request.user
            r.book = book
            r.save()
            messages.success(request, "تم إضافة التقييم.")
            return redirect('book_details', id=book.id)
        messages.error(request, "تأكد من إدخال نجوم بين 1 و 5.")
    else:
        form = ReviewForm()

    return render(request, 'library/review.html', {'book': book, 'form': form})
