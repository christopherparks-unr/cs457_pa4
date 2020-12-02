#Coded by Chris Parks
#November 27, 2020. due December 3, 2020
#For UNR CS 457

import sys;
import os;
import re;
import language.useful_functions;

def action(picked_keyword, unparsed_keywords):
    (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
    
    #CREATE DATABASE
    if(picked_keyword.upper() == 'DATABASE'):
        (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
        try:
            os.mkdir(language.useful_functions.root_directory + '/' + picked_keyword);
        except OSError:
            return (4, 'database ' + picked_keyword);

        if(unparsed_keywords != []):
            return (3, picked_keyword);

        return (0, 'Database ' + picked_keyword + ' created.');
            
    #CREATE TABLE
    elif(picked_keyword.upper() == 'TABLE'):
        #Catch using statement too early
        if(language.useful_functions.current_db == ''):
            return (1, '');

        (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
        
        #Create file if it does not exist
        try:
            with open(language.useful_functions.root_directory + '/' + language.useful_functions.current_db + '/' + picked_keyword, 'x') as table:
                table.close();
        except FileExistsError:
            return (4, 'table ' + picked_keyword);

        except FileNotFoundError:
            return (99, '!Failed to create table ' + picked_keyword + ' because the selected database does not exist.');
            
        #If no syntax errors are thrown, move on to editing contents of the file
        if(unparsed_keywords == [] or len(unparsed_keywords[0]) % 2 == 1):
            return (2, '');
            
        #Write table parameters into first line of file
        with open(language.useful_functions.root_directory + '/' + language.useful_functions.current_db + '/' + picked_keyword, 'w') as table:
            while(unparsed_keywords[0] != []):
                table.write(unparsed_keywords[0][0] + ' ' + unparsed_keywords[0][1]);
                unparsed_keywords[0] = unparsed_keywords[0][2:];
                if(unparsed_keywords[0] != []): table.write('|');
            table.close();
            return (0, 'Table ' + picked_keyword + ' created.');