from django.shortcuts import render, redirect
from .gallery_form import GalleryForm, Gallery
from .category_form import Category
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.files import File
from PIL import Image
from io import BytesIO
import base64

@login_required(login_url='login')
def gallery(request):
    context={}
    try:
        categoryname = request.GET.get('category')
        title = request.GET.get('title')
        photos = Gallery.objects.filter(user=request.user)    
        if categoryname != None:
            photos = photos.filter(category=categoryname)
        if title != None:
            photos = photos.filter(title__iexact=title)
        categories = Category.objects.all()
        
        for photo in photos:
            photo.image_data = base64.b64encode(photo.image_data).decode('utf-8')

        context = {'categories': categories, 'photos': photos}
    except Exception as e:
        print("An error occurred:", str(e))

    return render(request, 'gallery_manager/gallery.html', context)

@login_required(login_url='login')
def view_photo(request, pk):
    context={}
    try:
        photo = Gallery.objects.get(id=pk)
        context = {'photo': photo}
    except Exception as e:
        print("An error occurred:", str(e))
    return render(request, 'gallery_manager/view_photo.html', context)

@login_required(login_url='login')
def image_upload(request):
    context={}
    try:
        categories = Category.objects.all()
        error_message=""
        status=True
        if request.method == 'POST':
            data = request.POST
            
            title=None
            categoryname=None
            description=None
            imageurl=None
            images = request.FILES.getlist('images')

            if data['title'] != 'none':
                title=data['title']
            
            if data['category'] != 'none':
                categoryname = Category.objects.get(id=data['category'])
            elif data['category_new'] != '':
                categoryname=data['category_new']
                newcategory = Category.objects.create(
                    name=categoryname
                )
            
            if data['description'] != 'none':
                description=data['description']        

            try:
                for image in images:
                    validate_image_type(image)
                    photo = Gallery.objects.create(
                    title=title,
                    category=categoryname,
                    description=data['description'],
                    image=image,
                    image_data=image.read(),
                    user=request.user                
                )
                error_message="File is uploaded successfully."
            except ValidationError as e:
                error_message=str(e)
                error_message=error_message[2:len(error_message)-2]
                status=False
            form = GalleryForm(request.POST, request.FILES)
            context = {'form': form, 'categories': categories,'status':status, 'message':error_message}            
            return render(request, 'gallery_manager/add_photo.html', context)        
        else:
            form = GalleryForm()
            context = {'form': form, 'categories': categories}
    except Exception as e:
        print("An error occurred:", str(e))    
    return render(request, 'gallery_manager/add_photo.html', context)

def validate_image_type(image):
    valid_extensions=['jpg','jpeg','jfif','png','gif']
    max_file_size = 1 * 1024 * 1024
    file_extension=image.name.rsplit('.',1)[1].lower()
    if file_extension not in valid_extensions:
        raise ValidationError("Invalid image file. Only JPG, JPEG, JFIF, PNG, and GIF files are allowed.")
    elif image.size>max_file_size:
        raise ValidationError("File size exceeds the maximum allowed size.")