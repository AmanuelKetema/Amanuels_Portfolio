import sys  # to get the system parameter
import os
import re   # used for regular expressions
import pickle

# Person class to describe a person object
# Contains function to display a person object
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("Employee id:", self.id)
        print("\t    ", self.first, self.mi, self.last)
        print("\t    ", self.phone)

# Function to read a file
# @returns a text which is of type string
def readFile(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text = f.read()
    return text

# Function to process a text
# returns a dictionary of person objects
def processText(text):
    dict = {}
    # get all sentences
    sentences = text.split('\n')
    # iterate through each sentence skipping the first
    for sentence in sentences[1:]:
        # get all the valus for the person objet
        tokens = sentence.split(',')
        # make the last name and teh first name capital case
        lastName = tokens[0][0].upper() + tokens[0][1:].lower()
        firstName = tokens[1][0].upper() + tokens[1][1:].lower()
        # set the middle initial to 'X' if not present else just upper case it
        mid = tokens[2].upper() if tokens[2] != '' else 'X'
        # get the person ID
        personId = tokens[3]
        # match the pattern of the person ID which is 2 letters followed by 4 numbers
        patternMatched = re.search("[a-zA-Z]{2}[0-9]{4}", personId)
        # check if the pattern was matched
        # prompt the user to input a different id if the pattern was not matched until the input is a valid input
        while not patternMatched:
            print("ID is invalid:", personId)
            print("ID is two letters followed by 4 digits")
            personId = input("Please input a valid id: ")
            patternMatched = re.search("[a-zA-Z]{2}[0-9]{4}", personId)
        # check if the number is of the format 123-456-7890
        # if not prompt the user to re-input the number until a valid input is provided
        number = tokens[4]
        numberPattern = re.search("([0-9]{3})-([0-9]{3})-([0-9]{4})", number)
        while not numberPattern:
            print(f"Phone {number} is invalid")
            print("Enter phone number in the form 123-456-7890")
            number = input("Enter phone number: ")
            numberPattern = re.search("([0-9]{3})-([0-9]{3})-([0-9]{4})", number)
        # create the person object
        person = Person(lastName, firstName, mid, personId, number)
        # check if the personID already exist in the dictionary
        if personId in dict:
            print(f"{personId} already exists!")
        else:
            dict[personId] = person
    return dict


if __name__ == '__main__':
    # Check if system arg has been set
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        # read the file
        fp = sys.argv[1]
        readText = readFile(fp)
        dict = processText(readText)
        # save the pickle file
        pickle.dump(dict, open('dict.p', 'wb'))  # write binary
        # read the pickle file
        dict_in = pickle.load(open('dict.p', 'rb'))  # read binary
        print("Employee list:\n")
        # display each person object in the dictionary
        for person in dict_in.values():
            person.display()
            print()