from django.http import HttpRequest, QueryDict
from django.shortcuts import redirect

def get_bag(req: HttpRequest, method = None) -> QueryDict:
    if method == None:
        method = req.method.upper()
    
    if method == 'POST':
        return req.POST
    elif method == 'GET':
        return req.GET
    
    return req.GET

def redirect_back(req: HttpRequest, default_url='/'):
    return redirect(req.META.get('HTTP_REFERER', default_url))
