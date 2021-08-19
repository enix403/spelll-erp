import os
import re

from django.urls import path, re_path, include, reverse
from django.shortcuts import redirect
# from django.conf.urls import url

from app.bootstrap.configmanager import ConfigManager
from app.middleware.exception_handler import ExceptionHandlerMiddleware

# These handlers only take effect when running with DEBUG=False (production)
handler400 = ExceptionHandlerMiddleware.delegate_error_handler_400
handler403 = ExceptionHandlerMiddleware.delegate_error_handler_403
handler404 = ExceptionHandlerMiddleware.delegate_error_handler_404
handler500 = ExceptionHandlerMiddleware.delegate_error_handler_500
handler_csrf_failure = ExceptionHandlerMiddleware.delegate_error_handler_csrf

urlpatterns = [
    path("", lambda _req: redirect(reverse('manage'))),
    path("spl1/", include("app.routes")),
]

if ConfigManager.get_bool('runtime.debug'):
    try:
        # urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
        import debug_toolbar
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    except:
        # TODO: log error
        pass
else:
    # If we are in debug mode then django automatically serves static files
    # When debug mode is turned off and force_serve_static_files is True then
    # we explicitly serve static files here 
    if ConfigManager.get_bool('runtime.force_serve_static_files'):
        # from django.contrib.staticfiles.urls import staticfiles_urlpatterns
        # urlpatterns += staticfiles_urlpatterns()
        
        ## Well turns out the above code doesn't work in production as staticfiles_urlpatterns() checks for DEBUG being true
        ## so TODO: replace this line with a (WhiteNoise) library which serves static files even with DEBUG turned off
        ## Meanwhile the following customized staticfiles_urlpatterns() hack should work

        from django.conf import settings
        from django.contrib.staticfiles.views import serve
        prefix = settings.STATIC_URL
        urlpatterns += [re_path(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), serve)]





