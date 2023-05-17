from django.db import models

from post.models import Post
from account.models import Account

# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=2048)
