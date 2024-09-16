from flask import render_template, redirect, url_for, flash, request
from SECID import app, database,bcrypt
from SECID.forms import FormLogin, FormCriarConta, FormObras
from SECID.models import Usuario
from flask_login import current_user, login_required, login_user, logout_user


lista_usuarios = ['Marina','Pedro','Danilo','Joao','Kleber']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods =['GET','POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha,form_login.senha.data):
            login_user(usuario, remember = form_login.lembrar_dados.data)
            flash('Login Realizado {}'.format(form_login.email.data),'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no Login, email ou senha incorretos {}''alert-danger')
    return render_template('login.html', form_login=form_login)



@app.route('/criarconta', methods =['GET','POST'])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit() and'botao_submit_criarconta' in request.form :
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
        usuario = Usuario(username=form_criarconta.username.data, email =form_criarconta.email.data,senha=senha_cript,cargo=form_criarconta.cargo.data)
        database.session.add(usuario)
        database.session.commit()
        flash('Conta Criada{}'.format(form_criarconta.email.data),'alert-success')
        return redirect(url_for('home'))
    return render_template('criarconta.html',form_criarconta = form_criarconta)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))



@app.route('/paineis')
@login_required
def paines():
    return render_template('paines.html')



@app.route('/usuario')
@login_required
def usuario():
    return render_template('usuario.html',lista_usuarios=lista_usuarios)



@app.route('/administrador')
@login_required
def administrador():
    return render_template('administrador.html')



@app.route('/noticias')
@login_required
def noticias():
    return render_template('noticias.html')

