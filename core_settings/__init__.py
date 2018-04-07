import os
host_name = os.popen('hostname -I').read().strip()

if host_name.startswith("10.0"):
    from .server_settings import *
else:
    from .local_settings import *
