from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Page(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    page_identifier = models.CharField(max_length=200, blank=True)
    page_author = models.CharField(max_length=200, blank=True)
    general_link = models.CharField(max_length=200)
    page_img_link = models.CharField(max_length=400)

    def __str__(self):
        return self.general_link

    def get_absolute_url(self):
        return reverse('single_page_posts', args=[str(self.id)])


class Post(models.Model):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
    )
    post_id = models.CharField(max_length=200)
    post_author = models.CharField(max_length=100)
    post_text = models.TextField(null=True, blank=True)
    post_time = models.CharField(max_length=50)

    def __str__(self):
        return self.post_text

    def get_absolute_url(self):
        return reverse('single_page_posts', args=[str(self.id)])
