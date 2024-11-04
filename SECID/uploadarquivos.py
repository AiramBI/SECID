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

def executar_automacao():
    session_id = None  # Para armazenar o ID da sessão e garantir que podemos fechar depois
    
    try:
        logging.info("Iniciando o Selenium...")

        # Configuração para o servidor Selenium remoto no Railway
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Remova o comentário para rodar headless
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Inicializando a sessão do Selenium
        navegador = webdriver.Remote(
            command_executor='https://standalone-chrome-production-1308.up.railway.app/wd/hub',
            options=options
        )
        session_id = navegador.session_id  # Salva o ID da sessão
        logging.info(f"ID da sessão: {session_id}")
        
        # INICIO BLOCO DE LOGIN
        navegador.get("https://sei.rj.gov.br/sip/login.php?sigla_orgao_sistema=ERJ&sigla_sistema=SEI")
        
        # Localizando o campo de usuário e inserindo o login
        usuario = navegador.find_element(By.XPATH, '//*[@id="txtUsuario"]')
        usuario.send_keys(login)
    
        # Localizando o campo de senha e inserindo a senha
        campoSenha = navegador.find_element(By.XPATH, '//*[@id="pwdSenha"]')
        campoSenha.send_keys(senha)
    
        # Selecionando o órgão 'SEFAZ' na lista suspensa
        exercicio = Select(navegador.find_element(By.XPATH, '//*[@id="selOrgao"]'))
        exercicio.select_by_visible_text('SEFAZ')
    
        # Clicando no botão de login
        btnLogin = navegador.find_element(By.XPATH, '//*[@id="Acessar"]')
        btnLogin.click()
    
        # Maximiza o navegador e fecha pop-up
        navegador.maximize_window()
        time.sleep(1)
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@title='Fechar janela (ESC)']"))
        )
        botao_fechar = navegador.find_element(By.XPATH, "//img[@title='Fechar janela (ESC)']")
        botao_fechar.click()
    
        # FIM DO BLOCO DE LOGIN
    
        # INICIO DO BLOCO DE PROCURAR UM PROCESSO
        procurar_processo = navegador.find_element(By.XPATH, '//*[@id="txtPesquisaRapida"]')
        procurar_processo.send_keys('SEI-040009/000654/2024' + Keys.ENTER)
    
        # Acessa o campo de anotação
        navegador.switch_to.default_content()
        WebDriverWait(navegador, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt = 'Anotações']"))).click()
    
        # Preenche a anotação
        campo_anotacao = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="txaDescricao"]'))
        )
        campo_anotacao.send_keys('SEI-040009/000654/2024')
    
        # Clica no botão de salvar
        botao_salvar = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@value = "Salvar"]'))
        )
        botao_salvar.click()

        logging.info("Anotação salva com sucesso!")

    except Exception as e:
        logging.error(f"Ocorreu um erro: {traceback.format_exc()}")

    finally:
        # Fecha o navegador e encerra a sessão
        if navegador:
            navegador.quit()
            logging.info("Navegador fechado.")
        
        # Exclui a sessão do Selenium Grid remoto
        if session_id:
            try:
                response = requests.delete(
                    f'https://standalone-chrome-production-1308.up.railway.app/wd/hub/session/{session_id}'
                )
                if response.status_code == 200:
                    logging.info("Sessão encerrada com sucesso.")
                else:
                    logging.warning(f"Erro ao encerrar a sessão: {response.status_code} - {response.text}")
            except Exception as e:
                logging.error(f"Erro ao tentar encerrar a sessão: {e}")
