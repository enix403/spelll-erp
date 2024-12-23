import os
from app.utils import resolve_root

from app.bootstrap.settings.components.base import (
    INSTALLED_APPS,
    STATICFILES_DIRS
)
from app.bootstrap.settings.components.middleware import (
    MIDDLEWARE
)


DEBUG = True
# DEBUG = False
# CSRF_FAILURE_VIEW = 'app.bootstrap.rooturls.handler_csrf_failure'

INSTALLED_APPS.extend([
    'debug_toolbar',
    'django_extensions',
])

MIDDLEWARE.extend([
    'debug_toolbar.middleware.DebugToolbarMiddleware',
])

TEMPLATE_DEBUG = True

SHELL_PLUS = "plain"
HTML_MINIFY = True
X_ENABLE_DEBUGBAR = True
# X_ENABLE_DEBUGBAR = False

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda _: X_ENABLE_DEBUGBAR,
}

st_dist_dir = resolve_root('app/frontend/reactapp/dist/static')
st_build_dir = resolve_root('app/frontend/reactapp/build/static')
STATICFILES_DIRS.extend(tuple(d for d in [st_build_dir, st_dist_dir] if os.path.isdir(d)))

