from celery import Celery
from SECID import create_app, db  # Importe seu app Flask e o banco de dados
import os

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        broker=os.getenv("REDIS_URL", "redis://localhost:6379/0")
    )
    celery.conf.update(app.config)
    return celery

app = create_app()  # Substitua por como você cria sua aplicação Flask
celery = make_celery(app)
