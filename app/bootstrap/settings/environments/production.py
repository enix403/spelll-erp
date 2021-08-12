from app.utils import resolve_root

from app.bootstrap.settings.components.base import (
    STATICFILES_DIRS
)

DEBUG = False
HTML_MINIFY = True
CSRF_FAILURE_VIEW = 'app.bootstrap.rooturls.handler_csrf_failure'

st_build_dir = resolve_root('app/frontend/reactapp/build/static')
STATICFILES_DIRS.extend(st_build_dir)
