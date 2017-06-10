#coding:utf-8    
  
import urllib2
import requests
import re
from bs4 import BeautifulSoup
import time

def get_html_content(text, se_res):
    if not text:
        raise Exception("ERROR INFO :Input value is  null...")
       
    base_url = 'http://www.youdao.com/w/eng/%s/#keyfrom=dict2.top' % (text)
    content = requests.get(base_url).content
    get_res(content, se_res)
            
def  get_res(content, se_res):
    soup = BeautifulSoup(content, "html.parser")
    # get the word's soundmark
    try:
        res_sound = soup.find("div", { "id" : "phrsListTab" }).find_all("span", { "class" : "pronounce" })
        res_meaning = soup.find("div", { "id" : "phrsListTab" }).find_all('ul')       
    except AttributeError, e:
        raise Exception("ERROR INFO :Not found the word...")
                
    for key in res_sound:
        res = re.sub('[\n\t\b\s]', '', key.text)
        if res != None:
            se_res.append(res)
                   
    # get the word's meaning      
    ul_list = str(res_meaning[0])                                       # beautifulshop need string variables
    soup_ul = BeautifulSoup(ul_list, "html.parser")         
    for key in soup_ul.stripped_strings:
        if key != None:
            se_res.append(key)


    
