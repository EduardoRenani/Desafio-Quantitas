from selenium import webdriver
from bs4 import BeautifulSoup as soup
from nltk.tokenize import WhitespaceTokenizer
import math
import json
from selenium.common.exceptions import NoSuchElementException

def localiza(filename):
    localizaURL = "https://seminovos.localiza.com/carros-seminovos"
    tknzr = WhitespaceTokenizer()
    carsPerPage = 10

    chromeOptions = webdriver.ChromeOptions() #seta configs pra nao carregar imagens (aumenta velocidade do crawler)
    prefs = {"profile.managed_default_content_settings.images":2}
    chromeOptions.add_experimental_option("prefs", prefs)
    chromeOptions.add_argument("--incognito")
    browser = webdriver.Chrome(chrome_options=chromeOptions)

    browser.get('https://seminovos.localiza.com/') #entra no site e extrai o json com a lista de modelos em formato json (exploit do site em si)
    jsonCars = browser.find_element_by_id("hdnJsonFabricante").get_attribute("value")
    cars = json.loads(jsonCars)


    browser.get(localizaURL) #vai para a page 1 do estoque de carros
    page_soup = soup(browser.page_source, "html5lib")
    numberOfPages = page_soup.find("span", {"class": "lo-title-destaque-sub"}).text
    numberOfPages = tknzr.tokenize(numberOfPages)[1]
    numberOfPages = math.ceil(int(numberOfPages)/carsPerPage)
    filename = filename + ".csv" #abe arquivo para escrita
    f = open(filename, "w")
    mapCars = {}

    for car in cars:
        if car['Nome'] == 'GENERAL MOTORS':
            car['Nome'] = 'CHEVROLET'
        mapCars[car['DescricaoModelo']] = car
        print(car)

    while True:
        while True: #retrycatch para quando a pagina nao carrega (problemas de conexao)
            try:
                elem = browser.find_element_by_xpath("//div[@id = 'resultadoPesquisa']")  # procura o botao de proxima pagina.
                page_soup = soup(browser.page_source, "html5lib")
                containers = page_soup.body.find("div", {"id": "resultadoPesquisa"}).findAll("div", {"class": "col-xs-12 col-md-6 col-lg-12"})  # localiza a lista de containers com os carros em estoque
            except NoSuchElementException:  # se nao achou, captura exception e para o programa.
                print("pagina sem conteudo")
                browser.refresh()
                continue
            break
        for container in containers:
            info = container.find("a", {"class": "busca-resultado-item"}).find("img")['alt']  #localiza a referencia inteira do container em questao. puxa os dados padronizados da hashmap
            car = mapCars[info]

            fabricante = car['Nome'] #agora que temos os dados padronizados daquele modelo, extraimos do container os dados especificos que variam de carro pra carro (km, ano, preco)
            modelo = tknzr.tokenize(info)
            if modelo[0] == "GRAND" or modelo[1] == "+" or modelo[1] == "LOUNGE":
                modelo = modelo[0] + modelo[1]
            elif modelo[0] == "NEW" or modelo[0] == 'NOVA' or modelo[0] == "NOVO":
                modelo = modelo[1]
            elif modelo[0] == "320I":
                modelo = "320IA"
            else:
                modelo = modelo[0]
            modelo = modelo.upper()
            anoKm = container.find("div", {"class": "busca-container-ano-km"}).findAll("span")
            ano = anoKm[0].text[:4]
            km = anoKm[1].text.replace(".", "")
            preco = container.find("div", {"class": "busca-right-container"}).find("span", {"class":"car-price"}).text
            preco = tknzr.tokenize(preco)
            preco = preco[1].replace(".", "")

            print("Fabricante: " + fabricante)
            print("Modelo: " + modelo)
            print("Ano: " + ano)
            print("Quilometragem: " + km)
            print("Preço: " + preco)
            print("\n")
            f.write("Localiza," + fabricante + "," + modelo + "," + ano + "," + km + "," + preco + "\n")

        try:
            elem = browser.find_element_by_xpath("//div[@class = 'busca-header clearfix']//div[@class ='busca-paginacao']//a[@class='item option next']")  # procura o botao de proxima pagina.
            elem.click()  # se achou o botao, clica nele e começa o scrap na pagina seguinte.
        except NoSuchElementException:  # se nao achou, captura exception e para o programa.
            break
        continue
