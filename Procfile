web: apt-get update && apt-get install -y \
    libnss3 libatk-bridge2.0-0 libxcomposite1 libxrandr2 libxdamage1 libxi6 libxtst6 \
    libappindicator3-1 libgbm1 libxshmfence1 libasound2 libatk1.0-0 libcups2 \
    libgobject-2.0-0 libglib2.0-0 libpango-1.0-0 libcairo2 libatspi2.0-0 libx11-xcb1 \
    libxcb1 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 && \
    playwright install chromium && \
    gunicorn --timeout 180 -w 3 --threads 4 main:app




