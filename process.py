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
    return count

def get_sentences(corpus, words):
    sentence_dict = {}
    #sentences = []
    for word in words:
        sentences = []
        for html_class in corpus:
            for idx in range(len(corpus[html_class])):
                if word in corpus[html_class][idx]:
                    sentences.append(corpus[html_class][idx])
        sentence_dict[word] = sentences
    #pdb.set_trace()
    return sentence_dict

page = requests.get("https://www.ontario.ca/laws/statute/98e15#BK1")
to_be_removed = re.compile('<.*?>')
all_data = datascraping(page)
corpus = remove_html_tags(all_data, to_be_removed)
words = ['comply', 'shall', 'must', 'oblige']
print (count_words(corpus,words))
#print (get_sentences(corpus, words))
#pdb.set_trace()