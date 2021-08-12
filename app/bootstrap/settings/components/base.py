from app.utils import resolve_root
from app.bootstrap.configmanager import ConfigManager

SECRET_KEY = ConfigManager.get('main.secret_key')
ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'app.bootstrap.rooturls'
WSGI_APPLICATION = 'app.bootstrap.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'rest_framework',
    'app.appconfig.AppConfig',
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = False
USE_L10N = False
USE_TZ = False

MESSAGE_LEVEL = 0 # display all messages (above the given level, and 0 is the min level)

SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = resolve_root('storage/sessions')

STATIC_URL = '/static/'
STATIC_ROOT = resolve_root('storage/assets') + '/'  # target for collectstatic ( the ending '/' is required )

# places to look for static assets
STATICFILES_DIRS = [
    resolve_root('app/frontend/static'),
]

INTERNAL_IPS = [
    '*'
]
