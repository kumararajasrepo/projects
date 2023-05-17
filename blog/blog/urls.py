from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from ckeditor_uploader import urls as ckeditor_urls

urlpatterns = [
    path("", include("post.urls")),
    path("account/", include("account.urls")),
    path("ckeditor/", include(ckeditor_urls)),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
