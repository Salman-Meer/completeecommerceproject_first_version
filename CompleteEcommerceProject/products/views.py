from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from categories.models import parent_category,child_category,gender
from .models import product,ColorVariant,SizeVariant,product_image
from .forms import formValidations
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify #it creates slugs automatically
from django.shortcuts import get_object_or_404
from random import randrange
from django.conf import settings 
import string
import random
import os
from .views2 import generate_unique_filename

# Create your views here.

def add_products(request):
    try:
        values={}
        int_colors=[]
        int_sizes=[]
        colorlist=[]
        chctry=-1
        parent_category_obj=parent_category.objects.first()
        #parent_category_obj=parent_category.objects.all()[0]
        parent_categories_id=parent_category_obj.p_c_id
        
        obj=child_category.objects.filter(p_category=parent_categories_id).all()
        
                
        colors=ColorVariant.objects.all().order_by('color_name')
        sizes=SizeVariant.objects.all().order_by('size_name')
        #return HttpResponse(colors)
        slectctgrId=request.GET.get('slectedcategoryId')
        if(slectctgrId):
            chctry=slectctgrId
            chctry=int(chctry)
  #--_____|_______-------|-------________|________------|------__________|___________------------|---------_______|___________-----------------
        if(request.method=="POST"):
            errors={}
            renamad_images=[]
            P_category=request.POST['product_parent_category']#it returns id of subject
            P_category=int(P_category)
            ##---------here is error--------##
            
            C_category=request.POST['product_child']
            C_category=int(C_category)
            #return HttpResponse(C_category)
            product_name=request.POST["product_name"]
            if formValidations.is_valid_username(product_name):
                pass
            else:
            
                errors.update({"product_name":"invalid user name please use only characters and numbers only"})
            
            #------------------------------------------------------------------------
            product_price=request.POST["product_price"]
        
            if formValidations.is_valid_price(product_price):
                pass
            else:
                errors.update({"price":"invalid price , please input a valid price an integer or a float"})
            #--------------------------------------------------------------
            product_company=request.POST["product_company"]
            if formValidations.is_valid_username(product_company):
                pass
            else:
                errors.update({"company":"invalid name of company please use only characters and numbers only"})
            
            #--------------------------------------------------------------
            product_description =request.POST["product_description"]
            #--------------------------------------------------------------
            Gender=request.POST["Gender"]
            Gender1=int(Gender)
            #--------------------------------------------------------------
            product_color=request.POST.getlist("product_colors")
            int_colors=[int(i) for i in product_color]
            if not int_colors:
                errors.update({'colors':'please select atleast one color'})
            
        
            #--------------------------------------------------------------
            product_size=request.POST.getlist("product_sizes")
            int_sizes=[int(i) for i in product_size]
            if not int_sizes:
                errors.update({'sizes':'please select atleast one size'})
            #--------------------------------------------------------------
            images=request.FILES.getlist("image")
            if not images:
                errors.update({'images_empty':'please upload atleast one picture of the product'})
            #--------------------------------------------------------------
            l=[]
            for i in images:
                is_image_valid = formValidations.is_valid_image(i.name)
                if is_image_valid == 0:
                    errors.update({"image":"invalid formate of images please make sure that all images either be jpg,jpeg,or png"})
            parent_categories = parent_category.objects.all()
            c_ctr=int(C_category)
            child_categories=child_category.objects.filter(p_category=P_category).all()  
            random_number = randrange(100, 9999)  # Random odd number between 1 and 9
            random_number=str(random_number)
            slug=product_name+'-'+random_number+'-'+product_company 
            slug=slugify(slug)
         
            if(errors):
                values.update({'child_ctgry':child_categories,'parent_categories':parent_categories,'product_name':product_name,'product_price':product_price,'product_company':product_company,'product_description':product_description,'gender':Gender1,'slectrId':P_category,'C_category':c_ctr,'error':errors,'colors':colors,'sizes':sizes,'int_colors':int_colors,'int_sizes':int_sizes})   

                return render(request,'products/add_products.html',values)#if form validation errors occurs then to show errors in template files
            else:
                data=child_category.objects.get(c_c_id=c_ctr)
                #return HttpResponse(data)
                
                category_instance = get_object_or_404(child_category, c_c_id=c_ctr)
                gender_instance= get_object_or_404(gender,g_id=Gender1)
                #color_instance = ColorVariant.objects.filter(id__in=int_colors)
                #color_instance stored a list of instances of colorvariant table
                #return HttpResponse(color_instance)

              #  for i in images:
#
 #                   original_extension = os.path.splitext(i.name)[1]#it return extension(jpg,jpeg etc)
  #                  new_name = f"{product_name+str(randrange(1000,10000000))}{original_extension}"  # e.g., '123e4567-e89b-12d3-a456-426614174000.jpg'
   #                 renamad_images.append(new_name)
                
                #return HttpResponse(renamad_images)

                add_products_database=product(p_name=product_name,p_price=product_price,p_compony=product_company,p_description=product_description,p_child_category=category_instance,p_gender=gender_instance,slug=slug)
                add_products_database.save()
                add_products_database.color_variant.add(*int_colors)
                add_products_database.size_variant.add(*int_sizes)
                #-----------------------------------------------------------------------for images------------------------------

                #return HttpResponse(add_products_database.p_id)
            
                product_instance= get_object_or_404(product,p_id=add_products_database.p_id)
                #return HttpResponse(product_instance)
               
            

                for uploaded_image in images:
                    new_name = generate_unique_filename(uploaded_image.name)
                    fs = FileSystemStorage()
                    filename = fs.save(new_name, uploaded_image)
                    # Store the file path (URL) or ImageField instance for saving in the model
                    renamad_images.append(filename)

                #return HttpResponse(renamad_images)

                for image_file in renamad_images:
                    product_image.objects.create(product_id=product_instance,image=image_file)
                messages.success(request,'data saved successfully')
                
                total_products=product.objects.count()
                product_page=15
                totalpage=(total_products+product_page-1)//product_page
                
                #return HttpResponse(totalpage)
                return redirect(reverse('manipulation')+f'?page={str(totalpage)}')
                
                
                
                
        else:
            parent_categories = parent_category.objects.all().order_by('p_c_name')
            if(request.GET.get('slectedcategoryId')):
                
                slectctgrId=request.GET.get('slectedcategoryId')
                if(slectctgrId == None):
                    
                    obj=child_category.objects.all().order_by('c_c_name')
                #return HttpResponse(slectctgrId)
                else:
                    obj=child_category.objects.filter(p_category=slectctgrId).all().order_by('c_c_name')
            
                #data = employes.objects.get(id=id)
            #return HttpResponse(parent_categories)
                  
            values.update({'parent_categories':parent_categories,'child_ctgry':obj,'slectrId':chctry,'colors':colors,'sizes':sizes,'colorlist':colorlist,'int_sizes':int_sizes,'int_colors':int_colors})
            return render(request,'products/add_products.html',values)
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')

