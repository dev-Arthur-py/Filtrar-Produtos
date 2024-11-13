from services.mercadoLivreService import MercadoLivreService
from controllers.libraryController import *

class mercadoLivreController:
    def main(self, produto, preco_maximo):
        mercado_livre = MercadoLivreService(produto, preco_maximo)
        mercado_livre.valor_mercado_livre()



