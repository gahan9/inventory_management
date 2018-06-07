import os
host_name = os.popen('hostname -I').read().strip() if os.sys.platform != "win32" else '200.200.200.1'

if host_name.startswith("10.0"):
    # from .local_settings import *
    from .server_settings import *
elif host_name.startswith("46.101.17.77"):
    from .settings import *

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': os.path.join(BASE_DIR, 'mysql_digital_ocean.conf'),
            },
        }
    }
else:
    from .local_settings import *
