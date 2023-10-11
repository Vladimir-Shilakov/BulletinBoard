from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name


class Ads(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    time_created = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='AdsCategory')

    def __str__(self):
        return self.title

    def preview(self):
        if len(self.text) > 124:
            return self.text[:124] + '...'
        else:
            return self.text

    def get_absolute_url(self):
        return reverse('ads_detail', args=[str(self.id)])


class AdsCategory(models.Model):
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Reply(models.Model):
    text = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE, related_name='replies')

    def reply_confirmed(self):
        reply = Reply.objects.filter('ads').values('reply.id')




