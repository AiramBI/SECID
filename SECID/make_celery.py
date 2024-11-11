# SECID/make_celery.py
from celery import Celery
import os

def make_celery(app):
    # Configura o Celery com o broker e backend definidos no Redis (ou conforme sua escolha)
    celery = Celery(
        app.import_name,
        backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
        broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    )
    celery.conf.update(app.config)

    # Define o contexto da aplicação para tarefas do Celery
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():  # Garante que as tarefas sejam executadas no contexto do Flask
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
