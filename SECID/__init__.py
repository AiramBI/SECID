from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import sqlalchemy
import os
from flask_dropzone import Dropzone
from celery import Celery

app = Flask(__name__)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

# Configuração de Redis como backend e broker
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = make_celery(app)



# Configurações
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.pdf'  # Permitir apenas arquivos PDF
app.config['DROPZONE_MAX_FILE_SIZE'] = 10  # Tamanho máximo de cada arquivo em MB
app.config['DROPZONE_TIMEOUT'] = 600000  # 5 minutos em milissegundos
app.config['PERMANENT_SESSION_LIFETIME'] = 600  # 10 minutos
app.config['SECRET_KEY'] = '70898ff6cf8c6fc9a940820e7c211072'
#app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # Limita o tamanho do upload para 20MB, por exemplo
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Cache control for file uploads

# Configuração do diretório de uploads
UPLOAD_FOLDER = '/var/lib/postgresql/data/uploads'  # Diretório persistente
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Garante que o diretório exista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Inicializar Dropzone
dropzone = Dropzone(app)

# Configuração do banco de dados
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SECID.db'


   
# Inicialização das extensões
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

# Inicialização do Flask-Migrate
# migrate = Migrate(app, database)

# Importar modelos
from SECID import models


# Verificar se a tabela "usuario" existe e criar o banco de dados, se necessário
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)

if not inspector.has_table("usuario"):
    with app.app_context():
        database.drop_all()  # Remove todas as tabelas existentes (opcional)
        database.create_all()  # Cria todas as tabelas
        print("Base de dados criada")
else:
    print("Base de dados já existente")

# Importar as rotas
from SECID import routes


