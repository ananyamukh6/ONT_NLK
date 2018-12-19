from utils import datascraping, remove_html_tags
import pickle as pkl, pdb
import urllib.request, io, requests ,re
import spacy
from tqdm import tqdm
import nltk, string
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize

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
def calc_sentence_similarity(textbody, textbody2,no_of_sentences = None):#here textbody is a list of sentences
    similarity_score = {}
    #similarity_score2 = []
    if no_of_sentences is None:
        for idx1 in tqdm(range(len(textbody))):#len(textbody)):
            for idx2 in range(len(textbody2)):#len(textbody)):
            #similarity_score.append(nlp(textbody[idx1]).similarity(nlp(textbody[idx2])))
                similarity_score[(idx1, idx2)] = nlp(textbody[idx1]).similarity(nlp(textbody2[idx2]))
    else:
        for idx1 in tqdm(range(no_of_sentences)):#len(textbody)):
            for idx2 in range(no_of_sentences):#len(textbody)):
            #similarity_score.append(nlp(textbody[idx1]).similarity(nlp(textbody[idx2])))
                similarity_score[(idx1, idx2)] = nlp(textbody[idx1]).similarity(nlp(textbody2[idx2]))
    return similarity_score



def preprocessing(text):
    #tokenize the text
    tokenized_sents = [word_tokenize(i) for i in text] #this is a list of list
    #remove punctuations
    for idx in tokenized_sents:
        #pdb.set_trace()
        for i in idx:
            i = re.sub(r'[^\w\s]','',i)
    print (tokenized_sents[0])
            #[i.translate(None, string.punctuation) for i in tokenized_sents[idx]]
    '''
    nltk_stopwords = nltk.corpus.stopwords.words('english')
    print (nltk_stopwords)
    words = []
    for sentence in corpus:
        for word in word_tokenize(sentence.lower):
            if word not in nltk_stopwords:
                words += [word]
    '''




#get all the text from electricity act
page = requests.get("https://www.ontario.ca/laws/statute/98e15#BK1")
to_be_removed = re.compile('<.*?>')
all_data = datascraping(page)
corpus = remove_html_tags(all_data, to_be_removed)
words = ['comply', 'shall', 'must', 'oblige']
print (count_words(corpus,words))
electricity_act_text = get_textbody_per_page(corpus)
#pdb.set_trace()
preprocessing(electricity_act_text)
'''
#get all the text from climate act
page2 = requests.get("https://www.ontario.ca/laws/statute/16c07")
all_data2 = datascraping(page2)
corpus2 = remove_html_tags(all_data2, to_be_removed)
print (count_words(corpus2, words))
climate_act_text = get_textbody_per_page(corpus2)

#calculate similarity between each sentence in electricity act
score1 = calc_sentence_similarity(electricity_act_text,electricity_act_text)
score2 = calc_sentence_similarity(electricity_act_text,climate_act_text )
#print (score1)
#print (score2)
pkl.dump( score1, open( "savesamescore.p", "wb" ) )
pkl.dump(score2, open("savediffscore.p","wb"))
pdb.set_trace()
'''
