How_To_Develop_a_Chatbot_From_Scratch

1. Introduction of this project
-- The purpose of this project is to build a chatbot, named Eliza.

   Eliza plays the role of a psychotherapist, she can initialize a dialogue and encourage the user to talk with her.
   
   The whole project starts with Eliza's self introduction, and the question "what is your name?".
   
   And after that, the user can input his/her responses. Eliza will try to understand the input by keyword matching. 
   
   and give an appropriate answer to keep the converation going.
   

    for example: 
        
        [Eliza] Hi. I am a psychotherapist. What is your name?

        [User] Sree 

        [Eliza] Hi Sree. How can I help you today?

        [Sree] I feel bad

        [Eliza] Did you come to me because you feel bad?

        

2. Workflow of the project (including algorithms)
    -> initialize a dialogue by Eliza's self introduction and a question "What is your name?"
            ex: [Eliza] Hi. I am a psychotherapist. What is your name?
       
    -> User input: 
        -> if user did not enter anything in 20s, Eliza will ask the following question to encourage the user to talk with her. 
                    [Eliza] Hi, Could you please tell me more? I am here for you...?
                
        -> otherwise, if user can their names, supporting "Sree" or "[M|m]y name is Sree" 
                ex: [User] Sree   
      
    -> Eliza will extract name information from the input (if "name" is not in the input, then use the input as user's name. 
       Otherwise, select the last word as user's name), and start chatting with user by saying Hi user's name and asking "How can I help you today?"
            ex: [Eliza] Hi Sree, How can I help you today?
    
   
                                
    -> Eliza will give one of the following response based on the above input.
            -> if user did not enter anything in 20s, Eliza will ask the following question to keep the conversation going. 
                        [Eliza] Hi Sree. Could you please tell me more? I am here for you...    
    
            -> if user's input includes "(bye|quit|exit)" (case insensitive), 
               Eliza is able to find out these words by using regular expression and "re.findall()". 
               Eliza will say "Bye. Have a nice day!", and close the dialogue.
            
                    ex: [Sree] Bye.
                        [Eliza] Bye. Have a nice day!
            
            -> if user's input includes "kill|murder|suicide" (case insensitive).
               Eliza is able to find out these words by using regular expression and "re.findall()".
               Eliza will beep twice as a warning, and give an answer by using the following word spotting logic.
                
                    ex: [Sree] I will commit suicide        --> beep sound is heard twice (on windows system only)
                                
                                
            -> Eliza will perform word spotting by iterating the regular expressions, which are the keys of dictionary "response_dict".  
            
               Eliza will try to find a match between input and these regular expressions by using "re.search()". 
               Regular expression (.*) has been put at the end of the dictionary, which makes sure Eliza can find a match.
               
               Eliza will randomly choose a response from the value list corresponding to the key(regular expression). 
               (more detail can be found before the initialization of dictionary)
                  
                      -> if the response doesn't include "%s", Eliza will use the answer.
                              ex: [Sree] why?
                                  [Eliza] "Have you talked with your friends about that?"
                      
                      -> if the response includes "%s", 
                              -> if the response doesn't include the 2nd person pronoun(by searching the input among the keys of dictionary "pronoun_dict"). 
                                 Eliza will designate the first match to "%".
                                          ex: [Sree] I feel sad 
                                              [Eliza] Did you come to me because you are feeling sad? 
                              -> otherwise, the second pronoun will be transformed to the first pronoun.                              
                                          ex: [Sree] I hate you
                                              [Eliza] Why do you hate me?  
                                              

3. functionalities:

    -- conversation initialization
    -- users' name extraction
    -- keeping conversation with encouragement
    -- regular expression search
    -- pronoun transformation
    -- supporting exit the conversation
                                                                   
4. Additional functionalities

    -- 4.1 Suicide or murder detection(support Windows system): 
            -- if user's input includes "kill|murder|suicide" (case insensitive), Eliza will beep twice as a warning, 
            and give an answer by using the following word spotting logic.

    -- 4.2 Input timeout detection: if user didn't enter anything in 20s, Eliza would keep asking a question to keep the conversation going.


5. Techniques

    -- 5.1 NLP-related
            -- word spotting by using regular expressions and re syntax(re.findall and re.search).
            -- string operations, such as "re.sub", "join", "string.rstrip()"
            -- sentence tokenization
            -- case convert
    
    -- 5.2 Python
            -- input and print founctions
            -- dictionary and list
            -- while and for loop 
            -- if/else logic
            -- %s placeholder
            -- making beep sound
            -- random package 
