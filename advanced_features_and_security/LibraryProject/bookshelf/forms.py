from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'publication_year')

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError('Title is required')
        if len(title) > 200:
            raise forms.ValidationError('Title is too long')
        return title

    def clean_author(self):
        author = self.cleaned_data.get('author', '').strip()
        if not author:
            raise forms.ValidationError('Author is required')
        if len(author) > 100:
            raise forms.ValidationError('Author name is too long')
        return author

    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        if year is None:
            raise forms.ValidationError('Publication year is required')
        if year < 0 or year > 9999:
            raise forms.ValidationError('Publication year is invalid')
        return year
