import os
host_name = os.popen('hostname -I').read().strip() if os.sys.platform != "win32" else '200.200.200.1'

if host_name.startswith("10.0"):
    # from .local_settings import *
    from .server_settings import *
else:
    from .local_settings import *
