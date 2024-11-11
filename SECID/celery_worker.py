# SECID/celery_worker.py
from SECID.celery_app import celery, app  # Importe a instância de Celery e o app configurado
from SECID import db  # Importa db para uso no contexto do app já inicializado
from SECID.models import Medicao  # Importe o modelo Medicao
from SECID.utils import save_file  # Função para salvar arquivos

@celery.task
def processar_medicao(sei, projeto_nome, numero_medicao, descricao, valor, data_inicial, data_final, documentos):
    try:
        # Cria a nova medição
        nova_medicao = Medicao(
            sei=sei,
            projeto_nome=projeto_nome,
            numero_medicao=numero_medicao,
            descricao=descricao,
            valor=valor,
            data_inicial=data_inicial,
            data_final=data_final
        )

        # Salva cada documento individualmente
        for doc_key, doc_data in documentos.items():
            if doc_data:
                # Usa save_file ou atribui diretamente, conforme a lógica da sua aplicação
                setattr(nova_medicao, doc_key, save_file(doc_data))

        db.session.add(nova_medicao)
        db.session.commit()
        return "Medição processada com sucesso!"
    
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao processar medição: {e}")
        return f"Erro ao processar medição: {e}"

