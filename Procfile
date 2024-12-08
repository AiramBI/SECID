web: gunicorn --timeout 600 --limit-request-line 8190 --graceful-timeout 600 --limit-request-field_size 0 --worker-connections 100 --log-level debug --keep-alive 10 app:app
worker: celery -A SECID.celery worker --loglevel=info
