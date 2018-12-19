from utils import datascraping, remove_html_tags
import pickle as pkl
import pdb
import urllib.request
import io
#from lxml import html
import requests
#from bs4 import BeautifulSoup
import re
import spacy
from tqdm import tqdm

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

def get_textbody_per_page(corpus):
    text = []
    for tags in corpus:
        for idx in range(len(corpus[tags])):
            text.append(corpus[tags][idx])
    return text

nlp = spacy.load("en_core_web_lg")
def calc_sentence_similarity(textbody, textbody2 = None):#here textbody is a list of sentences
    similarity_score = []
    similarity_score2 = []
    if textbody2 is None:
        for idx1 in range(50):#len(textbody)):
            for idx2 in range(1,50):#len(textbody)):
                similarity_score.append(nlp(textbody[idx1]).similarity(nlp(textbody[idx2])))
    else:
        for idx1 in range(50):#len(textbody)):
            for idx2 in range(50):#len(textbody2)):
                similarity_score2.append(nlp(textbody[idx1]).similarity(nlp(textbody2[idx2])))
    return similarity_score, similarity_score2


#get all the text from electricity act
page = requests.get("https://www.ontario.ca/laws/statute/98e15#BK1")
to_be_removed = re.compile('<.*?>')
all_data = datascraping(page)
corpus = remove_html_tags(all_data, to_be_removed)
words = ['comply', 'shall', 'must', 'oblige']
print (count_words(corpus,words))
electricity_act_text = get_textbody_per_page(corpus)

#get all the text from climate act
page2 = requests.get("https://www.ontario.ca/laws/statute/16c07")
all_data2 = datascraping(page2)
corpus2 = remove_html_tags(all_data2, to_be_removed)
print (count_words(corpus2, words))
climate_act_text = get_textbody_per_page(corpus2)

#calculate similarity between each sentence in electricity act
for i in tqdm(range(10000)):
    score1 = calc_sentence_similarity(electricity_act_text)
    score2 = calc_sentence_similarity(electricity_act_text,climate_act_text )
