from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True, blank=True, editable=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse_lazy("url-task", kwargs={"pk": self.pk})
