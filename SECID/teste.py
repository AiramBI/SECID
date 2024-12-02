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
    
    # Fecha o navegador
    navegador.quit()
    logging.info("Navegador fechado, automação concluída.")

except Exception as e:
    logging.error(f"Ocorreu um erro: {traceback.format_exc()}")
