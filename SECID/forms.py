from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from sqlalchemy.testing.pickleable import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, Optional, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from SECID.models import Usuario, Obras


def file_size_limit(max_size):
    """Validador para limitar o tamanho do arquivo."""
    def _file_size_limit(form, field):
        if field.data:
            file = field.data
            file.seek(0, 2)  # Move o cursor para o final do arquivo
            file_length = file.tell()  # Obtém o tamanho do arquivo em bytes
            file.seek(0)  # Retorna o cursor para o início do arquivo
            if file_length > max_size:
                raise ValidationError(f'O tamanho do arquivo não pode exceder {max_size / (1024 * 1024):.1f} MB.')
    return _file_size_limit

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

class FormMedicao_resumida(FlaskForm):
    obra = QuerySelectField('Projeto Nome',query_factory=lambda:Obras.query.all(),get_label='obra',allow_blank=False,validators=[DataRequired()],render_kw={"class": "form-control"})
    data_inicio_medicao = StringField('Data Inicial', validators=[DataRequired()])  # Data Inicial da Medição
    data_fim_medicao = StringField('Data Final', validators=[DataRequired()])  # Data Final da Medição
    numero_medicao = IntegerField('Número da Medição', validators=[DataRequired()])  # Número da Medição
    valor_medicao = FloatField('Valor da Medição', validators=[DataRequired()])  # Valor da Medição
    letra_medicao = StringField('Letra da Medição', validators=[Optional()])  # Letra da Medição
    reajustamento = FloatField('Reajustamento', validators=[Optional()])  # Valor do Reajustamento

    botao_submit_medicao = SubmitField('Cadastrar Medicao Resumida')  # Botão de envio do formulário

class FormMedicao_inicial(FlaskForm):
    obra = QuerySelectField('Projeto Nome',query_factory=lambda:Obras.query.all(),get_label='obra',allow_blank=False,validators=[DataRequired()],render_kw={"class": "form-control"})
    medicao = IntegerField('Número da Medição', validators=[DataRequired()])  # Número da Medição
    valor = FloatField('Valor da Medição', validators=[DataRequired()])  # Valor da Medição
    acumulado = FloatField('Valor da Medição', validators=[DataRequired()])  # Valor da Medição

class FormMedicao_atualizada(FlaskForm):
    obra = QuerySelectField('Projeto Nome',query_factory=lambda:Obras.query.all(),get_label='obra',allow_blank=False,validators=[DataRequired()],render_kw={"class": "form-control"})
    medicao = IntegerField('Número da Medição', validators=[DataRequired()])  # Número da Medição
    valor = FloatField('Valor da Medição', validators=[DataRequired()])  # Valor da Medição
    acumulado = FloatField('Valor da Medição', validators=[DataRequired()])  # Valor da Medição


