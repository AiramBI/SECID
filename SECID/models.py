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
    # posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.Integer,nullable = False, default=0)


class Obras(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    obra = database.Column(database.String, nullable=False)
    sei = database.Column(database.String, nullable=False)
    # modelo = database.Column(database.String, nullable=False)
    # documento = database.Column(database.String, nullable=False)
    contrato =database.Column(database.String, nullable=False)
    empresa = database.Column(database.String, nullable=False)
    # termo = database.Column(database.String, nullable=False)
    cnpj = database.Column(database.String, nullable=False)
    valor_inicial = database.Column(database.Float, nullable=False)
    prazo_inicial = database.Column(database.Integer, nullable=False)
    inicio_obra = database.Column(database.Date, nullable=False)
    aditivos_prazo = database.Column(database.Integer, nullable=True)
    aditivos_valor = database.Column(database.Float, nullable=True)
    prazo_atual = database.Column(database.Integer, nullable=False)
    valor_atual = database.Column(database.Float, nullable=False)
    aniversario = database.Column(database.Date, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)


class Medicao(database.Model):

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    sei = database.Column(database.String, nullable=False)  # Número SEI
    projeto_nome = database.Column(database.String, nullable=False)  # Nome do Projeto
    numero_medicao = database.Column(database.Integer, nullable=False)  # Número da Medição
    descricao = database.Column(database.String, nullable=False)  # Descrição da Medição
    valor = database.Column(database.Float, nullable=False)  # Valor da Medição
    data_inicial = database.Column(database.String, nullable=False)  # Data Inicial da Medição
    data_final = database.Column(database.String, nullable=False)  # Data Final da Medição

    # Documentos
    documento_1 = database.Column(database.String, nullable=False)  # 1 - Carta assinada pela empresa
    documento_2 = database.Column(database.String, nullable=False)  # 2 - Publicação da Comissão de Fiscalização
    documento_3 = database.Column(database.String, nullable=False)  # 3 - Planilha de Medição (PDF)
    documento_3_1 = database.Column(database.String, nullable=False)  # 3.1 - Planilha de Medição - Arquivo em Excel
    documento_4 = database.Column(database.String, nullable=False)  # 4 - Memória de Cálculo
    documento_5 = database.Column(database.String, nullable=False)  # 5 - Cronograma Físico - Financeiro
    documento_6 = database.Column(database.String, nullable=False)  # 6 - Diário de Obras
    documento_7 = database.Column(database.String, nullable=False)  # 7 - Relatório Fotográfico
    documento_8 = database.Column(database.String, nullable=False)  # 8 - Relação de Funcionários
    documento_9 = database.Column(database.String, nullable=False)  # 9 - Folha de ponto dos funcionários
    documento_10 = database.Column(database.String, nullable=False)  # 10 - GFD FGTS DIGITAL
    documento_10_1 = database.Column(database.String, nullable=False)  # 10.1 - DCTF WEB
    documento_11 = database.Column(database.String, nullable=False)  # 11 - Guias e Comprovantes de Pagamentos de FGTS
    documento_12 = database.Column(database.String, nullable=False)  # 12 - Folha de Pagamento
    documento_13 = database.Column(database.String, nullable=False)  # 13 - Comprovante de Pagamento de salários
    documento_14 = database.Column(database.String, nullable=False)  # 14 - Plano de segurança do Trabalho
    documento_15 = database.Column(database.String, nullable=False)  # 15 - Certidões atualizadas
    documento_15_1 = database.Column(database.String, nullable=False)  # 15.1 - Certidão de regularidade junto ao FGTS
    documento_15_2 = database.Column(database.String, nullable=False)  # 15.2 - Certidão negativa de débito trabalhista
    documento_15_3 = database.Column(database.String, nullable=False)  # 15.3 - Certidão negativa de débitos federais
    documento_15_4 = database.Column(database.String,
                                     nullable=False)  # 15.4 - Certidão de regularidade fiscal junto ao ICMS
    documento_15_5 = database.Column(database.String,
                                     nullable=False)  # 15.5 - Certidão de regularidade fiscal junto ao ISS
    documento_16 = database.Column(database.String, nullable=False)  # 16 - Contrato
    documento_17 = database.Column(database.String, nullable=False)  # 17 - ART emitida pelo CREA
    documento_18 = database.Column(database.String, nullable=False)  # 18 - Nota de empenho
    documento_19 = database.Column(database.String, nullable=False)  # 19 - Nota fiscal e ISS

    data_criacao = database.Column(database.DateTime, nullable=False,
                                   default=datetime.utcnow)  # Data de criação do registro



class Medicao2(database.Model):

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    sei = database.Column(database.Integer, nullable=False)  # Número SEI
    obra = database.Column(database.String, nullable=False)  # Nome do Projeto
    numero_medicao = database.Column(database.Integer, nullable=False)  # Número da Medição
    descricao = database.Column(database.String, nullable=False)  # Descrição da Medição
    valor = database.Column(database.Float, nullable=False)  # Valor da Medição
    data_inicial = database.Column(database.String, nullable=False)  # Data Inicial da Medição
    data_final = database.Column(database.String, nullable=False)  # Data Final da Medição

    # Documentos
    documento_1 = database.Column(database.String, nullable=False)  # 1 - Carta assinada pela empresa
    documento_2 = database.Column(database.String, nullable=False)  # 2 - Publicação da Comissão de Fiscalização

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
