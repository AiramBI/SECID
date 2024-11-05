import logging
import os
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import requests  # para fechar sessão via requisição HTTP DELETE
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Variáveis de login
login = os.getenv("LOGIN", "asantos2")
senha = os.getenv("SENHA", "Ivinhema1994#*#*#*")

def executarautomacao():
    session_id = None  # Para armazenar o ID da sessão e garantir que podemos fechar depois
    
    try:
        logging.info("Iniciando o Selenium...")
    
        # Configuração para o servidor Selenium remoto no Railway
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        grid_url = "http://standalone-chrome-production-1308.up.railway.app:4444/wd/hub"
        navegador = webdriver.Remote(command_executor=grid_url,options=options)
        
        
        # INICIO BLOCO DE LOGIN
           
        # Acessando a página de login do SEI
        navegador.get("https://sei.rj.gov.br/sip/login.php?sigla_orgao_sistema=ERJ&sigla_sistema=SEI")
        # Localizando o campo de usuário e inserindo o login
        usuario = navegador.find_element(By.XPATH, '//*[@id="txtUsuario"]')
        usuario.send_keys(login)
        # Localizando o campo de senha e inserindo a senha
        campoSenha = navegador.find_element(By.XPATH, '//*[@id="pwdSenha"]')
        campoSenha.send_keys(senha)
        # Selecionando o órgão 'SEFAZ' na lista suspensa
        exercicio = Select(navegador.find_element(By.XPATH, '//*[@id="selOrgao"]'))
        exercicio.select_by_visible_text(secretaria)
        # Clicando no botão de login
        btnLogin = navegador.find_element(By.XPATH, '//*[@id="Acessar"]')
        btnLogin.click()
    
        #VERIFICAÇÃO SE TEM ALGUMA POPUP
    
        # Maximizar a janela do navegador
        navegador.maximize_window()
        time.sleep(1)
        botao_fechar = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//img[@title='Fechar janela (ESC)']")))
        # Encontre o elemento do botão de fechar
        botao_fechar.click()
    
        #INICIO DO BLOCO DE PROCURAR UM PROCESSO
        # PROCURAR PROCESSO
        procurar_processo = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="txtPesquisaRapida"]'))
        )
        procurar_processo.send_keys('SEI-040009/000654/2024' + Keys.ENTER)
    
        # Alterna para o iframe "ifrVisualizacao" e espera que ele esteja disponível
        WebDriverWait(navegador, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao"))
        )
        # Aguarda o elemento "Iniciar Processo Relacionado" estar clicável dentro do iframe
        iniciar_processo_relacionado = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//img[@alt='Iniciar Processo Relacionado']"))
        )
        iniciar_processo_relacionado.click()
    
        # Iniciar Processo Relacionado Financeiro Pagamento
        financeiro_pagamento = WebDriverWait(navegador, 5).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Financeiro: Pagamento"))
        )
        financeiro_pagamento.click()
    
        # Escrever especificação
        especificacao = WebDriverWait(navegador, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="txtDescricao"]'))
        )
        especificacao.send_keys(especificacao_processo)
    
        #Observações desta Unidade
        observacoes = navegador.find_element(By.XPATH, '//*[@id="txaObservacoes"]')
        observacoes.send_keys(observacoes_processo)
    
        #Nivel de Acesso(Publico)
        nivel_acesso = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lblPublico"]')))
        nivel_acesso.click()
    
        botao_salvar = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.ID, "btnSalvar")))
        botao_salvar.click()
    
        for nome in nomes_documentos:
            #UPLOAD DE DOCUMENTOS
            campo_clicavel = navegador.switch_to.default_content()
            campo_clicavel2 = WebDriverWait(navegador,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
            incluir_documento = WebDriverWait(navegador,10).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt = 'Incluir Documento']")))
            incluir_documento.click()
            upload_documento = navegador.find_element(By.LINK_TEXT, "Externo")
            upload_documento.click()
    
    
            #TIPO DE DOCUMENTO
            tipo_documento = navegador.find_element(By.XPATH, '//*[@id="selSerie"]')
            tipo_documento.send_keys('Anexo')
    
            #DataDocumento
            data_documento = navegador.find_element(By.XPATH, '//*[@id="txtDataElaboracao"]')
            data_documento.send_keys(hoje())
    
            #Nome Documento
            nome_documento = navegador.find_element(By.XPATH, '//*[@id="txtNumero"]')
            nome_documento.clear()
            nome_documento.send_keys(nome)
    
            #Formato (Digitalizado nesta Unidade)
            formato = navegador.find_element(By.XPATH, "//label[@for='optDigitalizado']")
            formato.click()
    
            formato = navegador.find_element(By.XPATH, '//*[@id="selTipoConferencia"]')
            formato.send_keys('Cópia Simples')
    
            #Nivel de Acesso(Publico)
            label_element = navegador.find_element(By.XPATH, "//label[@for='optPublico']")
            label_element.click()
    
            caminho_arquivo = "/app/static/seu_arquivo.pdf"
    
            # Localize o campo de upload e envie o caminho do arquivo
            campo_upload = navegador.find_element(By.ID, "filArquivo")
            campo_upload.send_keys(caminho_arquivo)
    
            # Aguarda o elemento "Remover Item" aparecer na página
            WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, "//img[@title='Remover Item']"))
            )
    
            # Depois que o elemento "Remover Item" aparece, clica no botão Salvar
            botao_salvar = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.ID, "btnSalvar"))
            )
            botao_salvar.click()
            
        #INICIO DO BLOCO DE PROCESSO RELACIONADO
    
        #INCLUIR NOTA TÉCNICA
        
        #UPLOAD DE DOCUMENTOS
        campo_clicavel = navegador.switch_to.default_content()
        campo_clicavel2 = WebDriverWait(navegador,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
        incluir_documento = WebDriverWait(navegador,10).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt = 'Incluir Documento']")))
        incluir_documento.click()
        upload_documento = navegador.find_element(By.LINK_TEXT, "Nota Técnica")
        upload_documento.click()
    
        #Texto_inicial
        texto_inicial = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lblProtocoloDocumentoTextoBase"]')))
        texto_inicial.click()
        texto_inicia_padrao = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtProtocoloDocumentoTextoBase"]')))
        texto_inicia_padrao.send_keys("86822754")
    
        # Escrever especificação
        #especificacao = WebDriverWait(navegador, 5).until(
        #    EC.element_to_be_clickable((By.XPATH, '//*[@id="txtDescricao"]'))
        #)
        #especificacao.send_keys(especificacao_processo)
    
        #Observações desta Unidade
        #observacoes = navegador.find_element(By.XPATH, '//*[@id="txaObservacoes"]')
        #observacoes.send_keys(observacoes_processo)
    
        #Nivel de Acesso(Publico)
        nivel_acesso = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lblPublico"]')))
        nivel_acesso.click()
    
        botao_salvar = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.ID, "btnSalvar")))
        botao_salvar.click()
    
        #EDITAR DOCUMENTO
        #campo_clicavel = navegador.switch_to.default_content()
        #campo_clicavel2 = WebDriverWait(navegador,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
        #incluir_documento = WebDriverWait(navegador,10).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt = 'Incluir Documento']")))
        #incluir_documento.click()
        #maximizar Janela
        #janela_original = navegador.current_window_handle
    
        # Alterna para a última janela aberta (a popup)
        #for handle in navegador.window_handles:
        #    if handle != janela_original:
        #        navegador.switch_to.window(handle)
        #        break    
        #navegador.maximize_window()
    
    
    
    
        #INCLUIR CHECKLIST
        
        #UPLOAD DE DOCUMENTOS
        campo_clicavel = navegador.switch_to.default_content()
        campo_clicavel2 = WebDriverWait(navegador,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
        incluir_documento = WebDriverWait(navegador,10).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt = 'Incluir Documento']")))
        incluir_documento.click()
        nivel_acesso = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt = 'Exibir todos os tipos']")))
        nivel_acesso.click()
        upload_documento = navegador.find_element(By.LINK_TEXT, "Checklist")
        upload_documento.click()
    
        #Texto_inicial
        texto_inicial = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lblProtocoloDocumentoTextoBase"]')))
        texto_inicial.click()
        texto_inicia_padrao = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtProtocoloDocumentoTextoBase"]')))
        texto_inicia_padrao.send_keys("86828862")
    
        # Escrever especificação
        #especificacao = WebDriverWait(navegador, 5).until(
        #    EC.element_to_be_clickable((By.XPATH, '//*[@id="txtDescricao"]'))
        #)
        #especificacao.send_keys(especificacao_processo)
    
        #Observações desta Unidade
        #observacoes = navegador.find_element(By.XPATH, '//*[@id="txaObservacoes"]')
        #observacoes.send_keys(observacoes_processo)
    
        #Nivel de Acesso(Publico)
        nivel_acesso = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lblPublico"]')))
        nivel_acesso.click()
    
        botao_salvar = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.ID, "btnSalvar")))
        botao_salvar.click()
    
    
        # Fecha o navegador
        navegador.quit()
        logging.info("Navegador fechado, automação concluída.")

    except Exception as e:
        logging.error(f"Ocorreu um erro: {traceback.format_exc()}")
        navegador.quit()
    

