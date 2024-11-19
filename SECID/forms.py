from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from sqlalchemy.testing.pickleable import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from SECID.models import Usuario


class FormCriarConta(FlaskForm):
    username = StringField('Nome Completo',validators=[DataRequired()])
    cargo = StringField('Cargo',validators=[DataRequired()])
    email = StringField('E-mail',validators=[DataRequired(),Email()])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
    confirmacao = PasswordField ('Confirmação de Senha',validators=[DataRequired(),EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Faça Login.')

class FormLogin(FlaskForm):
        email = StringField('E-mail',validators=[DataRequired(),Email()])
        senha = PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
        lembrar_dados = BooleanField('Lembrar Dados de Acesso')
        botao_submit_login = SubmitField('Fazer Login')


class FormObras(FlaskForm):
    sei = StringField('SEI', validators=[DataRequired(),Length(22,22)])  # Número SEI
    obra = StringField('Obra', validators=[DataRequired()])  # Nome da Obra
    contrato = StringField('Contrato', validators=[DataRequired()])  # Número do Contrato
    empresa = StringField('Empresa', validators=[DataRequired()])  # Nome da Empresa
    cnpj = StringField( 'CNPJ',validators=[DataRequired(),Length(18,18)])  # CNPJ da Empresa
    valor_inicial = FloatField('Valor Inicial', validators=[DataRequired()])  # Valor Inicial da Obra
    prazo_inicial = StringField('Prazo Inicial', validators=[DataRequired()])  # Prazo Inicial da Obra
    inicio_obra = StringField('Início da Obra', validators=[DataRequired()])  # Data de Início da Obra
    aditivos_prazo = StringField('Aditivos de Prazo', validators=[DataRequired()])  # Aditivos de Prazo
    aditivos_valor = FloatField('Aditivos de Valor', validators=[DataRequired()])  # Aditivos de Valor
    prazo_atual = StringField('Prazo Atual', validators=[DataRequired()])  # Prazo Atual da Obra
    valor_atual = FloatField('Valor Atual', validators=[DataRequired()])  # Valor Atual da Obra
    aniversario = StringField('Aniversário', validators=[DataRequired()])  # Data de Aniversário do Projeto
    fonte = StringField('Fonte', validators=[DataRequired()])  #Fonte Obra
    objeto = StringField('Objeto', validators=[DataRequired()])  #Objeto Obra
    documento_gestor_contrato = StringField('Documento Gestor Contrato', validators=[DataRequired()])  #Dcoumento gestor Contrato
    publicao_comissao_fiscalizacao = StringField('Publicação Comissão Fiscalização', validators=[DataRequired()])  #Publicação Comissão Fiscalização
    lei_contrato = StringField('Lei Contrato', validators=[DataRequired()])  #Lei Contrato

    # # Campo de seleção de usuário
    # usuario = SelectField('Usuário', coerce=int, validators=[DataRequired()])  # Usuário relacionado à obra

    botao_submit_obras = SubmitField('Cadastrar Obra')  # Botão de envio do formulário

class FormMedicao(FlaskForm):
    sei = StringField('SEI', validators=[DataRequired(),Length(22,22)])  # Número SEI
    projeto_nome = StringField('Obra', validators=[DataRequired()])  # Nome do Projeto
    numero_medicao = IntegerField('Número da Medição', validators=[DataRequired()])  # Número da Medição
    descricao = StringField('Descrição da Medição', validators=[DataRequired()])  # Descrição da Medição
    valor = FloatField('Valor da Medição', validators=[DataRequired()])  # Valor da Medição
    data_inicial = StringField('Data Inicial', validators=[DataRequired()])  # Data Inicial da Medição
    data_final = StringField('Data Final', validators=[DataRequired()])  # Data Final da Medição

    # Documentos
    documento_1 = FileField('01.Carta assinada pela empresa', validators=[DataRequired()])
    documento_2 = FileField('02.Publicação da Comissão de Fiscalização', validators=[DataRequired()])
    documento_3 = FileField('03.Planilha de Medição (PDF)', validators=[DataRequired()])
    documento_3_1 = FileField('03.1.Planilha de Medição - Arquivo em Excel', validators=[DataRequired()])
    documento_4 = FileField('04.Memória de Cálculo', validators=[DataRequired()])
    documento_5 = FileField('05.Cronograma Físico - Financeiro', validators=[DataRequired()])
    documento_6 = FileField('06.Diário de Obras', validators=[DataRequired()])
    documento_7 = FileField('07.Relatório Fotográfico', validators=[DataRequired()])
    documento_8 = FileField('08.Relação de Funcionários', validators=[DataRequired()])
    documento_9 = FileField('09.Folha de ponto dos funcionários', validators=[DataRequired()])
    documento_10 = FileField('10.GFD FGTS DIGITAL', validators=[DataRequired()])
    documento_10_1 = FileField('10.1.DCTF WEB', validators=[DataRequired()])
    documento_11 = FileField('11.Guias e Comprovantes de Pagamentos de FGTS', validators=[DataRequired()])
    documento_12 = FileField('12.Folha de Pagamento', validators=[DataRequired()])
    documento_13 = FileField('13.Comprovante de Pagamento de salários', validators=[DataRequired()])
    documento_14 = FileField('14.Plano de segurança do Trabalho', validators=[DataRequired()])
    documento_15 = FileField('15.Certidões atualizadas', validators=[DataRequired()])
    documento_15_1 = FileField('15.1.Certidão de regularidade junto ao FGTS', validators=[DataRequired()])
    documento_15_2 = FileField('15.2.Certidão negativa de débito trabalhista', validators=[DataRequired()])
    documento_15_3 = FileField('15.3.Certidão negativa de débitos federais', validators=[DataRequired()])
    documento_15_4 = FileField('15.4.Certidão de regularidade fiscal junto ao ICMS', validators=[DataRequired()])
    documento_15_5 = FileField('15.5.Certidão de regularidade fiscal junto ao ISS', validators=[DataRequired()])
    documento_16 = FileField('16.Contrato', validators=[DataRequired()])
    documento_17 = FileField('17.ART emitida pelo CREA', validators=[DataRequired()])
    documento_18 = FileField('18.Nota de empenho', validators=[DataRequired()])
    documento_19 = FileField('19.Nota fiscal e ISS', validators=[DataRequired()])

    botao_submit_medicao = SubmitField('Cadastrar Medicao Documentos')  # Botão de envio do formulário


class FormMedicao2(FlaskForm):
    sei = StringField('SEI', validators=[DataRequired()])  # Número SEI
    projeto_nome = StringField('Obra', validators=[DataRequired()])  # Nome do Projeto
    numero_medicao = IntegerField('Número da Medição', validators=[DataRequired()])  # Número da Medição
    descricao = StringField('Descrição da Medição', validators=[DataRequired()])  # Descrição da Medição
    valor = FloatField('Valor da Medição', validators=[DataRequired()])  # Valor da Medição
    data_inicial = StringField('Data Inicial', validators=[DataRequired()])  # Data Inicial da Medição
    data_final = StringField('Data Final', validators=[DataRequired()])  # Data Final da Medição

    # Documentos
    documento_1 = FileField('01.Carta assinada pela empresa', validators=[DataRequired()])
    documento_2 = FileField('02.Publicação da Comissão de Fiscalização', validators=[DataRequired()])

    botao_submit_medicao = SubmitField('Cadastrar Medicao Documentos')  # Botão de envio do formulário