class FormObras(FlaskForm):
    sei = StringField('SEI', validators=[DataRequired(),Regexp(r'^SEI-\d{6}/\d{6}/\d{4}$', message="SEI deve seguir o formato SEI-XXXXXX/XXXXXX/XXXX (22 caracteres).")])  # Número SEI
    obra = StringField('Obra', validators=[DataRequired()])  # Nome da Obra
    cidade = StringField('Cidade', validators=[DataRequired()])  # Nome da Obra
    regiao = StringField('Região', validators=[DataRequired()])  # Nome da Obra
    status = SelectField('status',choices=[('ENTREGUE','ENTREGUE'),('ADESÃO','ADESÃO'),('ORDEM DE INICIO','ORDEM DE INICIO'),('ORDEM DE INICIO PARCIAL','ORDEM DE INICIO PARCIAL'),('EM EXECUÇÃO','EM EXECUÇÃO')],validators=[DataRequired()],render_kw={"class": "form-control"})
    contrato = StringField('Contrato', validators=[DataRequired(),Regexp(r'^\d{3}/\d{4}$', message="Contrato deve seguir o formato XXX/XXXX (8 caracteres).")])  # Número do Contrato
    empresa = StringField('Empresa', validators=[DataRequired()])  # Nome da Empresa
    cnpj = StringField( 'CNPJ',validators=[DataRequired(),Regexp(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', message="CNPJ deve seguir o formato XX.XXX.XXX/XXXX-XX (18 caracteres).")])  # CNPJ da Empresa
    valor_inicial = FloatField('Valor Inicial', validators=[DataRequired()])  # Valor Inicial da Obra
    prazo_inicial = StringField('Prazo Inicial', validators=[DataRequired()])  # Prazo Inicial da Obra
    inicio_obra = StringField('Início da Obra', validators=[DataRequired()])  # Data de Início da Obra
    aditivos_prazo = StringField('Aditivos de Prazo', validators=[Optional()])  # Aditivos de Prazo
    aditivos_valor = FloatField('Aditivos de Valor', validators=[Optional()])  # Aditivos de Valor
    prazo_atual = StringField('Prazo Atual', validators=[DataRequired()])  # Prazo Atual da Obra
    valor_atual = FloatField('Valor Atual', validators=[DataRequired()])  # Valor Atual da Obra
    rerratificacao = FloatField('Rerratificação', validators=[Optional()])  # Rerratificação
    reajustamento = FloatField('Reajustamento', validators=[Optional()])  # Reajustamento
    aniversario = StringField('Aniversário', validators=[DataRequired()])  # Data de Aniversário do Projeto
    fonte = StringField('Fonte', validators=[DataRequired(),Length(min=3, max=3, message="Fonte deve ter exatamente 3 caracteres.")])  #Fonte Obra
    objeto = StringField('Objeto', validators=[DataRequired()])  #Objeto Obra
    documento_gestor_contrato = StringField('Documento Gestor Contrato', validators=[DataRequired(),Length(min=8, max=9, message="Documento Gestor Contrato deve ter entre 8 e 9 caracteres.")])  #Dcoumento gestor Contrato
    publicacao_comissao_fiscalizacao = StringField('Publicação Comissão Fiscalização', validators=[DataRequired()])  #Publicação Comissão Fiscalização
    lei_contrato = StringField('Lei Contrato', validators=[DataRequired()])  #Lei Contrato
    coordenacao = SelectField('Coordenação',choices=[('SECID/COORBAC', 'SECID/COORBAC'),('SECID/COOREM', 'SECID/COOREM'),('SECID/COORNOR', 'SECID/COORNOR'),('SECID/COORSUL', 'SECID/COORSUL')],validators=[DataRequired()],render_kw={"class": "form-control"})
    cod_contrato_sei = StringField('Código Contrato SEI', validators=[Optional(), Length(min=8, max=9, message="Código Contrato SEI deve ter entre 8 e 9 caracteres.")]) #Código Contrato SEI
    cod_seguro_garantia = StringField('Código Seguro Garantia', validators=[Optional(), Length(min=8, max=9, message="Código Seguro Garantia deve ter entre 8 e 9 caracteres.")])
    cod_carta_solicitacao_prorrogacao_contratual = StringField('Código Carta Solicitacação Prorrogação Contratual', validators=[Optional(), Length(min=8, max=9, message="Código Carta Solicitacação Prorrogação Contratual deve ter entre 8 e 9 caracteres.")])
    cod_processo_rerratificacao = StringField('Processo Rerratificação', validators=[Optional(),Regexp(r'^SEI-\d{6}/\d{6}/\d{4}$', message="SEI deve seguir o formato SEI-XXXXXX/XXXXXX/XXXX (22 caracteres).")])  # Número SEI
    cod_termo_aditivo = StringField('Código Termo Aditivo', validators=[Optional(), Length(min=8, max=9, message="Código Termo Aditivo deve ter entre 8 e 9 caracteres.")])
    fiscal1 = StringField('Fiscal 1', validators=[DataRequired()])
    id_fiscal1 = StringField('ID Fiscal 1', validators=[Optional(), Regexp(r'^\d{7}-\d$', message="ID Fiscal 1 deve seguir o formato XXXXXXX-X (9 caracteres).")])
    fiscal2 = StringField('Fiscal 2', validators=[DataRequired()])
    id_fiscal2 = StringField('ID Fiscal 2', validators=[Optional(), Regexp(r'^\d{7}-\d$', message="ID Fiscal 2 deve seguir o formato XXXXXXX-X (9 caracteres).")])
    gestor = StringField('Gestor', validators=[DataRequired()])
    gestor_id = StringField('Gestor ID', validators=[Optional(), Regexp(r'^\d{7}-\d$', message="Gestor ID deve seguir o formato XXXXXXX-X (9 caracteres).")])

    # # Campo de seleção de usuário
    # usuario = SelectField('Usuário', coerce=int, validators=[DataRequired()])  # Usuário relacionado à obra

    botao_submit_obras = SubmitField('Cadastrar Obra')  # Botão de envio do formulário

class FormMedicao(FlaskForm):
    sei = StringField('SEI', validators=[DataRequired(),Length(22,22)])  # Número SEI
    projeto_nome = QuerySelectField('Projeto Nome',query_factory=lambda:Obras.query.all(),get_label='obra',allow_blank=False,validators=[DataRequired()],render_kw={"class": "form-control"})
    numero_medicao = IntegerField('Número da Medição', validators=[DataRequired()])  # Número da Medição
    letra_medicao = StringField('Letra da Medição', validators=[Optional()])  # Letra da Medição
    descricao = StringField('Descrição da Medição', validators=[DataRequired()])  # Descrição da Medição
    valor = FloatField('Valor da Medição', validators=[DataRequired(), NumberRange(min=0, message="O valor não pode ser negativo.")])
    reajustamento = FloatField('Reajustamento', validators=[Optional()])  # Valor do Reajustamento
    data_inicial = StringField('Data Inicial', validators=[DataRequired()])  # Data Inicial da Medição
    data_final = StringField('Data Final', validators=[DataRequired()])  # Data Final da Medição

    # Documentos
    documento_1 = FileField('01.Carta assinada pela empresa', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_2 = FileField('02.Publicação da Comissão de Fiscalização', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_3 = FileField('03.Planilha de Medição (PDF)', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_3_1 = FileField('03.1.Planilha de Medição - Arquivo em Excel', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_4 = FileField('04.Memória de Cálculo', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_5 = FileField('05.Cronograma Físico - Financeiro', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_6 = FileField('06.Diário de Obras', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_7 = FileField('07.Relatório Fotográfico', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_8 = FileField('08.Relação de Funcionários', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_9 = FileField('09.Folha de ponto dos funcionários', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_10 = FileField('10.GFD FGTS DIGITAL', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_10_1 = FileField('10.1.DCTF WEB', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_11 = FileField('11.Guias e Comprovantes de Pagamentos de FGTS', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_12 = FileField('12.Folha de Pagamento', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_13 = FileField('13.Comprovante de Pagamento de salários', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_14 = FileField('14.Plano de segurança do Trabalho', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_15 = FileField('15.Certidões atualizadas', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_16 = FileField('16.Contrato', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_17 = FileField('17.ART emitida pelo CREA', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_18 = FileField('18.Nota de empenho', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_19 = FileField('19.Nota fiscal e ISS', validators=[DataRequired(), file_size_limit(10 * 1024 * 1024)])
    documento_15_1 = FileField('Documentos Auxiliares 1', validators=[Optional(), file_size_limit(10 * 1024 * 1024)])
    documento_15_2 = FileField('Documentos Auxiliares 2', validators=[Optional(), file_size_limit(10 * 1024 * 1024)])
    documento_15_3 = FileField('Documentos Auxiliares 3', validators=[Optional(), file_size_limit(10 * 1024 * 1024)])
    documento_15_4 = FileField('Documentos Auxiliares 4', validators=[Optional(), file_size_limit(10 * 1024 * 1024)])
    documento_15_5 = FileField('Documentos Auxiliares 5', validators=[Optional(), file_size_limit(10 * 1024 * 1024)])
    

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
