import os

from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'pca_proyect.settings'
)

app = Celery('pca_proyect')

app.config_from_object(
    'django.conf:settings',
    namespace='CELERY'
)

app.autodiscover_tasks()