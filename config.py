import os
PROPAGATE_EXCEPTIONS = True
DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ['OPENSHIFT_POSTGRESQL_DB_URL']
SQLALCHEMY_ECHO = False

DEBUG = True