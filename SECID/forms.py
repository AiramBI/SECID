from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from sqlalchemy.testing.pickleable import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
    sei = StringField('Sei',validators=[DataRequired()])
    empresa = StringField('Empresa',validators=[DataRequired()])
    id_pacto   = StringField('id_pacto',validators=[DataRequired()])
    obra = StringField('Obra',validators=[DataRequired()])
    responsavel = StringField('Responsavel',validators=[DataRequired()])
    cidade = StringField('Cidade',validators=[DataRequired()])
    regiao = StringField('Regiao',validators=[DataRequired()])
    procedimento = StringField('Procedimento',validators=[DataRequired()])
    #verificar informações necessária para poder fazer o despacho no SEI