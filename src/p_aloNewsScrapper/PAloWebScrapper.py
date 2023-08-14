# imports
import requests
import time
from datetime import datetime
import csv

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class ProthomAloNewsScrapper:
    def __init__(self, start_date, end_date, out_file="out.csv", output_file_type='csv'):
        self.__base_url = "https://www.prothomalo.com/search?type=text" #taking only text news (excluding video, image)
        self.__out_file=out_file
        self.__method=output_file_type
        self.__url=None
        self.driver = None
        self.__sdate=start_date
        self.__edate=end_date
        self.__sunix=None
        self.__eunix=None
        self.__news_links=None
        self.__articles=[]
        
    def convert_to_unix(self):
        # in miliseconds
        try:
            self.__sunix=datetime.strptime(self.__sdate, "%d-%m-%Y").timestamp()*1000
            self.__eunix=datetime.strptime(self.__edate, "%d-%m-%Y").timestamp()*1000
        except ValueError:
            raise
        
    def generate_url(self):
        self.convert_to_unix()
        self.__url=f'{self.__base_url}&published-after={self.__sunix}&published-before={self.__eunix}'
           
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
        #load url
        self.driver.get(self.__url)
        #give 5s to load
        time.sleep(1)
        #try to find add banner and dismiss
        try:
            wait = WebDriverWait(self.driver, 2)
            #find and switch to add banner frame
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[starts-with(@id,"google_ads_iframe_85406138/News_Int_")]')))
            #find closebutton
            ad_close_button = wait.until(EC.element_to_be_clickable((By.ID, "closebutton")))
            #click close buttton
            ad_close_button.click()
            print('-----------------------------')
            print('Add closed')
            #return to default frame
            self.driver.switch_to.default_content()
            print('Continuing')
            print('-----------------------------')
        except TimeoutException:
            print('-----------------------------')
            print("No adds banner found")
            print('Continuing')
            print('-----------------------------')
            
    def gather_news_links(self):
        if self.driver:
            self.driver.get(self.__url)
            print(self.__url)
            #scroll till end
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            #send it to bs4
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            #find all headlines in the page
            news_headlines = soup.find_all(
                ["h3", "h2", "h1"], class_="headline-title _1d6-d"
            )
            links=set()
            if len(news_headlines)>0:
                for article in news_headlines:
                    #find 1st parent <a> 
                    a_tag = article.find_parent("a")
                    if a_tag:
                        #find news link
                        links.add(a_tag["href"])
                self.__news_links=list(links)    
            else:
                print('no news found')
                
    def write_to_csv(self):
        with open(self.__out_file, "w", encoding="utf-8", newline="\n") as f:
            csv_writer = csv.writer(f, delimiter=",")
            csv_writer.writerow(("title", "content"))
            for article in self.__articles:
                csv_writer.writerow(article)
            
    def dump_to_json(self, aricle):
        pass
        
    def scrape_individual_news(self, news_link):
        self.driver.get(news_link)
        #Locating heading
        print(f'getting article: {news_link}')
        head_element=self.driver.find_element(By.TAG_NAME, "h1")
        heading=head_element.text
        print(f'found heading: {heading}')
        #scroll till end of the article
        scroll_till_element=self.driver.find_element(By.XPATH, '//div[@class="_0wq3t"]')
        ActionChains(self.driver).scroll_to_element(scroll_till_element).perform()
        #Locating article body 
        print('Locating article body')
        article_element=self.driver.find_element(By.XPATH, '//div[contains(@class,"story-------0")]')
        #an article body is combination of multiple <p> 
        texts=article_element.find_elements(By.XPATH, './/div[@class="story-element story-element-text"]')
        print('Article Body found')
        # text method is used in python to retrieve the text of WebElement
        texts=[t.text for t in texts]
        texts=''.join(texts).replace('\n',' ').replace('\r',' ')  
        return [heading, texts]        

    def batch_scrap(self):
        print(f'----Scrapping News from {self.__sdate} to {self.__edate}----')
        self.generate_url()
        self.init_driver()
        self.adds_remove()
        self.gather_news_links()
        for news_link in self.__news_links:
            if news_link.startswith('https://www.prothomalo.com/'):
                self.__articles.append(self.scrape_individual_news(news_link))
            time.sleep(2)
        print(f'Total news: {len(self.__articles)}')
        if self.__articles:
            if self.__method=='csv':
                self.write_to_csv()
            else:
                self.dump_to_json({"title":heading, "content":texts})
        else:
            print('no news found, Ending...')
        self.driver.quit()
        
        
        


if __name__ == "__main__":
    print(':::Enter date in %d-%m-%Y format:::')
    s_date=input('Enter Start Date (%d-%m-%Y): ')
    e_date=input('Enter End Date (%d-%m-%Y): ')
    print()
    pa_scrapper = ProthomAloNewsScrapper(s_date, e_date)
 
    pa_scrapper.batch_scrap()
