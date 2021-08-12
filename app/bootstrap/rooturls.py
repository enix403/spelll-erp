import os

import debug_toolbar
from django.http.response import HttpResponse

from django.urls import path, include
from django.shortcuts import redirect
from django.urls import reverse

from app.bootstrap.configmanager import ConfigManager
from app.middleware.exception_handler import ExceptionHandlerMiddleware

# These handlers only take effect when running with DEBUG=False (production)
handler400 = ExceptionHandlerMiddleware.delegate_error_handler_400
handler403 = ExceptionHandlerMiddleware.delegate_error_handler_403
handler404 = ExceptionHandlerMiddleware.delegate_error_handler_404
handler500 = ExceptionHandlerMiddleware.delegate_error_handler_500
handler_csrf_failure = ExceptionHandlerMiddleware.delegate_error_handler_csrf

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path("spl1/", include("app.routes")),
    path("", lambda _req: redirect(reverse('manage')))
]

if ConfigManager.get_bool('runtime.force_serve_static_files'):
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Well turns out it doesn't work in production as staticfiles_urlpatterns() checks for DEBUG being true
    # so TODO: replace this line with a (WhiteNoise) library which serves static files even with DEBUG turned off
    urlpatterns += staticfiles_urlpatterns()