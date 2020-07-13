import numpy as np
import pandas as pd
from sklearn import preprocessing

import seaborn as sns
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS


import re
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from wordcloud import WordCloud,STOPWORDS
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize,sent_tokenize
from bs4 import BeautifulSoup
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from textblob import TextBlob
    
#stop_words = stopwords.words('english')
#stop_words.extend(['please', 'pls'])
#punctuation = list(string.punctuation)
#stop_words.update(punctuation)

    #spell correction
#def spellcorrection(str1):
      #return str(TextBlob(str1).correct())

def known_contractions(embed):
    known = []
    for contract in contraction_mapping:
        if contract in embed:
            known.append(contract)
    return known


def clean_contractions(text, mapping):
    specials = ["’", "‘", "´", "`"]
    for s in specials:
        text = text.replace(s, "'")
    text = ' '.join([mapping[t] if t in mapping else t for t in text.split(" ")])
    return text

def unknown_punct(embed, punct):
    unknown = ''
    for p in punct:
        if p not in embed:
            unknown += p
            unknown += ' '
    return unknown

def clean_special_chars(text, punct, mapping):
    for p in mapping:
        text = text.replace(p, mapping[p])

    for p in punct:
        text = text.replace(p, f' {p} ')

    specials = {'\u200b': ' ', '…': ' ... ', '\ufeff': '', }  #
    for s in specials:
        text = text.replace(s, specials[s])

    return text

def removeString(data, regex):
    return data.str.lower().str.replace(regex.lower(), ' ')

def cleanDataset(dataset, columnsToClean, regexList):
    for column in columnsToClean:
        for regex in regexList:
            dataset[column] = removeString(dataset[column], regex)
    return dataset

def getregexList():
    '''
    Adding regex list as per the given data set to flush off the unnecessary text
    '''
    regexList = []
    regexList += ['From:(.*)\r\n']  # from line
    regexList += ['Sent:(.*)\r\n']  # sent to line
    regexList += ['received from:(.*)\r\n']  # received data line
    regexList += ['received']  # received data line
    regexList += ['To:(.*)\r\n']  # to line
    regexList += ['CC:(.*)\r\n']  # cc line
    regexList += ['(.*)infection']  # footer
    regexList += ['\[cid:(.*)]']  # images cid
    regexList += ['https?:[^\]\n\r]+']  # https & http
    regexList += ['Subject:']
    regexList += ['[\w\d\-\_\.]+@[\w\d\-\_\.]+']  # emails are not required
    regexList += ['[0-9][\-0–90-9 ]+']  # phones are not required
    regexList += ['[0-9]']  # numbers not needed
    regexList += ['[^a-zA-z 0-9]+']  # anything that is not a letter
    regexList += ['[\r\n]']  # \r\n
    # regexList += [' [a-zA-Z] ']  # single letters makes no sense
    # regexList += [' [a-zA-Z][a-zA-Z] ']  # two-letter words makes no sense
    regexList += ["  "]  # double spaces

    regexList += ['^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$']
    # regexList += ['[\w\d\-\_\.]+ @ [\w\d\-\_\.]+']
    # regexList += ['Subject:']
    # regexList += ['[^a-zA-Z]']
    # Replace all $, ! and ? with special strings
    regexList += ['[$]']
    regexList += ['[!]']
    regexList += ['[?]']
    regexList += ['[#]']
    # Remove all other punctuation (replace with white space)
    regexList += ['([^\w\d\s]+)|([_-]+)']
    # whitespaces of any length
    regexList += ['\s+']

    return regexList

