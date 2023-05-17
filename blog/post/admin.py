from django.contrib import admin

from post.models import Author, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date")
    list_filter = ("author", "date")


# Register your models here.
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
