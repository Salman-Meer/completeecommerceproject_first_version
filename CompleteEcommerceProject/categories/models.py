from django.db import models
# Create your models here.
class parent_category(models.Model):
    p_c_id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False,)
    p_c_name=models.CharField(max_length=100,unique=True)
   # def __str__(self)-> str:
    #        return self.p_c_name#it is returning the name of category e.g shirt coat. without this the object was returning

class child_category(models.Model):
    c_c_id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False,)
    c_c_name=models.CharField(max_length=100,unique=True)
    p_category=models.ForeignKey(parent_category,on_delete=models.CASCADE,related_name='child_category')
   #def __str__(self)-> str:
    #        return self.c_c_name    #it is returning the name of category e.g shirt coat. without this the object was returning


class gender(models.Model):
    g_id=models.BigAutoField(auto_created=True,primary_key=True,serialize=False)
    g_name=models.IntegerField()
    
    


