from celery import Celery
from SECID import app, database  # Importa o app Flask e o banco de dados

def make_celery(app):
    # Configura o Celery com o broker e o backend definidos no Redis (ou conforme sua escolha)
    celery = Celery(
        app.import_name,
        backend=app.config.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
        broker=app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    )
    celery.conf.update(app.config)

    # Defina o contexto da aplicação para tarefas do Celery
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():  # Garante que as tarefas sejam executadas no contexto do Flask
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# Inicializa o Celery com o contexto do Flask
celery = make_celery(app)
