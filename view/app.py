import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.mercadoLivreController import mercadoLivreController
from controllers.amazonController import amazonController
from controllers.libraryController import *


ctk.set_appearance_mode("System")

def iniciar_scraping():
    produto = entrada_produto.get()
    valor = entrada_valor.get()
    site = opcoes_site.get()
    
    if not produto or site == "":
        messagebox.showwarning("Aviso", "Por favor, preencha o termo de busca e escolha a plataforma.")
  
    print(site)
    print(produto)
    print(valor)

    if site.lower() == 'mercado livre':
        new_ml = mercadoLivreController()
        new_ml.main(produto,valor)
        print(f'Iniciando a busca do produto {produto} no site: {site}')
    elif site.lower() == 'amazon':
        new_az = amazonController()
        new_az.main(produto, valor)
        print(f'Iniciando a busca do produto {produto} no site {site}')
    elif site.lower() == 'ambos':
        new_ml = mercadoLivreController()
        new_ml.main(produto, valor)
        new_az = amazonController()
        new_az.main(produto,valor)  

janela = ctk.CTk()
janela.title("Projeto, Web Scrapping")
janela.geometry("500x400")

produto_pesquisa = ctk.CTkLabel(janela, text="Qual produto gostaria de procurar?")
produto_pesquisa.pack(pady=10)

entrada_produto = ctk.CTkEntry(janela, placeholder_text="Digite o produto...")
entrada_produto.pack(pady=5)

entrada_valor = ctk.CTkEntry(janela, placeholder_text="Digite o valor...")
entrada_valor.pack(pady=5)


rotulo_site = ctk.CTkLabel(janela, text="Sites:")
rotulo_site.pack(pady=8)

opcoes_site = ctk.CTkComboBox(janela, values=["Mercado Livre", "Amazon", "Ambos"])
opcoes_site.pack(pady=5)


botao_iniciar = ctk.CTkButton(janela, text="Iniciar a busca", command=iniciar_scraping)
botao_iniciar.pack(pady=20)



janela.mainloop()
