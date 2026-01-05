from django.db import models
from categories.models import child_category,gender
from django.http import HttpResponse
# Create your models here.

class ColorVariant(models.Model):
    color_name=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    #def __str__(self)-> str:
     #       return self.color_name#it is returning the name of product in admin site e.g shirt coat. without this the object was returning

class SizeVariant(models.Model):
    size_name = models.CharField(max_length=100)
    price=models.IntegerField(default=0)
   # def __str__(self)-> str:
    #        return self.size_name#it is returning the name of product in admin site e.g shirt coat. without this the object was returning

class product(models.Model):
    p_id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False,)
    p_name=models.CharField(max_length=100)
    p_price=models.IntegerField()
    p_compony=models.CharField(max_length=100)
    p_is_sale=models.BooleanField(default=False)
    p_description=models.CharField(max_length=1500)
    p_child_category=models.ForeignKey(child_category,on_delete=models.CASCADE,related_name='p_child_category')
    p_gender=models.ForeignKey(gender,on_delete=models.CASCADE,related_name='child_category')
    slug=models.SlugField()
    color_variant = models.ManyToManyField(ColorVariant,blank=True)
    size_variant = models.ManyToManyField(SizeVariant,blank=True)
    def get_product_price_by_size(self,size):
        return (self.p_price + SizeVariant.objects.get(size_name=size).price)
    def get_product_price_by_color(self,color):
        return (self.p_price + ColorVariant.objects.get(color_name=color).price)
        
    #def __str__(self)-> str:
     #       return self.p_name#it is returning the name of product in admin site e.g shirt coat. without this the object was returning
    #def colors(self):
     #     return ",".join([str(p) for p in self.color_variant.all()])
    #def size(self):
     #     return ",".join([str(p) for p in self.size_variant.all()])
    
    

class product_image(models.Model):
    i_id=  models.BigAutoField(auto_created=True, primary_key=True, serialize=False,)
    image=models.ImageField(upload_to='images')
    product_id=models.ForeignKey(product,on_delete=models.CASCADE,related_name='p_image')
    