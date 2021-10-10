import sys
import urllib.request
from bs4 import BeautifulSoup
from nltk.corpus import stopwords, words, names
from nltk.stem import WordNetLemmatizer
import nltk

def analyseText(website):
    """website must be a http website address."""
    # read webcontent
    textsite = urllib.request.urlopen(website)
    html = textsite.read()

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
    lemmatizer = WordNetLemmatizer()

    # filter out stop words and rubbish
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

    # lemmatize
    newtokenlist = []
    for token in clean_tokens:
        new_token = lemmatizer.lemmatize(token)
        newtokenlist.append(new_token)

    freq = nltk.FreqDist(newtokenlist)

    mc = freq.most_common(5)
    print(mc[0][0])
    print(mc[1][0])
    print(mc[2][0])
    print(mc[3][0])
    print(mc[4][0])


if __name__ == "__main__":
    website = sys.argv[1]
    analyseText(website)

