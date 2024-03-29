from collections import OrderedDict
from os import getenv
import logging


MONGODB_HOST = getenv("MONGODB_HOST", "127.0.0.1")
MONGODB_PORT = int(getenv("MONGODB_PORT", 27017))
MONGODB_DB = getenv("MONGODB_DB", "monitor_provider")
MONGODB_USER = getenv("MONGODB_USER", None)
MONGODB_PWD = getenv("MONGODB_PWD", None)
MONGODB_ENDPOINT = getenv("DBAAS_MONGODB_ENDPOINT", None)

MONGODB_PARAMS = {'document_class': OrderedDict}
if MONGODB_ENDPOINT:
    MONGODB_PARAMS["host"] = MONGODB_ENDPOINT
else:
    MONGODB_PARAMS['host'] = MONGODB_HOST
    MONGODB_PARAMS['port'] = MONGODB_PORT
    MONGODB_PARAMS['username'] = MONGODB_USER
    MONGODB_PARAMS['password'] = MONGODB_PWD

APP_USERNAME = getenv("APP_USERNAME", None)
APP_PASSWORD = getenv("APP_PASSWORD", None)

LOGGING_LEVEL = int(getenv('LOGGING_LEVEL', logging.INFO))

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
# Flask Restplus validate model via serializer default = False
RESTPLUS_VALIDATE = False
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False
