from django.contrib import admin
from.models import product,product_image,ColorVariant,SizeVariant
admin.site.register(product)
admin.site.register(product_image)
admin.site.register(ColorVariant)
admin.site.register(SizeVariant)

class ProductAdmin(admin.ModelAdmin):
    list_display=['p_id','p_name','p_price','p_compony','colors','size']
# Register your models here.
