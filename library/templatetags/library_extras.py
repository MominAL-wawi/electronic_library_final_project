from django import template

register = template.Library()

@register.filter
def book_status(book):
    # يرجع نص + كلاس Bootstrap
    if book.is_available:
        return "متاح"
    return "مستعار بالكامل"
