from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time, traceback, logging, os, re
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from num2words import num2words



def registrar_medicao(coordenacao,observacoes_processo,caminho_arquivo,data_inicial, data_final, valor_total_prervisto, valor_atual_previsto, valor_total_inicial, valor_atual_inicial, valor_atual_medido, aditivo,inicial, numero_contrato, numero_medicao, cronograma_atualizado, reajustamento, reajustamento_total,valor_medicao
medicoes, rerratificacao,processo_mae, objeto, documento_gestor_contrato, publicacao_comissao_fiscalização, lei_contrato,contrato,seguro_garantia,carta_solicitacao_prorrogacao_contratual,processo_rerratificacao,termo_aditivo,contratada,obra, fiscal_tecnico_1,id_fiscal_tecnico_1,fiscal_tecnico_2,id_fiscal_tecnico_2, gestor1,
id_gestor,cnpj_empresa):
    login = os.getenv("LOGIN", "asantos2") #PRECISO MEXER NISSO ANTES DE IMPLEMENTAR VALORES FIXOS
    senha = os.getenv("SENHA", "Ivinhema1994#*#*#*") #PRECISO MEXER NISSO ANTES DE IMPLEMENTAR VALORES FIXOS
    secretaria = os.getenv("SECRETARIA","SEFAZ")  #PRECISO MEXER NISSO ANTES DE IMPLEMENTAR VALORES FIXOS
    coordenacao = "SEFAZ/COOCPP" 
    observacoes_processo = os.getenv("OBSERVACOES_PROCESSO","") #ATÉ O MOMENTO NÃO TEM ATRIBUIÇÃO
    nomes_documentos = [
        "01.Carta assinada pela empresa","02.Publicação da Comissão de Fiscalização","03.Planilha de Medição (PDF)","03.1.Planilha de Medição - Arquivo em Excel",
        "04.Memória de Cálculo","05.Cronograma Físico - Financeiro","06.Diário de Obras","07.Relatório Fotográfico",
        "08.Relação de Funcionários","09.Folha de ponto dos funcionários","10.GFD FGTS DIGITAL","10.1.DCTF WEB","11.Guias e Comprovantes de Pagamentos de FGTS",
        "12.Folha de Pagamento","13.Comprovante de Pagamento de salários","14.Plano de segurança do Trabalho","15.Certidões atualizadas","15.1.Certidão de regularidade junto ao FGTS","15.2.Certidão negativa de débito trabalhista",
        "15.3.Certidão negativa de débitos federais","15.4.Certidão de regularidade fiscal junto ao ICMS","15.5.Certidão de regularidade fiscal junto ao ISS","16.Contrato",
        "17.ART emitida pelo CREA","18.Nota de empenho","19.Nota fiscal e ISS"]
    periodo_medicao = f"'{data_inicial}' a '{data_final}'"
    porcentagem_concluida_previsto = valor_atual_previsto/valor_total_previsto
    porcentagem_concluida_inicial = valor_atual_inicial/valor_total_inicial
    porcentagem_concluida_medida = valor_atual_medido/valor_total_previsto
    prazo_aditivo = f"'{aditivo}' ('{num2words(aditivo, lang ='pt_BR')}"
    prazo_inicial = f"'{inicial}' ('{num2words(inicial, lang ='pt_BR')}" 
      
    especificacao_processo = f"'{numero_medicao}'ª Medição - Obra:'{obra}' - Período:'{periodo_medicao}'"
    carimbo_fiscal1 = f"{fiscal_tecnico_1}\nFiscal Técnico\n{id_fiscal_tecnico_1}"
    carimbo_fiscal2 = f"{fiscal_tecnico_2}\nFiscal Técnico\n{id_fiscal_tecnico_2}"
    carimbo_gestor = f"{gestor1}\nGestor do Contrato\n{id_gestor}"
    
    def  indexar_checklist_1():
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']"))
        )
        
    def  indexar_checklist_2():    
        navegador.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
        time.sleep(1)
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
        navegador.switch_to.frame(iframes[2])
        corpoTexto.send_keys(Keys.PAGE_UP*2,Keys.ARROW_UP)
    
    def hoje():
        return datetime.now().strftime("%d/%m/%Y")  # Exemplo de formato: 04/11/2024
    def registrar_medicao():
        pass
    
    try:
        logging.info("Iniciando o Selenium...")
    
        # Configuração para o servidor Selenium remoto no Railway
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        grid_url = 'https://standalone-chrome-production-1308.up.railway.app/wd/hub'
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
    
    
        coordenacao_atual = navegador.find_elements(By.XPATH, "//a[@id = 'lnkInfraUnidade']")[1]
        if coordenacao_atual.get_attribute("innerHTML") != coordenacao:
            coordenacao_atual.click()
            WebDriverWait(navegador,5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Trocar Unidade')]")))
            navegador.find_element(By.XPATH, "//td[text() = '"+coordenacao+"' ]").click() 
    
        #INICIO DO BLOCO DE PROCURAR UM PROCESSO
        # PROCURAR PROCESSO
        procurar_processo = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="txtPesquisaRapida"]'))
        )
        procurar_processo.send_keys('SEI-040009/000654/2024' + Keys.ENTER)
    
    
        #INICIO DO BLOCO DE PROCESSO RELACIONADO
    
        #INICIAR PROCESSO RELACIONADO
    
        
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
    
        for nome, caminhoarquivo in zip(nomes_documentos, caminho_arquivo):
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
    
            # Localize o campo de upload e envie o caminho do arquivo
            campo_upload = navegador.find_element(By.ID, "filArquivo")
            campo_upload.send_keys(caminhoarquivo)
    
            # Aguarda o elemento "Remover Item" aparecer na página
            WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, "//img[@title='Remover Item']"))
            )
    
            # Depois que o elemento "Remover Item" aparece, clica no botão Salvar
            botao_salvar = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.ID, "btnSalvar"))
            )
            botao_salvar.click()
            try:
                time.sleep(0.5)
                alert = Alert(navegador)
                alert.accept()
            except:
                pass
    
    
        # Alterna para o iframe "ifrVisualizacao" e espera que ele esteja disponível
        #WebDriverWait(navegador, 10).until(
        #    EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao"))
        #)
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
    
        WebDriverWait(navegador, 10).until(lambda d: len(navegador.window_handles) > 1)
    
        # Alterna para a nova janela
        navegador.switch_to.window(navegador.window_handles[1])
    
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
    
    
        navegador.switch_to.frame(iframes[2])
            
        corpoTexto = navegador.find_element(By.TAG_NAME, 'body')
        corpoTexto.click()
    
        #Movimenta o cursor até o início do texto
        corpoTexto.send_keys(Keys.PAGE_UP *2)
        time.sleep(2)
        #Movimenta o cursor até o início do texto localizado numero do contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 1472)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *8)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(numero_contrato)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia inicio e fim medicao
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 1435)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *23)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(periodo_medicao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia numero da medicao
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 1400)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *2)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(numero_medicao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia Cronograma Atualizado
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 1278)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *5)
        corpoTexto.send_keys(Keys.DELETE)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_181']").click()
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']"))
        )
        input_field.send_keys(cronograma_atualiado)
        navegador.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
        time.sleep(1)
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
        navegador.switch_to.frame(iframes[2])
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia % concluida previsto atualizado
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 1145)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *3)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(porcentagem_concluida_previsto)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia R$ previsto atualizado
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 1127)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *3)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(valor_atual_previsto)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia % CRONOGRAMA inicial
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 1044)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *3)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(porcentagem_concluida_inicial)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia R$ CRONOGRAMA inicial
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 1021)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *4)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(valor_atual_inicial)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia % medido com relação ao total do contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 909)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *2)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(porcentagem_concluida_medida)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
        
        #Movimenta o cursor até o início do texto localizado Referencia R$ medido com relação ao total do contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 887)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *4)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(valor_atual_medido)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia R$ valor reajustamento
        if reajustamento == 0:
            corpoTexto.send_keys(Keys.ARROW_RIGHT * 818)
            corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *33)
            corpoTexto.send_keys(Keys.DELETE)
        else:
            corpoTexto.send_keys(Keys.ARROW_RIGHT * 845)
            corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *4)
            corpoTexto.send_keys(Keys.DELETE)
            corpoTexto.send_keys(reajustamento)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia R$ valor da medição atual
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 821)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *6)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(valor_medicao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia data da medição
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 781)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *23)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(periodo_medicao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia numero da medição
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 762)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *1)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(numero_medicao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia numero da medição
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 760)
        corpoTexto.send_keys(Keys.ENTER)# alterar essa parte
        medicoes= [
        "1ª Medição período 01/09/2022 a 30/09/2022 no valor de R$ 668.194,70;",
        "2ª Medição período 01/10/2022 a 31/10/2022 no valor de R$ 0,00;",
        "3ª Medição período 01/11/2022 a 30/11/2022 no valor de R$ 0,00;",
        "4ª Medição período 01/12/2022 a 31/12/2022 no valor de R$ 0,00;",
        "5ª Medição período 01/01/2023 a 31/01/2023 no valor de R$ 1.448.169,70;",
        "6ª Medição período 01/02/2023 a 28/02/2023 no valor de R$ 600.039,67;",
        "7ª Medição período 01/03/2023 a 31/03/2023 no valor de R$ 1.010.519,04;",
        "8ª Medição período 01/04/2023 a 30/04/2023 no valor de R$ 1.168.928,91;",
        "9º Medição período 01/05/2023 a 31/05/2023 no valor de R$ 802.372,34;",
        "10º Medição período 01/06/2023 a 30/06/2023 no valor de R$ 479.811,71;",
        "11º Medição período 01/07/2023 a 31/07/2023 no valor de R$ 128.692,36;",
        "12º Medição período 01/08/2023 a 31/08/2023 no valor de R$ 0,00;",
        "13º Medição período 01/09/2023 a 30/09/2023 no valor de R$ 0,00;",
        "14º Medição período 01/10/2023 a 31/10/2023 no valor de R$ 0,00;",
        "15º Medição período 01/11/2023 a 30/11/2023 no valor de R$ 0,00;",
        "16º Medição período 01/12/2023 a 31/12/2023 no valor de R$ 0,00;",
        "17º Medição período 01/01/2024 a 31/01/2024 no valor de R$ 15.694,77;",
        "18º Medição período 01/02/2024 a 29/02/2024 no valor de R$ 15.271,67;",
        "19º Medição período 01/03/2024 a 31/03/2024 no valor de R$ 27.149,67;",
        "20º Medição período 01/04/2024 a 30/04/2024 no valor de R$ 140.839,20;",
        "21º Medição período 01/05/2024 a 31/05/2024 no valor de R$ 54.299,40;",
        "22º Medição período 01/06/2024 a 30/06/2024 no valor de R$ 74.661,72;",
        "23º Medição período 01/07/2024 a 31/07/2024 no valor de R$ 81.449,13;",
        "24º Medição período 01/08/2024 a 31/08/2024 no valor de R$ 149.323,51;"
    ]
        for medicao in medicoes:
            corpoTexto.send_keys(medicao)
            corpoTexto.send_keys(Keys.SHIFT,Keys.ENTER)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado valor total do contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 727)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *8)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(valor_total_previsto)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado rerratificação
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 692)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *6)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(rerratificacao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado reajuste
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 663)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *9)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(reajustemento_total)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado valor inicial contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 640)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *9)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(valor_total_inicial)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado prazo contrato aditivo
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 572)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *12)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(prazo_aditivo)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado prazo contrato inicial 
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 532)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *11)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(prazo_inicial)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia processo mãe
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 511)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *13)
        corpoTexto.send_keys(Keys.DELETE)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_181']").click()
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']"))
        )
        input_field.send_keys(processo_mae) # processo inicial
        navegador.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
        time.sleep(1)
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
        navegador.switch_to.frame(iframes[2])
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado numero do contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 505)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *5)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(numero_contrato)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
        
        #Movimenta o cursor até o início do texto localizado objeto do contrato em maiuscula
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 449)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *50)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(objeto)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia DOCUMENTO GESTOR DO CONTRATO
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 237)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *3)
        corpoTexto.send_keys(Keys.DELETE)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_181']").click()
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']"))
        )
        input_field.send_keys(documento_gestor_contrato) # DOCUMENTO GESTOR DO CONTRATO
        navegador.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
        time.sleep(1)
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
        navegador.switch_to.frame(iframes[2])
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado objeto do DOCUMENTO GESTOR DO CONTRATO PUBLICACAO
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 187)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *32)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(publicacao_comissao_fiscalização)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado objeto do LEI DO CONTRATO 14.133 OU 8.666
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 23)
        corpoTexto.send_keys(Keys.SHIFT,Keys.ARROW_RIGHT *30)
        corpoTexto.send_keys(Keys.DELETE)
        corpoTexto.send_keys(lei_contrato)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o final do texto e insere carimbo
        corpoTexto.send_keys(Keys.PAGE_DOWN *2)
        corpoTexto.send_keys(Keys.DOWN)
        corpoTexto.send_keys(Keys.ENTER)
        corpoTexto.send_keys(carimbo_fiscal1)
        corpoTexto.send_keys(Keys.ENTER*2)
        corpoTexto.send_keys(carimbo_fiscal2)
    
        time.sleep(5)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_145']").click()
            
        time.sleep(5)
    
        #fechar navegador
        navegador.close()
    
        navegador.switch_to.window(navegador.window_handles[0])
        #Mudar para o contexto da arvore
        navegador.switch_to.default_content()
        WebDriverWait(navegador,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvore")))
        listaDocs = WebDriverWait(navegador,5).until(EC.presence_of_element_located((By.ID, "divArvore")))
        pastas = listaDocs.find_elements(By.XPATH, '//a[contains(@id, "joinPASTA")]//img[contains(@title, "Abrir")]')
        
        #Abrir todas as pastas que existam
        for doc in pastas:
            doc.click() 
            WebDriverWait(navegador,5).until(EC.presence_of_element_located((By.XPATH, "//*[text() = 'Aguarde...']")))
            WebDriverWait(navegador,5).until(EC.invisibility_of_element((By.XPATH, "//*[text() = 'Aguarde...']")))
    
        # XPath para buscar o elemento pelo texto (dentro do propio processo)
        processo_atual_elemento = navegador.find_element(By.XPATH,f"//span[contains(text(), 'SEI-')]").text
        nota_tecnica_elemento = navegador.find_element(By.XPATH,f"//span[contains(text(), 'Nota Técnica')]").text
        diario_de_obra_elemento = navegador.find_element(By.XPATH,f"//span[contains(text(), 'Anexo 06.Diário de Obras')]").text
        cronograma_fisico_financeiro_elemento = navegador.find_element(By.XPATH,f"//span[contains(text(), 'Anexo 05.Cronograma Físico - Financeiro')]").text
        nota_fiscal_elemento = navegador.find_element(By.XPATH,f"//span[contains(text(), 'Anexo 19.Nota fiscal e ISS')]").text
        comissao_fiscalizacao_elemento = navegador.find_element(By.XPATH,f"//span[contains(text(), 'Anexo 02.Publicação da Comissão de Fiscalização')]").text
    
        # Nomeação das Variaveis no processo
        processo_atual = processo_atual_elemento
        nota_tecnica = re.search(r'Nota Técnica\s+(\d+)', nota_tecnica_elemento).group(1)
        diario_de_obra = re.findall(r"\((\d+)\)", diario_de_obra_elemento)[0]
        cronograma_fisico_financeiro = re.findall(r"\((\d+)\)", cronograma_fisico_financeiro_elemento)[0]
        nota_fiscal = re.findall(r"\((\d+)\)", nota_fiscal_elemento)[0]
        comissao_fiscalizacao = re.findall(r"\((\d+)\)", comissao_fiscalizacao_elemento)[0]
    
    
    
        time.sleep(1)
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
    
        time.sleep(5)
    
        WebDriverWait(navegador, 10).until(lambda d: len(navegador.window_handles) > 1)
    
        # Alterna para a nova janela
        navegador.switch_to.window(navegador.window_handles[1])
    
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
    
    
        navegador.switch_to.frame(iframes[2])
            
        corpoTexto = navegador.find_element(By.TAG_NAME, 'body')
        corpoTexto.click()
    
        #Movimenta o cursor até o início do texto
        corpoTexto.send_keys(Keys.PAGE_UP *2)
        time.sleep(2)
        
        #Movimenta o cursor até o início do texto localizado (37 - processo Matriz)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 8805)
        indexar_checklist_1()
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(processo_mae)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (36 - processo Matriz)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 8508)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(processo_mae)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (35 - comissao)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 8379)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(comissao_fiscalizacao)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (32 - processo atual)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 7768)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(processo_atual)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (31 - processo atual)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 7184)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(processo_atual)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (30 - termo aditivo)
        if termo_aditivo == 0:
            pass
        else:
            corpoTexto.send_keys(Keys.ARROW_RIGHT * 6990)
            navegador.switch_to.default_content()
            navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
            WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
            input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
            input_field.send_keys(termo_aditivo)
            indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (29 - diario de obra)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 6760)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(diario_de_obra)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (26 - processo atual)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 5851)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(processo_atual)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (25 - processo rerratificacao)
        if processo_rerratificacao ==0:
            pass
        else:
            corpoTexto.send_keys(Keys.ARROW_RIGHT * 5695)
            navegador.switch_to.default_content()
            navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
            WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
            input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
            input_field.send_keys(processo_rerratificacao)
            indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (22 nota fiscal)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 4844)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(nota_fiscal)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (18 Carta de Solicitação de Prorrogação contratual)
        if carta_solicitacao_prorrogacao_contratual == 0:
            pass
        else:
            corpoTexto.send_keys(Keys.ARROW_RIGHT * 3923)
            navegador.switch_to.default_content()
            navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
            WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
            input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
            input_field.send_keys(carta_solicitacao_prorrogacao_contratual)
            indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (17 Carta de Solicitação de Prorrogação contratual)
        if carta_solicitacao_prorrogacao_contratual == 0:
            pass
        else:
            corpoTexto.send_keys(Keys.ARROW_RIGHT * 3748)
            navegador.switch_to.default_content()
            navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
            WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
            input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
            input_field.send_keys(carta_solicitacao_prorrogacao_contratual)
            indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (16 Carta de Solicitação de Prorrogação contratual)
        if carta_solicitacao_prorrogacao_contratual == 0:
            pass
        else:
            corpoTexto.send_keys(Keys.ARROW_RIGHT * 3570)
            navegador.switch_to.default_content()
            navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
            WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
            input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
            input_field.send_keys(carta_solicitacao_prorrogacao_contratual)
            indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (15 cronograma fisico financeiro)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 3364)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(cronograma_fisico_financeiro)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (12 diario de obras)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 2466)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(diario_de_obra)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (11 seguro garantia)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 2302)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(seguro_garantia)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (10 seguro garantia)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 2094)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(seguro_garantia)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (9 nota tecnica)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 1874)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(nota_tecnica)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (8 nota tecnica)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 1681)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(nota_tecnica)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (7 nota tecnica)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 1504)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(nota_tecnica)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (6 processo atual)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 1294)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(processo_atual)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (5 processo atual)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 1145)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(processo_atual)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (3 processo mae)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 884)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(processo_mae)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (2 processo atual)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 737)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(processo_atual)
        indexar_checklist_2()
    
        #Movimenta o cursor até o início do texto localizado (1 contrato)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 605)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field.send_keys(contrato)
        indexar_checklist_2()
    
        
        #Movimenta o cursor até o início do texto localizado objeto
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 193)
        corpoTexto.send_keys(objeto)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado (contratada)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 185)
        corpoTexto.send_keys(contratada)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado (processo mae)
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 172)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']"))
        )
        input_field.send_keys(processo_mae)
        navegador.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
        time.sleep(1)
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
        navegador.switch_to.frame(iframes[2])
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
    
        corpoTexto.send_keys(Keys.PAGE_DOWN *2)
        corpoTexto.send_keys(Keys.DOWN)
        corpoTexto.send_keys(Keys.ENTER)
        corpoTexto.send_keys(carimbo_gestor)
    
        
        #SALVA ALTERAÇOES
        time.sleep(5)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_149']").click()
            
        time.sleep(5)
        #fechar navegador
        navegador.close()
    
        navegador.switch_to.window(navegador.window_handles[0])
    
        # Alterna para o iframe "ifrVisualizacao" e espera que ele esteja disponível
        WebDriverWait(navegador, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao"))
        )
        
        #INCLUIR Despacho Gestor
        
        #UPLOAD DE DOCUMENTOS
        campo_clicavel = navegador.switch_to.default_content()
        campo_clicavel2 = WebDriverWait(navegador,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
        incluir_documento = WebDriverWait(navegador,10).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt = 'Incluir Documento']")))
        incluir_documento.click()
        upload_documento = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Despacho de Encaminhamento de Processo")))
        upload_documento.click()
    
        #Texto_inicial
        texto_inicial = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lblProtocoloDocumentoTextoBase"]')))
        texto_inicial.click()
        texto_inicia_padrao = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtProtocoloDocumentoTextoBase"]')))
        texto_inicia_padrao.send_keys("87936268")
    
        # Escrever especificação
        nome_arvore = WebDriverWait(navegador, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="txtNomeArvore"]'))
        )
        nome_arvore.send_keys("Gestor")
    
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
    
        time.sleep(5)
    
        WebDriverWait(navegador, 10).until(lambda d: len(navegador.window_handles) > 1)
    
        # Alterna para a nova janela
        navegador.switch_to.window(navegador.window_handles[1])
    
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
    
    
        navegador.switch_to.frame(iframes[2])
            
        corpoTexto = navegador.find_element(By.TAG_NAME, 'body')
        corpoTexto.click()
    
        #Movimenta o cursor até o início do texto
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado numero contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 292)
        corpoTexto.send_keys(numero_contrato)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 218)
        corpoTexto.send_keys(valor_medicao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
    
        #Movimenta o cursor até o início do texto localizado 
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 201)
        corpoTexto.send_keys(periodo_medicao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado numero contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 188)
        corpoTexto.send_keys(numero_contrato)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia processo mãe
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 174)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']"))
        )
        input_field.send_keys(processo_mae) # processo inicial
        navegador.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
        time.sleep(1)
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
        navegador.switch_to.frame(iframes[2])
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 153)
        corpoTexto.send_keys(cnpj_empresa)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
    
        #Movimenta o cursor até o início do texto localizado
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 134)
        corpoTexto.send_keys(contratada)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 105)
        corpoTexto.send_keys(objeto)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
    
        #Movimenta o cursor até o início do texto localizado
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 67)
        corpoTexto.send_keys(numero_medicao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        time.sleep(5)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_149']").click()
    
        
        #fechar navegador
        navegador.close()
    
        navegador.switch_to.window(navegador.window_handles[0])
    
        time.sleep(2)
        #Mudar para o contexto da arvore
        navegador.switch_to.default_content()
        WebDriverWait(navegador,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvore")))
        listaDocs = WebDriverWait(navegador,5).until(EC.presence_of_element_located((By.ID, "divArvore")))
        pastas = listaDocs.find_elements(By.XPATH, '//a[contains(@id, "joinPASTA")]//img[contains(@title, "Abrir")]')
        
        #Abrir todas as pastas que existam
        for doc in pastas:
            doc.click() 
            WebDriverWait(navegador,5).until(EC.presence_of_element_located((By.XPATH, "//*[text() = 'Aguarde...']")))
            WebDriverWait(navegador,5).until(EC.invisibility_of_element((By.XPATH, "//*[text() = 'Aguarde...']")))
    
        # XPath para buscar o elemento pelo texto (dentro do propio processo)
        despacho_gestor_elemento = navegador.find_element(By.XPATH,f"//span[contains(text(), 'Despacho de Encaminhamento de Processo Gestor')]").text
        despacho_checklist_elemento = navegador.find_element(By.XPATH,f"//span[contains(text(), 'Checklist')]").text
        nota_tecnica_elemento = navegador.find_element(By.XPATH,f"//span[contains(text(), 'Nota Técnica')]").text
        # Nomeação das Variaveis no processo
        despacho_gestor = re.findall(r"\((\d+)\)", despacho_gestor_elemento)[0]
        print(despacho_checklist_elemento)
        despacho_checklist = re.search(r'Checklist\s+(\d+)', despacho_checklist_elemento).group(1)
    
        
    
        #INCLUIR Despacho SUPERINTENDENTE
        
        #UPLOAD DE DOCUMENTOS
        campo_clicavel = navegador.switch_to.default_content()
        campo_clicavel2 = WebDriverWait(navegador,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
        incluir_documento = WebDriverWait(navegador,10).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt = 'Incluir Documento']")))
        incluir_documento.click()
        upload_documento = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Despacho de Encaminhamento de Processo")))
        upload_documento.click()
    
        #Texto_inicial
        texto_inicial = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lblProtocoloDocumentoTextoBase"]')))
        texto_inicial.click()
        texto_inicia_padrao = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtProtocoloDocumentoTextoBase"]')))
        texto_inicia_padrao.send_keys("87935581")
    
        # Escrever especificação
        nome_arvore = WebDriverWait(navegador, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="txtNomeArvore"]'))
        )
        nome_arvore.send_keys("Superintendente")
    
    
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
    
        time.sleep(5)
    
        WebDriverWait(navegador, 10).until(lambda d: len(navegador.window_handles) > 1)
    
        # Alterna para a nova janela
        navegador.switch_to.window(navegador.window_handles[1])
    
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
    
    
        navegador.switch_to.frame(iframes[2])
            
        corpoTexto = navegador.find_element(By.TAG_NAME, 'body')
        corpoTexto.click()
    
        #Movimenta o cursor até o início do texto
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
    
        #Movimenta o cursor até o início do texto localizado Referencia processo mãe
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 386)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']"))
        )
        input_field.send_keys(despacho_gestor) # processo inicial
        navegador.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
        time.sleep(1)
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
        navegador.switch_to.frame(iframes[2])
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia processo mãe
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 345)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']"))
        )
        input_field.send_keys(despacho_checklist) # processo inicial
        navegador.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
        time.sleep(1)
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
        navegador.switch_to.frame(iframes[2])
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia processo mãe
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 333)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']"))
        )
        input_field.send_keys(nota_tecnica) # processo inicial
        navegador.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
        time.sleep(1)
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
        navegador.switch_to.frame(iframes[2])
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
    
        #Movimenta o cursor até o início do texto localizado
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 235)
        corpoTexto.send_keys(valor_medicao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 218)
        corpoTexto.send_keys(periodo_medicao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
    
        #Movimenta o cursor até o início do texto localizado 
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 202)
        corpoTexto.send_keys(numero_contrato)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
    
        #Movimenta o cursor até o início do texto localizado Referencia processo mãe
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 188)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']"))
        )
        input_field.send_keys(processo_mae) # processo inicial
        navegador.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
        time.sleep(1)
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
        navegador.switch_to.frame(iframes[2])
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
    
        #Movimenta o cursor até o início do texto localizado numero contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 168)
        corpoTexto.send_keys(cnpj_empresa)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado numero contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 149)
        corpoTexto.send_keys(contratada)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado numero contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 120)
        corpoTexto.send_keys(objeto)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado numero contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 83)
        corpoTexto.send_keys(numero_medicao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        time.sleep(5)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_149']").click()
    
        #FECHAR ABA ATUAL
        navegador.close()
    
        navegador.switch_to.window(navegador.window_handles[0])
    
    
        #Mudar para o contexto da arvore
        navegador.switch_to.default_content()
        WebDriverWait(navegador,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvore")))
        listaDocs = WebDriverWait(navegador,5).until(EC.presence_of_element_located((By.ID, "divArvore")))
        pastas = listaDocs.find_elements(By.XPATH, '//a[contains(@id, "joinPASTA")]//img[contains(@title, "Abrir")]')
        
        #Abrir todas as pastas que existam
        for doc in pastas:
            doc.click() 
            WebDriverWait(navegador,5).until(EC.presence_of_element_located((By.XPATH, "//*[text() = 'Aguarde...']")))
            WebDriverWait(navegador,5).until(EC.invisibility_of_element((By.XPATH, "//*[text() = 'Aguarde...']")))
    
        # XPath para buscar o elemento pelo texto (dentro do propio processo)
        despacho_superintendente_elemento = navegador.find_element(By.XPATH,f"//span[contains(text(), 'Despacho de Encaminhamento de Processo Gestor')]").text
    
        # Nomeação das Variaveis no processo
        despacho_superintendente = re.findall(r"\((\d+)\)", despacho_superintendente_elemento)[0]
           
        #INCLUIR Despacho SUBSECRETARIO
        #UPLOAD DE DOCUMENTOS
        campo_clicavel = navegador.switch_to.default_content()
        campo_clicavel2 = WebDriverWait(navegador,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
        incluir_documento = WebDriverWait(navegador,10).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt = 'Incluir Documento']")))
        incluir_documento.click()
        upload_documento = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Despacho de Encaminhamento de Processo")))
        upload_documento.click()
    
        #Texto_inicial
        texto_inicial = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lblProtocoloDocumentoTextoBase"]')))
        texto_inicial.click()
        texto_inicia_padrao = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtProtocoloDocumentoTextoBase"]')))
        texto_inicia_padrao.send_keys("87935587")
    
    
        # Escrever especificação
        nome_arvore = WebDriverWait(navegador, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="txtNomeArvore"]'))
        )
        nome_arvore.send_keys("Subsecretário")
    
    
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
    
        time.sleep(5)
    
        WebDriverWait(navegador, 10).until(lambda d: len(navegador.window_handles) > 1)
    
        # Alterna para a nova janela
        navegador.switch_to.window(navegador.window_handles[1])
    
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
    
    
        navegador.switch_to.frame(iframes[2])
            
        corpoTexto = navegador.find_element(By.TAG_NAME, 'body')
        corpoTexto.click()
    
        #Movimenta o cursor até o início do texto
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
    
        #Movimenta o cursor até o início do texto localizado
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 425)
        corpoTexto.send_keys(valor_medicao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 408)
        corpoTexto.send_keys(periodo_medicao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
    
        #Movimenta o cursor até o início do texto localizado numero contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 392)
        corpoTexto.send_keys(objeto)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado numero contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 363)
        corpoTexto.send_keys(numero_contrato)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado numero contrato
        corpoTexto.send_keys(Keys.ARROW_RIGHT *327)
        corpoTexto.send_keys(numero_medicao)
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia processo mãe
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 259)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']"))
        )
        input_field.send_keys(despacho_gestor) # processo inicial
        navegador.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
        time.sleep(1)
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
        navegador.switch_to.frame(iframes[2])
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        #Movimenta o cursor até o início do texto localizado Referencia processo mãe
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 210)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']"))
        )
        input_field.send_keys(despacho_checklist) # processo inicial
        navegador.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
        time.sleep(1)
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
        navegador.switch_to.frame(iframes[2])
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
    
        #Movimenta o cursor até o início do texto localizado Referencia processo mãe
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 188)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']"))
        )
        input_field.send_keys(nota_tecnica) # processo inicial
        navegador.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
        time.sleep(1)
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
        navegador.switch_to.frame(iframes[2])
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
    
        #Movimenta o cursor até o início do texto localizado Referencia processo mãe
        corpoTexto.send_keys(Keys.ARROW_RIGHT * 93)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_185']").click()
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']")))
        input_field = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']"))
        )
        input_field.send_keys(nota_tecnica) # processo inicial
        navegador.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
        time.sleep(1)
        iframes = navegador.find_elements(By.TAG_NAME, 'iframe')
        navegador.switch_to.frame(iframes[2])
        corpoTexto.send_keys(Keys.PAGE_UP *2)
    
        time.sleep(5)
        navegador.switch_to.default_content()
        navegador.find_element(By.XPATH, "//a[@id = 'cke_149']").click()
        #FECHAR ABA ATUAL
        navegador.close()
    
        # Fecha o navegador
        navegador.quit()
        logging.info("Navegador fechado, automação concluída.")
    
    except Exception as e:
        logging.error(f"Ocorreu um erro: {traceback.format_exc()}")
