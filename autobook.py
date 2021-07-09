from nltk.corpus import wordnet as wn
from nltk.tokenize import TweetTokenizer
import nltk
import re
import random


def makeNewParagraph(paragraphList, wordTypeDict):
    newParagraphCode = paragraphList[random.randint(0,len(paragraphList))]
    newParagraph = ""
    newSentence = True
    startQuote = False
    quoteSpaceRemoved = False
    prevWord = ""
    failedWord = False
    nextWordNewSentence = False

    for word in newParagraphCode:

        if startQuote == True and quoteSpaceRemoved != True:
            newParagraph = newParagraph[:len(newParagraph)-1]
            quoteSpaceRemoved = True
            newSentence = True
        
        
        if word in [",",".","!","?",'"',"'"]:
            newWord = word
            newParagraph = newParagraph[:len(newParagraph)-1]
            if word in [".","!","?"]:
                nextWordNewSentence = True
            if newWord in ['"']:
                if startQuote == False:   
                    startQuote = True
                    newParagraph += " "
                    quoteSpaceRemoved = False
                else:
                    startQuote = False
            
        else:
            newWord = wordTypeDict[word][random.randint(0,len(wordTypeDict[word])-1)]
            if newWord in [",",".","!","?",'"',"'"]:
                newParagraph = newParagraph[:len(newParagraph)-1]
                if newWord in [".","!","?"]:
                    newSentence = True
                if newWord in ['"']:
                    if startQuote == False:   
                        startQuote = True
                        newParagraph += " "
                        quoteSpaceRemoved = False
                    else:
                        startQuote = False
        if newSentence == True:
            newWord = newWord.capitalize()
            newSentence = False
        if nextWordNewSentence == True:
            newSentence = True
            nextWordNewSentence = False
        newParagraph += newWord + " "
        prevWord = newWord.lower()
        

        
    if startQuote == True and prevWord != '"':
        newParagraph = newParagraph[:len(newParagraph)-1] + '"'

    print(newParagraph)
    
text = r"C:\Users\rolle\Dropbox\Completed Works\The Agora Files\the-agora-files-paperback1.txt"

book = open(text)
paragraphs = book.read().splitlines()

global nextWordDict
nextWordDict = {}
paragraphList = []
wordTypeDict = {}

#section for final tagger
from nltk.corpus import brown
fd = nltk.FreqDist(brown.words(categories='adventure'))
cfd = nltk.ConditionalFreqDist(brown.tagged_words(categories='adventure'))
most_freq_words = fd.most_common(10000)
likely_tags = dict((word, cfd[word].max()) for (word, _) in most_freq_words)
baseline_tagger = nltk.UnigramTagger(model=likely_tags)


for paragraph in paragraphs:

    #original recipe
    tknr = TweetTokenizer()
    #sentenceCodeDefault = nltk.pos_tag(tknr.tokenize(paragraph))
    
    #default tagger, works slightly better
    #tagger = nltk.DefaultTagger('NN')
    #sentenceCode = tagger.tag(nltk.word_tokenize(paragraph))

    #does a better job of recoginizing parts of speech
    patterns = [
     (r'.*ing$', 'VBG'),                # gerunds
     (r'.*ed$', 'VBD'),                 # simple past
     (r'.*es$', 'VBZ'),                 # 3rd singular present
     (r'.*ould$', 'MD'),                # modals
     (r'.*\'s$', 'NN$'),                # possessive nouns
     (r'.*s$', 'NNS'),                  # plural nouns
     (r'^-?[0-9]+(\.[0-9]+)?$', 'CD'),  # cardinal numbers
     (r'.*', 'NN')                      # nouns (default)
 ]
    regexp_tagger = nltk.RegexpTagger(patterns)
    sentenceCodeDefault = regexp_tagger.tag(tknr.tokenize(paragraph))

    
    sentenceCode = baseline_tagger.tag(tknr.tokenize(paragraph))
    

    thisSentence = []
    prevWord = ""
    i = 0
    for code in sentenceCode:
        thisCode = code[1]
        if code[1] is None:
            thisCode = sentenceCodeDefault[i][1]
        if code[0] not in ['na']:
            wordCode = thisCode
            thisWord = code[0].lower()
            if code[0] in ['“','”']:
                wordCode = '"'
                thisWord = '"'
            if code[0] in [',',".","!","?",'"',"'"]:
                wordCode = code[0]
                thisWord = code[0]    
            thisSentence.append(wordCode)
            if prevWord == "" or prevWord not in nextWordDict:
                nextWordDict[prevWord] = {thisWord : 1}
            else:
                if thisWord not in nextWordDict[prevWord]:
                    nextWordDict[prevWord][thisWord] = 1
                else:
                    nextWordDict[prevWord][thisWord] += 1
            if not wordCode in wordTypeDict:
                wordTypeDict[wordCode] = [thisWord]
            elif thisWord not in wordTypeDict[wordCode]:
                wordTypeDict[wordCode].append(thisWord)
            prevWord = thisWord
        i += 1

            
    paragraphList.append(thisSentence)


for x in range(1,50):
    makeNewParagraph(paragraphList, wordTypeDict)

