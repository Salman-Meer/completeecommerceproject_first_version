
from django.contrib import admin
from django.urls import path
from .views import add_products
from .views2 import get_products,product_list
from .views3 import update_products,delete_products
from .views4 import images,delete_images
urlpatterns = [
    path('manipulations',product_list ,name='manipulation'),
    path('update_product/<slug>/',update_products ,name='update_product'),
    
    path('delete_products/<slug>',delete_products ,name='delete_products'),
    path('add_products',add_products ,name='add_products'),
    path('images/<slug>',images,name="images"),
    path('delete_images/<id>',delete_images,name="delete_images"),
    path('<slug>/',get_products,name="products_detail"),
    path('admin/', admin.site.urls),
]
