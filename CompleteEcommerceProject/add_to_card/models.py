
from django.db import models
from products.models import product,ColorVariant,SizeVariant
from django.contrib.auth.models import User
# Create your models here.
class Card(models.Model):
    c_id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    c_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    c_product=models.ForeignKey(product,on_delete=models.CASCADE,related_name='product')
    c_color_variant=models.ForeignKey(ColorVariant,on_delete=models.CASCADE,related_name='c_v')
    c_size_variant=models.ForeignKey(SizeVariant,on_delete=models.CASCADE,related_name='s_v')
    quantity=models.IntegerField(default=1)
    price=models.IntegerField(default=0)
    
    
    
  
# Create your models here.
