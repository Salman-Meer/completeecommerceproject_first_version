
from django.urls import path
from .views import home,check_session,search
from .views2 import set_cookie_view,delete_cookie_view,show_cookie_view
urlpatterns = [
    path('',home,name='home'),
    path('home/',home,name='home'),
    path('check/',check_session,name='check_session'),
    path('search/',search,name='search'),
    path('setcookies/',set_cookie_view),
    path('deletecookies/',delete_cookie_view),
    path('showcookies/',show_cookie_view),
    
    
    
]
