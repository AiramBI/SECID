from SECID import create_app  # Função de fábrica que cria o app
from SECID.make_celery import make_celery  # Função make_celery para configurar o Celery

app = create_app()  # Cria uma nova instância do app Flask
celery = make_celery(app)  # Configura o Celery com o contexto do app
