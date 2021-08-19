from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from app.exceptions import (
    ApiException,
    UIException,
    HttpException,

    HttpExceptionNotFound,
    HttpExceptionBadRequest,
    HttpExceptionPermissionDenied,
    HttpExceptionCSRFFailure,
    HttpExceptionInternalServerError
)

from app.utils.request_handling import redirect_back

class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, req):
        return self.get_response(req)

    def process_exception(self, request: HttpRequest, exp: Exception):

        if isinstance(exp, ApiException):
            response = JsonResponse({
                'type': 'error',
                'payload': exp.data,
                'message': exp.msg 
            }, status=exp.code)

            return response

        # Note the ordering of if-elif statements. ApiException itself is a subclass of HttpException
        elif isinstance(exp, HttpException):
            return self._process_exception_generic(request, exp)

        elif isinstance(exp, UIException):
            messages.error(request, exp.user_msg)

            if exp.route_name is None:
                # Note the exp.query_params are ignored here (i.e if redirecting back) because if you
                # are redirecting 'back' in the first place, you do not know where it will redirect to
                # and hence cannot figure out in advance the suitable query params to send  
                return redirect_back(request)
            else:
                # exp.query_params includes the trailing question mark "?" if it is not empty
                return redirect(reverse(exp.route_name, args=exp.route_args) + exp.query_params)

        return None

    @classmethod
    def _process_exception_generic(cls, request: HttpRequest, exp: HttpException):
        return render(request, 'main/errors/generic.html', {
            "code": exp.code,
            "msg": exp.msg
        }, status=exp.code)

    @classmethod
    def delegate_error_handler_400(cls, request, *args, **kwargs):
        return cls._process_exception_generic(request, HttpExceptionBadRequest())

    @classmethod
    def delegate_error_handler_403(cls, request, *args, **kwargs):
        return cls._process_exception_generic(request, HttpExceptionPermissionDenied())

    @classmethod
    def delegate_error_handler_404(cls, request, *args, **kwargs):
        return cls._process_exception_generic(request, HttpExceptionNotFound())

    @classmethod
    def delegate_error_handler_500(cls, request, *args, **kwargs):
        return cls._process_exception_generic(request, HttpExceptionInternalServerError())

    @classmethod
    def delegate_error_handler_csrf(cls, request, *args, **kwargs):
        return cls._process_exception_generic(request, HttpExceptionCSRFFailure())

