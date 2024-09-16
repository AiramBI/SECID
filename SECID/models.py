from sqlalchemy.testing.pickleable import User

from SECID import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))




class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String,nullable=False ,unique=True)
    senha = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    cargo = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.Integer,nullable = False, default=0)

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

class Obras(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    sei = database.Column(database.Integer, primary_key=True)
    modelo = database.Column(database.String, nullable=False)
    documento = database.Column(database.String, nullable=False)
    contrato =database.Column(database.String, nullable=False)
    empresa = database.Column(database.String, nullable=False)
    termo = database.Column(database.String, nullable=False)
    cnpj = database.Column(database.String, nullable=False)
    valor = database.Column(database.Float, nullable=False)
    prazo_inicial = database.Column(database.String, nullable=False)
    inicio_obra = database.Column(database.String, nullable=False)
    aditivos = database.Column(database.String, nullable=False)
    prazo_atual = database.Column(database.String, nullable=False)
    vigencia = database.Column(database.String, nullable=False)
    aniversario = database.Column(database.String, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)

class Textos(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    sei = database.Column(database.Integer, primary_key=True)
    modelo = database.Column(database.String, nullable=False)
    documento = database.Column(database.String, nullable=False)
    contrato =database.Column(database.String, nullable=False)
    empresa = database.Column(database.String, nullable=False)
    termo = database.Column(database.String, nullable=False)
    cnpj = database.Column(database.String, nullable=False)
    valor = database.Column(database.Float, nullable=False)
    prazo_inicial = database.Column(database.String, nullable=False)
    inicio_obra = database.Column(database.String, nullable=False)
    aditivos = database.Column(database.String, nullable=False)
    prazo_atual = database.Column(database.String, nullable=False)
    vigencia = database.Column(database.String, nullable=False)
    aniversario = database.Column(database.String, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)

#modelos
# Despacho de Encaminhamento de Análise
# Nota tecnica aditivo de contrato

# Nota Tecnica - Prorrogação de prazo
# Checklist - Prorrogação de Prazo

# Nota Técnica – Medição
# Checklist Medição
# Despacho de Encaminhamento de Medição

# Nota Técnica - Rerratificação
# Checklist  - Rerratificação
# Nota Técnica Coordenação

#Exposição de Motivos
#Despacho de Encaminhamento de Projeto Executivo

#GARANTIA CONTR. - DESPACHO DE ENCAMINHAMENTO DE P.

#Nota técnica ASSJUR – Modelo
