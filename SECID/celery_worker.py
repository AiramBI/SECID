from SECID import app, db  # Importa o app Flask e o banco de dados
from SECID.make_celery import make_celery  # Importa a função make_celery para configurar o Celery
from SECID.models import Medicao  # Importe o modelo Medicao diretamente
from SECID.utils import save_file  # Função para salvar arquivos, se aplicável

# Inicializa o Celery com o contexto do Flask
celery = make_celery(app)

@celery.task
def processar_medicao(sei, projeto_nome, numero_medicao, descricao, valor, data_inicial, data_final, documentos):
    try:
        # Cria uma nova instância de Medicao
        nova_medicao = Medicao(
            sei=sei,
            projeto_nome=projeto_nome,
            numero_medicao=numero_medicao,
            descricao=descricao,
            valor=valor,
            data_inicial=data_inicial,
            data_final=data_final
        )

        # Salva cada documento com base na chave (documento_1, documento_2, etc.)
        for doc_key, doc_data in documentos.items():
            if doc_data:
                # Usa save_file ou atribui diretamente conforme a lógica da sua aplicação
                setattr(nova_medicao, doc_key, save_file(doc_data))

        # Adiciona a nova medição ao banco de dados e faz commit
        db.session.add(nova_medicao)
        db.session.commit()
        return "Medição processada com sucesso!"
    
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao processar medição: {e}")
        return f"Erro ao processar medição: {e}"

