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



def registrar_medicao():
    login = os.getenv("LOGIN", "asantos2")
    senha = os.getenv("SENHA", "Ivinhema1994#*#*#*")
    secretaria = os.getenv("SECRETARIA","SECID")
    coordenacao = "SEFAZ/COOCPP"
    observacoes_processo = os.getenv("OBSERVACOES_PROCESSO","") #ATÉ O MOMENTO NÃO TEM ATRIBUIÇÃO
    nomes_documentos = [
        "01.Carta assinada pela empresa",
        "02.Publicação da Comissão de Fiscalização",
        "03.Planilha de Medição (PDF)",
        "03.1.Planilha de Medição - Arquivo em Excel",
        "04.Memória de Cálculo",
        "05.Cronograma Físico - Financeiro",
        "06.Diário de Obras",
        "07.Relatório Fotográfico",
        "08.Relação de Funcionários",
        "09.Folha de ponto dos funcionários",
        "10.GFD FGTS DIGITAL",
        "10.1.DCTF WEB",
        "11.Guias e Comprovantes de Pagamentos de FGTS",
        "12.Folha de Pagamento",
        "13.Comprovante de Pagamento de salários",
        "14.Plano de segurança do Trabalho",
        "15.Certidões atualizadas",
        "15.1.Certidão de regularidade junto ao FGTS",
        "15.2.Certidão negativa de débito trabalhista",
        "15.3.Certidão negativa de débitos federais",
        "15.4.Certidão de regularidade fiscal junto ao ICMS",
        "15.5.Certidão de regularidade fiscal junto ao ISS",
        "16.Contrato",
        "17.ART emitida pelo CREA",
        "18.Nota de empenho",
        "19.Nota fiscal e ISS"
    ]
    caminho_arquivo = [
    "medicao.documento_1",
    "medicao.documento_2",
    "medicao.documento_3",
    "medicao.documento_3_1",
    "medicao.documento_4",
    "medicao.documento_5",
    "medicao.documento_6",
    "medicao.documento_7",
    "medicao.documento_8",
    "medicao.documento_9",
    "medicao.documento_10",
    "medicao.documento_10_1",
    "medicao.documento_11",
    "medicao.documento_12",
    "medicao.documento_13",
    "medicao.documento_14",
    "medicao.documento_15",
    "medicao.documento_15_1",
    "medicao.documento_15_2",
    "medicao.documento_15_3",
    "medicao.documento_15_4",
    "medicao.documento_15_5",
    "medicao.documento_16",
    "medicao.documento_17",
    "medicao.documento_18",
    "medicao.documento_19"]
    # [medicao.documento_1 
    #     medicao.documento_2,
    #     medicao.documento_3,
    #     medicao.documento_3_1,
    #     medicao.documento_4,
    #     medicao.documento_5,
    #     medicao.documento_6,
    #     medicao.documento_7,
    #     medicao.documento_8,
    #     medicao.documento_9,
    #     medicao.documento_10,
    #     medicao.documento_10_1,
    #     medicao.documento_11,
    #     medicao.documento_12,
    #     medicao.documento_13,
    #     medicao.documento_14,
    #     medicao.documento_15,
    #     medicao.documento_15_1,
    #     medicao.documento_15_2,
    #     medicao.documento_15_3,
    #     medicao.documento_15_4,
    #     medicao.documento_15_5,
    #     medicao.documento_16,
    #     medicao.documento_17,
    #     medicao.documento_18,
    #     medicao.documento_19]
    data_inicial = "01/08/2024"
    data_final = "15/08/2024"
    valor_total_previsto = 5000000.00
    valor_atual_previsto = 1000000.00
    valor_total_inicial = 4000000.00
    valor_atual_inicial = 3000000.00
    valor_atual_medido = 2000000.00
    aditivo = 150
    inicial = 300
    #Documentos Necessários Nota técnica
    numero_contrato = "021/2024"
    periodo_medicao = f"'{data_inicial}' a '{data_final}'"
    numero_medicao = "15"
    cronograma_atualiado = "74850757"
    porcentagem_concluida_previsto = valor_atual_previsto/valor_total_previsto
    valor_atual_previsto = valor_atual_previsto
    porcentagem_concluida_inicial = valor_atual_inicial/valor_total_inicial
    valor_atual_inicial = valor_atual_inicial
    porcentagem_concluida_medida = valor_atual_medido/valor_total_previsto
    valor_atual_medido = valor_atual_medido
    reajustamento = 0
    reajustemento_total = 1000000
    valor_medicao = 504152.00
    medicoes = ["colocar as medicoes das medicoes"]
    rerratificacao = 1000000.00
    prazo_aditivo = f"'{aditivo}' ('{num2words(aditivo, lang ='pt_BR')}"
    prazo_inicial = f"'{inicial}' ('{num2words(inicial, lang ='pt_BR')}"
    processo_mae = "SEI-040009/000654/2024"#NUMERO DO PROCESSO MÃE (BUSCAR NUMERO DO PROCESSO MÃE) #SINALIZAR NO CADASTRO O SEI DO PROCESSO MÃE
    objeto = "objeto"
    documento_gestor_contrato = "74850775"
    publicacao_comissao_fiscalização = "021/2024 de 15 de Novembro de 2024"
    lei_contrato = "8.666, de 21 de junho de 1993"
    
    
    #Documento Necessário CHECKLIST
    contrato = "87715423" #CONTRATO (BUSCAR CONTRATO NO PROCESSO MÃE) # SINALIZAR NO CADASTRO O CÓDIGO DO DOCUMENTO CONTRATO NO PROCESSO MÃE
    seguro_garantia = "87715423" #SEGURO GARANTIA(BUSCAR SEGURO GARANTIA NO PROCESSO MÃE) #SINALIZAR NO CADASTRO O CÓDIGO DO DOCUMENTO SEGURO GARANTIA PROCESSO MATRIZ
    carta_solicitacao_prorrogacao_contratual = "87715423" #CARTA DE SOLICITAÇÃO DE PRORROGAÇÃO CONTRATUAL (BUSCAR CARTA NO PROCESSO INICIAL ) SINALIZAR NO CADASTRO DO DOCUMENTO CARTA DE SOLICITACAO PROGRRAGACAO 
    processo_rerratificacao = "SEI-260006/010954/2024" #PROCESSO DE RERRATIFICAÇÃO ( BUSCAR INDEX NO PROCESSO ORIGINAL)# SINALIZAR NO CADASTRO DO PROCESSO INICIAL
    termo_aditivo = "87715447" #TERMO ADITIVO ( BUSCAR TERMO ADITIVIO NO PROCESSO MÃE)# SINALIZAR NO CADASTRO DO PROCESSO MÃE
    contratada = "empresa1234"
    obra = "Cachoeiras de Macacu I - Praça Village"
    
    especificacao_processo = f"'{numero_medicao}'ª Medição - Obra:'{obra}' - Período:'{periodo_medicao}'" #Numero da Medicação -  OOBRA -  COMPETENCIA
    fiscal_tecnico_1 = "Fulano da Silva Santos"
    id_fiscal_tecnico_1 = "5115709-8"
    fiscal_tecnico_2 = "Beltrano da Silva Santos"
    id_fiscal_tecnico_2 = "5115709-9"
    gestor1 = "Ciclano da Silva dos Santos"
    id_gestor = "5115709-0"
    carimbo_fiscal1 = f"{fiscal_tecnico_1}\nFiscal Técnico\n{id_fiscal_tecnico_1}"
    carimbo_fiscal2 = f"{fiscal_tecnico_2}\nFiscal Técnico\n{id_fiscal_tecnico_2}"
    carimbo_gestor = f"{gestor1}\nGestor do Contrato\n{id_gestor}"
    cnpj_empresa = "01.158.700/0001-20"
    
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
