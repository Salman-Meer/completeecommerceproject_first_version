from . import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404
#from .views import custom_404_view  # Import from wherever you placed it

#handler404 = custom_404_view
urlpatterns = [
    path('',include('home.urls')),
    path('categories/',include('categories.urls')),
    path('accounts/',include('accounts.urls')),
    path('products/',include('products.urls')),
    path('cart/',include('add_to_card.urls')),
    #path('check/',include('home.urls')),
    #path('search/',include('home.urls')),
    #path('signup/',include('accounts.urls')),
    #path('logout/',include('accounts.urls')),
    #path('products/update_product/<slug>/',include('products.urls')),
    #path('products/delete_products/<slug>',include('products.urls')),
    
    
    #path('products/add_products',include('products.urls')),
    #path('products/images',include('products.urls')),
    #path('products/delete_images/<id>',include('products.urls')),
    #path('products/',include('products.urls')),
    #path('delete_card/<int:id>',include('add_to_card.urls')),

    path('admin/', admin.site.urls),
    path('social_accounts/', include('allauth.urls')),
    path('whatsapp/', include('whatsapp.urls')),
    

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)#here may be +=
