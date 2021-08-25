from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import bs4
import requests
import json


#setting up the wwebdriver
driver=webdriver.Chrome('E:\My_projects\web scraping\chromedriver.exe')
driver.get("https://www.alchourouk.com/%D8%A7%D9%84%D8%B1%D8%A6%D9%8A%D8%B3%D9%8A%D8%A9")

#list of the topic that we want to scrape
l=["سياسة","وطنية","جهاتنا","رياضة"]

#generate a soup
def create_soup(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    return soup

#get the new from providen url
def get_event(url):
    page = create_soup(url)
    events = page.find_all(class_="field field--name-body field--type-text-with-summary field--label-hidden field--item")
    event = events[4].text.strip()
    return event 

#save news to dict
def collect_all_data(li,key_word,out_data):
    out_data[key_word]=dict()
    for i in range(len(li)):
        out_data[key_word][i+1]=get_event(li[i])


#enter into given keyword then scrape the links of the news to scrape later
def collect_data_from_one_page(key_word,out_data):
    out=set()
    link=driver.find_element_by_link_text(key_word)
    link.click()
    sleep(5)
    print(key_word+"\n\n")
    elems = driver.find_elements_by_css_selector(".fieldset [href]")
    links = [elem.get_attribute('href') for elem in elems]
    for li in links:
        out.add(li)
    driver.back()
    sleep(2)
    li=list(out)
    collect_all_data(li,key_word,out_data)


#scrape all data
def scrape(l):
    out_data = dict()
    for key_word in l:
        collect_data_from_one_page(key_word,out_data)
        
    return out_data


if __name__=="__main__":
    out_data=scrape(l)
    data_file = open("data.json", "w")
    json.dump(out_data, data_file, ensure_ascii=False)
    data_file.close()

