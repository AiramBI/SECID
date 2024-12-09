# Função para salvar o arquivo no diretório configurado
def save_file(file):
    if file:
        try:
            # Gera um timestamp único baseado na data e hora
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Sanitiza o nome do arquivo
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{timestamp}{ext}"  # Adiciona o timestamp ao nome

            # Define o caminho completo para salvar o arquivo
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Garante que o diretório existe
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            # Salva o arquivo no caminho configurado
            file.save(file_path)

            # Retorna o nome do arquivo salvo
            return filename
        except Exception as e:
            # Log do erro para diagnóstico
            print(f"Erro ao salvar o arquivo: {str(e)}")
            return None
    return None
