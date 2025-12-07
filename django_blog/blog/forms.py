from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text='Comma separated tags', widget=forms.TextInput())
    class Meta:
        model = Post
        fields = ("title", "content", "tags")
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if instance:
            tag_names = ', '.join([t.name for t in instance.tags.all()])
            self.fields['tags'].initial = tag_names

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
