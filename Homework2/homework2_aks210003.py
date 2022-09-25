import sys  # to get the system parameter
import os
from random import *
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')


# Function to read a file
# @returns a text which is of type string
def readFile(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text = f.read()
    return text

# Function to display the word guessing game
# @param: nouns; which is a dictionary of {String: int}
# @returns: void

def guessingGame(nouns):
    guesses = 5
    print("Let's play a word guessing game!")

    while guesses is not 0:
        wordMatched = False
        randomNum = randint(0, 49)
        guessWord = nouns[randomNum]
        currentGuess = []
        first_display = True
        while not wordMatched and guesses is not 0:
            if first_display:
                for i in range(0, len(guessWord)):
                    currentGuess.append('_')
                first_display = False
            str = ""
            print(str.join(currentGuess))
            letter = input("Guess a letter: ")
            letterFound = False
            for i in range(0, len(guessWord)):
                if guessWord[i] is letter and currentGuess[i] == '_':
                    letterFound = True
                    currentGuess[i] = letter
            if not letterFound:
                guesses -= 1
                if guesses is 0:
                    print("Sorry, incorrect word! The word was ", guessWord)
                else:
                    print("Sorry, guess again. Score is ", guesses)
                letterFound = False
            else:
                guesses += 1
                print('Right! Score is ', guesses)
            matchTracker = True
            for i in range(0, len(guessWord)):
                if currentGuess[i] == '_':
                    matchTracker = False
                    break

            if matchTracker:
                print("You solved it!")
                wordMatched = True
                print("\n\nCurrent Score: ", guesses)
                print("\nGuess another word!")

# Preprocesses text
# @param rawText; String
# @returns a tuple of list of noun Strings and a list of token strings

def processText(text):
    # tokenize the raw text and make them unique
    tokens = nltk.word_tokenize(text)
    uniqueTokens = set(tokens)
    print("\nLexical diversity: %.2f" % (len(uniqueTokens)/len(tokens)))
    # of the unique token choose the ones that are greater than 5, alpha and not stopwords
    tokens = [t for t in tokens if t.isalpha() and
           t not in stopwords.words('english') and len(t) > 5]

    # lemmatize the tokens and use set to make them unique lemmas
    number_of_long_words = len(tokens)
    print("\nThe words greater than 5 characters and not stop words are: ", tokens)
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    lemmas_unique = list(set(lemmas))
    print("\nThe number of unique lemmas in text4: ", len(lemmas_unique))

    # process the unique lemmas to get the tags for the lemmmas
    tags = nltk.pos_tag(lemmas_unique)
    print(tags)
    first_twenty_tags = tags[:20]
    print("\nThe first twenty tagged items from the text are:")
    for single_tag in first_twenty_tags:
        print(single_tag)
    list_of_nouns = []
    for single_tag in tags:
        if(single_tag[1][0] is 'N'):
            list_of_nouns.append(single_tag)
    print("\nThe nouns from the text are: ", list_of_nouns)

    print("\nNumber of long words that were not stopwords were: ", number_of_long_words)
    print("\nNumber of nouns in the first twenty tags are: ", len(list_of_nouns))

    return tokens, list_of_nouns



if __name__ == '__main__':
    # Check if system arg has been set
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        # read the file
        fp = sys.argv[1]
        readText = readFile(fp)
        result = processText(readText)
        tokens = result[0]
        nouns = result[1]
        noun_set = set()
        for a_noun in nouns:
            noun_set.add(a_noun[0])
        noun_dict = {}
        for token in tokens:
            if token not in noun_dict and token in noun_set:
                noun_dict[token] = 1
            if token in noun_dict and token in noun_set:
                noun_dict[token] += 1
        print(len(noun_dict))
        sortedDictionary = sorted(noun_dict, key=noun_dict.get, reverse=True)
        sortedDictionary = sortedDictionary[:50]
        guessingGame(sortedDictionary)