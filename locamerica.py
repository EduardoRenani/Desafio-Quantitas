from selenium import webdriver
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup as soup
from nltk.tokenize import WhitespaceTokenizer
import math
import json
import HashMap as dicionario
import time
from selenium.common.exceptions import NoSuchElementException


def locamerica(filename):
    locamericaURL = "https://seminovos.locamerica.com.br/seu-carro?marca=&anode=0&cambio=&combustivel=&cor=&acessorios=&por_pagina=36&per_page=0&precode=&precoate="
    tknzr = WhitespaceTokenizer()

    chromeOptions = webdriver.ChromeOptions() #seta configs pra nao carregar imagens (aumenta velocidade do crawler)
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.add_experimental_option("prefs", prefs)
    chromeOptions.add_argument("--incognito")
    browser = webdriver.Chrome(chrome_options=chromeOptions)

    browser.get(locamericaURL)
    page_soup = soup(browser.page_source, "html5lib")

    filename = filename + '.csv'
    f = open(filename, "w")
    page_soup
    numberOfPages = page_soup.find("ul", {"class", "pagination-bottom"}).findAll("li")
    numberOfPages = numberOfPages[4].find("a")['href']
    numberOfPages = numberOfPages[numberOfPages.find("page=")+5:]

    for i in range(1, int(numberOfPages)+1, 1):
        containers = page_soup.find("div", {"class": "resultad-carros-busca"}).findAll("div", {"class": "item-carro"})
        for container in containers:
            fabricanteModelo = container.find("div").find("div", {"class": "titulo"}).find("h1").find("a").text
            fabricanteModelo = tknzr.tokenize(fabricanteModelo)
            fabricante = fabricanteModelo[0]
            modelo = fabricanteModelo[1]
            anoKmInfos = container.find("div").find("div", {"class": "col-md-6 detalhes"}).text
            anoKmInfos = tknzr.tokenize(anoKmInfos)
            ano = anoKmInfos[1][5:10]
            km = anoKmInfos[5].replace(".", "") if anoKmInfos[5].replace(".", "") != '-' else "0"
            preco = container.find("div").find("div", {"class": "col-md-6 detalhes-no-border"}).find("div",{"class": "preco"}).find("h4").text
            preco = preco[:len(preco)-3].replace(".", "")
            print("Fabricante: " + fabricante)
            print("Modelo: " + modelo)
            print("Ano: " + ano)
            print("Quilometragem: " + km)
            print("Preço: " + preco)
            print("\n")
            if modelo == "IS":
                modelo = "IS250"
            elif fabricanteModelo[1] == "GRAND" or fabricanteModelo[2] == "+" or fabricanteModelo[2] == "LOUNGE":
                modelo = fabricanteModelo[1] + fabricanteModelo[2]

            f.write("Locamerica," + fabricante + "," + modelo + "," + ano + "," + km + "," + preco + "\n")

        if i < int(numberOfPages):
            while True: #retrycatch para tentar achar o nextButton várias vezes enquanto a pagina nao carrega por completo.
                try:
                    elem = browser.find_element_by_xpath("//li[@class='next page']//a").get_attribute("href") #procura o botao de proxima pagina.
                    browser.get(elem)
                    page_soup = soup(browser.page_source, "html5lib")
                except NoSuchElementException:  # se nao achou, captura exception e para o programa.
                    print("procurando next.button")
                    continue
                break
