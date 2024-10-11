from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import sqlalchemy
import os

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = '70898ff6cf8c6fc9a940820e7c211072'

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

# Importar modelos
from SECID import models

# Verificar se a tabela "usuario" existe e criar o banco de dados, se necessário
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)

if not inspector.has_table("medicao"):
    with app.app_context():
        database.drop_all()  # Remove todas as tabelas existentes (opcional)
        database.create_all()  # Cria todas as tabelas
        print("Base de dados criada")
else:
    print("Base de dados já existente")

# Importar as rotas
from SECID import routes
