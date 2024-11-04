from flask import render_template, redirect, url_for, flash, request, Flask, send_from_directory, abort
from SECID import app, database,bcrypt
from SECID.forms import FormLogin, FormCriarConta, FormObras, FormMedicao, FormMedicao2
from SECID.models import Usuario, Obras, Medicao, Medicao2
from flask_login import current_user, login_required, login_user, logout_user
import traceback
from werkzeug.utils import secure_filename
import os
import logging
from SECID.uploadarquivos import executarautomacao

logging.basicConfig(level=logging.INFO)

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



@app.route('/paineis/gestor')
@login_required
def paines():
    return render_template('gestor.html')

@app.route('/paineis/administrativo')
@login_required
def administrativo():
    return render_template('administrativo.html')

@app.route('/paineis/financeiro')
@login_required
def financeiro():
    return render_template('financeiro.html')



@app.route('/usuario')
@login_required
def usuario():
    obras = Obras.query.all()
    return render_template('usuario.html',obras =obras)



@app.route('/administrador', methods =['GET','POST'])
# @login_required
def administrador():
    form_obras = FormObras()

    # Verifica se o formulário foi submetido corretamente
    if form_obras.validate_on_submit():
        # print("Formulário validado com sucesso!")
        # Cria uma nova instância da obra com os dados do formulário
        obra = Obras(
            sei=form_obras.sei.data,
            # id = form_obras.id.data,
            obra=form_obras.obra.data,
            contrato=form_obras.contrato.data,
            empresa=form_obras.empresa.data,
            cnpj=form_obras.cnpj.data,
            valor_inicial=form_obras.valor_inicial.data,
            prazo_inicial=form_obras.prazo_inicial.data,
            inicio_obra=form_obras.inicio_obra.data,
            aditivos_prazo=form_obras.aditivos_prazo.data,
            aditivos_valor=form_obras.aditivos_valor.data,
            prazo_atual=form_obras.prazo_atual.data,
            valor_atual=form_obras.valor_atual.data,
            aniversario=form_obras.aniversario.data
        )

        # Adiciona a obra ao banco de dados
        database.session.add(obra)
        database.session.commit()

        flash('Obra Cadastrada{}'.format(form_obras.obra.data), 'alert-success')

        # # Chama a função que irá abrir a página com o Selenium em modo headless
        # abrir_pagina_com_selenium()

        return redirect(url_for('administrador'))

    # Renderiza a página novamente, passando o formulário
    # print("Erros de validação:", form_obras.errors)
    return render_template('administrador.html', form_obras=form_obras)

# Configuração da pasta para upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Função save_file para salvar o arquivo no diretório configurado
def save_file(file):
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return filename
    return None

   

@app.route('/usuario/medicao', methods=['GET', 'POST'])
@login_required
def medicao():
    form_medicao = FormMedicao()

    if form_medicao.validate_on_submit():
        try:
            # Dicionário para os documentos dinamicamente
            documentos = {}
            for field in form_medicao:
                if "documento_" in field.name:
                    documentos[field.name] = save_file(field.data)
                    
            # Salva os arquivos e cria uma nova instância de Medicao
            medicao1 = Medicao(
                sei=form_medicao.sei.data,
                projeto_nome=form_medicao.projeto_nome.data,
                numero_medicao=form_medicao.numero_medicao.data,
                descricao=form_medicao.descricao.data,
                valor=form_medicao.valor.data,
                data_inicial=form_medicao.data_inicial.data,
                data_final=form_medicao.data_final.data,
                **documentos  # Atribuição dinâmica dos documentos
            )
            
            # Adiciona a medição ao banco de dados
            database.session.add(medicao1)
            database.session.commit()

            flash('Medição cadastrada com sucesso!', 'alert-success')
            return redirect(url_for('administrador'))

        except Exception as e:
            flash(f'Ocorreu um erro ao processar o formulário: {str(e)}', 'danger')
            app.logger.error(f"Erro ao processar o formulário: {str(e)}")
            database.session.rollback()

    return render_template('medicao.html', form_medicao=form_medicao)


@app.route('/usuario/medicao2', methods =['GET','POST'])
@login_required
def medicao2():
    form_medicao2 = FormMedicao2()

    if form_medicao2.validate_on_submit():
        try:
            # Salva os arquivos e cria uma nova instância de Medicao
            medicao2 = Medicao2(
                sei=form_medicao2.sei.data,
                obra=form_medicao2.projeto_nome.data,
                numero_medicao=form_medicao2.numero_medicao.data,
                descricao=form_medicao2.descricao.data,
                valor=form_medicao2.valor.data,
                data_inicial=form_medicao2.data_inicial.data,
                data_final=form_medicao2.data_final.data,
                documento_1=save_file(form_medicao2.documento_1.data),
                documento_2=save_file(form_medicao2.documento_2.data)
                )

            
            # Adiciona a medição ao banco de dados
            database.session.add(medicao2)
            database.session.commit()

            flash('Medição cadastrada com sucesso!', 'alert-success')
            return redirect(url_for('administrador'))

        except Exception as e:
            flash(f'Ocorreu um erro ao processar o formulário: {str(e)}', 'danger')
            app.logger.error(f"Erro ao processar o formulário: {str(e)}")
            database.session.rollback()

    return render_template('medicao2.html', form_medicao2=form_medicao2)

@app.route('/download/<filename>')
def download_file(filename):
    try:
        # Tenta enviar o arquivo especificado para o navegador
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        # Retorna uma mensagem de erro se o arquivo não for encontrado
        abort(404, "Arquivo não encontrado")

# Rota no Flask para acionar a automação
@app.route('/usuario/medicao3', methods=['GET', 'POST'])
@login_required
def medicao3():
    executarautomacao()
    return render_template('medicao3.html')

@app.route('/paineis/sei')
@login_required
def sei():
    return render_template('sei.html')



@app.route('/noticias')
@login_required
def noticias():
    return render_template('noticias.html')

