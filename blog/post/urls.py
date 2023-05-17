from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome),
    path("welcome", views.welcome, name="url-welcome"),
    path("posts", views.posts, name="url-posts"),
    path("post/new", views.new_post, name="url-new-post"),
    path("post/<int:pk>", views.post, name="url-post"),
    path("post/<int:pk>/edit", views.UpdatePost.as_view(), name="url-edit-post"),
    path("post/<int:pk>/delete", views.delete_post, name="url-delete-post"),
]
