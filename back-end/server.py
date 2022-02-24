#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 11:10:15 2022

@author: navneethkrishna
"""
import ast
import csv
import sys
from flask import Flask, render_template, jsonify, request
#from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin
import random
import string
import datetime
import json
import os
import time

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/', methods=['POST', 'GET', 'OPTIONS'])
def helloWorld():
    return 'Hello! Welcome to the server of Wordle Optimizer!'

def declareVariables():
    global movie_frequency
    movie_frequency = []
    global movie_frequency_probability
    movie_frequency_probability = []
    global movie_frequency_total_count
    movie_frequency_total_count = 0
    global movie_word
    movie_word = ''
    global movie_word_frequency
    movie_word_frequency = 0
    global word_count
    word_count = 0
    print('word count')
    print(word_count)
    global lettersDict
    lettersDict = {}
    global processedWords
    processedWords = []
    global filename
    filename = 'movie_popularity.csv'
    global lettersPositionDict
    lettersPositionDict = {}
    global lettersPositionSum
    lettersPositionSum = [0,0,0,0,0]
    global wordlist_file
    wordlist_file = 'sgb-words.txt'
    global firstGuess, secondGuess, thirdGuess, fourthGuess, fifthGuess, sixthGuess
    firstGuess = ''
    secondGuess = ''
    thirdGuess = ''
    fourthGuess = ''
    fifthGuess = ''
    sixthGuess = ''
    global acceptableInputs, yellowSet, greenSet, blackSet, letter_index, lettersProbabilityDict, lettersProbabilityPerLetterDict
    acceptableInputs = 'YGB'
    yellowSet = [0,0,0,0,0]
    greenSet = [0,0,0,0,0]
    blackSet = [0,0,0,0,0]
    letter_index = 0
    global correct_set, incorrect_set, lettersFrequencyList
    correct_set = [1, 1, 1, 1, 1]
    incorrect_set = [[], [], [], [], []]



def init():
    declareVariables()
    readMovieFile()
    global lettersFrequencyList
    lettersFrequencyList = calculateLettersFrequencyList()
    global lettersProbabilityDict, lettersProbabilityPerLetterDict
    lettersProbabilityDict = getLettersProbability(lettersPositionDict, lettersPositionSum)
    lettersProbabilityPerLetterDict = getLettersProbabilityPerLetter(lettersPositionDict, lettersDict)
    weightedSum1(processedWords, lettersProbabilityPerLetterDict, lettersFrequencyList)
    weightedSum2(processedWords, lettersProbabilityDict, lettersFrequencyList)
    weightedSum3(processedWords, lettersFrequencyList)


'''
movie_frequency = []
movie_frequency_probability = []
movie_frequency_total_count = 0
movie_word = ''
movie_word_frequency = 0
word_count = 0
lettersDict = {}
processedWords = []
filename = 'movie_popularity.csv'

lettersPositionDict = {}
lettersPositionSum = [0,0,0,0,0]
'''
def processWord(value):
    global processedWords, lettersDict, lettersPositionDict, lettersPositionSum
    wordIndex = 0
    if(value not in processedWords):
        for i in value:
            if i in lettersDict:
                lettersDict[i] = lettersDict[i] + 1
                lettersPositionDict[i][wordIndex] = lettersPositionDict[i][wordIndex]+1
            else:
                lettersDict[i] = 1
                lettersPositionDict[i] = [0,0,0,0,0]
                lettersPositionDict[i][wordIndex] = lettersPositionDict[i][wordIndex]+1
            lettersPositionSum[wordIndex] = lettersPositionSum[wordIndex] + 1
            wordIndex = wordIndex + 1
        processedWords.append(value)

def readMovieFile():
    i = 0
    global word_count
    global movie_frequency_total_count
    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if(i==0):
                i = 1
                continue
            if(len(row[0])==5):
                movie_word = row[0]
                movie_word_frequency = int(row[1])
                word_type = row[12]
                #print(word_type)
                if('Noun' in word_type or 'Name' in word_type):
                    #print('Word '+word_type)
                    if('Adverb' not in word_type and 'Verb' not in word_type and 'Adjective' not in word_type):
                        continue
                processWord(movie_word)
                word_count = word_count+1
                movie_frequency_total_count = movie_frequency_total_count + movie_word_frequency
                movie_frequency.append([movie_word, movie_word_frequency])
    print(len(movie_frequency))

    for i in movie_frequency:
        val = i[1]
        prob = val/movie_frequency_total_count
        movie_frequency_probability.append([i[0], prob])

'''
with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        if(i==0):
            i = 1
            continue
        if(len(row[0])==5):
            movie_word = row[0]
            movie_word_frequency = int(row[1])
            word_type = row[12]
            #print(word_type)
            if('Noun' in word_type or 'Name' in word_type):
                #print('Word '+word_type)
                if('Adverb' not in word_type and 'Verb' not in word_type and 'Adjective' not in word_type):
                    continue
            processWord(movie_word)
            word_count = word_count+1
            movie_frequency_total_count = movie_frequency_total_count + movie_word_frequency
            movie_frequency.append([movie_word, movie_word_frequency])
print(len(movie_frequency))

for i in movie_frequency:
    val = i[1]
    prob = val/movie_frequency_total_count
    movie_frequency_probability.append([i[0], prob])
'''
#for i in range(0, 5):
    #print(movie_frequency_probability[i])


def takeSecond(elem):
    return elem[1]
'''
movie_frequency_probability.sort(key=takeSecond, reverse=True)
print("5-letter Movie words probability after sorting")
for i in range(0, 50):
    print(movie_frequency_probability[i])
'''




def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

'''
english_words = load_words()
print('English words length:')
print(len(english_words))
print(type(english_words))
x = english_words.pop()
print(x)
print(len(x))

for i in english_words:
    if(len(i) == 5):
        #print('LM')
        processWord(i)
        word_count = word_count+1
'''

'''
corpusfile = 'unigram_freq.csv'
corpus_frequency = []
corpus_frequency_probability = []
corpus_frequency_total_count = 0
corpus_word = ''
corpus_word_frequency = 0
i = 0
with open(corpusfile, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        if(i==0):
            i = 1
            continue
        if(len(row[0])==5):
            corpus_word = row[0]
            corpus_word_frequency = int(row[1])
            processWord(corpus_word)
            word_count = word_count+1
            corpus_frequency_total_count = corpus_frequency_total_count + corpus_word_frequency
            corpus_frequency.append([corpus_word, corpus_word_frequency])

print(len(corpus_frequency))

for i in corpus_frequency:
    val = i[1]
    prob = val/corpus_frequency_total_count
    corpus_frequency_probability.append([i[0], prob])

#for i in range(0, 5):
    #print(corpus_frequency_probability[i])

def takeSecond(elem):
    return elem[1]
corpus_frequency_probability.sort(key=takeSecond, reverse=True)
print("Corpus word probability after sorting")
for i in range(0, 50):
    print(corpus_frequency_probability[i])
'''


wordlist_file = 'sgb-words.txt'

def readWordList(wordlist_file):
    global word_count
    ccfile = open(wordlist_file, "r")
    for aline in ccfile:
        value = aline.split('\n')
        #print(value)
        processWord(value[0])
        word_count = word_count + 1
    ccfile.close()
    print("Total words that are processed:")
    print(word_count)
    print("Frequency of letters in all words:")
    print(lettersDict)
    print("Frequency of letters at each position:")
    print(lettersPositionDict)

'''
ccfile = open(wordlist_file, "r")
for aline in ccfile:
    value = aline.split('\n')
    #print(value)
    processWord(value[0])
    word_count = word_count + 1
ccfile.close()
print("Total words that are processed:")
print(word_count)
print("Frequency of letters in all words:")
print(lettersDict)
print("Frequency of letters at each position:")
print(lettersPositionDict)
'''
#readWordList(wordlist_file)


def sortDict(dict1):
    sorted_values = sorted(dict1.values())
    sorted_dict = {}
    for i in sorted_values:
        for k in dict1.keys():
            if(dict1[k] == i):
                sorted_dict[k] = dict1[k]
                break
    return sorted_dict
def getLettersFrequencyList(word_count, lettersDict):
    lettersFrequencyList = {}
    total_letters = word_count
    for i in lettersDict:
        lettersFrequencyList[i] = lettersDict[i]*100/total_letters
        #lettersFrequencyList.append([i, lettersDict[i]/total_letters])
    print("Letters sorted by frequency of appearance in words:")
    #lettersFrequencyList.sort(key=takeSecond, reverse=True)
    print(sortDict(lettersFrequencyList))
    #print(lettersFrequencyList)
    return lettersFrequencyList
def calculateLettersFrequencyList():
    print("Sums of each index")
    print(lettersPositionSum)
    lettersFrequencyList = {}
    total_letters = word_count*5
    for i in lettersDict:
        lettersFrequencyList[i] = lettersDict[i]*100/total_letters

    print("Letters sorted by frequency of appearance in words:")
    print(sortDict(lettersFrequencyList))
    return lettersFrequencyList
'''
print("Sums of each index")
print(lettersPositionSum)
lettersFrequencyList = {}
total_letters = word_count*5
for i in lettersDict:
    lettersFrequencyList[i] = lettersDict[i]/total_letters

print("Letters sorted by frequency of appearance in words:")
print(sortDict(lettersFrequencyList))
'''

def getLettersProbability(lettersPositionDict, lettersPositionSum):

    lettersProbabilityDict = {}
    for i in lettersPositionDict:
        lettersProbabilityDict[i] = [0,0,0,0,0]
        first = lettersPositionDict[i][0]
        second = lettersPositionDict[i][1]
        third = lettersPositionDict[i][2]
        fourth = lettersPositionDict[i][3]
        fifth = lettersPositionDict[i][4]
        lettersProbabilityDict[i] = [first*100/lettersPositionSum[0], second*100/lettersPositionSum[1], third*100/lettersPositionSum[2], fourth*100/lettersPositionSum[3], fifth*100/lettersPositionSum[4]]
    print("Probability of letters at indices (per all words): ")
    print(lettersProbabilityDict)
    return lettersProbabilityDict

def getLettersProbabilityPerLetter(lettersPositionDict, lettersDict):
    lettersProbabilityPerLetterDict = {}
    for i in lettersPositionDict:
        lettersProbabilityPerLetterDict[i] = [0, 0, 0, 0, 0]
        first = lettersPositionDict[i][0]
        second = lettersPositionDict[i][1]
        third = lettersPositionDict[i][2]
        fourth = lettersPositionDict[i][3]
        fifth = lettersPositionDict[i][4]
        if(lettersDict[i] == 0):
            continue
        lettersProbabilityPerLetterDict[i] = [first*100/lettersDict[i], second*100/lettersDict[i], third*100/lettersDict[i], fourth*100/lettersDict[i], fifth*100/lettersDict[i]]
    print("Probability of letters at indices (per specific letter): ")
    print(lettersProbabilityPerLetterDict)
    return lettersProbabilityPerLetterDict

'''
firstGuess = ''
secondGuess = ''
thirdGuess = ''
fourthGuess = ''
fifthGuess = ''
sixthGuess = ''
acceptableInputs = 'YGB'
yellowSet = [0,0,0,0,0]
greenSet = [0,0,0,0,0]
blackSet = [0,0,0,0,0]
letter_index = 0
lettersProbabilityDict = getLettersProbability(lettersPositionDict, lettersPositionSum)
lettersProbabilityPerLetterDict = getLettersProbabilityPerLetter(lettersPositionDict, lettersDict)
correct_set = [1, 1, 1, 1, 1]
incorrect_set = [[], [], [], [], []]
'''

def weightedSum1(processedWords, lettersProbabilityPerLetterDict, lettersFrequencyList):
    wordWeightage = []

    for i in processedWords:
        sub_list = []
        sub_list.append(i)
        weightedSum = 0
        word_index = 0
        letters_added = ''
        adjustedProb = lettersProbabilityPerLetterDict
        for j in i:
            if(j in letters_added):
                adjustedProb[j][word_index] = 0.5*adjustedProb[j][word_index]
            weightedSum = weightedSum + lettersFrequencyList[j]*adjustedProb[j][word_index]/10000
            word_index = word_index + 1
            letters_added = letters_added + str(j)
        sub_list.append(weightedSum)
        wordWeightage.append(sub_list)
    #print(wordWeightage)
    print('Sorting word weightage per index per specific letter:')
    wordWeightage.sort(key=takeSecond, reverse=True)
    x = len(wordWeightage)
    if(len(wordWeightage))>15:
        x = 15

    for i in range(0, x):
        print(wordWeightage[i])

def weightedSum2(processedWords, lettersProbabilityDict, lettersFrequencyList):
    wordWeightage = []

    for i in processedWords:
        sub_list = []
        sub_list.append(i)
        weightedSum = 0
        word_index = 0
        adjustingProb = lettersProbabilityDict
        letters_added = ''
        for j in i:
            if(j in letters_added):
                adjustingProb[j][word_index] = 0.5*adjustingProb[j][word_index]
            weightedSum = weightedSum + lettersFrequencyList[j]*adjustingProb[j][word_index]/10000
            word_index = word_index + 1
            letters_added = letters_added + str(j)
        sub_list.append(weightedSum)
        wordWeightage.append(sub_list)
    #print(wordWeightage)
    print('Sorting word weightage per index per probability:')
    wordWeightage.sort(key=takeSecond, reverse=True)
    x = len(wordWeightage)
    if(len(wordWeightage))>15:
        x = 15

    for i in range(0, x):
        print(wordWeightage[i])
    return wordWeightage

def weightedSum3(processedWords, lettersFrequencyList):
    wordWeightage = []

    for i in processedWords:
        sub_list = []
        sub_list.append(i)
        weightedSum = 0
        word_index = 0
        adjustedProb = lettersFrequencyList
        lettersAdded = ''
        for j in i:
            if(j in lettersAdded):
                adjustedProb[j] = adjustedProb[j]*0.5
            weightedSum = weightedSum + adjustedProb[j]/100
            word_index = word_index + 1
            lettersAdded = lettersAdded + str(j)
        sub_list.append(weightedSum)
        wordWeightage.append(sub_list)
    #print(wordWeightage)
    print('Sorting word weightage per probability:')
    wordWeightage.sort(key=takeSecond, reverse=True)
    x = len(wordWeightage)
    if(len(wordWeightage))>15:
        x = 15

    for i in range(0, x):
        print(wordWeightage[i])
    return wordWeightage
'''
weightedSum1(processedWords, lettersProbabilityPerLetterDict, lettersFrequencyList)
weightedSum2(processedWords, lettersProbabilityPerLetterDict, lettersFrequencyList)
weightedSum3(processedWords, lettersFrequencyList)
'''

def readInput(guessSet, count, correct_set, incorrect_set):
    acceptableInputs = 'YGB'
    yellowSet = [0,0,0,0,0]
    greenSet = [0,0,0,0,0]
    blackSet = [0,0,0,0,0]
    letter_index = 0
    print("Guess number: "+str(count+1))
    guess = guessSet[count]
    print(guess)
    if(not len(guess) == 5):
        print("Invalid input")
    else:
        for i in guess:
            letter = input("Is "+i+" Y, G, or B?")
            if(letter not in acceptableInputs):
                print("Invalid input.")
            else:
                if(letter == 'Y'):
                    yellowSet[letter_index] = 1
                    incorrect_set[letter_index].append(i)
                elif(letter == 'G'):
                    greenSet[letter_index] = 1
                    correct_set[letter_index] = i
                else:
                    blackSet[letter_index] = 1
            letter_index = letter_index + 1
    for i in range(0, len(blackSet)):
        if blackSet[i] == 1:
            letter = guess[i]
            if letter in correct_set or letter in incorrect_set:
                blackSet[i] = 0
    print(yellowSet)
    print(greenSet)
    print(blackSet)
    print(correct_set)
    print(incorrect_set)
    return [guess, yellowSet, greenSet, blackSet, correct_set, incorrect_set]


'''
firstGuess = input("Enter the first guess:")
if(not len(firstGuess) == 5):
    print("Invalid input")
else:
    for i in firstGuess:
        letter = input("Is "+i+" Y, G, or B?")
        if(letter not in acceptableInputs):
            print("Invalid input.")
        else:
            if(letter == 'Y'):
                yellowSet[letter_index] = 1
                incorrect_set[letter_index].append(i)
            elif(letter == 'G'):
                greenSet[letter_index] = 1
                correct_set[letter_index] = i
            else:
                blackSet[letter_index] = 1
        letter_index = letter_index + 1
print(yellowSet)
print(greenSet)
print(blackSet)
print(correct_set)
print(incorrect_set)
'''
def updateLettersCount(word, lettersDict, lettersPositionDict, lettersPositionSum):
    word_index = 0
    for i in word:
        lettersDict[i] = lettersDict[i] - 1
        lettersPositionDict[i][word_index] = lettersPositionDict[i][word_index] - 1
        lettersPositionSum[word_index] = lettersPositionSum[word_index] - 1
        word_index = word_index + 1

def filterYGB(processedWords, guess, yellowSet, greenSet, blackSet, lettersDict, lettersPositionDict, lettersPositionSum):
    newlyProcessedWords = []

    for i in processedWords:
        flag = 0
        wordIndex = 0
        for j in range(0, len(guess)):
            if(blackSet[j]):
                if(guess[j].lower() in i):
                    flag = 1
                    #print('Not including word '+i)
                    break
            elif(greenSet[j]):
                if(not guess[j].lower() == i[j]):
                    flag = 1
                    break
            else:
                if(not guess[j].lower() in i):
                    flag = 1
                    break
                if(guess[j].lower() == i[j]):
                    flag = 1
                    break

        if(flag):
                #print('Flag found for word '+i)
                updateLettersCount(i, lettersDict, lettersPositionDict, lettersPositionSum)
                continue
        newlyProcessedWords.append(i)
    print('Value of lettersDict')
    print(lettersDict)

    lettersFrequencyL = getLettersFrequencyList(sum(lettersDict.values()), lettersDict)
    print("Value of letters sorted by frequency")
    print(lettersFrequencyL)
    print('Value of letters position Dict')
    print(lettersPositionDict)
    print('Value of sums')
    print(lettersPositionSum)
    print(newlyProcessedWords)
    return [newlyProcessedWords, lettersDict, lettersPositionDict, lettersPositionSum, lettersFrequencyL]




def calculateWeightage(processedWords, lettersFrequencyList, lettersProbabilityDict, lettersProbabilityPerLetterDict):
    #weightedSum1(processedWords, lettersProbabilityPerLetterDict, lettersFrequencyList)
    #weightedSum2(processedWords, lettersProbabilityDict, lettersFrequencyList)
    return weightedSum3(processedWords, lettersFrequencyList)
    #print(wordWeightage)

def filterRoute(processedWords, lettersProbabilityPerLetterDict, lettersProbabilityDict, correctSet, incorrectSet, lettersFrequencyList):
    letterIndex = 0
    print('After word removal, here is the updated probability:')
    print(lettersProbabilityDict)
    print('Per letter:')
    print(lettersProbabilityPerLetterDict)
    wordWeightage = []
    wordWeightage = calculateWeightage(processedWords, lettersFrequencyList, lettersProbabilityDict, lettersProbabilityPerLetterDict)
    return wordWeightage

def needMoreLettersRoute(processedWords, lettersProbabilityDict, lettersFrequencyList):
    return weightedSum2(processedWords, lettersProbabilityDict, lettersFrequencyList)


def guessProcess(guess, processedWords, yellowSet, greenSet, blackSet, lettersProbabilityDict, lettersProbabilityPerLetterDict, lettersFrequencyList, lettersPositionDict, correctSet, incorrectSet, lettersDict, lettersPositionSum):
    retr = filterYGB(processedWords, guess, yellowSet, greenSet, blackSet, lettersDict, lettersPositionDict, lettersPositionSum)
    processedWords = retr[0]
    lettersDict = retr[1]
    lettersPositionDict = retr[2]
    lettersPositionSum = retr[3]
    lettersFrequencyList = retr[4]
    print(len(processedWords))
    if(len(processedWords) == 1):
        return "Word found! Congratulations!"
    lettersProbabilityDict = getLettersProbability(lettersPositionDict, lettersPositionSum)
    lettersProbabilityPerLetterDict = getLettersProbabilityPerLetter(lettersPositionDict, lettersDict)
    #print(firstProcessedWords)
    #filterRoute(processedWords, lettersProbabilityPerLetterDict, lettersProbabilityDict, correctSet, incorrectSet, lettersFrequencyList)
    if(len(processedWords)>1000):
        wordsOutput = needMoreLettersRoute(processedWords, lettersProbabilityDict, lettersFrequencyList)
    else:
        wordsOutput = filterRoute(processedWords, lettersProbabilityPerLetterDict, lettersProbabilityDict, correctSet, incorrectSet, lettersFrequencyList)
    return [processedWords, lettersProbabilityDict, lettersProbabilityPerLetterDict, lettersFrequencyList, lettersPositionDict, lettersDict, lettersPositionSum, wordsOutput]
'''
print("The words processed at first:")
print(len(processedWords))
print("The words processed after first removal:")
'''

'''
for count in range(6):
    inputVal = readInput(count+1, correct_set, incorrect_set)
    #yellowSet, greenSet, blackSet, correct_set, incorrect_set
    guess = inputVal[0]
    yellowSet = inputVal[1]
    greenSet = inputVal[2]
    blackSet = inputVal[3]
    correct_set = inputVal[4]
    incorrect_set = inputVal[5]
    return_val = guessProcess(guess, processedWords, yellowSet, greenSet, blackSet, lettersProbabilityDict, lettersProbabilityPerLetterDict, lettersFrequencyList, lettersPositionDict, correct_set, incorrect_set, lettersDict, lettersPositionSum)
    if(type(return_val) == str):
        print(return_val)
        break
        exit()
    processedWords = return_val[0]
    lettersProbabilityDict = return_val[1]
    lettersProbabilityPerLetterDict = return_val[2]
    lettersFrequencyList = return_val[3]
    lettersPositionDict = return_val[4]
    lettersDict = return_val[5]
    lettersPositionSum = return_val[6]
#return_val = guessProcess(firstGuess, processedWords, yellowSet, greenSet, blackSet, lettersProbabilityDict, lettersProbabilityPerLetterDict, lettersFrequencyList, lettersPositionDict, correct_set, incorrect_set, lettersDict, lettersPositionSum)
'''

def processGuess(guessSet, noOfTimes, yellow_set, green_set, black_set, correctSet, incorrectSet):
    global processedWords, lettersProbabilityDict, lettersDict, lettersPositionSum, lettersProbabilityPerLetterDict, lettersFrequencyList, lettersPositionDict
    for count in range(noOfTimes):
        #inputVal = readInput(guessSet, count, correct_set, incorrect_set)
        #yellowSet, greenSet, blackSet, correct_set, incorrect_set
        '''
        guess = inputVal[0]
        yellowSet = inputVal[1]
        greenSet = inputVal[2]
        blackSet = inputVal[3]
        correct_set = inputVal[4]
        incorrect_set = inputVal[5]
        '''
        guess = guessSet[count]
        yellowSet = yellow_set[count]
        greenSet = green_set[count]
        blackSet = black_set[count]
        correct_set = correctSet[count]
        incorrect_set = incorrectSet[count]

        return_val = guessProcess(guess, processedWords, yellowSet, greenSet, blackSet, lettersProbabilityDict, lettersProbabilityPerLetterDict, lettersFrequencyList, lettersPositionDict, correct_set, incorrect_set, lettersDict, lettersPositionSum)
        if(type(return_val) == str):
            print(return_val)

            break
            exit()
        processedWords = return_val[0]
        lettersProbabilityDict = return_val[1]
        lettersProbabilityPerLetterDict = return_val[2]
        lettersFrequencyList = return_val[3]
        lettersPositionDict = return_val[4]
        lettersDict = return_val[5]
        lettersPositionSum = return_val[6]
        words_output = return_val[7]
    return [words_output, lettersProbabilityDict, lettersFrequencyList]

def extractJSONFromString(val):
    json_data = "{ \"processedWords\": "+json.dumps(val[0])+", "
    json_data = json_data + "\"lettersProbability\": "+json.dumps(val[1])+", "
    json_data = json_data + "\"lettersFrequency\": "+json.dumps(val[2])+" }"
    print(json_data)
    return json_data



@app.route('/first-guess', methods = ['POST', 'OPTIONS'])
@cross_origin()
def guessHandling():
   request_data = request.get_json()
   print(request_data)
   first_guess = request_data['first-guess']
   yellow_set = request_data['yellow-set']
   green_set = request_data['green-set']
   black_set = request_data['black-set']
   correct_set = request_data['correct_set']
   incorrect_set = request_data['incorrect_set']
   guess_number = request_data['guess-number']
   print(first_guess[0])
   init()
   first_guess = ast.literal_eval(first_guess)
   yellow_set = ast.literal_eval(yellow_set)
   green_set = ast.literal_eval(green_set)
   black_set = ast.literal_eval(black_set)
   correct_set = ast.literal_eval(correct_set)
   incorrect_set = ast.literal_eval(incorrect_set)
   print(first_guess[0])
   print(first_guess[1])
   print(yellow_set[0])
   print(yellow_set[1])
   print(green_set[0])
   print(green_set[1])
   print(black_set[0])
   print(black_set[1])
   print(correct_set[0])
   print(correct_set[1])
   print(incorrect_set[0])
   print(incorrect_set[1])

   ans = processGuess(first_guess, int(guess_number), yellow_set, green_set, black_set, correct_set, incorrect_set)
   json_data = json.loads(extractJSONFromString(ans))
   #json_data = extractJSONFromString(ans)
   val = jsonify({
   "status": "success",
   "message": json_data
   })
   return val

if __name__ == '__main__':
    #correct_set = [1, 1, 1, 1, 1]
    app.run()
