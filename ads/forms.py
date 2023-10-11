from django import forms
from .models import Ads, Reply
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AdsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Ads
        fields = ['title', 'category', 'content']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']

