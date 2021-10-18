from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from word2number import w2n

# knowledge database
kdb = {"things": {}}

lemmatizer = WordNetLemmatizer()

aggregates_words = ("has", "have", "consists of", "consist of", "made of", "owns", "own", "characterized by")

generalizes_words = ("is", "are")

def isAggregatesVerb(verb_phrase):
  """heuristic to check whether the phrase has the semantics of aggregation."""
  verb = leavesToString(verb_phrase).strip()
  if ("is " in verb) and (verb_phrase.__len__() > 1):
    verb = verb.replace("is", "").strip()

  if verb in aggregates_words:
    return True
  else:
    return False

def isGeneralizesVerb(verb_phrase):
  """heuristic to check whether the phrase has the semantics of generalization."""
  if (verb_phrase.__len__() == 1) and (getVBZString(verb_phrase) in generalizes_words):
    return True
  else:
    return False

def getVBZString(verb_term):
  """Return the verb word."""
  res = ""
  for e in verb_term.leaves():
    if e[1] == "VBZ" or e[1] == "VBP":
      res = e[0]

  return res

def getNNString(nn_term):
  """Return the noun word, evtl. with count word."""
  res = []
  ret_res = ""
  res_cd = ""
  for e in nn_term.leaves():
    if e[1] == "NN":
      res.append(e[0].lower())
    elif e[1] == "NNS":
      # I will store words only in their singular form
      res.append(lemmatizer.lemmatize(e[0].lower()))
    elif e[1] == "NNP":
      res.append(e[0])
    elif e[1] == "CD":
      num = 0
      if e[0].isdecimal():
        res_cd = int(e[0])
      else:
        res_cd = w2n.word_to_num(e[0])


  for n in res:
    ret_res = ret_res + n + " "

  return ret_res.strip(), res_cd


def addToKDB(subj, pred, obj):
  """Add information to knowledge database."""

  global kdb

  if isGeneralizesVerb(pred):
    nso, _ = getNNString(obj)
    nss, _ = getNNString(subj)
    if not nso in kdb["things"]:
      obj_dict = {nso: {"generalizes": [nss]}}
      kdb["things"][nso] = {"generalizes": [nss]}
      print("==> added that to my knowledge base: ", obj_dict)
    else:
      if not "generalizes" in kdb["things"][nso]:
        kdb["things"][nso]["generalizes"]=[nss]
      else:
        if not nss in kdb["things"][nso]["generalizes"]:
          obj_dict = {nso: {"generalizes": [nss]}}
          kdb["things"][nso]["generalizes"].append(nss)
          print("==> added that to my knowledge base: ", obj_dict)
          #print()
        else:
          print("==> I already know that...\n")

    if not nss in kdb["things"]:
      kdb["things"][nss] = {"specializes": [nso]}
    else:
      if not "specializes" in kdb["things"][nss]:
        kdb["things"][nss]["specializes"] = [nso]
      else:
        if not nso in kdb["things"][nss]["specializes"]:
          kdb["things"][nss]["specializes"].append(nso)
        else:
          print("==> I already know that...\n")

  elif isAggregatesVerb(pred):
    nss, _ = getNNString(subj)
    nso, ncd = getNNString(obj)
    if not nss in kdb["things"]:
      apdstr = []
      kdb["things"][nss] = {"aggregates": []}
      if ncd == "":
        kdb["things"][nss]["aggregates"].append(nso)
      else:
        apdstr = [ncd, nso]
        kdb["things"][nss]["aggregates"].append(apdstr)
    else:
      if not "aggregates" in kdb["things"][nss]:
        if ncd == "":
          kdb["things"][nss]["aggregates"] = [nso]
        else:
          apdstr = [ncd, nso]
          kdb["things"][nss]["aggregates"] = [apdstr]
      else:
        if not nso in kdb["things"][nss]["aggregates"]:
          if ncd == "":
            kdb["things"][nss]["aggregates"].append(nso)
          else:
            apdstr = [ncd, nso]
            kdb["things"][nss]["aggregates"].append(apdstr)
        else:
          print("==> I already know that...\n")

    if not nso in kdb["things"]:
      kdb["things"][nso] = {"is part of": [nss]}
    else:
      if not "is part of" in kdb["things"][nso]:
        kdb["things"][nso]["is part of"] = [nss]
      else:
        if not nss in kdb["things"][nso]["is part of"]:
          kdb["things"][nso]["is part of"].append(nss)
        else:
          print("==> I already know that...\n")

def leavesToString(leaves):
  """Return the leaves as concatenated string with whitespace separation."""
  retstr = ""
  for e in leaves:
    retstr = retstr + e[0] + " "

  return retstr


def nltk_regex_parse(sentence):
  """parse a given sentence with a simple RSS regex parser. Result will be added
     to the global knowledge base 'kdb', which is a python dictionary."""
  #   PP: {<IN><NP>}                    # Chunk prepositions followed by NP
  #   CLAUSE: {<NP><VP>}                # Chunk NP, VP
  #  VP: {<VB.*><NP|PP|CLAUSE|CD>+$}   # Chunk verbs and their arguments
  grammar = r"""
  NP: {<DT|JJ|CD|NN.*>+}            # Noun Phrase, chunk sequences of DT, JJ, NN
  VERB: {<RB>*<VB.*>*<RP>*<IN>*}          # verb with possible prepositions
  RSS: {<NP><VERB><NP>}             # A really simple sentence (RSS) with <subject> <predicate> <object>
  """
  cp = nltk.RegexpParser(grammar)

  parsed_sentence = cp.parse(sentence)
  print('parsed_sentence=', parsed_sentence)

  result = None

  # find a "real simple sentence" (RSS rule in grammar)
  for s in parsed_sentence.subtrees(lambda parsed_sentence: parsed_sentence.label() == "RSS"):
    result = s

  # make sure that it is a RSS
  if not result == None:
    print("Result = ", result)

    # popping the tree element gets the items
    # in reverse order
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
  """process a given sentence with a learning processing chain."""
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
             "A Cessna is a plane.",
             "A duo consists of two persons",
             "A trio consists of three persons.",
             "A bread is made of wheat flour.",
             "A bread is made of salt.",
             "Humans consist of water.",
             "Humans have blood.",
             "A human has a head.",
             "A human has 2 legs.",
             "Humans have two arms.",
             "A human head has two eyes.",
             "Human heads have two ears.",
             "The car has a manual transmission.",
             "The dog is characterized by an upturning tail.",
             "Arms are extremities.",
             "Legs are extremities.",
             "Persons are humans.",
             "A human is a lifeform.",
             "A man is a person.",
             "A woman is a person."]

for s in sentences:
  learnFromSentence(s)

print("learned knowledge base:")
print(kdb)

#nltk.help.upenn_tagset()

