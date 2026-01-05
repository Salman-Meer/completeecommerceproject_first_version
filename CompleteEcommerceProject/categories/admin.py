from django.contrib import admin
from .models import parent_category,child_category,gender
# Register your models here.
admin.site.register(parent_category)
admin.site.register(child_category)
admin.site.register(gender)



