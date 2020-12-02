#Coded by Chris Parks
#November 27, 2020. due December 3, 2020
#For UNR CS 457

import sys;
import os;
import re;
import language.useful_functions;

def action(picked_keyword, unparsed_keywords):
    (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
    
    #DROP DATABASE
    if(picked_keyword.upper() == 'DATABASE'):
        (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
        
        if(unparsed_keywords != []):
            return (3, picked_keyword);
            
        try:
            if(picked_keyword in os.listdir(language.useful_functions.root_directory)):
                for files in os.listdir(language.useful_functions.root_directory + '/' + picked_keyword):
                    #No directories are expected in this subfolder, not checking for errors
                    os.remove(language.useful_functions.root_directory + '/' + picked_keyword + '/' + files);
            os.rmdir(language.useful_functions.root_directory + '/' + picked_keyword);
        except FileNotFoundError:
            return (5, 'delete database ' + picked_keyword);

        except OSError:
            return (99, '!Failed to delete database ' + picked_keyword + ' because it is not empty.');

        return (0, 'Database ' + picked_keyword + ' deleted.');
            
    #DROP TABLE
    elif(picked_keyword.upper() == 'TABLE'):
        #Catch using statement too early
        if(language.useful_functions.current_db == ''):
            return (1, '');
        
        (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
        
        if(unparsed_keywords != []):
            return (3, picked_keyword);
        
        #Remove file if it exists
        if(picked_keyword in os.listdir(language.useful_functions.root_directory + "/" + language.useful_functions.current_db)):
            os.remove(language.useful_functions.root_directory + "/" + language.useful_functions.current_db + "/" + picked_keyword);
            return (0, 'Table ' + picked_keyword + ' deleted.');

        else:
            return (5, 'delete ' + picked_keyword);