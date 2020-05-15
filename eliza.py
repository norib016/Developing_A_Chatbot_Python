# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 10:36:50 2019

@author: Sree Nori

@date: 9/17/2019
"""

import nltk
#nltk.download("punkt")
from nltk.tokenize import word_tokenize
import re
import random
import time
from threading import Timer


"""
Key is regular expression which is used to do word spotting. Value is the possible answers. 
If a match has been found by using the regular expression. Eliza will randomly choose an answer from the dictionary values.
Some answer include place holder, which will be replaced by the first match.

For example:
    [Sree] I am studying
    [Eliza] How long have you been studying    
    
The regular expressions fall into the following categories:  
    - kill|murder|suicide check
    - feelings
    - status
    - willingness
    - frustration/stability
    - changes
    - family/friends
    - yes/no
    - others
    
"""
response_dict = {  
        
        r'.*(kill|murder|suicide).*':
        [
                "What's going on? Tell me more.",
                "I am so glad you told me. Tell me more.",
                "Tell me about your friends.",
                "Tell me about your family.",
                "Have you talked with your friends about that?",
                "Have you talked with your parents about that?",
                "People achive the most by living.",
                "It is better to divert your mind from thoughts like that.",
                "I hope you will keep talking to me."
         ],  
        
     r'i feel (.*)':
        [
                "Did you come to me because you feel %s?",
                "How do you feel about being %s?",
                "What things made you feel that way?",
                "What situations made you feel that way?"
         ],   
         
     r'i am (.*)':
        [
                "How long have you been %s?",
                "Why do you think you're %s?"
         ], 
                
    r'i hate (.*)':
        [
                "Why you hate %s?",
                "Do you enjoy being hate %s?",
                "Have you talked with your friends about that?",
                "Have you talked with your parents about that?"
         ], 
    
    r'i love (.*)':
        [
            "What makes you love %s?",
            "Tell me more about your %s",
            "Does it make you happy to love %s?"
        ],
                
     r'i need (.*)':
         [
                 "Could you tell me why do you need %s?",
                 "Would it really help you if you get %s?",
                 "Are you sure you need %s?"
         ],
                 
    r'i want (.*)':
        [
                "How much does it mean to you if you got %s?",
                "Are you sure, why do you want %s?"
        ],
    
    r'i will (.*)':
        [
                "Why will you %s?",
                "When will you %s?",
                "Could please tell more details about how will you %s?"
        ],
    
    r'i can\'?n?o?t (.*)':
       [
              "What would it take for you to %s?",
              "How do you know you cannot %s?",
              "Perhaps you could %s if you tried."
       ],
      
     r'why can\'?n?o?t i (.*)\??':
     [  
              "Did you try it?",
              "Maybe you could if you give it a try.",
              "Have you asked for help from your friends?",
              "Have you asked for help from your family?"
     ],
         
    r"why don't you (.*)?":
        [
             "Is this really what you want me to do?",
             "I will %s if that is what you want."
        ],  
    
    r'(.*)(hurt|hurtful|pain|painful)(.*)':
        [
            "I'm sorry you are suffering.",
            "I'm sorry you are struggling",
            "Talk more about it please.",
            "May be you should consult a doctor."
        ],  

               
    r'(.*)(because|since|due to)(.*)':
        [  
               "What other reasons come to mind?",
               "Is that the really why?",
               "Does that reason apply to anything else?"
         ],
                
                  
    r'(.*)changes?(.*)':
        [
                "What positive changes would you make happen in your life?",
                "Would it make you feel better if you had a change in your life?"
        ],
                
    r'(.*)friends?(.*)':
        [               
                "Your friend seems interesting. Tell me more.",
                "Tell me more about your friend please.",
                "Perhaps your friends worry about you."
        ],
                  
    r'(.*)family(.*)':
        [
                "How does your family feel about your situation?",
                "Is your family ready to help you?",
                "Have you talked to your family recently?",
                "Perhaps your family worries about you."
        ],
    
    r'(.*)ready(.*)':
        [
                "Good to know! Tell me more."
        ],
   
    r'i (read|reading)(.*)':
        [       
                "Do you like %s?",
                "Could you please talk %s with me?",
                "Sure, reading books might help.",
                "Does reading help?"
        ],                
                
    r'(.*)talk(.*)':
        [ 
                "Can you elaborate that?",
                "I am always here for you. Tell me more.",
                "I am programmed to talk to you. Tell me what is on your mind?"
         ],               
                    
    r'(.*)yes(.*)':
        [
             "You seem quite positive",
             "I understand. Tell me more.",
             "Are you sure?",
             "That is good to know, how is that going?"
        ], 
                
    r'(.*)no(.*)':
        [
              "Are you sure?",
              "Have you thought about it in a different way?"
        ],
    
    r'(.*)sleepy?(.*)':
          [
                  "Have a nice sleep",                     
                  "Goodnight"
          ],
               
     r'(.*)\?':
         [
                 "Have you talked with your friends about that?",
                 "Have you talked with your parents about that?",
                 "Why do you ask that?"
        ],
                 
    r'(.*)':
         [
                  "Let's change the subject. Tell me a funny thing you recently experienced.",
                  "Please tell me how can I help you?",        
                  "I see, please tell me more.",
                  "Very interesting, please tell me more."
        ]
    }
    
   
# it will be used to tranformed from 2nd person to 1st person
pronoun_dict = {
    "you": "me",
    "your": "my",
    "yours": "mine",
    "you've": "I have",
    "you'll": "I will",      
        }    
         
def make_a_beep():
    for i in range(1, 3):
        print('\a')
        time.sleep(1)
        
#    sys.stdout.close()
#    for i in range(1,3):
#        sys.stdout.write('\a')
#        sys.stdout.flush()
#        time.sleep(1)
#    sys.stdout.close()


# check whether input includes "kill" or "murder" or "suicide". if yes, make 2 beeps        
def suicide_detect(user_input):
    suicide_reg =  r'.*(kill|murder|suicide).*'       
    ans = re.findall(suicide_reg, user_input) 
    
    if ans:
        make_a_beep()

def transform_pronoun(match_word):    
    tokenizer = word_tokenize(match_word)    # tokenize the match words
    #print(match_word, tokenizer)
    
    for index, token in enumerate(tokenizer):           # iterate list of tokenizer
        if token in pronoun_dict:                       # if the element is one of the keys of dictionary "pronoun_dict", such as "you"
            tokenizer[index] = pronoun_dict[token]      # use the key's value to replace the element in tokenizer, such as "me"
    return ' '.join(tokenizer)                          # join the tokens in tokenizer, and return tokenizer
   
# Analyze input and return answer
def analyze_input(user_input):   
    # initialize answer, if no match in the above dictionary    
    
    # iterate over the "response_dict"
    for pattern, responses in response_dict.items():   
        
        # check whether input matches the key(pattern/regular expression)
        ans = re.search(pattern, user_input.rstrip(",.!"))   
        
        if ans:    # if find a match                                                
            response = random.choice(responses)      # choose a random response  
            # print("response", response)
            # if the question include "%s", means it needed to be replaced with the information from the input
            if "%s" in response:                     
                match_word = ans[1]                  
                
                # if the match word include 2nd person, such as "you", it will be transformed to 1st person, such as "me".
                trans_response = transform_pronoun(match_word)  
                response = response %(trans_response)    # use the first match to replace "%s" in eliza's response                          
                return response
            else: 
                return response

# check the input about name, if user didn't enter anything in 10s, Eliza will ask "Hi. Are you still there?"
def input_name():
        timeout = 20
        t = Timer(timeout, print, ['\n[Eliza] Hi. Are you still there? Could you please tell me your name?\n[User] ' ] )
        t.start()
        name = input('[User] ') 
        t.cancel()
        return name

# check the input during the conversation, if user didn't enter anything in 10s, 
# Eliza will ask "Hi. Could you please tell me more? I am here for you..."
def input_answer(user_name):
        timeout = 20
        t = Timer(timeout, print, ['\n[Eliza] Hi %s. Could you please tell me more? I am here for you...\n[%s] ' %(user_name, user_name)] )
        t.start()
        name = input('[%s] ' %user_name)  # check input and get input information
        t.cancel()
        return name        
    
def dialogue_body(user_name):
    print("[Eliza] Hi %s. How can I help you today?" %user_name, end = '\n')
        
    quits = [r'.*bye.*', r'.*quit.*', r'.*exit.*']                           # regular expression for 'bye'  
    
    while True:
        user_input = input_answer(user_name)    # check input name and get input information
        print()
        user_input = user_input.lower()         # convert input to lower case
        
        find_quits = 0
        
        for i in quits:
            matches = re.findall(i, user_input)     # re syntax checks whether there's "bye" in input
            find_quits += len(matches)            
             
        if find_quits == 0:                         # if there's no 'bye' in input
            suicide_detect(user_input)              # check whether input includes "kill" or "murder" or "suicide". if yes, make 2 beeps
            response = analyze_input(user_input)    # analyze input, and return an appropriate response
            print("[Eliza] " + response, end = '\n')            
        else: 
            print("[Eliza] Bye. Have a nice day!")   # if there's 'bye' in input, print this information, and exit while loop
            break
       
        
# Initializa dialogue and return user's name
def initialize_chat():       
    print("[Eliza] Hi. I am a psychotherapist. What is your name?", end = '\n')

    user_name = "User"                               # Initialize user's name       
    name_input = input_name()
    print()
    
    name_input = re.sub(r'[^\w]', ' ', name_input)    # replace NON[alphanumeric characters(\w)] with space

    tokenizer = word_tokenize(name_input)            # Tokenizing user's name
    #tokenizer = [word for word in tokenizer if word.isalpha()]
    
    if "name" not in name_input:            # if "name" does not appear in input
        user_name = name_input              # use input as the user's name
    else:
        user_name = tokenizer[-1]           # if "name" does appear in input, use the last word as user's name

    #print(user_name) 
    return user_name
    
        
# main function
def main():
   user_name = initialize_chat()        # initialize chat
   dialogue_body(user_name)             # main conversation part
    
if __name__ == "__main__":
    main()
    
