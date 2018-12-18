
import pickle as pkl
import pdb
import urllib.request
#import io
#from lxml import html
import requests
from bs4 import BeautifulSoup
import re

page = requests.get("https://www.ontario.ca/laws/statute/98e15#BK1")

def datascraping(page):
   #print ("start")
#status_code indicates if the page was downloaded successfully. status_code of 200 means success. status_code starting with 4 or 5 indicates an error
   #print (page.status_code)
   soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())
   html_classes = ["paragraph", "subsection", "definition", "Pnote", "Yheadnote", "Ydefinition", "Ysection", "Yparagraph","Ysubsection", "Ysubpara","Ysubsubpara","Yclause", "Yfirstdef","subsubpara","section"]
   dict_soup_obj = {}
   corpus_dict = {}

   #this for loop creates a soup object for every html class we need 
   for elem in html_classes:
      dict_soup_obj[elem] = soup.find_all(class_ = elem)
   #pdb.set_trace()
   
   #this for loop is used to convert the soup object to string
   for elem in dict_soup_obj:
      corpus = []
      for lines in dict_soup_obj[elem]:
         corpus.append(str(lines))
      corpus_dict[elem] = (corpus)

   return corpus_dict
   
#the below function removes the html tags from the text
to_be_removed = re.compile('<.*?>')
def remove_html_tags(corpus, to_be_removed):
   for html_class in corpus:
      for idx in range(0, len(corpus[html_class])):
         corpus[html_class][idx] = re.sub(to_be_removed, '',corpus[html_class][idx])
   return corpus 

'''
all_data = datascraping(page)
all_data_with_no_tags = remove_html_tags(all_data, to_be_removed)
'''