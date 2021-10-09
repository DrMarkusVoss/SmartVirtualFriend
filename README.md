# SmartVirtualFriend
Trying to use NLP and suitable knowledge representation to make a smart, learning and reasoning friend that
is able to answer all your questions.

With today's NLP approaches the processing of human language has made big progress, but the understanding of 
the contents by semantics is still not achieved. I want to find out where the challenges still are, and
which approaches might work and which limits they have.

## The Goal
- build up a knowledge base by processing natural language texts (texts written to be understood/processed
  by humans, like e.g. articles in Wikipedia or on news-websites) or from textual conversation (pseudo
  messenger communication interface)
- answer questions by processing/evaluating/searching the knowledge base incl. reasoning

## System Requirements
- Python3
- pip3

pip install the following:
- bs4
- html5lib
- matplotlib
- nltk

Then open the Python console and do:
```
import nltk

nltk.download()
```
Then install all.

If you encounter problems reading webcontent with Python using bs4 (done in 
some examples), make sure to install the certificates:

- goto Macintosh HD/Applications/Python3.x/
- execute "Install Certificates.command"
