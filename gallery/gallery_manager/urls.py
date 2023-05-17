from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ViewPhoto/<str:pk>/',views.view_photo,name='view_photo'),    
    path('imageupload',views.image_upload,name='image_upload'),
    path('gallery',views.gallery,name='gallery'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
