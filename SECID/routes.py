from flask import render_template, redirect, url_for, flash, request, Flask, send_from_directory, abort, jsonify
from SECID import app, database,bcrypt
from SECID.forms import FormLogin, FormCriarConta, FormObras, FormMedicao, FormMedicao2, FormMedicao_inicial, FormMedicao_atualizada, FormMedicao_resumida
from SECID.models import Usuario, Obras, Medicao, Medicao2, Medicao_inicial, Medicao_atualizada, Medicao_resumida
from flask_login import current_user, login_required, login_user, logout_user
import traceback
from werkzeug.utils import secure_filename
import os
import logging
from SECID.uploadarquivos import executarautomacao
import uuid


logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():

    # Consulta para pegar as 4 últimas medições ordenadas por data_criacao
    ultimas_medicoes = Medicao.query.order_by(Medicao.data_criacao.desc()).limit(4).all()

    # Lista de imagens fixas
    imagens = ['secid (1).jpeg', 'secid (7).jpeg', 'secid (9).jpeg', 'secid (2).jpeg']

    # Combinar medições com imagens e formatar valores
    combinacoes = [
        {
            "medicao": medicao,
            "imagem": imagem,
            "valor_formatado": f"{medicao.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        }
        for medicao, imagem in zip(ultimas_medicoes, imagens)
    ]

    #Consultas específicas para cada região
    regioes_dados = {
        "Norte": Obras.query
            .filter(Obras.regiao == "Norte")
            .with_entities(
                database.func.count(Obras.id).label("quantidade"),
                database.func.sum(Obras.valor_atual).label("valor_total")
            )
            .first(),
        "Metropolitana": Obras.query
            .filter(Obras.regiao == "Metropolitana")
            .with_entities(
                database.func.count(Obras.id).label("quantidade"),
                database.func.sum(Obras.valor_atual).label("valor_total")
            )
            .first(),
        "Centro Sul": Obras.query
            .filter(Obras.regiao == "Centro Sul")
            .with_entities(
                database.func.count(Obras.id).label("quantidade"),
                database.func.sum(Obras.valor_atual).label("valor_total")
            )
            .first(),
    }

    # Formatar dados para o template
    regioes = [
        {
            "nome": "Região Norte",
            "quantidade": regioes_dados["Norte"][0],
            "valor_total": f"{regioes_dados['Norte'][1]:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        },
        {
            "nome": "Região Metropolitana",
            "quantidade": regioes_dados["Metropolitana"][0],
            "valor_total": f"{regioes_dados['Metropolitana'][1]:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        },
        {
            "nome": "Região Centro Sul",
            "quantidade": regioes_dados["Centro Sul"][0],
            "valor_total": f"{regioes_dados['Centro Sul'][1]:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        },
    ]

    # Retornar o template com as variáveis
    return render_template('home.html', combinacoes=combinacoes, regioes=regioes)

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

@app.route('/status/<task_id>')
def status_task(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Aguardando...'}
    elif task.state == 'SUCCESS':
        response = {'state': task.state, 'status': 'Tarefa concluída com sucesso!'}
    elif task.state == 'FAILURE':
        response = {'state': task.state, 'status': str(task.info)}
    else:
        response = {'state': task.state, 'status': task.info}

    return jsonify(response)

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

@app.route('/selecionar_obra', methods=['GET'])
# @login_required
def selecionar_obra():
    # Busca todas as obras no banco de dados
    obras = Obras.query.all()
    return render_template('selecionar_obra.html', obras=obras)

@app.route('/editar_obra/<int:id>', methods=['GET', 'POST'])
# @login_required
def editar_obra(id):
    # Busca a obra pelo ID no banco de dados
    obra = Obras.query.get_or_404(id)

    # Cria o formulário e pré-preenche com os dados da obra
    form_obras = FormObras(obj=obra)

    # Verifica se o formulário foi submetido corretamente
    if form_obras.validate_on_submit():
        # Atualiza os campos da obra com os dados do formulário
        obra.sei = form_obras.sei.data
        obra.obra = form_obras.obra.data
        obra.cidade = form_obras.cidade.data
        obra.regiao = form_obras.regiao.data
        obra.status = form_obras.status.data
        obra.contrato = form_obras.contrato.data
        obra.empresa = form_obras.empresa.data
        obra.cnpj = form_obras.cnpj.data
        obra.valor_inicial = form_obras.valor_inicial.data
        obra.prazo_inicial = form_obras.prazo_inicial.data
        obra.inicio_obra = form_obras.inicio_obra.data
        obra.aditivos_prazo = form_obras.aditivos_prazo.data
        obra.aditivos_valor = form_obras.aditivos_valor.data
        obra.prazo_atual = form_obras.prazo_atual.data
        obra.valor_atual = form_obras.valor_atual.data
        obra.reajustamento = form_obras.reajustamento.data
        obra.rerratificacao = form_obras.rerratificacao.data
        obra.aniversario = form_obras.aniversario.data
        obra.fonte = form_obras.fonte.data
        obra.objeto = form_obras.objeto.data
        obra.documento_gestor_contrato = form_obras.documento_gestor_contrato.data
        obra.publicacao_comissao_fiscalizacao = form_obras.publicacao_comissao_fiscalizacao.data
        obra.lei_contrato = form_obras.lei_contrato.data
        obra.coordenacao = form_obras.coordenacao.data
        obra.cod_contrato_sei = form_obras.cod_contrato_sei.data
        obra.cod_seguro_garantia = form_obras.cod_seguro_garantia.data
        obra.cod_carta_solicitacao_prorrogacao_contratual = form_obras.cod_carta_solicitacao_prorrogacao_contratual.data
        obra.cod_processo_rerratificacao = form_obras.cod_processo_rerratificacao.data
        obra.cod_termo_aditivo = form_obras.cod_termo_aditivo.data
        obra.fiscal1 = form_obras.fiscal1.data
        obra.id_fiscal1 = form_obras.id_fiscal1.data
        obra.fiscal2 = form_obras.fiscal2.data
        obra.id_fiscal2 = form_obras.id_fiscal2.data
        obra.gestor = form_obras.gestor.data
        obra.gestor_id = form_obras.gestor_id.data

        # Salva as alterações no banco de dados
        database.session.commit()

        flash('Obra Atualizada com Sucesso', 'alert-success')

        return redirect(url_for('selecionar_obra'))  # Redireciona para a lista de obras ou outra página
    del form_obras.botao_submit_obras
    
    return render_template('editar_obra.html', form_obras=form_obras, obra=obra)

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
            obra=form_obras.obra.data,
            cidade=form_obras.cidade.data,
            regiao=form_obras.regiao.data,
            status = form_obras.status.data,
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
            reajustamento = form_obras.reajustamento.data,
            rerratificacao=form_obras.rerratificacao.data,
            aniversario=form_obras.aniversario.data,
            fonte=form_obras.fonte.data,
            objeto=form_obras.objeto.data,
            documento_gestor_contrato=form_obras.documento_gestor_contrato.data,
            publicacao_comissao_fiscalizacao=form_obras.publicacao_comissao_fiscalizacao.data,
            lei_contrato=form_obras.lei_contrato.data,
            coordenacao=form_obras.coordenacao.data,
            cod_contrato_sei=form_obras.cod_contrato_sei.data,
            cod_seguro_garantia=form_obras.cod_seguro_garantia.data,
            cod_carta_solicitacao_prorrogacao_contratual=form_obras.cod_carta_solicitacao_prorrogacao_contratual.data,
            cod_processo_rerratificacao=form_obras.cod_processo_rerratificacao.data,
            cod_termo_aditivo=form_obras.cod_termo_aditivo.data,
            fiscal1=form_obras.fiscal1.data,
            id_fiscal1=form_obras.id_fiscal1.data,
            fiscal2=form_obras.fiscal2.data,
            id_fiscal2=form_obras.id_fiscal2.data,
            gestor=form_obras.gestor.data,
            gestor_id=form_obras.gestor_id.data
        )

        # Adiciona a obra ao banco de dados
        database.session.add(obra)
        database.session.commit()

        flash('Obra Cadastrada{}'.format(form_obras.obra.data), 'alert-success')

        return redirect(url_for('administrador'))
    return render_template('administrador.html', form_obras=form_obras)

# Configuração da pasta para upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo encontrado'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    # Salvar o arquivo
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'success': 'Arquivo salvo com sucesso'}), 200

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
    
    if request.method == 'POST' and form_medicao.validate_on_submit():
        try:
            # Salva os arquivos e cria uma nova instância de Medicao
            medicao1 = Medicao(
                sei=form_medicao.sei.data,
                projeto_nome=form_medicao.projeto_nome.data,
                numero_medicao=form_medicao.numero_medicao.data,
                letra_medicao=form_medicao.numero_medicao.data,
                descricao=form_medicao.descricao.data,
                valor=form_medicao.valor.data,
                reajustamento=form_medicao.reajustamento.data,
                data_inicial=form_medicao.data_inicial.data,
                data_final=form_medicao.data_final.data,
                documento_1=save_file(form_medicao.documento_1.data),
                documento_2=save_file(form_medicao.documento_2.data),
                documento_3=save_file(form_medicao.documento_3.data),
                documento_3_1=save_file(form_medicao.documento_3_1.data),
                documento_4=save_file(form_medicao.documento_4.data),
                documento_5=save_file(form_medicao.documento_5.data),
                documento_6=save_file(form_medicao.documento_6.data),
                documento_7=save_file(form_medicao.documento_7.data),
                documento_8=save_file(form_medicao.documento_8.data),
                documento_9=save_file(form_medicao.documento_9.data),
                documento_10=save_file(form_medicao.documento_10.data),
                documento_10_1=save_file(form_medicao.documento_10_1.data),
                documento_11=save_file(form_medicao.documento_11.data),
                documento_12=save_file(form_medicao.documento_12.data),
                documento_13=save_file(form_medicao.documento_13.data),
                documento_14=save_file(form_medicao.documento_14.data),
                documento_15=save_file(form_medicao.documento_15.data),
                documento_15_1=save_file(form_medicao.documento_15_1.data),
                documento_15_2=save_file(form_medicao.documento_15_2.data),
                documento_15_3=save_file(form_medicao.documento_15_3.data),
                documento_15_4=save_file(form_medicao.documento_15_4.data),
                documento_15_5=save_file(form_medicao.documento_15_5.data),
                documento_16=save_file(form_medicao.documento_16.data),
                documento_17=save_file(form_medicao.documento_17.data),
                documento_18=save_file(form_medicao.documento_18.data),
                documento_19=save_file(form_medicao.documento_19.data)
            )

            # Cria uma nova instância de Medicao_resumida
            medicao_resumida = Medicao_resumida(
                obra=form_medicao.projeto_nome.data,
                data_inicio_medicao=form_medicao.data_inicial.data,
                data_fim_medicao=form_medicao.data_final.data,
                numero_medicao=form_medicao.numero_medicao.data,
                valor_medicao=form_medicao.valor.data,
                letra_medicao=form_medicao.numero_medicao.data,
                reajustamento=form_medicao.reajustamento.data
            )
            
            # Adiciona a medição ao banco de dados
            database.session.add(medicao1)
            database.session.add(medicao_resumida)
            database.session.commit()

            flash('Medição cadastrada com sucesso!', 'alert-success')
            return redirect(url_for('administrador'))

        except Exception as e:
            flash(f'Ocorreu um erro ao enviar a tarefa para o Celery: {str(e)}', 'danger')
            db.session.rollback()

    else:
        if request.method == 'POST':
            flash('Erro ao enviar o formulário. Verifique todos os campos obrigatórios.', 'danger')

    return render_template('medicao.html', form_medicao=form_medicao)
    
@app.route('/usuario/medicao2', methods=['GET', 'POST'])
@login_required
def medicao2():
    if request.method == 'POST':
        # Captura o projeto selecionado pelo usuário
        projeto_nome = request.form.get('projeto_nome')
        # Busca os números de medição associados ao projeto
        numeros_medicao = Medicao.query.filter(Medicao.projeto_nome == projeto_nome).all()
        return render_template(
            'medicao2_resultados.html', 
            projeto_nome=projeto_nome, 
            numeros_medicao=numeros_medicao
        )

    # Exibe opções únicas de `projeto_nome` para seleção inicial
    projetos = Medicao.query.with_entities(Medicao.projeto_nome).distinct().all()
    return render_template('medicao2.html', projetos=projetos)


@app.route('/usuario/medicao2/detalhes/<int:id>', methods=['GET'])
@login_required
def medicao2_detalhes(id):
    # Busca detalhes da medição específica
    medicao = Medicao.query.get_or_404(id)

    # Ajusta o caminho dos documentos para servir via a pasta `static`
    base_url = '/static'  # Caminho usado para servir arquivos na web
    medicao.documento_1 = f"{base_url}/{medicao.documento_1}"  # 1 - Carta assinada pela empresa
    medicao.documento_2 = f"{base_url}/{medicao.documento_2}"  # 2 - Publicação da Comissão de Fiscalização
    medicao.documento_3 = f"{base_url}/{medicao.documento_3}"  # 3 - Planilha de Medição (PDF)
    medicao.documento_3_1 = f"{base_url}/{medicao.documento_3_1}"  # 3.1 - Planilha de Medição - Arquivo em Excel
    medicao.documento_4 = f"{base_url}/{medicao.documento_4}"  # 4 - Memória de Cálculo
    medicao.documento_5 = f"{base_url}/{medicao.documento_5}"  # 5 - Cronograma Físico - Financeiro
    medicao.documento_6 = f"{base_url}/{medicao.documento_6}"  # 6 - Diário de Obras
    medicao.documento_7 = f"{base_url}/{medicao.documento_7}"  # 7 - Relatório Fotográfico
    medicao.documento_8 = f"{base_url}/{medicao.documento_8}"  # 8 - Relação de Funcionários
    medicao.documento_9 = f"{base_url}/{medicao.documento_9}"  # 9 - Folha de ponto dos funcionários
    medicao.documento_10 = f"{base_url}/{medicao.documento_10}"  # 10 - GFD FGTS DIGITAL
    medicao.documento_10_1 = f"{base_url}/{medicao.documento_10_1}"  # 10.1 - DCTF WEB
    medicao.documento_11 = f"{base_url}/{medicao.documento_11}"  # 11 - Guias e Comprovantes de Pagamentos de FGTS
    medicao.documento_12 = f"{base_url}/{medicao.documento_12}"  # 12 - Folha de Pagamento
    medicao.documento_13 = f"{base_url}/{medicao.documento_13}"  # 13 - Comprovante de Pagamento de salários
    medicao.documento_14 = f"{base_url}/{medicao.documento_14}"  # 14 - Plano de segurança do Trabalho
    medicao.documento_15 = f"{base_url}/{medicao.documento_15}"  # 15 - Certidões atualizadas
    medicao.documento_15_1 = f"{base_url}/{medicao.documento_15_1}"  # 15.1 - Certidão de regularidade junto ao FGTS
    medicao.documento_15_2 = f"{base_url}/{medicao.documento_15_2}"  # 15.2 - Certidão negativa de débito trabalhista
    medicao.documento_15_3 = f"{base_url}/{medicao.documento_15_3}"  # 15.3 - Certidão negativa de débitos federais
    medicao.documento_15_4 = f"{base_url}/{medicao.documento_15_4}"  # 15.4 - Certidão de regularidade fiscal junto ao ICMS
    medicao.documento_15_5 = f"{base_url}/{medicao.documento_15_5}"  # 15.5 - Certidão de regularidade fiscal junto ao ISS
    medicao.documento_16 = f"{base_url}/{medicao.documento_16}"  # 16 - Contrato
    medicao.documento_17 = f"{base_url}/{medicao.documento_17}"  # 17 - ART emitida pelo CREA
    medicao.documento_18 = f"{base_url}/{medicao.documento_18}"  # 18 - Nota de empenho
    medicao.documento_19 = f"{base_url}/{medicao.documento_19}"  # 19 - Nota fiscal e ISS

    # Busca a obra associada com base no projeto_nome da medição
    obra = Obras.query.filter_by(obra=medicao.projeto_nome).first()

    return render_template('medicao2_detalhes.html', medicao=medicao, obra=obra)

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

@app.route('/sobre')
@login_required
def sobre():
    return render_template('sobre.html')


@app.route('/noticias')
@login_required
def noticias():
    # Consulta para pegar as 20 últimas medições ordenadas por data_criacao
    ultimas_medicoes = Medicao.query.order_by(Medicao.data_criacao.desc()).limit(20).all()

    # Formatar os dados para exibição no template
    noticias = [
        {
            "projeto_nome": medicao.projeto_nome,
            "numero_medicao": medicao.numero_medicao,
            "valor_formatado": f"{medicao.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        }
        for medicao in ultimas_medicoes
    ]

    return render_template('noticias.html', noticias=noticias)

