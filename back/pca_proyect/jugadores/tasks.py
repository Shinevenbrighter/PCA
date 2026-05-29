from celery import shared_task

from .services import verificar_modelo

@shared_task
def verificar_modelo_task():
    print("cerficando si existe modelo")
    verificar_modelo()