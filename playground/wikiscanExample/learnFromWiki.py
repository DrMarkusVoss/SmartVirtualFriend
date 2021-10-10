import urllib.request
from bs4 import BeautifulSoup
from nltk.corpus import stopwords, words, names
import nltk.corpus
import nltk

# read webcontent
#wikidog = urllib.request.urlopen('https://en.wikipedia.org/wiki/Dog')
wikidog = urllib.request.urlopen('https://en.wikipedia.org/wiki/Winston_Churchill')
html = wikidog.read()

# extract text
soup = BeautifulSoup(html,'html5lib')
text = soup.get_text(strip = True)

tokens = [t for t in text.split()]

# process
setofstopwords = set(stopwords.words('english'))
# basic set of words
#setofwords = set(words.words("en-basic"))
# full set of words
setofwords = set(words.words())
setofnames = set(names.words())
clean_tokens = tokens[:]
for token in tokens:
    if token in setofstopwords:
        clean_tokens.remove(token)
    else:
        # eliminate rubbish
        isword = True
        #print("check: " + token)
        isword = token in setofwords
        isname = token in setofnames
        if (not isword) and (not isname):
            clean_tokens.remove(token)

freq = nltk.FreqDist(clean_tokens)
for key, val in freq.items():
    print(str(key) + ':' + str(val))
freq.plot(20, cumulative=False)