from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from word2number import w2n

# knowledge database
kdb = {"things": {}}

lemmatizer = WordNetLemmatizer()

def getVBZString(verb_term):
  """Return the verb word."""
  res = ""
  for e in verb_term.leaves():
    if e[1] == "VBZ" or e[1] == "VBP":
      res = e[0]

  return res

def getNNString(nn_term):
  """Return the noun word, evtl. with count word."""
  res = ""
  res_cd = ""
  for e in nn_term.leaves():
    if e[1] == "NN":
      res = e[0].lower()
    elif e[1] == "NNS":
      res = lemmatizer.lemmatize(e[0].lower())
    elif e[1] == "NNP":
      res = e[0]
    elif e[1] == "CD":
      num = 0
      if e[0].isdecimal():
        res_cd = int(e[0])
      else:
        res_cd = w2n.word_to_num(e[0])

  return res, res_cd


def addToKDB(subj, pred, obj):
  """Add information to knowledge database."""

  global kdb

  p = getVBZString(pred)

  if p == "is" or p == "are":
    nso, _ = getNNString(obj)
    nss, _ = getNNString(subj)
    if not nso in kdb["things"]:
      obj_dict = {nso: {"generalizes": [nss]}}
      kdb["things"][nso] = {"generalizes": [nss]}
      print("==> added that to my knowledge base: ", obj_dict)
      #print()
    else:
      if not nss in kdb["things"][nso]["generalizes"]:
        obj_dict = {nso: {"generalizes": [nss]}}
        kdb["things"][nso]["generalizes"].append(nss)
        print("==> added that to my knowledge base: ", obj_dict)
        #print()
      else:
        print("==> I already know that...\n")
  elif p == "has" or p == "have":
    nss, _ = getNNString(subj)
    nso, ncd = getNNString(obj)
    if not nss in kdb["things"]:
      apdstr = []
      kdb["things"][nss] = {"has": []}
      if ncd == "":
        kdb["things"][nss]["has"].append(nso)
      else:
        apdstr = [ncd, nso]
        kdb["things"][nss]["has"].append(apdstr)
    else:
      if not nso in kdb["things"][nss]["has"]:
        if ncd == "":
          kdb["things"][nss]["has"].append(nso)
        else:
          apdstr = [ncd, nso]
          kdb["things"][nss]["has"].append(apdstr)
      else:
        print("==> I already know that...\n")



def leavesToString(leaves):
  """Return the leaves as concatenated string with whitespace separation."""
  retstr = ""
  for e in leaves:
    retstr = retstr + e[0] + " "

  return retstr


def nltk_regex_parse(sentence):
  #   PP: {<IN><NP>}                    # Chunk prepositions followed by NP
  #   CLAUSE: {<NP><VP>}                # Chunk NP, VP
  #  VP: {<VB.*><NP|PP|CLAUSE|CD>+$}   # Chunk verbs and their arguments
  grammar = r"""
  NP: {<DT|JJ|CD|NN.*>+}            # Chunk sequences of DT, JJ, NN
  VERB: {<RB>*<VB.*><RP>*}
  RSS: {<NP><VERB><NP>}             # A really simple sentence with <subject> <predicate> <object>
  """
  cp = nltk.RegexpParser(grammar)

  parsed_sentence = cp.parse(sentence)
  print('parsed_sentence=', parsed_sentence)

  result = None
  for s in parsed_sentence.subtrees(lambda parsed_sentence: parsed_sentence.label() == "RSS"):
    result = s

  if not result == None:
    print("Result = ", result)

    obj = result.pop()
    pred = result.pop()
    subj = result.pop()


    subject = leavesToString(subj.leaves())
    predicate = leavesToString(pred.leaves())
    sobject = leavesToString(obj.leaves())


    print("subject =", subject)
    print("predicate =", predicate)
    print("object =", sobject)
    # add to knowledge database
    addToKDB(subj, pred, obj)
    print("------------------------------")
  else:
    print("No RSS sentence!\n")


def learnFromSentence(sentence):
  sent_tokens = word_tokenize(sentence)
  sent_pos_tags = nltk.pos_tag(sent_tokens)
  nltk_regex_parse(sent_pos_tags)


sentences = ["The dog or domestic dog (Canis familiaris) is a domesticated descendant of the grey wolf, characterized by an upturning tail.",
             "A car has four wheels.",
             "A car has a steering.",
             "Dogs are animals.",
             "A dog is an animal.",
             "A dog is a pet",
             "A horse is an animal.",
             "A dog strays down the street slowly.",
             "A car is a vehicle.",
             "Trucks are vehicles.",
             "Bicycles are vehicles.",
             "A Cessna is a plane."]

for s in sentences:
  learnFromSentence(s)

print("learned knowledge base:")
print(kdb)

#nltk.help.upenn_tagset()
