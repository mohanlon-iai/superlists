from superlists.settings import *
from decouple import config

# ALLOWED_HOSTS updated with another default value for DC/OS containers
ALLOWED_HOSTS.append(config('HOST', default=''))

# You can add/update/delete settings for the project to run in DC/OS as needed here. It's up to you how you do this.