from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from .forms import PostForm
from .models import Author, Post


def welcome(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.order_by("-date")[:3]
    return render(request, "post/posts.html", {"posts": posts})


def posts(request: HttpRequest) -> HttpResponse:
    return render(request, "post/posts.html", {"posts": Post.objects.order_by("-date")})


def post(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)
    return render(request, "post/post.html", {"post": post})


class UpdatePost(LoginRequiredMixin, UpdateView):
    template_name = "post/edit-post.html"
    form_class = PostForm
    model = Post

    def get_object(self) -> Post:
        pk = self.kwargs.get("pk")
        return get_object_or_404(Post, pk=pk)

    def get_success_url(self) -> str:
        return reverse_lazy("url-post", kwargs={"pk": self.get_object().pk})


def edit_post(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("post_detail", pk=post.pk)
    return render(request, "post/edit-post.html", {"form": form, "post": post})


def delete_post(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("url-posts")


@login_required(login_url="url-signin")
def new_post(request: HttpRequest) -> HttpResponse:
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            data = request.POST
            author = Author.objects.get_or_create(account=request.user)

            image = request.FILES.get("image")

            Post.objects.create(
                title=data["title"],
                description=data["description"],
                content=data["content"],
                image=image,
                author=author,
            )

            return redirect("url-posts")
        else:
            errors = {field: error_list for field, error_list in form.errors.items()}
            return render(
                request,
                "post/new_post.html",
                {"form": form, "errors": errors},
            )

    return render(request, "post/new_post.html", {"form": form})
