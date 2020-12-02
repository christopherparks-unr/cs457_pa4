#Coded by Chris Parks
#November 27, 2020. due December 3, 2020
#For UNR CS 457

import sys;
import os;
import re;
import language.useful_functions;

def action(picked_keyword, unparsed_keywords):
    if(unparsed_keywords[0:1][0].upper() != 'INTO'):
        return (3, picked_keyword);

    if(language.useful_functions.current_db == ''):
            return (1, '');
        
    picked_keyword = unparsed_keywords[1:2][0];
    unparsed_keywords = unparsed_keywords[2:];
    filename = picked_keyword;
    
    #If no arguments are left 'INSERT INTO table'
    if(unparsed_keywords == []):
        return (2, '');

    #Check if file exists
    if(picked_keyword in os.listdir(language.useful_functions.root_directory + "/" + language.useful_functions.current_db)):
        (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
        
        #INSERT INTO table VALUES
        if(picked_keyword.upper() == 'VALUES'):
            (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
            
            #INSERT INTO table VALUES ()
            #Extract header
            with open(language.useful_functions.root_directory + '/' + language.useful_functions.current_db + '/' + filename, 'r') as table:
                header = table.readlines()[0];
                table.close();
                #Split header info
                header = [i.split(' ') for i in header.split('|')];
                
                #Compare header
                if(len(picked_keyword) != len(header)):
                    return(2, '');
                else:
                    with open(language.useful_functions.root_directory + '/' + language.useful_functions.current_db + '/' + filename, 'a') as table:
                        table.write('\n');
                        while(picked_keyword != []):
                            table.write(picked_keyword[0]);
                            picked_keyword = picked_keyword[1:];
                            if(picked_keyword != []): table.write('|');
                        table.close();
                        return(0, '1 new record inserted.');

        else:
            return (3, filename);

    else:
        return (5, 'insert into table ' + filename);