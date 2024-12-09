from SECID import celery
from SECID.models import Medicao, Medicao_resumida
from SECID.routes import save_file

@celery.task
def process_form_data(data, files):
    # Processar os dados do formulário e os arquivos
    for file in files:
        # Simular upload ou processamento
        print(f"Processando arquivo: {file}")
    return "Tarefa concluída!"


@celery.task
def process_form_data(data, files):
    try:
        # Salvar arquivos individualmente
        saved_files = {
            key: save_file(file) if file else None
            for key, file in files.items()
        }

        # Criar instâncias do banco de dados
        medicao1 = Medicao(
            sei=data['sei'],
            projeto_nome=data['projeto_nome'],
            numero_medicao=data['numero_medicao'],
            letra_medicao=data['letra_medicao'],
            descricao=data['descricao'],
            valor=data['valor'],
            reajustamento=data['reajustamento'],
            data_inicial=data['data_inicial'],
            data_final=data['data_final'],
            documento_1=saved_files.get("documento_1"),
            documento_2=saved_files.get("documento_2"),
            documento_3=saved_files.get("documento_3"),
            documento_3_1=saved_files.get("documento_3_1"),
            documento_4=saved_files.get("documento_4"),
            documento_5=saved_files.get("documento_5"),
            documento_6=saved_files.get("documento_6"),
            documento_7=saved_files.get("documento_7"),
            documento_8=saved_files.get("documento_8"),
            documento_9=saved_files.get("documento_9"),
            documento_10=saved_files.get("documento_10"),
            documento_10_1=saved_files.get("documento_10_1"),
            documento_11=saved_files.get("documento_11"),
            documento_12=saved_files.get("documento_12"),
            documento_13=saved_files.get("documento_13"),
            documento_14=saved_files.get("documento_14"),
            documento_15=saved_files.get("documento_15"),
            documento_16=saved_files.get("documento_16"),
            documento_17=saved_files.get("documento_17"),
            documento_18=saved_files.get("documento_18"),
            documento_19=saved_files.get("documento_19"),
            documento_15_1=saved_files.get("documento_15_1"),
            documento_15_2=saved_files.get("documento_15_2"),
            documento_15_3=saved_files.get("documento_15_3"),
            documento_15_4=saved_files.get("documento_15_4"),
            documento_15_5=saved_files.get("documento_15_5"),
        )

        medicao_resumida = Medicao_resumida(
            obra=data['projeto_nome'],
            data_inicio_medicao=data['data_inicial'],
            data_fim_medicao=data['data_final'],
            numero_medicao=data['numero_medicao'],
            valor_medicao=data['valor'],
            letra_medicao=data['letra_medicao'],
            reajustamento=data['reajustamento'],
        )

        # Salvar no banco de dados
        database.session.add(medicao1)
        database.session.add(medicao_resumida)
        database.session.commit()

        return "Medição processada com sucesso!"

    except Exception as e:
        database.session.rollback()
        return f"Erro ao processar a medição: {str(e)}"
