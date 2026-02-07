from django.contrib.auth.decorators import login_required
from library.models import Borrowing

@login_required
def my_books(request):
    borrowings = Borrowing.objects.filter(
    student=request.user,
    returned_at__isnull=True
)

  return render(request, 'library/my_books.html', {
    'borrowings': borrowings
})
