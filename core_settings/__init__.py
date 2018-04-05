import os
from . import local_settings
from . import server_settings
host_name = os.popen('hostname -I').read().strip()

if host_name.startswith("10.0"):
    settings = server_settings
else:
    settings = local_settings
