from django import forms
from .models import Photo, Review

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
