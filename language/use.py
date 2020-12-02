#Coded by Chris Parks
#November 27, 2020. due December 3, 2020
#For UNR CS 457

import sys;
import os;
import re;
import language.useful_functions;

#Select DB to use
def action(picked_keyword, unparsed_keywords):
    (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
    
    if(unparsed_keywords != []):
        return (2, picked_keyword);
    
    #Check if file exists, then set current_db
    if(picked_keyword in os.listdir(language.useful_functions.root_directory)):
        language.useful_functions.current_db = picked_keyword;
        return (0, 'Using database ' + picked_keyword + '.', language.useful_functions.current_db);

    else:
        return (5, 'select ' + picked_keyword);