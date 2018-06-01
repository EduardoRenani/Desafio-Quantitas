class Carro:
    def __init__(self, empresa, fabricante, modelo, ano, kilometragem, preco, fipePreco):
        self.key = str(fabricante)+str(modelo)+str(ano)
        self.fabricante = fabricante
        self.modelo = modelo
        self.ano = ano
        self.kilometragem = kilometragem
        self.empresa = empresa
        self.preco = preco
        self.fipePreco = fipePreco

    def print(self):
        print("\nRevendedora: " +self.empresa+ "\nMarca: " +self.fabricante+ "\nModelo: " +self.modelo+ "\nAno: " +self.ano+ "\nQuilometragem: " +self.kilometragem+ "\nPreco: " +self.preco+ "\nPreco FIPE: " +self.fipePreco+ "\n")
