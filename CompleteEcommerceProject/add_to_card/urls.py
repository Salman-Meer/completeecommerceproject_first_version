from django.urls import path
from .views import cart,delete_card
urlpatterns = [
    
    path('',cart,name='AtToCard'),
    path('delete_card/<int:id>',delete_card,name='delete_card'),
    

]
