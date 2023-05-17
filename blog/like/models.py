from django.db import models

from post.models import Post
from account.models import Account

# Create your models here.


class Like(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