def data_cleaning(tickets_df):
    tickets_df['Short description'][3383]="User login issue"
    tickets_df['Short description'][3906]="vpn issue user login"
    tickets_df['Short description'][3906]="vpn issue user login"
    tickets_df['Short description'][3915]="vpn issue user login"
    tickets_df['Short description'][3921]="vpn issue user login"
    tickets_df['Short description'][3924]="vpn issue user login"
    tickets_df['Short description'][4341]="vpn issue user login"
    tickets_df['Short description'][2604]="Link issues"
    tickets_df['Description'][4395]="Skype login issues"
            
    stop_words = stopwords.words('english')
    stop_words.extend(["sr", "psa", "perpsr", "psa", "good", "evening", "will", "night", "afternoon","png", "mailto" "ca","nt","at" "i", "vip", "llv", "xyz",
                  "cid", "image", "gmail","co", "in", "com", "ticket", "company", "received", "0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "A", "a1", "a2",
                  "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad",
                  "added", "adj", "ae", "af", "affected", "affecting", "after", "afterwards", "ag", "again", "against", "ah", "ain", "aj", "al", "all",
                  "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount",
                  "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anyway", "anyways", "anywhere", "ao", "ap", "apart",
                  "apparently", "appreciate", "approximately", "ar", "are", "aren", "arent", "arise", "around","articl", "as", "aside", "ask", "asking", "at", "au",
                  "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "B", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became",
                  "been", "before", "beforehand", "beginnings", "behind", "below", "beside", "besides", "best", "between", "beyond", "bi", "bill", "biol",
                  "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "C", "c1", "c2", "c3",
                  "ca", "call", "came", "can", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "ci", "cit", "cj", "cl", "clearly", "cm", "cn",
                  "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "could", "couldn", "couldnt", "course",
                  "cp", "cq", "cr", "cry", "cs", "ct", "cu", "cv", "cx", "cy", "cz", "d", "D", "d2", "da", "date", "dc", "dd", "de", "definitely",
                  "describe", "described", "despite", "detail", "df", "di", "did", "didn", "dj", "dk", "dl", "do", "does", "doesn", "doing", "don",
                  "done", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "E", "e2", "e3", "ea", "each", "ec",
                  "ed", "edu", "ee", "ef", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "en", "end", "ending",
                  "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every",
                  "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "F", "f2", "fa", "far", "fc", "few",
                  "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows",
                  "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore",
                  "fy", "g", "G", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going",
                  "gone", "got", "gotten", "gr", "greetings","greeting", "gs", "gy", "h", "H", "h2", "h3", "had", "hadn", "happens", "hardly", "has", "hasn", "hasnt",
                  "have", "haven", "having", "he", "hed", "hi","hello", "help", "hence", "here", "hereafter", "hereby", "herein", "heres", "hereupon", "hes",
                  "hh", "hi", "hid", "hither", "hj", "ho", "hopefully", "how", "howbeit", "however", "hs", "http", "hu", "hundred", "hy", "i2", "i3", "i4",
                  "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "im", "immediately", "in",
                  "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest",
                  "into", "inward", "io", "ip", "iq", "ir", "is", "isn", "it", "itd", "its", "iv", "ix", "iy", "iz", "j", "J", "jj", "jr", "js",
                  "jt", "ju", "just", "k", "K", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "ko", "l", "L", "l2", "la", "largely", "last",
                  "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "lf", "like", "liked",
                  "likely", "line", "little", "lj", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "M", "m2",
                  "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "meantime", "meanwhile", "merely", "mg", "might", "mightn",
                  "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu",
                  "much", "mug", "must", "mustn", "my", "n", "N", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily",
                  "neither", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "nobody", "non", "none", "nonetheless", "noone",
                  "normally", "nos", "noted", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "O", "oa", "ob", "obtain", "obtained", "obviously",
                  "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones",
                  "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "otherwise", "ou", "ought", "our", "out", "outside", "over", "overall",
                  "ow", "owing", "own", "ox", "oz", "p", "P", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly",
                  "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po",
                  "poorly", "pp", "pq", "pr", "predominantly", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps",
                  "pt", "pu", "put", "py", "q", "Q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "R", "r2", "ra", "ran", "rather", "rc", "rd", "re",
                  "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively",
                  "research", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq",
                  "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "S", "s2", "sa", "said", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second",
                  "secondly", "section", "seem", "seemed", "seeming", "seems", "seen", "sent", "seven", "several", "sf", "shall", "shan", "shed", "shes",
                  "show", "showed", "shown", "showns", "shows", "si", "side", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so",
                  "some", "somehow", "somethan", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified",
                  "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such",
                  "sufficiently", "suggest", "sup", "sure", "sy", "sz", "t", "T", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te",
                  "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "thats", "the", "their", "theirs", "them", "themselves",
                  "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "thereof", "therere", "theres", "thereto",
                  "thereupon", "these", "they", "theyd", "theyre", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou",
                  "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn",
                  "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "tt",
                  "tv", "twelve", "twenty", "twice", "two", "tx", "u", "U", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless",
                  "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "used", "useful", "usefully", "usefulness", "using",
                  "usually", "ut", "v", "V", "va", "various", "vd", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt",
                  "vu", "w", "W", "wa", "was", "wasn", "wasnt", "way", "we", "wed", "welcome", "well", "well-b", "went", "were", "weren", "werent", "what",
                  "whatever", "whats", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "whereupon",
                  "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "whom", "whomever", "whos", "whose",
                  "why", "wi", "widely", "with", "within", "without", "wo", "won", "wonder", "wont", "would", "wouldn", "wouldnt", "www", "x", "X",
                  "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "Y", "y2", "yes", "yet", "yj", "yl", "you",
                  "youd", "your", "youre", "yours", "yr", "ys", "yt", "z", "Z", "zero", "zi", "zz"])

    tickets_df.drop_duplicates(inplace=True)
    
    # tickets_df = tickets_df.astype(str)
    convert_dict = {
        'Short description': str,
        'Description': str,
        'Caller': str,
        'Assignment group': str,}
    tickets_df = tickets_df.astype(convert_dict)
    tickets_df['word_count'] = tickets_df['Short description'].apply(lambda x: len(str(x).split(" ")))
    tickets_df['word_count'] = tickets_df['Description'].apply(lambda x: len(str(x).split(" ")))
    tickets_df['word_count'] = tickets_df['Caller'].apply(lambda x: len(str(x).split(" ")))
    tickets_df['word_count'] = tickets_df['Assignment group'].apply(lambda x: len(str(x).split(" ")))
    tickets_df['char_count'] = tickets_df['Short description'].str.len()  ## this also includes spaces
    tickets_df['char_count'] = tickets_df['Description'].str.len() ## this also includes spaces
    tickets_df['char_count'] = tickets_df['Caller'].str.len()  ## this also includes spaces
    tickets_df['char_count'] = tickets_df['Assignment group'].str.len()  ## this also includes spaces

    tickets_df['stopwords'] = tickets_df['Short description'].apply(lambda x: len([x for x in x.split() if x in stop_words]))
    tickets_df['stopwords'] = tickets_df['Description'].apply(lambda x: len([x for x in x.split() if x in stop_words]))
    tickets_df['stopwords'] = tickets_df['Caller'].apply(lambda x: len([x for x in x.split() if x in stop_words]))
    tickets_df['stopwords'] = tickets_df['Assignment group'].apply(lambda x: len([x for x in x.split() if x in stop_words]))

    tickets_df['hastags'] = tickets_df['Short description'].apply(lambda x: len([x for x in x.split() if x.startswith('#')]))
    tickets_df['hastags'] = tickets_df['Description'].apply(lambda x: len([x for x in x.split() if x.startswith('#')]))
    tickets_df['hastags'] = tickets_df['Caller'].apply(lambda x: len([x for x in x.split() if x.startswith('#')]))
    tickets_df['hastags'] = tickets_df['Assignment group'].apply(lambda x: len([x for x in x.split() if x.startswith('#')]))
    tickets_df['numerics'] = tickets_df['Short description'].apply(lambda x: len([x for x in x.split() if x.isdigit()]))
    tickets_df['numerics'] = tickets_df['Description'].apply(lambda x: len([x for x in x.split() if x.isdigit()]))

    tickets_df['numerics'] = tickets_df['Caller'].apply(lambda x: len([x for x in x.split() if x.isdigit()]))
    tickets_df['numerics'] = tickets_df['Assignment group'].apply(lambda x: len([x for x in x.split() if x.isdigit()]))
    tickets_df['upper'] = tickets_df['Short description'].apply(lambda x: len([x for x in x.split() if x.isupper()]))
    tickets_df['upper'] = tickets_df['Description'].apply(lambda x: len([x for x in x.split() if x.isupper()]))
    tickets_df['upper'] = tickets_df['Caller'].apply(lambda x: len([x for x in x.split() if x.isupper()]))

    freq = pd.Series(' '.join(tickets_df['Short description']).split()).value_counts()[:10]
    freq = pd.Series(' '.join(tickets_df['Description']).split()).value_counts()[:10]
    freq = pd.Series(' '.join(tickets_df['Caller']).split()).value_counts()[:10]
    freq = pd.Series(' '.join(tickets_df['Assignment group']).split()).value_counts()[:10]
    
    contraction_mapping = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not", "didn't": "did not",  "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not", "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is",  "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have","I'm": "I am", "I've": "I have", "i'd": "i would", "i'd've": "i would have", "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would", "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have","it's": "it is", "let's": "let us", "ma'am": "madam", "mayn't": "may not", "might've": "might have","mightn't": "might not","mightn't've": "might not have", "must've": "must have", "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock", "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would", "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", "she's": "she is", "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have","so's": "so as", "this's": "this is","that'd": "that would", "that'd've": "that would have", "that's": "that is", "there'd": "there would", "there'd've": "there would have", "there's": "there is", "here's": "here is","they'd": "they would", "they'd've": "they would have", "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", "to've": "to have", "wasn't": "was not", "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have", "what're": "what are",  "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", "where's": "where is", "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have", "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have", "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have","you'd": "you would", "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have", "you're": "you are","hr": "human resource" , }

    tickets_df['Short description_Contrt'] = tickets_df['Short description'].apply(lambda x: clean_contractions(x, contraction_mapping))
    tickets_df['Description_Contrt'] = tickets_df['Description'].apply(lambda x: clean_contractions(x, contraction_mapping))

    punct = "/-'?!,#$%\'()*+-/:;<=>[\\]^{|}~" + '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
    punct_mapping = {"‘": "'", "₹": "e", "´": "'", "°": "", "€": "e", "™": "tm", "√": " sqrt ", "×": "x", "²": "2", "—": "-", "–": "-", "’": "'", "_": "-", "`": "'", '“': '"', '”': '"', '“': '"', "£": "e", '∞': 'infinity', 'θ': 'theta', '÷': '/', 'α': 'alpha', '•': '.', 'à': 'a', '−': '-', 'β': 'beta', '∅': '', '³': '3', 'π': 'pi', }

    tickets_df['punct_Short description'] = tickets_df['Short description_Contrt'].apply(lambda x: clean_special_chars(x, punct, punct_mapping))
    tickets_df['punct_Description'] = tickets_df['Description_Contrt'].apply(lambda x: clean_special_chars(x, punct, punct_mapping))

    # Select columns for cleaning
    # Create list of regex to remove sensitive data
    # Clean dataset and remove sensitive data
    tickets_df['Clean Short Description'] = tickets_df['punct_Short description']
    columnsToClean = ['Clean Short Description']
    clean_tickets_df = cleanDataset(tickets_df, columnsToClean, getregexList())

    tickets_df['Clean Description'] = tickets_df['punct_Description']
    # Select columns for cleaning
    columnsToClean = ['Clean Description']
    clean_tickets_df = cleanDataset(tickets_df, columnsToClean, getregexList())

    tickets_df['Clean Caller'] = tickets_df['Caller']
    # Select columns for cleaning
    columnsToClean = ['Clean Caller']
    clean_tickets_df = cleanDataset(tickets_df, columnsToClean, getregexList())
    
    # Create list of regex to remove sensitive data
    # Clean dataset and remove sensitive data
    clean_tickets_df['word_count'] = clean_tickets_df['Clean Short Description'].apply(lambda x: len(str(x).split(" ")))
    clean_tickets_df['word_count'] = clean_tickets_df['Clean Description'].apply(lambda x: len(str(x).split(" ")))
    clean_tickets_df['char_count'] = clean_tickets_df['Clean Short Description'].str.len()  ## this also includes spaces
    clean_tickets_df['char_count'] = clean_tickets_df['Clean Description'].str.len()  ## this also includes spaces
    clean_tickets_df['stopwords'] = clean_tickets_df['Clean Short Description'].apply(lambda x: len([x for x in x.split() if x in stop_words]))
    clean_tickets_df['stopwords'] = clean_tickets_df['Clean Description'].apply(lambda x: len([x for x in x.split() if x in stop_words]))
    clean_tickets_df['hastags'] = clean_tickets_df['Clean Description'].apply(lambda x: len([x for x in x.split() if x.startswith('#')]))
    clean_tickets_df['hastags'] = clean_tickets_df['Clean Short Description'].apply(lambda x: len([x for x in x.split() if x.startswith('#')]))

    clean_tickets_df['numerics'] = clean_tickets_df['Clean Short Description'].apply(lambda x: len([x for x in x.split() if x.isdigit()]))
    clean_tickets_df['upper'] = clean_tickets_df['Clean Description'].apply(lambda x: len([x for x in x.split() if x.isupper()]))
    clean_tickets_df['upper'] = clean_tickets_df['Clean Short Description'].apply(lambda x: len([x for x in x.split() if x.isupper()]))
    clean_tickets_df['Clean Short Description_1'] = clean_tickets_df['Clean Short Description'].apply(lambda x: " ".join(x.lower() for x in x.split()))
    clean_tickets_df['Clean Description_1'] = clean_tickets_df['Clean Description'].apply(lambda x: " ".join(x.lower() for x in x.split()))

    freq = pd.Series(' '.join(clean_tickets_df['Clean Short Description_1']).split()).value_counts()[:10]
    freq = pd.Series(' '.join(clean_tickets_df['Clean Description_1']).split()).value_counts()[:10]


    #stop words
    stop_words = stopwords.words('english')
    stop_words.extend(['please', 'pls','hello','help','good morning','able','yes','na',])
 
    clean_tickets_df['Clean_Shrt_Desc_SWR'] = clean_tickets_df['Clean Short Description_1'].apply(lambda x: " ".join(x for x in x.split() if x not in stop_words))
    clean_tickets_df['Clean_Desc_SWR'] = clean_tickets_df['Clean Description_1'].apply(lambda x: " ".join(x for x in x.split() if x not in stop_words))

    #Lemmatization
    from textblob import Word
    clean_tickets_df['Clean_Shrt_Desc_lem'] = clean_tickets_df['Clean_Shrt_Desc_SWR'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
    clean_tickets_df['Clean_Desc_lem'] = clean_tickets_df['Clean_Desc_SWR'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

    return clean_tickets_df


def spell_correction(df,desc_colname,shortdesc_colname):
    df['SpellCorrected_Desc'] = df[desc_colname].apply(lambda x: str(TextBlob(x).correct()))
    df['SpellCorrected_Short_Desc'] = df[shortdesc_colname].apply(lambda x: str(TextBlob(x).correct()))
    return df


































