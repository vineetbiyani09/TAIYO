#Importing libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

#Initializing a driver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(4)

url = 'https://news.google.com'

driver.get(url)
driver.maximize_window()

class scraper() :
    def scroller(self) :
        x = 0
        while x < 5 :
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
            x = x + 1
        self.scraper()

    def scraper(self) :
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.findAll('article')
        self.final_list = []
        for article in articles :
            try :
                h3 = article.find('h3')
                link = h3.find('a').get('href', None)
                self.final_list.append((h3.text.strip(), url + link))
            except : pass
        self.csv_saver()

    def csv_saver(self) :
        columns = ['TITLE', 'LINK']
        file_name = 'news.csv'
        df = pd.DataFrame(self.final_list, columns = columns)
        df.to_csv(file_name, index = False)
        driver.quit()
        print('News scraped successfully.')

scraper_object = scraper()
scraper_object.scroller()
