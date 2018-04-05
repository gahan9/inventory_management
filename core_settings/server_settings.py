"""
MySQL database & settings for server
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.mysql',
        'NAME'    : 'tony221b$default',
        'USER'    : 'tony221b',
        'PASSWORD': 'r@123456',
        'HOST'    : 'tony221b.mysql.pythonanywhere-services.com',
        # 'URI'     : 'tony221b.mysql.pythonanywhere-services.com',
        # 'PORT'    : '5432',
    }
}

