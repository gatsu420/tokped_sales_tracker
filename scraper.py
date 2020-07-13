from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import os
import pymysql
import time
import secrets

product_names = []
product_links = []

display = Display(visible = 0, size = (800, 600))
display.start()

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.79'

opts = Options()
opts.add_argument('--disable-notifications')
opts.add_argument(f'user-agent={user_agent}')
#opts.add_argument('--headless') #no need to invoke headless due to running in linux ec2 environment
opts.add_argument('--no-sandbox') #need to invoke no sandbox due to running in linux ec2 environment

driver = webdriver.Chrome(options = opts)
driver.get('https://www.tokopedia.com/search?st=product&ob=5&q=kaos%20polos')
time.sleep(secrets.choice(range(5, 16)))
product_link_elements = driver.find_elements_by_class_name('css-89jnbj')

for i in range(len(product_link_elements)):
    product_links.append(product_link_elements[i].get_attribute('href'))

for j in range(1, 11):
    driver.get(product_links[j])
    time.sleep(8)

    product_name = driver.find_element_by_class_name('css-x7lc0h').text 
    product_names.append(product_name)
    
    product_link = driver.current_url.split('?', 1)[0]
    product_links.append(product_link)
    
    driver.save_screenshot('error_screenshot.png')

os.system('killall -9 Xvfb chromedriver')
print(product_names)
print(product_links)