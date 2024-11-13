from controllers.libraryController import *


def delete_cache():
    pyautogui.keyDown('ctrl')
    pyautogui.press('f5')
    pyautogui.keyUp('ctrl')

class AmazonService:
    def __init__(self, product_name, product_price):  
        self.product_name = product_name
        self.product_price = product_price
        self.driver = webdriver.Chrome()

    def valor_amazon(self):
        print("Iniciando a busca de produtos na Amazon...")
        prod_links_amazon = self.amazon()

        products_amazon = []

        for link in prod_links_amazon:
            self.driver.get(link)
            try:
                price_text = self.driver.find_element(By.CLASS_NAME, 'a-price-whole').text
                price_value = float(price_text.replace('.', '').replace(',', '.'))

                name_product = self.driver.find_element(By.ID, 'productTitle').text
                description = self.driver.find_element(By.CSS_SELECTOR, '#prodDetails > div').text

                # Verificação de preço
                if price_value < float(self.product_price):
                    products_amazon.append({
                        "Nome": name_product,
                        "Valor": f"R${price_value:,.2f}",
                        "Descrição": description,
                        "Link": link
                    })
                    print(f"Produto encontrado: Nome: {name_product}, Valor: R${price_value:,.2f}, Descrição: {description}, Link: {link}")
            
            except Exception as e:
                print(f"Erro ao processar o link {link}. Detalhes: {e}")

        # Salvar dados na planilha
        self.salvar_em_planilha(products_amazon)

    def amazon(self):
        url = 'https://www.amazon.com.br/'
        self.driver.get(url)

        delete_cache()

        # Buscar o produto na barra de pesquisa
        search_box = self.driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
        search_box.send_keys(self.product_name, Keys.ENTER)

        # Coletar os links dos produtos na página de resultados
        search_links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, self.product_name)

        valid_links = []

        for link_element in search_links:
            link = link_element.get_attribute('href')
            if link and len(valid_links) < 10:  
                valid_links.append(link)

        print(f"Links encontrados: {valid_links}")
        return valid_links

    def salvar_em_planilha(self, products):
        if not products:
            print("Nenhum produto para salvar na planilha.")
            return
        
        df = pd.DataFrame(products)
        df.to_excel("produtos_amazon.xlsx", index=False)

        # Ajustar colunas e adicionar filtros
        wb = load_workbook("produtos_amazon.xlsx")
        ws = wb.active
        ws.auto_filter.ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"

        for col in ws.columns:
            max_length = max(len(str(cell.value)) for cell in col if cell.value)
            adjusted_width = (max_length + 2) if max_length else 10
            ws.column_dimensions[get_column_letter(col[0].column)].width = adjusted_width

        wb.save("produtos_amazon.xlsx")
        print("Planilha salva como 'produtos_amazon.xlsx' com colunas ajustadas e filtro aplicado.")
