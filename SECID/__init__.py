from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import sqlalchemy
import os
flask_dropzone
# from flask_migrate import Migrate
from flask_dropzone import Dropzone

app = Flask(__name__)
dropzone = Dropzone(app)

# Configurações
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['SECRET_KEY'] = '70898ff6cf8c6fc9a940820e7c211072'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # Limita o tamanho do upload para 20MB, por exemplo
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Cache control for file uploads

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
