from celery import Celery
from SECID import app, database  # Importa o app Flask e o banco de dados
from .celery_worker import celery
from your_flask_app import db
from your_flask_app.models import Medicao


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

@celery.task
def processar_medicao(sei, projeto_nome, numero_medicao, descricao, valor, data_inicial, data_final, documentos):
    try:
        # Lógica para processar a medição e salvar no banco de dados
        nova_medicao = Medicao(
            sei=sei,
            projeto_nome=projeto_nome,
            numero_medicao=numero_medicao,
            descricao=descricao,
            valor=valor,
            data_inicial=data_inicial,
            data_final=data_final
        )

        for doc_key, doc_data in documentos.items():
            # Salve cada documento com base na chave (documento_1, documento_2, etc.)
            setattr(nova_medicao, doc_key, doc_data)

        db.session.add(nova_medicao)
        db.session.commit()
    except Exception as e:
        # Lide com erros
        db.session.rollback()
        print(f"Erro ao processar medição: {e}")
