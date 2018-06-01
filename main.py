import movida
import locamerica
import localiza
import unidas
import geraDatabase
import fipeScraper
import shutil

fMovida = "carrosMovida"
fLocamerica = "carrosLocamerica"
fLocaliza = "carrosLocaliza"
fUnidas = "carrosUnidas"

def salvaCarrosRevendedoras():
    with open('carros.csv', 'wb') as wfd:
        for f in [fMovida + '.csv', fLocamerica + '.csv', fLocaliza + '.csv', fUnidas + '.csv']:
            with open(f, 'rb') as fd:
                shutil.copyfileobj(fd, wfd, 1024 * 1024 * 10)

while True:
    print(
        "1 - Atualizar banco Unidas\n"
        "2 - Atualizar banco Locamerica\n"
        "3 - Atualizar banco Movida\n"
        "4 - Atualizar banco Localiza\n"
        "5 - Atualizar todos os bancos de revendedoras\n"
        "6 - Apenas Extrair os dados FIPE e gerar Database a partir de bancos atuais das revendedoras\n"
        "7 - Atualizar todos os bancos, extrair dados FIPE e gerar database\n"
        "8 - Sair"
        )
    option = input()

    if option == "1":
        unidas.unidas(fUnidas)
        salvaCarrosRevendedoras()
    elif option == "2":
        locamerica.locamerica(fLocamerica)
        salvaCarrosRevendedoras()
    elif option == "3":
        movida.movida(fMovida)
        salvaCarrosRevendedoras()
    elif option == "4":
        localiza.localiza(fLocaliza)
        salvaCarrosRevendedoras()
    elif option == "5":
        movida.movida(fMovida)
        locamerica.locamerica(fLocamerica)
        localiza.localiza(fLocaliza)
        unidas.unidas(fUnidas)
        salvaCarrosRevendedoras()
    elif option == "6":
        fipeScraper.atualizaFipe()
        geraDatabase.geraDatabase()
    elif option == "7":
        movida.movida(fMovida)
        locamerica.locamerica(fLocamerica)
        localiza.localiza(fLocaliza)
        unidas.unidas(fUnidas)
        salvaCarrosRevendedoras()
        fipeScraper.atualizaFipe()
        geraDatabase.geraDatabase()
    elif option == "8":
        break
