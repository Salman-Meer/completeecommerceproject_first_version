from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.hashers import make_password,check_password
from django.core.mail import send_mail, BadHeaderError

from .forms import formValidations
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from add_to_card.models import Card
from django.http import HttpRequest,request
def signup(request):
    try:
        errors={}
        values={}
        if(request.method == "POST"):
            firstname=request.POST['firstname']
            email=request.POST['email']
            password=request.POST['password']
            confirm_password=request.POST['confirm_password']
            if(formValidations.is_valid_username(firstname)==False):
                errors.update({'username':'invalid username ,please enter only characters in user name'})
            if formValidations.is_valid_mail(email) == False:
                errors.update({'email':'please input a valid email'})
            if( formValidations.password_match(password,confirm_password) == False ):
                errors.update({'password':'passwords did not not match'})
       
            if(errors):
                values.update({'username':firstname})
                values.update({'email':email})
                values.update({'password':password})
                values.update({'errors':errors})
                return render(request,'accounts/singup.html',values)
            else:
            
                if not User.objects.filter(username=email).exists():
                    
                        #send_email_to_client()
                # If email sent successfully, save user to database
                        user = User(username=email, email=email,first_name=firstname)
                
                        user.set_password(password)  # Hash the password
                        user.save()
                        login(request, user)
                        request.session['NumberOfCartItems']=0

                          # Automatically log in the user after signup
                        messages.success(request, f"you have signup successfully  {user.first_name}")
                        #return HttpResponse("you have signup successfully")
                        previous_url = request.session.get('previous_url')
                        return redirect(request.session['path'])
                    
                # ---------------------dynamic path will come
                else:
                    errors.update({'email_exist':'this email is already exist'})
       
                values.update({'errors':errors})
                return render(request,'accounts/singup.html',values)
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')

        

    
        

    return render(request,'accounts/singup.html')
def signin(request):
#    try:
        if request.method == "POST":
            username = request.POST['email']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
            # Log in the user and redirect to home
                login(request, user)
                CartItems=Card.objects.filter(c_user=request.user)
                items=0
                request.session['NumberOfCartItems']=0
                for c in CartItems:
                    items=items+c.quantity

                request.session['NumberOfCartItems']=items
                
                messages.success(request, f"you have loggined successfully  {user.first_name}")
                #return HttpResponse("you have signup successfully")

                return redirect(request.session['path'])
            else:
                messages.warning(request,"you intered incorrect username password")
        return render(request,'accounts/signin.html')

 #   except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')


@login_required
def logout_view(request):
    try:
        logout(request)
        
        messages.success(request, "You have been logged out successfully.")
        request.session['NumberOfCartItems']=None
        previous_url = request.session.get('previous_url', '/')
        
        return redirect(previous_url)
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
