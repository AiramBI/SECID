# Use uma imagem Python slim como base
FROM python:3.12-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo requirements.txt e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instale as dependências do sistema necessárias para o Chromium
RUN apt-get update && apt-get install -y \
    libnss3 libatk-bridge2.0-0 libxcomposite1 libxrandr2 libxdamage1 libxi6 libxtst6 \
    libappindicator3-1 libgbm1 libxshmfence1 libasound2 libatk1.0-0 libcups2 \
    libgobject-2.0-0 libglib2.0-0 libpango-1.0-0 libcairo2 libatspi2.0-0 libx11-xcb1 \
    libxcb1 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libsmime3 libnspr4 libdbus-1-3 libcups2 libgio-2.0-0 libdrm2 libexpat1 \
    libxext6 libxkbcommon0 libX11-6 libXcomposite1 libXdamage1 libXext6 libXfixes3 libXrandr2 && \
    rm -rf /var/lib/apt/lists/*

# Instale o Chromium com o Playwright
RUN playwright install chromium

# Copie o código da aplicação
COPY . .

# Comando para iniciar o servidor
CMD ["gunicorn", "--timeout", "180", "-w", "3", "--threads", "4", "main:app"]
