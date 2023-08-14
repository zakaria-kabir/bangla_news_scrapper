# imports
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class ProthomAloNewsScrapper:
    def __init__(self, out_file="out.csv"):
        self.base_url = "https://www.prothomalo.com/search"
        self.driver = None

    def init_driver(self):
        # try to find any webdriver
        try:
            # run browser headless (silent)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")

            # init driver
            self.driver = webdriver.Chrome(chrome_options)
        except:
            try:
                # run browser headless (silent)
                edge_options = webdriver.EdgeOptions()
                edge_options.add_argument("--headless=new")
                edge_options.add_argument("--disable-gpu")
                # init driver
                self.driver = webdriver.Edge(edge_options)
            except:
                try:
                    # run browser headless (silent)
                    firefox_options = webdriver.FirefoxOptions()
                    firefox_options.add_argument("--headless=new")
                    firefox_options.add_argument("--disable-gpu")
                    # init driver
                    self.driver = webdriver.Firefox(firefox_options)
                except:
                    try:
                        # run browser headless (silent)
                        safari_options = webdriver.safari.options.Options()
                        safari_options.add_argument("--headless=new")
                        safari_options.add_argument("--disable-gpu")
                        # init driver
                        self.driver = webdriver.Safari(safari_options)
                    except:
                        print("Error: Unable to initialize any webdriver")
    
    def adds_remove(self):
        #initialize driver
        self.init_driver()
        #load url
        self.driver.get(self.base_url)
        #give 5s to load
        time.sleep(5)
        #try to find add banner and dismiss
        try:
            wait = WebDriverWait(self.driver, 10)
            #find and switch to add banner frame
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[starts-with(@id,"google_ads_iframe_85406138/News_Int_")]')))
            #find closebutton
            ad_close_button = wait.until(EC.element_to_be_clickable((By.ID, "closebutton")))
            #click close buttton
            ad_close_button.click()
            print('Add closed')
            #return to default frame
            self.driver.switch_to.default_content()
        except TimeoutException:
            print("No adds found")

        time.sleep(5)
        self.driver.quit()


if __name__ == "__main__":
    pa_scrapper = ProthomAloNewsScrapper()
    pa_scrapper.adds_remove()
