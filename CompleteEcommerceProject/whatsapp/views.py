from django.shortcuts import render
from django.conf import settings
from twilio.rest import Client
from django.contrib import messages

def send_whatsapp_message(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        message = request.POST.get('message')
        
        client = Client(settings.WHATSAPP_ACCOUNT_SID, settings.WHATSAPP_AUTH_TOKEN)
        
        try:
            message = client.messages.create(
                body=message,
                from_=settings.WHATSAPP_NUMBER,
                to=f'whatsapp:{phone_number}'
            )
            messages.success(request, "message sent successfully ")
                        
            return render(request,'whatsapp/whatsapp.html')
        except Exception as e:
            messages.warning(request, "message couldnot sent ")
                        
            return render(request,'whatsapp/whatsapp.html')
    return render(request,'whatsapp/whatsapp.html')
          