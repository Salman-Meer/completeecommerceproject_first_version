from django.db import models
from products.models import product
from django.contrib.auth.models import User

# Create your models here.
class Buyed_history(models.Model):
    b_h_id=  models.BigAutoField(auto_created=True, primary_key=True, serialize=False,)
    b_h_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='history_product')
    b_h_product=models.ForeignKey(product,on_delete=models.CASCADE,related_name='history_user')
  
