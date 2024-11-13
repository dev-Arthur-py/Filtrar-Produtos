from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class Olx:
    def __init__(self, item_name, max_price):
        self.item_name = item_name
        self.max_price = max_price
        self.driver = webdriver.Chrome()

    def find_items_max_price(self):
        item_links = self.search_olx()

        for link in item_links:
            self.driver.get(link)
            time.sleep(2)  # Espera para garantir que a página carregue
            
            try:
                # Alterei para By.CSS_SELECTOR
                price_text1 = self.driver.find_element(By.CLASS_NAME, 'olx-text olx-text--body-medium olx-text--block olx-text--semibold ad__sc-1md5bii-0 zQuo olx-color-neutral-100').text
                price_text2 = self.driver.find_element(By.CLASS_NAME, 'olx-text olx-text--title-medium olx-text--block').text

                print(price_text1, price_text2)
                
                price_text = price_text.replace('R$', '').strip()
                price = float(price_text.replace('.', '').replace(',', '.'))

                if price < float(self.max_price):
                    print(f'Link: {link}, Valor: {price}')
            except Exception as e:
                print(f"Erro ao pegar o preço de {link}: {e}")

    def search_olx(self):
        search_url = f'https://www.olx.com.br/estado-rj?q={self.item_name}'
        self.driver.get(search_url)

        item_elements = self.driver.find_elements(By.PARTIAL_LINK_TEXT, self.item_name)
        item_links = []

        for element in item_elements:
            link = element.get_attribute('href')
            if link:
                item_links.append(link)

        print(item_links)        

        return item_links


