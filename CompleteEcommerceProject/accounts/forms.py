from django import forms
import re
class formValidations(forms.ModelForm):

    
    def is_valid_username(name):
        pattern = r'^[a-zA-Z ]+$'
    
        if re.match(pattern, name):
            return True
        else:
            return False
        
    def password_match(password,confirm_password):
        if(password == confirm_password):
            return True
        else:
            return False
    def is_valid_mail(email):
        gmail_regex = r'^[a-zA-Z0-9._%+-]+@+[a-zA-Z]+mail\.com$'
    
        if re.match(gmail_regex, email):
            return True
        else:
            return False