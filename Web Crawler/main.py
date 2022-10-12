import urllib
from nltk.tokenize import word_tokenize, sent_tokenize
import requests
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords

stopwords = stopwords.words('english')


def readAndProcess():
    frequency_dict = {}
    allSentencesFromWebsites = []
    for i in range(1,16):
        with open(f"file{i}.txt", 'r') as f:
            text = f.read()
            sentences = sent_tokenize(text)
            pattern = "[\n|\r|\r\n]"
            cleanSentences = []
            for sentence in sentences:
                new_sentence = re.sub(pattern,'', sentence)
                new_sentence = re.sub(r'[``.\'%?–^!,\—:;()\-\n\d]',' ', new_sentence.lower())
                cleanSentences.append(new_sentence)
                print("The sentence is: ", new_sentence)
                allSentencesFromWebsites.append(new_sentence)
            f = open(f"fileoutput{i}.txt", "a")
            for sentence in cleanSentences:
                tokens = word_tokenize(sentence)
                updated_tokens = [t for t in tokens if t not in stopwords]

                for token in updated_tokens:
                    if token in frequency_dict:
                        frequency_dict[token] += 1
                    else:
                        frequency_dict[token] = 1
                f.write(sentence + "\n")
            f.close()
    sortedDictionary = sorted(frequency_dict, key=frequency_dict.get, reverse=True)
    print("The top 40 terms in the dictionary are: ")
    print(sortedDictionary[:40])

    # manually determine the most important 10 terms
    final_array = []
    final_array.append(sortedDictionary[0])
    final_array.append(sortedDictionary[5])
    final_array.append(sortedDictionary[7])
    final_array.append(sortedDictionary[8])
    final_array.append(sortedDictionary[9])
    final_array.append(sortedDictionary[11])
    final_array.append(sortedDictionary[13])
    final_array.append(sortedDictionary[15])
    final_array.append(sortedDictionary[39])
    final_array.append(sortedDictionary[24])
    print("Final 10 words are: ")
    print(final_array)

    knowledgeBase = {}
    for word in final_array:
        knowledgeBase[word] = []
    print(knowledgeBase)

    for sentence in allSentencesFromWebsites:
        tokens = word_tokenize(sentence)
        if word.lower() in knowledgeBase:
            if sentence not in knowledgeBase[word]:
                knowledgeBase[word].append(sentence)
    print(knowledgeBase)

def parseAndStore():
    count = 0
    with open('urls.txt', 'r') as f:
        urls = f.read().splitlines()
    for my_url in urls:
        # function to determine if an element is visible
        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element.encode('utf-8'))):
                return False
            return True

        html = urllib.request.urlopen(my_url)
        soup = BeautifulSoup(html)
        data = soup.findAll(text=True)
        result = filter(visible, data)
        temp_list = list(result)  # list from filter
        temp_str = ' '.join(temp_list)
        count += 1
        f = open(f"file{count}.txt", "a")
        f.write(temp_str)
        f.close()


starter_url = "https://www.google.com/search?q=muhammad+ali&rlz=1C5CHFA_enUS968US968&oq=muhamm&aqs=chrome.0.0i67i131i355i433j46i67i131i433j69i57j46i67i131i433j0i433i512j46i67i131i433j0i131i433i512l2j46i433i512l2.1640j0j7&sourceid=chrome&ie=UTF-8"
queue = []
counter = 0
# write urls to a file
with open('urls.txt', 'w') as f:
    while True:
        r = requests.get(starter_url)
        data = r.text
        soup = BeautifulSoup(data)
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))
            if 'muhammad' in link_str or 'Muhammad' in link_str:
                if link_str.startswith('/url?q='):
                    link_str = link_str[7:]
                if '&' in link_str:
                    i = link_str.find('&')
                    link_str = link_str[:i]
                if link_str.startswith('http') and 'google' not in link_str and 'facebook' not in link_str and 'twitter' not in link_str and 'instagram' not in link_str and "britannica" not in link_str and "ny" not in link_str and "pinterest" not in link_str:
                    queue.append(link_str)
                    counter += 1
                    f.write(link_str + '\n')
                if counter == 15:
                    break
        if counter == 15:
            break
        starter_url = queue.pop()


parseAndStore()
readAndProcess()
