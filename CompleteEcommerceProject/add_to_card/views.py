from django.shortcuts import render,HttpResponse,redirect
from products.models import product,ColorVariant,SizeVariant
from .models import Card
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.
def cart(request):
    try:
        values={}
    
        if(request.GET.get('decreaseQuantity')):
            id=request.GET.get('decreaseQuantity')
            cartObj=Card.objects.get(c_id=id)
            if cartObj.quantity>1:
                cartObj.quantity=cartObj.quantity-1
                cartObj.save()
                request.session['NumberOfCartItems']=request.session['NumberOfCartItems']-1
            
            
        if(request.GET.get('increaseQuantity')):
            id=request.GET.get('increaseQuantity')
            cartObj=Card.objects.get(c_id=id)
            cartObj.quantity=cartObj.quantity+1
            cartObj.save()
            request.session['NumberOfCartItems']=request.session['NumberOfCartItems']+1
        
        if(request.method == "POST"):
            if(request.user.id):
                
                color= ColorVariant.objects.get(color_name=request.POST['color'])
                size=SizeVariant.objects.get(size_name=request.POST['size'])
                slug=request.POST['slug']
                quantity=int(request.POST['quantity'])
                product_obj=product.objects.get(slug=slug)
                #user_obj is instance of user table and request.user is also instance
                if(Card.objects.filter(c_size_variant=size,c_color_variant=color,c_user=request.user,c_product=product_obj).exists()):
                    add_card=Card.objects.get(c_size_variant=size,c_color_variant=color,c_user=request.user,c_product=product_obj)
                    add_card.quantity=add_card.quantity+quantity
                    add_card.save()
                    request.session['NumberOfCartItems']=request.session['NumberOfCartItems']+quantity
                else: 
                    add_card=Card(c_size_variant=size,c_color_variant=color,c_user=request.user,c_product=product_obj,quantity=quantity)
                    add_card.save()
                    request.session['NumberOfCartItems']=request.session['NumberOfCartItems']+quantity
                    messages.success(request,'Item added in card successfully')
                    
            else:

                return redirect("siginin")
        #product_object=product.objects.get()
        card_data=Card.objects.filter(c_user=request.user)
    
        values.update({'card_data':card_data})
        total=0
        for productss in card_data:
            price=productss.c_product.p_price*productss.quantity
            total=total+price
        values.update({'total':total})
        return render(request,'addtocart/addtocart.html',values)
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')

def delete_card(request,id):
    try:
        record = get_object_or_404(Card,c_id=id)
        quantity=record.quantity
        request.session['NumberOfCartItems']=request.session['NumberOfCartItems']-quantity
        record.delete()
        messages.warning(request,'data deleted successfully')
        return redirect('AtToCard')  
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
