from services.amazonService import AmazonService
from controllers.libraryController import *

class amazonController:
    def main(self, produto, preco_maximo):
        driver = webdriver.Chrome()
        amazon_control = AmazonService(produto, preco_maximo)
        amazon_control.valor_amazon()


        
