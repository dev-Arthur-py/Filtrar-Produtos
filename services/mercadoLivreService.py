from controllers.libraryController import *

class MercadoLivreService:
    url = 'https://www.mercadolivre.com.br'

    def __init__(self, product_name, product_price):  
        self.product_name = product_name
        self.product_price = product_price
        self.driver = webdriver.Chrome()

    def exibir_valores(self):
        print(f"Produto: {self.product_name}")
        print(f"Preço Limite: {self.product_price}")


    def valor_mercado_livre(self):
        prod_links_mercado_livre = self.mercado_livre(self.product_name)
        products = []  # Lista para armazenar os produtos que atendem ao critério de preço

        for link in prod_links_mercado_livre:
            self.driver.get(link)
            time.sleep(2)

            try:
                # Extrai o valor do preço
                price_element = self.driver.find_element(By.CLASS_NAME, 'andes-money-amount__fraction').text
                price_value = float(price_element.replace('.', '').replace(',', '.'))

                # Extrai o nome do produto
                name_element = self.driver.find_element(By.CLASS_NAME, 'ui-pdp-title').text

                try:
                    # Tenta extrair a descrição
                    description_element = self.driver.find_element(By.CLASS_NAME, 'ui-pdp-description')
                    description = description_element.text
                except Exception:
                    description = "Descrição não encontrada"

                # Verifica se o preço é menor que o especificado
                if price_value < float(self.product_price):
                    products.append({
                        "Nome": name_element,
                        "Valor": f"R${price_value:,.2f}",  # Formata o valor com 'R$' e separador de milhar
                        "Descrição": description,
                        "Link": link
                    })
                    print(f"Nome: {name_element}, Valor: R${price_value:,.2f}, Descrição: {description}, Link: {link}")
            
            except Exception as e:
                print(f"Erro ao processar o link {link}. Detalhes: {e}")

        self.salvar_em_planilha(products)



    def mercado_livre(self, product_name):
        self.driver.get(self.url)
        search_box = self.driver.find_element(By.XPATH, '//*[@id="cb1-edit"]')
        search_box.send_keys(product_name, Keys.ENTER)
        time.sleep(2)

        search_links = self.driver.find_elements(By.CSS_SELECTOR, '.ui-search-layout__item a[href*="MLB"]')
        
        links = []
        for selenium in search_links:
            link = selenium.get_attribute('href')
            if link and len(links) < 10:  
                links.append(link)

        return links

    def salvar_em_planilha(self, products):
 
        df = pd.DataFrame(products)

        if df.empty:
            print("Nenhum produto para salvar na planilha.")
            return
        
        df.to_excel("produtos_mercadolivre.xlsx", index=False)

        wb = load_workbook("produtos_mercadolivre.xlsx")
        ws = wb.active

        ws.auto_filter.ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"

        for col in ws.columns:
            max_length = max(len(str(cell.value)) for cell in col if cell.value)
            adjusted_width = (max_length + 2) if max_length else 10
            ws.column_dimensions[get_column_letter(col[0].column)].width = adjusted_width


        wb.save("produtos_mercadolivre.xlsx")
        print("Planilha salva como 'produtos_mercadolivre.xlsx' com colunas ajustadas e filtro aplicado.")
