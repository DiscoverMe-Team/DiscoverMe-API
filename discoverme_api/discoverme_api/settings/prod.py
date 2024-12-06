from .base import *
import boto3
import json

DEBUG = False

ALLOWED_HOSTS = ['discovermeapp.com']

# Secrets Manager
def get_secret():
    secret_name = os.getenv('DISCOVERME_SECRET_NAME')
    if not secret_name:
        raise EnvironmentError('DISCOVERME_SECRET_NAME environment variable not set')
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

secret = get_secret()

# Database: PostgreSQL for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': secret['dbname'],
        'USER': secret['username'],
        'PASSWORD': secret['password'],
        'HOST': secret['host'],
        'PORT': secret['port'],
    }
}
