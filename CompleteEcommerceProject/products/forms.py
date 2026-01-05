from django import forms
from .models import product,product_image
import re
class formValidations(forms.ModelForm):

    def is_valid_image(image):
        image_partition=image.split('.')
        image_extension=image_partition[-1]
        allowed_formates=['jpg','jpeg','png']
        is_valid=0
        for i in allowed_formates:
            if(i==image_extension):
                
                is_valid=1
                return is_valid

            return is_valid
            

    def is_valid_username(name):
        pattern = r'^[a-zA-Z0-9 ]+$'
    
        if re.match(pattern, name):
            return True
        else:
            return False
        
    def is_valid_price(price):
        try:
            price=float(price)
            if(isinstance(price, int) or isinstance(price,float)):
                return True 
            else:
                return False
        except:
            return False
