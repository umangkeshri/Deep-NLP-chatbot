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

questions_to_int = []
for question in clean_questions:
    integers = []
    for word in question.split():
        if word not in questionsword2int:
            integers.append(questionsword2int['<OUT>'])
        else:
            integers.append(questionsword2int[word])
        questions_to_int.append(integers)
    
answers_to_int = []
for answer in clean_answers:
    integers = []
    for word in answer.split():
        if word not in answersword2int:
            integers.append(answersword2int['<OUT>'])
        else:
            integers.append(answersword2int[word])
        answers_to_int.append(integers)
        
#sorting questions and answers by the length of qustions
        
sorted_clean_questions = []
sorted_clean_answers = []

for length in range(1, 25 + 1):
    for i in enumerate(questions_to_int):
        if len(i[1]) == length:
            sorted_clean_questions.append(questions_to_int[i[0]])
            sorted_clean_answers.append(answers_to_int[i[0]])


##---------Building seq2seq model-----------#
            
#creating placeholders for the inputs and the targets

def model_inputs():
    inputs = tf.placeholder(tf.int32, [None, None], name ='input')
    targets= tf.placeholder(tf.int32, [None, None], name ='target')
    lr = tf.placeholder(tf.float32, name = 'learning rate')
    keep_prob = tf.placeholder(tf.float32, name = 'keep_prob')
    return inputs,targets,lr,keep_prob

#pprocessing the targets
     
def preprocess_targets(targets, word2int, batch_size):
    left_side = tf.fill([batch_size, 1], word2int['<SOS>'])
    right_side = tf.strided_slice(targets, [0,0], [batch_size,-1], [1,1])
    preprocessed_targets = tf.concat([left_side,right_side],1)
    return preprocessed_targets

#Creating the encoder RNN layer    

    
    
    
    
    
    
    
    