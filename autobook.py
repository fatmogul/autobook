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
    print(newParagraphCode)
    for word in newParagraphCode:
        
        addWord = True
        if prevWord == "":
            newWord = wordTypeDict[word][random.randint(0,len(wordTypeDict[word])-1)]
        else:
            failedWord = False
            foundWord = False
            iterCount = 0
            while foundWord == False:
                trialWordList = list(nextWordDict[prevWord].keys())
                if iterCount >= len(trialWordList):
                    foundWord = True
                    newWord = trialWordList[0]
                    nextWordDict[prevWord][newWord] -= 1
                    if nextWordDict[prevWord][newWord] == 0:
                        nextWordDict[prevWord].pop(newWord,None)
                else:
                    trialWord = trialWordList[iterCount]
                    if trialWord in wordTypeDict[word]:
                        newWord = trialWord
                        nextWordDict[prevWord][trialWord] -= 1
                        if nextWordDict[prevWord][trialWord] == 0:
                            nextWordDict[prevWord].pop(trialWord,None)
                            foundWord = True
                iterCount += 1
        if startQuote == True and quoteSpaceRemoved == False:
            newParagraph = newParagraph[:len(newParagraph)-1]
            quoteSpaceRemoved = True
            newSentence = True
        if newSentence == True:
            newWord = newWord.capitalize()
            newSentence = False
        if word in [",",".","!","?",'"',"'"]:
            newWord = word
            newParagraph = newParagraph[:len(newParagraph)-1]
            if word in [".","!","?"]:
                newSentence = True
            if newWord == '"':
                if startQuote == False and newSentence != True:
                    startQuote = True
                    newParagraph += " "
                    quoteSpaceRemoved = False
                else:
                    startQuote = False
        newParagraph += newWord + " "
        prevWord = newWord.lower()
        

        
    if startQuote == True:
        newParagraph = newParagraph[:len(newParagraph)-1] + "”"
#        print(3)
    print(newParagraph)
    
text = r"C:\Users\rolle\Dropbox\Completed Works\The Agora Files\the-agora-files-paperback1.txt"

book = open(text)
paragraphs = book.read().splitlines()

global nextWordDict
nextWordDict = {}
paragraphList = []
wordTypeDict = {}
for paragraph in paragraphs:
    tknr = TweetTokenizer()
    sentenceCode = nltk.pos_tag(tknr.tokenize(paragraph))
    thisSentence = []
    prevWord = ""
    for code in sentenceCode:
        if code[0] not in ['na']:
            wordCode = code[1]
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
        

            
    paragraphList.append(thisSentence)

       
for x in range(1,10):
    makeNewParagraph(paragraphList, wordTypeDict)

