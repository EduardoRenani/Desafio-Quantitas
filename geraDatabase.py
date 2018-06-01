import carro as car
import csv
from nltk.tokenize import WhitespaceTokenizer

#le os dados da tabela "CARRO-ANO: PREÇO-FIPE"
#le os dados da tabela com todos os registros de carros das 4 revededoras
#gera database com comparativo

def geraDatabase():
    tknzr = WhitespaceTokenizer()

    carrosMap = {}

    with open('carrosEFipe.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            carrosMap[row[0]] = row[1]

    filename = "database.csv" #abe arquivo para escrita
    fw = open(filename, "w")
    fw.write("Revendedora, Fabricante, Modelo, Ano, Kilometragem, Preco, Preço Fipe, %Desconto-Fipe, %Desconto/1000Kilometros\n")
    with open('carros.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            fipePreco = carrosMap[row[1]+row[2]+str(row[3])]
            car1 = car.Carro(row[0], row[1], row[2], row[3], row[4], row[5], fipePreco)
            car1.print()
            desconto = 100*(float(car1.fipePreco) - float(car1.preco))/float(car1.fipePreco)
            descontoPerKm = 1000*float(desconto)/(float(car1.kilometragem)+1)
            fw.write(car1.empresa + "," + car1.fabricante + "," + car1.modelo + "," + car1.ano + "," + car1.kilometragem + "," + car1.preco + "," + car1.fipePreco + "," + str(desconto) + "%," + str(descontoPerKm) + "\n")
