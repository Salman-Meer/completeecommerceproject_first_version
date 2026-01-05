import random 
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
import string
from random import randrange
import os
from categories.models import parent_category,child_category,gender
from products.models import product
from django.http import HttpRequest,HttpResponse
from django.contrib import messages


def generate_unique_filename(filename):
    r=int(randrange(100,150))
    r1=str(r*100000)
    random_string = ''.join(random.choices(string.ascii_letters+r1+string.digits, k=r))
    extension = os.path.splitext(filename)[1]  # Get the file extension
    return f"{random_string}{extension}"

def get_products(request,slug):
    try:
        if request.GET.get('page'):
            page_number=request.GET.get('page') #this will come in url
        
        else:
            page_number='1'
        selected_size=[]
        products_list=[]
        values={}
        child_categories_products=[]
        products=product.objects.get(slug=slug)
        values.update({"product":products})
        selected_color=None
        selected_price=None
        child_category_obj=products.p_child_category#it returned child category object of recored 1
        #related_products=product.objects.filter(p_child_category=child_category_obj)
        child_categories_products.append(child_category_obj)
        parent_category_obj=child_category_obj.p_category
        child_categories=child_category.objects.filter(p_category=parent_category_obj)
        product_gender=products.p_gender


        for i in child_categories:
            if(i.c_c_id is child_category_obj.c_c_id):
                pass
            else:
                child_categories_products.append(i)

        for child_category_item in child_categories_products:
            for productitem in child_category_item.p_child_category.all():
                
                if productitem.p_gender == product_gender:
                    products_list.append(productitem)

        paginator = Paginator(products_list, 16)
        ServiceDatafinal = paginator.get_page(page_number)
        totalpage=ServiceDatafinal.paginator.num_pages
        values.update({
            'page_no':int(page_number),
            'related_products':ServiceDatafinal,
            'lastpage':totalpage,
            'totalPagelist':[n+1 for n in range(totalpage)]
            })

                
        for size in products.size_variant.all() :
        
            selected_size=size.size_name
            if selected_size:
                break

        for color in products.color_variant.all() :
        
            selected_color=color.color_name
            if selected_color:
                break
        normal_price=products.p_price
        
        selected_color_price=products.get_product_price_by_color(selected_color)
        selected_size_price=products.get_product_price_by_size(selected_size)
        colors_charg=selected_color_price-normal_price
        sizes_charg=selected_size_price-normal_price
        price=normal_price+colors_charg+sizes_charg
        values.update({'product':products,'selected_size':selected_size,'selected_color':selected_color,'selected_price':price})
        
        if(request.GET.get('size')):
                
                size=request.GET.get('size')
                #return HttpResponse(size)

                price=products.get_product_price_by_size(size)
                
                selected_size=size
                selected_price=price
                
                values.update({'product':products,'selected_size':selected_size,'selected_color':selected_color,'selected_price':selected_price})
                
        if(request.GET.get('color')):
            
                selected_color=request.GET.get('color')
                #return HttpResponse(size)
                selected_price=products.get_product_price_by_color(selected_color)
                values.update({'product':products,'selected_size':selected_size,'selected_color':selected_color,'selected_price':selected_price,'size_status':0})
        
        
        categories=parent_category.objects.all()
        values.update({'categories':categories})
    #-----------------------------------------------------------------------------------

        request.session['path']=request.path
        
        return render(request,'products/products.html',values)
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')


def product_list(request):
    try:
        values={}
        ##products=product.objects.all()
        ##products = product.objects.select_related('p_child_category').all()
        
        products = product.objects.select_related('p_child_category').prefetch_related('color_variant').prefetch_related('size_variant').all()
        
        parent_categories=parent_category.objects.all()
        child_categories=child_category.objects.all()
        values.update({'parent_categories':parent_categories})
        values.update({'child_categories':child_categories})
        if(request.GET.get('slectedPcategoryId') and not request.GET.get('slectedCcategoryId')):
            
            p_category_id=request.GET.get('slectedPcategoryId')
            p_c_id=int(p_category_id)
            child_categories=child_category.objects.filter(p_category=p_category_id)
            l=[]
            for i in child_categories:
               l.append(i.c_c_id)
            products=product.objects.filter(p_child_category__in = l).select_related('p_child_category').prefetch_related('color_variant').prefetch_related('size_variant').distinct()

            values.update({'child_categories':child_categories})
            values.update({'p_category_id':p_c_id})
            
        elif(request.GET.get('slectedCcategoryId') and request.GET.get('slectedPcategoryId')):
             
             
             c_category_id=request.GET.get('slectedCcategoryId')
             p_category_id=request.GET.get('slectedPcategoryId')
             p_c_id=int(p_category_id)
             c_c_id=int(c_category_id)
             if(p_c_id is -1):
                  child_category_obj=child_category.objects.get(c_c_id=c_c_id)
                  p_c_id=child_category_obj.p_category_id
                  
             values.update({'p_category_id':p_c_id})
             values.update({'c_category_id':c_c_id})
             products=product.objects.filter(p_child_category = c_c_id).select_related('p_child_category').prefetch_related('color_variant').prefetch_related('size_variant').distinct()
             
             child_categories=child_category.objects.filter(p_category = p_c_id)
             values.update({'child_categories':child_categories})
             
             
        p=Paginator(products,15) #every page will show 2 records
        if not request.GET.get('page'):
            page_number='1'
        
        else:
            page_number=request.GET.get('page') #this will come in url
        ServiceDatafinal=p.get_page(page_number) #it will return the two records to display in page
        totalpage=ServiceDatafinal.paginator.num_pages #it will return how much pages can be create from compairing/dividing the number of records and number should display for one page
        values.update({
		'products':ServiceDatafinal,
        'lastpage':totalpage,
        'totalPagelist':[n+1 for n in range(totalpage)],
        'page_number':int(page_number)
        })
        
        return render(request,'products/productslist.html',values)
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
