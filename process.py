from utils import datascraping, remove_html_tags
import pickle as pkl
import pdb
import urllib.request
import io
#from lxml import html
import requests
#from bs4 import BeautifulSoup
import re

def count_words(corpus, words):
    count = {}
    for word in words:
        for html_class in corpus:
            for idx in range(len(corpus[html_class])):
                if word in corpus[html_class][idx]:
                    count[word] = count.get(word, 0)+1
    '''
    for word in words:
        for idx in range(0,len(text)):
            if word in text[idx]:
                count[word] = count.get(word, 0)+1
    '''
    pdb.set_trace()
    return count

page = requests.get("https://www.ontario.ca/laws/statute/98e15#BK1")
to_be_removed = re.compile('<.*?>')
all_data = datascraping(page)
corpus = remove_html_tags(all_data, to_be_removed)
print (count_words(corpus,['shall', 'must', 'comply', 'oblige']))
pdb.set_trace