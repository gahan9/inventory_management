"""
MySQL database & settings for server
"""
from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'mysql.conf'),
        },
    }
}
