from django.contrib.auth.models import User
import time
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpRequest,request
from django.shortcuts import render,HttpResponse
from django.conf import settings

def send_email_to_client():
    try:
        subject='Welcome to Our Website!'  # Subject
        message='Thank you for signing up!'  # Message
        from_email=settings.EMAIL_HOST_USER  # From email salmanmeergabbar@gmail.com
        recipient_client=['sulligabbar@gmail.com']  # To email
        send_mail(subject,message,from_email,recipient_client)
    
    except BadHeaderError:
        return HttpResponse(' Unexisted email header.')
    except Exception:
        return HttpResponse('wrong email')
