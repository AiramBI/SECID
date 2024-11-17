# Usar uma imagem base leve do Python
FROM python:3.12-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o requirements.txt para instalar as dependências
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos da aplicação para o diretório de trabalho
COPY . .

# Expôr a porta que o Flask vai usar (por padrão, pode ser 8000)
EXPOSE 8000

# Comando para iniciar a aplicação com gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "300", "--graceful-timeout", "300", "--limit-request-line", "8190", "--limit-request-field_size", "0", "--worker-connections", "100", "--log-level", "debug", "--keep-alive", "10", "main:app"]

