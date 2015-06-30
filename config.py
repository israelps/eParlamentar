import os

PROPAGATE_EXCEPTIONS = True
DEBUG = True
SQLALCHEMY_ECHO = False
DEBUG = True

if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL'):
    SQLALCHEMY_DATABASE_URI = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL')
else:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/eparlamentar'
