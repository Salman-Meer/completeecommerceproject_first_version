from django.shortcuts import render,HttpResponse
from django.core.paginator import Paginator
from .models import child_category,parent_category
from products.models import product,gender
from django.contrib import messages

def add_categories(request):
    return render(request,'categories/add_categories.html')
# Create your views here.
def category_data(request,id):
    try:
        values={}

        if request.GET.get('page'):
            page_number=request.GET.get('page') #this will come in url
        
        else:
            page_number='1'

        child_categories=child_category.objects.filter(p_category=id)
        l=[]
        for i in child_categories:
            l.append(i.c_c_id)
        products=product.objects.filter(p_child_category__in = l).all()

        if request.GET.get('PriceRange') and not request.GET.get('gender'):
            category_id=id
            priceRange=int(request.GET.get('PriceRange'))
            p_category_obj=parent_category.objects.get(p_c_id=category_id)
            c_category_obj=child_category.objects.filter(p_category=p_category_obj)
            l=[]
                
            if 'gender' in request.session:
                    
                for i in c_category_obj:
                    l.append(i.c_c_id)
                    gender_id=gender.objects.get(g_id=request.session['gender'])
                    products=product.objects.filter(p_child_category__in = l,p_price__lte=priceRange,p_gender=gender_id).order_by('-p_price')
                
            else:
                for i in c_category_obj:
                    l.append(i.c_c_id)
                    products=product.objects.filter(p_child_category__in = l,p_price__lte=priceRange).order_by('-p_price')

            
            values.update({'priceRange':priceRange})
                
                
        elif request.GET.get('PriceRange') and request.GET.get('gender'):
            
            category_id=id
            gender_id=int(request.GET.get('gender'))
            priceRange=int(request.GET.get('PriceRange'))
            p_category_obj=parent_category.objects.get(p_c_id=category_id)
            c_category_obj=child_category.objects.filter(p_category=p_category_obj)
            l=[]
            if gender_id is -1:
                for i in c_category_obj:
                    l.append(i.c_c_id)
                    products=product.objects.filter(p_child_category__in = l,p_price__lte=priceRange).order_by('-p_price')
                if 'gender' in request.session:
                    del request.session['gender']
            else:   
                for i in c_category_obj:
                    l.append(i.c_c_id)
                    products=product.objects.filter(p_child_category__in = l,p_price__lte=priceRange,p_gender=gender_id).order_by('-p_price')
            
            #return HttpResponse('ok now you can work')
                request.session['gender']=gender_id
            values.update({'priceRange':priceRange})
                
        elif(request.GET.get('gender') or 'gender' in request.session):
            category_id=id
            if request.GET.get('gender'):
                gender_id=int(request.GET.get('gender'))
                if(gender_id is -1):
                    if 'gender' in request.session:
                        del request.session['gender']
                
                    gender_id=int(request.GET.get('gender'))
                    p_category_obj=parent_category.objects.get(p_c_id=category_id)
                    c_category_obj=child_category.objects.filter(p_category=p_category_obj)
                    l=[]
                    for i in c_category_obj:
                        l.append(i.c_c_id)
                        products=product.objects.filter(p_child_category__in = l)
            
                else:
                
                    request.session['gender']=gender_id
                    p_category_obj=parent_category.objects.get(p_c_id=category_id)
                    c_category_obj=child_category.objects.filter(p_category=p_category_obj)
                    l=[]
                    for i in c_category_obj:
                        l.append(i.c_c_id)
                        products=product.objects.filter(p_child_category__in = l,p_gender=gender_id)
            
            else:
                p_category_obj=parent_category.objects.get(p_c_id=id)
                c_category_obj=child_category.objects.filter(p_category=p_category_obj)
                l=[]
                for i in c_category_obj:
                    l.append(i.c_c_id)
                    products=product.objects.filter(p_child_category__in = l,p_gender=request.session['gender'])
            
            
            #return HttpResponse('ok now you can work')
            
        paginator = Paginator(products, 15)
        ServiceDatafinal = paginator.get_page(page_number)
        totalpage=ServiceDatafinal.paginator.num_pages
        values.update({
            'page_no':int(page_number),
            'products':ServiceDatafinal,
            'lastpage':totalpage,
            'totalPagelist':[n+1 for n in range(totalpage)]
            })

        categories=parent_category.objects.all()
        values.update({'categories':categories})
        values.update({'category_id':id})
        genders=gender.objects.all()
        values.update({'genders':genders})
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
            values.update({'max_price':max_price})
            values.update({'pricelist':pricelist})
            

        request.session['path']=request.path        
        return render(request,'home/category_wise_data.html',values)
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')

