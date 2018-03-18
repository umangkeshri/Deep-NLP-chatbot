# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 03:16:36 2018

@author: UMANG KESHRI
"""

#Building a chatbot using Deep NLP

#libraries Imports

import numpy as np
import tensorflow as tf
import re
import time

################Data Preprocessing######

#Importing Dataset

lines = open('movie_lines.txt',encoding = 'utf-8',errors = 'ignore').read().split('\n')
conversations = open('movie_conversations.txt',encoding = 'utf-8',errors = 'ignore').read().split('\n')

#creatig a dictionary that maps each line with it's id
id2line = {}

for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line) == 5:
        id2line[_line[0]] = _line[4]
        
#creating a list of all the conversations
conversations_ids = []
for conversation in conversations[:-1]:
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
    conversations_ids.append(_conversation.split(','))    
    
#getting questions ad answers
    
questions = []
answers = []

for conversation in conversations_ids:
    for i in range(len(conversation) - 1):
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i+1]])
        
#cleaning of texts

def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"don't", "do not", text)
    text = re.sub(r"didn't", "did not", text)
    text = re.sub(r"doesn't", "does not", text)
    text = re.sub(r"let's", "let us", text)
    text = re.sub(r"[-()\"#@/;,:<>+=~.?|]", "", text)
    return text

#cleaning of questions
clean_questions = []
for question in questions:
    clean_questions.append(clean_text(question))


#cleaning f answers
clean_answers = []
for answer in answers:
    clean_answers.append(clean_text(answer))
    
#creating a dictionary that maps each word to it's number of occurences

word2count = {}

for question in clean_questions:
    for word in question.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1


for answer in clean_answers:
    for word in answer.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1
            
#creating two dictionaries that map the questions words and th answers words to aunique integer
threshold = 20
questionsword2int = {}
word_number = 0

for word,count in word2count.items():
    if count >= threshold:
        questionsword2int[word] = word_number
        word_number += 1

answersword2int = {}
word_number = 0
        
for word,count in word2count.items():
    if count >= threshold:
        answersword2int[word] = word_number
        word_number += 1    
        
#Adding the last tokens to these two dictionaries
tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']

for token in tokens:
    questionsword2int[token] = len(questionsword2int) + 1
    
for token in tokens:
    answersword2int[token] = len(questionsword2int) + 1   
    
#creating he inverse dictionary of the answersword2int dictionary
answersint2word = {w_i : w for w, w_i in answersword2int.items()}

#Ading EOS token to end of every answer
for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>'
    
    
#Translaing allthe questions and the answers into integers
#and replacing allhe wordsthat were filtered out by <OUT>

    
    
    