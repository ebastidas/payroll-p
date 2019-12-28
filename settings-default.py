import os

from api.domain import DOMAIN

# mongo connection string
# see https://docs.mongodb.com/manual/reference/connection-string/
MONGO_URI = os.environ.get('PERS_PAYROLL_DB_HOST')
MONGO_DBNAME = os.environ.get('PERS_PAYROLL_DB_NAME')

# On IBM Cloud Cloud Foundry, set the ssl_ca_certs
if 'PORT' in os.environ:
    # For production, connect to IBM Databases for Mongo
    ca_cert_filepath = os.path.abspath("config/db/creds/CA.pem")
    MONGO_OPTIONS = {'ssl': True, 'ssl_ca_certs': ca_cert_filepath}
else:
    # For local dev, connect to local mongo
    pass


# api will be rendered to /api/<endpoint>
URL_PREFIX = 'api'

# Will be used in conjunction with URL_PREFIX to build API endpoints,
# eg. if API_VERSION='v1' will be rendered to /v1/<endpoint>
# eg. if URL_PREFIX='api', and API_VERSION='v1' will be rendered to api/v1/<endpoint>
API_VERSION = 'v1'

# methods allowed at the resource (collection) endpoint
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# methods allowed at the item (document) endpoint
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

# CORS support
# Allow access from all domains (javascript/web clients)
# see https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
X_DOMAINS = '*'
X_HEADERS = ['content-type', 'if-match',
             'authorization', 'cache-control', 'expires']

# We also disable endpoint caching as we don't want client apps to cache any data.
CACHE_CONTROL = 'max-age=1,must-revalidate'
CACHE_EXPIRES = 0

# A Python date format used to parse and render datetime values.
# DATE_FORMAT = 'a, %d %b %Y %H:%M:%S GMT' # Eve defaults format, to the RFC1123, ex “Tue, 02 Apr 2013 10:29:13 GMT”
DATE_FORMAT = '%Y%m%d'

# True to enable concurrency control, False otherwise. Defaults to True.
#IF_MATCH = True

# True to always enforce concurrency control when it is enabled, False otherwise. Defaults to True.
#ENFORCE_IF_MATCH = False
