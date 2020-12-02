#Coded by Chris Parks
#November 27, 2020. due December 3, 2020
#For UNR CS 457

import sys;
import os;
import re;
import language.useful_functions;

def action(picked_keyword, unparsed_keywords):
    #Catch early end of statement
    if(unparsed_keywords == []):
        return (3, picked_keyword);
    
    (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
    
    if(picked_keyword == 'transaction'):
        #Catch arguments after end of statement
        if(unparsed_keywords != []):
            return (3, unparsed_keywords[0:1]);
            
        #Check if transaction is in progress
        if(language.useful_functions.transactioning):
            return (99, '!Transaction already in progress.');
        else:
            language.useful_functions.transactioning = True;
            language.useful_functions.transactions = [];
            language.useful_functions.table_locks = [];
        
        return (0, 'Transaction starts.');
    
    else:
        return (3, picked_keyword);
    