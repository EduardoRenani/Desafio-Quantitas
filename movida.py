from selenium import webdriver
from bs4 import BeautifulSoup as soup
from nltk.tokenize import WhitespaceTokenizer
import math

def movida(filename):
    carsPerPage = 24
    movidaURL = "https://busca.movidaseminovos.com.br/filtros/class/usado"
    movidaSection = "?page="
    tknzr = WhitespaceTokenizer()

    chromeOptions = webdriver.ChromeOptions() #seta configs pra nao carregar imagens (aumenta velocidade do crawler)
    prefs = {"profile.managed_default_content_settings.images":2}
    chromeOptions.add_experimental_option("prefs", prefs)
    chromeOptions.add_argument("--incognito")
    browser = webdriver.Chrome(chrome_options=chromeOptions)


    browser.get(movidaURL) #procura a informacao de quantos carros tem no estoque.
    page_soup = soup(browser.page_source, "html5lib")
    numberOfCars = page_soup.body.find("div", {"class": "neemu-total-products-container"}).text
    numberOfCars = tknzr.tokenize(numberOfCars)
    numberOfCars = numberOfCars[0] #divide pelo numero de carros em cada pagina e arredonda pra cima para tirar o numero de paginas. Essa abordagem navega mudando URL, sem interaçao com botoes. (abordagem mais rapida)
    numberOfPages = math.ceil(float(numberOfCars)/carsPerPage)

    filename = filename + ".csv"
    f = open(filename, "w")


    for i in range(1, numberOfPages+1, 1):
        url = movidaURL + movidaSection + str(i)
        browser.get(url)
        page_soup = soup(browser.page_source, "html5lib") #acha a lista de containers com os carros em estoque
        containers = page_soup.body.find("ul", {"class": "neemu-products-container nm-view-type-grid"}).findAll("li", {"class": "nm-product-item"})
        for vehicle in containers: #limpas as infos
            carInfo = vehicle.find("div", {"class": "nm-product-info"})
            nameAndPrice = carInfo.findAll("a")
            details = carInfo.find("ul", {"class": "nm-group-details"}).findAll("li")
            allName = nameAndPrice[0].text
            allName = tknzr.tokenize(allName)
            fabricante = allName[0]
            modelo = allName[1]
            price = nameAndPrice[1].text
            price = tknzr.tokenize(price)
            price = price[1][:len(price)-5].replace(".", "")
            km = details[0].find("span").text.replace(".", "")
            year = details[2].find("span").text
            if modelo == "C" or modelo == "GRAND" or allName[2] == "+" or allName[2] == "LOUNGE":
                modelo = str(allName[1]) + str(allName[2])
            print(fabricante)
            print(modelo)
            print(price)
            print(km)
            print(year)
            print("\n")
            f.write("Movida," + fabricante + "," + modelo + "," + year + "," + km + "," + price + "\n") #salva.