from SECID import celery

@celery.task
def process_form_data(data, files):
    # Processar os dados do formulário e os arquivos
    for file in files:
        # Simular upload ou processamento
        print(f"Processando arquivo: {file}")
    return "Tarefa concluída!"

