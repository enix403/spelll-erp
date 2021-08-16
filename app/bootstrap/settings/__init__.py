from split_settings.tools import include
from app.bootstrap.configmanager import ConfigManager

ConfigManager.load_config()
environment = 'development' if ConfigManager.get_bool('runtime.debug') else 'production'

setting_files = [
    'components/base.py',
    'components/db.py',
    'components/monkeypatchmigrations.py',
    'components/middleware.py',
    'components/templates.py',
    
    f'environments/{environment}.py'
]

include(*setting_files)
