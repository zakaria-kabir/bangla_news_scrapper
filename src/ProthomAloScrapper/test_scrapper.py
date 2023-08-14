# _*_coding: utf-8_*_

# import
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class Scrapper:
    def __init__(self, url):
        self.__url = url

    # retriving news urls from base or sub_page url
    def retrive_news_urls(self):
        
        driver = None

        #try to find any webdriver 
        try:
            #run browser headless (silent)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
            #init driver
            driver = webdriver.Chrome(chrome_options)
        except:
            try:
                #run browser headless (silent)
                edge_options = webdriver.EdgeOptions()
                edge_options.add_argument("--headless=new")
                edge_options.add_argument("--disable-gpu")
                #init driver
                driver = webdriver.Edge(edge_options)
            except:
                try:
                    #run browser headless (silent)
                    firefox_options = webdriver.FirefoxOptions()
                    firefox_options.add_argument("--headless=new")
                    firefox_options.add_argument("--disable-gpu")
                    #init driver
                    driver = webdriver.Firefox(firefox_options)
                except:
                    try:
                        #run browser headless (silent)
                        safari_options = webdriver.safari.options.Options()
                        safari_options.add_argument("--headless=new")
                        safari_options.add_argument("--disable-gpu")
                        #init driver
                        driver = webdriver.Safari(safari_options)
                    except:
                        print("Error: Unable to initialize any webdriver")
        '''
        ----current structure of ProthomAlo News----
        <a aria-label=" কিছু একটা হেডলাইন।" target="_self" class="card-with-image-zoom" href="https://www.prothomalo.com/bangladesh/crime/y2x5arnnpx">
            <h3 class="headline-title  _1d6-d"> ----> ....Capturing this class....
                <span class="tilte-no-link-parent"> কিছু একটা হেডলাইন।</span>
            </h3>
            <p class="excerpt _4Nuxp">
                পরিবার বলছে, দূর সম্পর্কের এক আত্মীয় গতকাল শনিবার রাত সাড়ে ১০টার দিকে বসন্তকে ঢাকা বিশ্ববিদ্যালয় এলাকায় ডেকে নিয়ে যান। এরপর কলাভবনের সামনে এলোপাতাড়ি কিলঘুষি, চড়থাপ্পড় দেন।
            </p>
            <div>
                <div class="story-meta-data sONJ0">
                    <time class="published-time fw8bp">৮ ঘণ্টা আগে</time>
                </div>
            </div>
        </a>
        '''
        if driver:
            driver.get(self.__url)
            #scroll till end
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            #send it to bs4
            soup = BeautifulSoup(driver.page_source, "html.parser")
            #find all headlines in the page
            news_headlines = soup.find_all(
                ["h3", "h2", "h1"], class_="headline-title _1d6-d"
            )
            for article in news_headlines:
                #find 1st parent <a> 
                a_tag = article.find_parent("a")
                if a_tag:
                    #find news link
                    link = a_tag["href"]
                    print(link)
            #close browser        
            driver.quit()


# global var
base_url = "https://www.prothomalo.com/"

sub_list = [
    "politics",
    "bangladesh",
    "bangladesh/crime",
    "world",
    "business",
    "opinion",
    "sports",
    "entertainment",
    "lifestyle",
    "technology",
    "education",
    "lifestyle/health",
    "religion",
]
s = Scrapper(base_url + sub_list[0])
s.retrive_page()
