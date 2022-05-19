import json
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, InvalidSessionIdException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import copy
import argparse
import time

class Scraping():
    def __init__(self):
        self.mainObject = list()
        self.obj = dict()
        
    def getSite(self):
        s=Service(ChromeDriverManager().install())
        self.browser=webdriver.Chrome(service=s)
        self.browser.get('https://www.gittigidiyor.com')
        self.browser.maximize_window()
        
    def toPage(self, name):
        self.getSite()
        enterKey = self.browser.find_element(By.TAG_NAME, "input")
        enterKey.send_keys(name)
        enterKey.send_keys(Keys.ENTER)
        self.addClose()
        self.nextProduct()
            
    def addClose(self):
        self.browser.find_element(By.CLASS_NAME, "tyj39b-5.bEEsJG").click()
        
    def nextProduct(self):
        i=1
        while True:
            try:
                time.sleep(1)
                self.browser.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/ul/li["+str(i)+"]").click()
                i=i+1
                self.getData()
            except(NoSuchElementException):
                self.nextPage()
                
    def getData(self):
        self.obj["Ürün Adı"] = self.browser.find_element(By.ID, "sp-title").text
        self.obj["Yüksek Fiyat"] = self.browser.find_element(By.ID, "sp-price-highPrice").text
        self.obj["Düşük Fiyat"] = self.browser.find_element(By.ID, "sp-price-lowPrice").text
        self.obj["Satış ve Stok"] = self.browser.find_element(By.ID, "sp-soldInfoContainer").text
        
        self.mainObject.append(copy.copy(self.obj))
        self.browser.execute_script("window.history.go(-1)")
    
    def nextPage(self):
        try:
            self.browser.find_element(By.LINK_TEXT, "Sonraki").click()
            self.nextProduct()
        except:
            self.toJson()
            self.browser.quit()
        
    def toJson(self):
        with open('web_scraping.json', 'w', encoding='utf-8') as f:
            json.dump(self.mainObject, f, ensure_ascii=False, indent=2)
            
    def run(self, name):
        self.toPage(name)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--productName', type = str, required = True, help = "please enter info")
    
    args = parser.parse_args()
    Scraping.run("productName")
    
#Scraping().run("lg cep telefonu")
