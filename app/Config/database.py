import os
from django.conf import settings
from django.db import connections

# Load the database URI from environment variables
PGDB_URI = os.getenv('PGDB_URI')

# Print the database URI for debugging purposes
print("PGDB_URI:", PGDB_URI)

# Configure the database settings for Django
# You may need to parse PGDB_URI to extract the database name, user, password, host, and port
# For this example, let's assume the URI format is: postgres://USER:PASSWORD@HOST:PORT/DBNAME

if PGDB_URI:
    from urllib.parse import urlparse

    # Parse the database URI
    result = urlparse(PGDB_URI)
    db_name = result.path[1:]  # Remove leading slash
    db_user = result.username
    db_password = result.password
    db_host = result.hostname
    db_port = result.port

    # Set the Django database settings
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': db_host,
        'PORT': db_port,
    }

# Create a database connection
db_connection = connections['default']
