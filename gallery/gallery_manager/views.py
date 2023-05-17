from django.shortcuts import render, redirect
from .gallery_form import GalleryForm, Gallery
from .category_form import Category
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def gallery(request):
    categoryname = request.GET.get('category')
    title = request.GET.get('title')
    photos = Gallery.objects.filter(user=request.user)
    if categoryname != None:
        photos = photos.filter(category=categoryname)
    if title != None:
        photos = photos.filter(title__iexact=title)
    categories = Category.objects.all()
    context = {'categories': categories, 'photos': photos}
    return render(request, 'gallery_manager/gallery.html', context)

@login_required(login_url='login')
def view_photo(request, pk):
    photo = Gallery.objects.get(id=pk)
    return render(request, 'gallery_manager/view_photo.html', {'photo': photo})

@login_required(login_url='login')
def image_upload(request):
    categories = Category.objects.all()
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

        for image in images:
            photo = Gallery.objects.create(
                title=title,
                category=categoryname,
                description=data['description'],
                image=image,
                user=request.user
            )
        
        form = GalleryForm()
        context = {'form': form, 'categories': categories}
        form = GalleryForm(request.POST, request.FILES)
        return render(request, 'gallery_manager/add_photo.html', context)
        if form.is_valid():
            form.save()
            return redirect('image_upload')
    else:
        form = GalleryForm()
        context = {'form': form, 'categories': categories}    
    return render(request, 'gallery_manager/add_photo.html', context)