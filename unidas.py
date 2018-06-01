from selenium import webdriver
from bs4 import BeautifulSoup as soup
from nltk.tokenize import WhitespaceTokenizer


#abordagem parecida com o da movida. Nesse caso, há explicitamente a info de numero de paginas e a url de uma pag pra outra segue um padrao simples. Iremos iterar um for com o numero de paginas, limpar infos e salvar.

def unidas(filename):
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromeOptions.add_argument("--incognito")
    browser = webdriver.Chrome(chrome_options=chromeOptions)


    unidasURL = "https://www.seminovosunidas.com.br/veiculos"
    unidasSection = "/page:"

    tknzr = WhitespaceTokenizer()

    browser.get(unidasURL)
    page_soup = soup(browser.page_source, "html5lib")
    numberOfPages = str(page_soup.body.find("ul", {"class": "list-unstyled list-inline header-paginator pull-right"}).findAll("li")[4].find("a"))
    numberOfPages = numberOfPages[numberOfPages.find('">')+2:numberOfPages.find("</")]
    print(numberOfPages)

    filename = filename + ".csv"
    f = open(filename, "w")


    for i in range(1, int(numberOfPages)+1, 1):
        url = unidasURL + unidasSection + str(i)
        browser.get(url)
        page_soup = soup(browser.page_source, "html5lib")
        containers = page_soup.body.find("div", {"class": "container busca-resultados"}).find("div", {"class": "resultados"}).ul.findAll("li")
        for vehicle in containers:
            car = vehicle
            fabricante = car.find("article").find('div').find("div", {"class":"col-sm-6 col-md-9"}).find("span", {"class": "makeModel"}).findAll("span")[0].text
            modelo = car.find("article").find('div').find("div", {"class":"col-sm-6 col-md-9"}).find("span", {"class": "makeModel"}).findAll("span")[1].text
            ano = car.find("article").find('div').find("div", {"class":"col-sm-6 col-md-9"}).find("span", {"class": "description"}).text
            km = car.find("article").find('div').find("div", {"class":"col-sm-6 col-md-9"}).find("span", {"class": "details"}).text
            preco = car.find("article").find('div').find("div", {"class":"col-sm-6 col-md-9"}).find("span", {"class": "valor"}).text
            ano = tknzr.tokenize(ano)
            ano = ano[len(ano)-1].replace(")", "")
            km = km[km.find("Km: ") + 4:]
            km = km[:km.find(",")]
            preco = preco[:len(preco)-3]
            if fabricante == 'MERCEDES':
                fabricante = "MERCEDES-BENZ"
            print("Fabricante: " + fabricante)
            print("Modelo: " + modelo)
            print("Ano: " + ano)
            print("Quilometragem: " + km)
            print("Preço: " + preco)
            print("\n")
            f.write("Unidas," + fabricante + "," + modelo.replace(" ","").upper() + "," + ano + "," + km.replace(".", "") + "," + preco.replace(".", "") + "\n")

