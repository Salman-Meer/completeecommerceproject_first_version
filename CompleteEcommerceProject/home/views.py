from django.shortcuts import render
from django.http import request,HttpResponse
from products.models import product,gender
from django.core.paginator import Paginator
from categories.models import parent_category
from django.db.models import Q
from django.contrib import messages
# Create your views here.
def home(request):
    #try:
        if request.GET.get('page'):
            page_number=request.GET.get('page') #this will come in url
    
        else:
            page_number='1'

        data={}
        
        if request.GET.get('PriceRange') and not request.GET.get('gender'):
            
            priceRange=request.GET.get('PriceRange')
            if 'gender' in request.session:
                products=product.objects.filter(p_price__lte=priceRange,p_gender=request.session['gender']).order_by('-p_price')
            else:
                products=product.objects.filter(p_price__lte=priceRange).order_by('-p_price')
            priceRange=int(priceRange)
            data.update({'priceRange':priceRange})
            
        
        elif request.GET.get('PriceRange') and request.GET.get('gender'):
            
            priceRange=int(request.GET.get('PriceRange'))
            gender_id=int(request.GET.get('gender'))
            if(gender_id is -1):
           
                products=product.objects.filter(p_price__lte=priceRange).order_by('-p_price')
                if 'gender' in request.session:
                    del request.session['gender']
                
            
            else:
                products=product.objects.filter(p_price__lte=priceRange,p_gender=gender_id).order_by('-p_price')
                priceRange=int(priceRange)
                request.session['gender']=gender_id
            
            data.update({'priceRange':priceRange})
            
        elif(request.GET.get('gender') or 'gender' in request.session):
            if request.GET.get('gender'):
            
            
                gender_id=int(request.GET.get('gender'))

            else:
                gender_id=request.session['gender']
            if(gender_id is -1):
                
                products=product.objects.all()
                del request.session['gender']
            else:
                
                products=product.objects.filter(p_gender=gender_id)
                request.session['gender']=gender_id
        else:
            products=product.objects.all()
        
        p=Paginator(products,18) #every page will show 2 records
        ServiceDatafinal=p.get_page(page_number) #it will return the two records to display in page
        totalpage=ServiceDatafinal.paginator.num_pages #it will return how much pages can be create from compairing/dividing the number of records and number should display for one page
        #return HttpResponse(ServiceDatafinal)
        data.update({
        'page_no':int(page_number),
		'serviceData':ServiceDatafinal,
        'lastpage':totalpage,
        'totalPagelist':[n+1 for n in range(totalpage)]
	      })
  
    
        #return HttpResponse(products)
        categories=parent_category.objects.all()
        data.update({'categories':categories})
        genders=gender.objects.all()
        data.update({'genders':genders})
        min_price=0
        
        max_price=0
        productstemp=product.objects.all()
        
        for p in productstemp:
            if p.p_price>max_price:
                max_price=p.p_price
            elif p.p_price<min_price:
                min_price=p.p_price
            if(min_price is 0):
                min_price=p.p_price
        pricelist=[]
        
        gap=int((max_price-min_price)/14) # because we want to bring only 14 values to display in home page
        if gap is not 0:
            for k in range(min_price,max_price,gap):
                r=k%100
                s=100-r
                prce=k+s
                pricelist.append(prce)

            if pricelist:
                pricelist.pop()
            r=max_price%gap
            s=gap-r
            prce=max_price+s
            pricelist.append(prce)
            data.update({'max_price':max_price})
            data.update({'pricelist':pricelist})
        if 'search' in request.session:
            del request.session['search']
        request.session['path']=request.path
        return render(request,"home/home.html",data)
    #except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')


def check_session(request):
    return render(request,'home/check_session.html')
def search(request):
    #try:
        data={}
        if request.GET.get('page'):
            page_number=request.GET.get('page') #this will come in url
        else:
            page_number='1' 
        if request.method=="POST":
            search_query=request.POST['search']
            request.session['search']=search_query
        else:
            search_query=request.session['search']
        if request.GET.get('gender'):
            gender_id=int(request.GET.get('gender'))
            if gender_id is -1:
                if 'gender' in request.session:
                    del request.session['gender']
                products=product.objects.filter(Q(p_name__icontains=search_query)|Q(p_description__icontains=search_query)|Q(p_compony__icontains=search_query))
            else:
                products=product.objects.filter(Q(p_name__icontains=search_query)|Q(p_description__icontains=search_query)|Q(p_compony__icontains=search_query),p_gender=gender_id)
                request.session['gender']=gender_id
        else:
            products=product.objects.filter(Q(p_name__icontains=search_query)|Q(p_description__icontains=search_query)|Q(p_compony__icontains=search_query))
        p=Paginator(products,18) #every page will show 2 records
        ServiceDatafinal=p.get_page(page_number) #it will return the two records to display in page
        totalpage=ServiceDatafinal.paginator.num_pages #it will return how much pages can be create from compairing/dividing the number of records and number should display for one page
        #return HttpResponse(ServiceDatafinal)
        data.update({
            'page_no':int(page_number),
            'serviceData':ServiceDatafinal,
            'lastpage':totalpage,
            'totalPagelist':[n+1 for n in range(totalpage)]
            })
        categories=parent_category.objects.all()
        data.update({'categories':categories})
        genders=gender.objects.all()
        data.update({'genders':genders})
        #return HttpResponse(products)
        
        request.session['path']=request.path
        return render(request,"home/search.html",data)
    #except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')

