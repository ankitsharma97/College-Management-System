from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'author', 'publisher', 'semester', 'department', 'subject', 'quantity', 'issued_date', 'submit_date']
