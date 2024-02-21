import logging as log

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from datetime import datetime
import time

class Bot:

    def __init__(self, username='', password=''):
        """
        Allows you to set initial configs of bot

        :Args:
        - username: your username of instagram account
        - password: your password of instagram account
        - targets: a list of URLs (locations and tags) to like most recent posts
        - interactions: define the number of interactions in each post
        """
        self.username = username
        self.password = password
        self.time_wait = 2
        self.target=''
        self.driver = self.configure_bot()
        log.basicConfig(level=log.INFO, filename="logs/sagah_bot.log", format="%(levelname)s - %(asctime)s -  %(message)s", encoding="utf-8",  datefmt="%d-%m-%Y %H:%M:%S")
        


    def configure_bot(self):
        """
        Initialize selenium.

        :return: a instance of webdriver for Chrome
        """
        options = Options()
        options.headless = False
        options.add_argument('--window-size=1280,768')
        return webdriver.Chrome(options=options)

    def run_bot(self, operation, data):
        """
        Execute interations
        :return: void
        """
        self.login()
        time.sleep(self.time_wait)
        
        
        if operation == 'cursos':
            self.cadastrar_cursos(data)
            
        elif operation == 'disciplinas':
            self.cadastrar_disciplinas(data)
        
        
        self.driver.quit()
        
    def cadastrar_cursos(self, cursos:list):
        self.open_target('https://catalogo.grupoa.education/courses')
        time.sleep(3)
        driver = self.driver
        
        try:
            input_curso = driver.find_element_by_xpath('//*[@id="input-32"]')
            novo_curso = driver.find_element_by_xpath('//*[@id="input-27"]')
            salvar = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div/div/div[2]/div/div/div/div[3]/div[1]/div[2]/button')
            
            for curso in cursos:
                print(f'Cadastrando curso: {curso}')
                input_curso.send_keys('eee')
                time.sleep(1)
                limpar = driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[1]/div[2]/div/div/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]/div/div[1]/div[3]/div/button')
                limpar.click()
                input_curso.send_keys( curso )
                input_curso.send_keys(Keys.ENTER )
                log.info(f'Search: {curso}')
                time.sleep(2)
                
                if (driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div/div/div[2]/div/div/div/div[3]/div[2]/div[2]/div/span').text == 'Nenhum curso encontrado'):
                    novo_curso.send_keys(curso)
                    salvar.click()
                    log.info(f'Curso novo: {curso}')
                    time.sleep(1)

            self.driver.quit()
        except:
            print('Ocorreu uma exceção na função cadastrar_cursos! ',
                datetime.now().strftime('%H:%M:%S'))
            log.error('Ocorreu uma exceção na função cadastrar_cursos! ', stack_info=True, exc_info=True, extra={'curso': curso})
    
    def cadastrar_disciplinas(self, disciplinas:dict):
        self.open_target('https://catalogo.grupoa.education/discipline')
        time.sleep(2)
        
        driver = self.driver
        try:
            input_disciplina = driver.find_element_by_xpath('//*[@id="input-25"]')
            input_curso = driver.find_element_by_xpath('//*[@id="input-28"]')
            salvar = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/button')
            total = len(disciplinas)
            i = 1
            disc_log = ''
            
            for disciplina, curso in disciplinas.items():
                print(f'Cadastrando disciplina: {disciplina} - {curso} ({i}/{total})')
                log.info(f'Cadastrando disciplina: {disciplina} - {curso} ({i}/{total})')
                disc_log = disciplina
                input_disciplina.send_keys(disciplina)
                input_curso.send_keys(curso)
                time.sleep(0.5)
                salvar.click()
                time.sleep(1)
                
                i += 1
                
            driver.quit()
                                
        except:
            print('Houve um erro ao tentar cadastrar disciplinas!')
            log.error(f'Houve um erro ao tentar cadastrar disciplinas!', stack_info=True, exc_info=True, extra={'disciplina': disc_log})
        
        
    def login(self):
        try:
            driver = self.driver
            driver.get("https://catalogo.grupoa.education/login")

            time.sleep(self.time_wait)
            driver.find_element_by_xpath(
                '//*[@id="input-10"]') \
                .send_keys(self.username)

            driver.find_element_by_xpath(
                '//*[@id="input-11"]') \
                .send_keys(self.password)

            time.sleep(1)

            driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[1]/div[2]/div/button') \
                .click()
                
            log.info('Login!')
        except:
            print('Erro ao logar! ',
                datetime.now().strftime('%H:%M:%S'))
            log.error('Erro ao logar! ',
                datetime.now().strftime('%H:%M:%S'))


    def set_time_wait(self, secs):
        self.time_wait = secs


    def open_target(self, target):
        driver = self.driver
        try:
            log.info(f'Carregando destino: {target}')
            driver.get(target)
            time.sleep(self.time_wait)
        except:
            print('Erro ao carregar destino!',
                datetime.now().strftime('%H:%M:%S'))

