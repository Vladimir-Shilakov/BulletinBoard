from django.contrib import admin
from .models import Author, Ads, Category, Reply
from django import forms
from ckeditor.widgets import CKEditorWidget


class AdsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Ads
        fields = '__all__'


class AdsAdmin(admin.ModelAdmin):
    form = AdsAdminForm


admin.site.register(Author)
admin.site.register(Ads, AdsAdmin)
admin.site.register(Category)
admin.site.register(Reply)


