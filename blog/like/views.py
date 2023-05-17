from django.http import HttpRequest, HttpResponse

from django.shortcuts import get_object_or_404, redirect, render

# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy
# from django.views.generic.edit import UpdateView

from .models import Like

# from post.models import Post


def comments(request: HttpRequest) -> HttpResponse:
    return render(request, "likes.html", {"likes": Like.objects.all()})
