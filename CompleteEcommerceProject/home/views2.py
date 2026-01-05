
from django.http import HttpResponse,cookie
def set_cookie_view(request):
    response=HttpResponse('Cookie set ! ')
    response.set_cookie('user','salman')
    return response

def delete_cookie_view(request):
    response=HttpResponse('Cookie deleted ! ')
    response.delete_cookie('user')
    return response
def show_cookie_view(request):
    cookie_value=request.COOKIES.get('user')
    return HttpResponse(f'Cookie value is  {cookie_value} ')
    

