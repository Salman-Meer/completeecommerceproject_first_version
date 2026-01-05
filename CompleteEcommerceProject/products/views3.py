import os
from django.shortcuts import get_object_or_404
from django.http import HttpRequest,HttpResponse
from products.models import ColorVariant,SizeVariant,gender
from django.shortcuts import render,redirect
from products.models import product,product_image
from .forms import formValidations
from django.conf import settings
from .utils import delete_image_file
from django.contrib import messages

def update_products(request,slug):
   try:
      if(request.method == "POST"):
         errors={}
         product_name=request.POST["product_name"]
         product_price=request.POST["product_price"]
         product_company=request.POST["product_company"]
         product_description=request.POST["product_description"]
         Gender=request.POST['Gender']
         product_colors=request.POST.getlist("product_colors")
         product_sizes=request.POST.getlist("product_sizes")
         int_colors=[int(i) for i in product_colors]
         int_sizes=[int(i) for i in product_sizes]
         Gender1=int(Gender)
         gender_instance = get_object_or_404(gender,g_id=Gender1)
         #return HttpResponse(gender_instance)
         #------------------------validations------------------------------------
         
         product_name=request.POST["product_name"]
         if formValidations.is_valid_username(product_name):
            pass
         else:
            
            errors.update({"product_name":"invalid user name please use only characters and numbers only"})
         if formValidations.is_valid_price(product_price):
                pass
         else:
                errors.update({"price":"invalid price , please input a valid price an integer or a float"})
         if formValidations.is_valid_username(product_company):
                pass
         else:
                errors.update({"company":"invalid name of company please use only characters and numbers only"})

         if(errors):
            return render(request,'products/update_products.html',values,errors)
         else:
             
            products=product.objects.get(slug=slug)
            products.p_name=product_name
            products.p_compony=product_company
            products.p_price=product_price
            products.p_gender=gender_instance
            products.p_description=product_description
            products.save()
            products.color_variant.set(int_colors)
            products.size_variant.set(int_sizes)
            messages.success(request,'data updated successfully')
                
            return redirect('manipulation')
#        return HttpResponse("data have been saved")
            


      values={}
      colorlist=[]
      sizelist=[]
      products=product.objects.filter(slug = slug).prefetch_related('color_variant').prefetch_related('size_variant').distinct()
      genderr=None
      for p in products:
         for c in p.color_variant.all():
            colorlist.append(c.id)  
         for s in p.size_variant.all():
            sizelist.append(s.id)
         genderr=p.p_gender.g_id
   
      values.update({'gender':genderr})
      values.update({'products':products})
      colorsV=ColorVariant.objects.all()
      sizesV=SizeVariant.objects.all()
      values.update({'colorsV':colorsV})
      values.update({'sizesV':sizesV})
      values.update({'sizelist':sizelist})
      values.update({'colorlist':colorlist})
      values.update({'slug':slug})



      
   

      return render(request,'products/update_products.html',values)
   except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')

def delete_products(request,slug):
   try:
      image_names=[]
      record = get_object_or_404(product, slug=slug)
      
      imagelist=product_image.objects.filter(product_id=record)
      for image in imagelist:
         image_names.append(str(image.image))
     
      for image in image_names:
         #return HttpResponse(image)
         delete_image_file(image)
           # Deletes the file from media folder
         
      record.delete()
      messages.warning(request,'data deleted successfully')
                
      return redirect('manipulation')    
 #     return HttpResponse('product deleted successfully')
   except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')

