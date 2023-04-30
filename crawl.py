from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup


def NewChrome():
    options = Options()
    options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    #options.add_argument('--headless')
    options.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.notifications": 2})
    return webdriver.Chrome(service=Service(executable_path="chromedriver.exe"), options=options)

productName = input("Nhập từ khóa sản phẩm: ")
max_price = int(input('Nhập giá tối đa: '))
min_price = int(input('Nhập giá tối thiểu: '))

driver = NewChrome()

for pages in range(1,99999):
    url = f"https://www.amazon.com/s?k={productName.replace(' ','+')}&page={str(pages)}"
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all("div", {"data-component-type": "s-search-result"})
    product_names = []
    product_prices = []
    for product in products:
        try:
            product_name = product.find("h2", {"class": "a-size-mini a-spacing-none a-color-base s-line-clamp-2"}).text.strip()
            product_price = str(product.find("span", {"class": "a-price-whole"}).text).strip().replace('.','')
            if int(product_price) > min_price and int(product_price) < max_price:
                product_names.append(product_name)
                product_prices.append(product_price)
                with open('result.txt','a+',encoding='utf-8') as f:
                    f.write(product_name+'|'+product_price+'\n')
        except:
            pass
    pages+=1
    xx = [x.text for x in driver.find_elements(By.CLASS_NAME, 'a-text-normal') if x.text != '']
    del xx[0]
    if xx == []:
        print('ĐÃ SCAN HẾT SẢN PHẨM !')
        break

driver.quit()
