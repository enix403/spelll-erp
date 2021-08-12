from app.bootstrap.configmanager import ConfigManager

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': ConfigManager.get('db.user'),
        'NAME': ConfigManager.get('db.name'),
        'PASSWORD': ConfigManager.get('db.pass'),
        'HOST': ConfigManager.get('db.host'),
        'PORT': ConfigManager.get('db.port'),
    }
}

migration_subfolder = ConfigManager.get('main.migration_branch_name')
if not migration_subfolder:
    migration_subfolder = 'unnamed'

MIGRATION_MODULES = {'app': f'migrations.{migration_subfolder}'}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'