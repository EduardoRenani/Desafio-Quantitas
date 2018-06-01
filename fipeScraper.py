from selenium import webdriver
from bs4 import BeautifulSoup as soup
from nltk.tokenize import WhitespaceTokenizer
import json
import HashMap as dicionario
import time
import csv
#comunica com API para extrair os dados da tabela FIPE

def atualizaFipe():
    carsTree = None
    carrosList = []
    carrosMap = {}
    fipeMap = dicionario.HashMap()

    fipeURL = "http://fipeapi.appspot.com/api/1/carros/marcas.json"
    tknzr = WhitespaceTokenizer()

    chromeOptions = webdriver.ChromeOptions()  # seta configs pra nao carregar imagens (aumenta velocidade do crawler)
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.add_experimental_option("prefs", prefs)
    chromeOptions.add_argument("--incognito")
    browser = webdriver.Chrome(chrome_options=chromeOptions)

    browser.get(fipeURL)
    page_json = soup(browser.page_source,'html5lib').find("body").find("pre").text
    filename = 'fipe.csv'
    f = open(filename, "w")
    jsonMarcas = json.loads(page_json)
    mapMarcas = dicionario.HashMap()
    mapVeiculos = dicionario.HashMap()
    for marca in jsonMarcas:
        browser.get('http://fipeapi.appspot.com/api/1/carros/veiculos/'+str(marca['id'])+'.json')
        time.sleep(1)
        modelos = soup(browser.page_source,'html5lib').find("body").find("pre").text
        modelos = json.loads(modelos)
        mapMarcas.put(marca["fipe_name"], modelos)
        for modelo in modelos:
            print(modelo)
            modeloNome = tknzr.tokenize(modelo['name'])
            if modeloNome[0].upper() == "GRAND" or (len(modeloNome) > 1 and modeloNome[1].upper() == "LOUNGE") or modeloNome[0].upper() == "XC":
                modeloNome = str(modeloNome[0] + modeloNome[1])
            elif modeloNome[0].upper() == "SANTA":
                modeloNome = str(modeloNome[0] + modeloNome[1][:2])
            else:
                modeloNome = modeloNome[0]
            modeloNome = modeloNome.upper()
            modeloNome = modeloNome.replace("-", "")
            modeloNome = modeloNome.replace("!", "")
            if modelo['fipe_marca'].upper() == 'VW - VOLKSWAGEN':
                modelo['fipe_marca'] = 'VOLKSWAGEN'
            elif modelo['fipe_marca'].upper() == 'GM - CHEVROLET':
                modelo['fipe_marca'] = 'CHEVROLET'
            elif modelo['fipe_marca'] == 'Citro\u00ebn':
                modelo['fipe_marca'] = 'CITROEN'
            elif modelo['fipe_marca'].upper() == 'KIA MOTORS':
                modelo['fipe_marca'] = 'KIA'
            f.write(modelo["fipe_marca"].upper() + "," + str(marca['id']) + "," + modeloNome + "," + modelo["id"] + "\n")

    with open('fipe.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            fipeMap.put(str(row[0])+str(row[2]), str(row[1])+" "+str(row[3])) #pair(fipeMarca+fipeNome,marcaID+nomeID)

    with open('carros.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            chave = str(row[1]) + str(row[2]) + str(row[3]) #fabricante + modelo + ano
            objId = fipeMap.getObj(str(row[1]) + str(row[2])) #guarda objeto com os varios codigos fip para aquele veículo. (vamos precisar iterar ele depois quando formos acessar os dados via selenium)
            car1 = {"chave": chave, "fabricante": row[1], "modelo": row[2], "ano": row[3], "objID": objId} #tal iteracao é para driblar falta de informacao dos veículos das revendedoras (fipe usa nome completo com especificacoes e as revendedoras nao)
            if carrosList.count(car1) == 0:
                carrosList.append(car1)

    print(len(carrosList))
    print(carrosList)
    i = 0
    filename = "carrosEFipe.csv" #abe arquivo para escrita
    fw = open(filename, "w")
    for car1 in carrosList:
        i += 1
        print(i)
        for ID in car1['objID'].listValues:
            ID = tknzr.tokenize(str(ID))
            marcaID = ID[0]
            fipeID = ID[1]
            year = str(car1["ano"]) + "-1"
            time.sleep(0.5) #servidor da api tem limite de requisicoes por minuto
            browser.get("http://fipeapi.appspot.com/api/1/carros/veiculo/" + marcaID + "/" + fipeID + "/" + year + ".json")
            elem = soup(browser.page_source, "html5lib").find("body").find("h1")
            if elem is not None and elem.text == '500 Internal Server Error':
                continue
            else:
                carroFipeInfo = soup(browser.page_source, 'html5lib').find("body").find("pre").text
                carroFipeInfo = json.loads(carroFipeInfo)
                preco = tknzr.tokenize(carroFipeInfo["preco"])
                preco = preco[1]
                preco = preco[:len(preco)-3].replace(".", "")
                print(car1["chave"])
                fw.write(car1["chave"] + "," + preco + "\n")
                break
