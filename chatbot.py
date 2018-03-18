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