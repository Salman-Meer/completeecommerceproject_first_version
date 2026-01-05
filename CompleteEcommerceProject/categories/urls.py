
from django.contrib import admin
from django.urls import path
from .views import add_categories,category_data
urlpatterns = [

    path('categories/category_data/<int:id>',category_data,name='category_data'),
    path('admin/', admin.site.urls),
    

]
