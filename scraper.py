from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import os
import pymysql
from airflow.models import Variable
import time
import secrets
import re

start_time = datetime.now()

keywords = []
product_names = []
product_links = []
product_links_tidy = []
product_reviewcounts = []
product_soldcounts = []
product_viewcounts = []
keyword_ids = []
keyword_ids_tidy = []

try:
    conn = pymysql.connect(host = Variable.get('HAKASETEST_HOST'), 
                            user = Variable.get('HAKASETEST_USER'),
                            password = Variable.get('HAKASETEST_PASS'))
    cur = conn.cursor()
    cur.execute('select * from {TP_KEYWORDS}'.format(TP_KEYWORDS=Variable.get('TP_KEYWORDS')))
    keywords_raw = cur.fetchall()
    conn.close()
except:
    print('fail to read {TP_KEYWORDS}'.format(TP_KEYWORDS=Variable.get('TP_KEYWORDS')))

display = Display(visible = 0, size = (800, 600))
display.start()

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.79'

opts = Options()
opts.add_argument('--disable-notifications')
opts.add_argument(f'user-agent={user_agent}')
#opts.add_argument('--headless') #no need to invoke headless due to running in gce environment
opts.add_argument('--no-sandbox') #need to invoke no sandbox due to running in gce environment
driver = webdriver.Chrome(options = opts)

for i in range(len(keywords_raw)):
    keywords.append(keywords_raw[i][1].replace(' ', '%20'))
    keyword_ids.append(keywords_raw[i][0])

for j in range(len(keywords)):
    driver.get('https://www.tokopedia.com/search?st=product&ob=5&q=' + keywords[j])
    time.sleep(secrets.choice(range(5, 11)))
    product_link_elements = driver.find_elements_by_class_name('css-gwkf0u')

    for ji in range(len(product_link_elements)):
        if 'https://ta.tokopedia.com' not in str(product_link_elements[ji].get_attribute('href')):
            product_links.append(product_link_elements[ji].get_attribute('href'))
            keyword_ids_tidy.append(keyword_ids[j])

for k in range(len(product_links)):
    driver.get(product_links[k])
    time.sleep(secrets.choice(range(3, 7)))
    #driver.save_screenshot('error_screenshot.png') #capture screenshot for element debugging

    try:
        product_name = driver.find_element_by_class_name('css-x7lc0h').text 
        product_names.append(product_name)
    except NoSuchElementException:
        product_names.append(None)

    product_link_tidy = driver.current_url.split('?', 1)[0]
    product_links_tidy.append(product_link_tidy)

    try:
        product_reviewcount = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[3]/span[1]/span[2]').text
        product_reviewcounts.append(''.join(re.findall('[0-9]', product_reviewcount)))
    except NoSuchElementException:
        product_reviewcounts.append(None)

    try:
        product_soldcount = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[3]/span[2]/b/span').text 
        product_soldcounts.append(''.join(re.findall('[0-9]', product_soldcount)))
    except NoSuchElementException:
        product_soldcounts.append(None)

    try:
        product_viewcount = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[3]/span[3]/b').text 
        product_viewcounts.append(''.join(re.findall('[0-9]', product_viewcount)))
    except NoSuchElementException:
        product_viewcounts.append(None)

current_time = str(datetime.now())
inserted_time = [current_time] * len(product_names)

try:
    conn = pymysql.connect(host = Variable.get('HAKASETEST_HOST'), 
                            user = Variable.get('HAKASETEST_USER'),
                            password = Variable.get('HAKASETEST_PASS'))
    cur = conn.cursor()
    query = '''insert into {TP_RECENT_UPDATE} 
            (keyword_id, product_name, product_link, sold_count, review_count, view_count, inserted_time) values (%s, %s, %s, %s, %s, %s, %s)
            '''.format(TP_RECENT_UPDATE=Variable.get('TP_RECENT_UPDATE'))
    recent_update = list(zip(keyword_ids_tidy, product_names, product_links_tidy, product_soldcounts, product_reviewcounts, product_viewcounts, inserted_time))
    cur.executemany(query, recent_update)
    conn.commit()
    conn.close()
except:
    print('fail to write {TP_RECENT_UPDATE}'.format(TP_RECENT_UPDATE=Variable.get('TP_RECENT_UPDATE')))

os.system('killall -9 Xvfb chromedriver')

#log runtime and inserted_time
end_time = datetime.now()
log_runtime = 'runtime: ' + str(end_time - start_time)
log_inserted_time = ' | inserted time: ' + current_time
print(log_runtime + log_inserted_time)