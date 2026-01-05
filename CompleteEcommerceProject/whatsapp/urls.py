


from django.urls import path
from .views import send_whatsapp_message
urlpatterns = [
    
    path('',send_whatsapp_message,name='whatsapp'),
   
    

]
