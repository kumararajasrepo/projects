from django.db import models

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name
    
class Gallery(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    category=models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')
    user = models.CharField(max_length=50)

    def __str__(self):
        return self.title  

