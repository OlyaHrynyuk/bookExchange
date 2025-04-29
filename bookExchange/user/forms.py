from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Offer

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'category', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class OfferForm(forms.ModelForm):
    offered_book = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Offer
        fields = ['offered_book']

    def __init__(self, user=None, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['offered_book'].queryset = Book.objects.filter(owner=user, available=True)