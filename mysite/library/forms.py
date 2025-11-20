from django.contrib.auth.models import User
from .models import BookReview, Profile, BookInstance
from django import forms

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['content']

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class InstanceUpdateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'status', 'reader', 'due_back']
        widgets = {'due_back': forms.DateInput(attrs={"type": "date"})}
