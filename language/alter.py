#Coded by Chris Parks
#November 27, 2020. due December 3, 2020
#For UNR CS 457

import sys;
import os;
import re;
import language.useful_functions;

def action(picked_keyword, unparsed_keywords):
    if(language.useful_functions.current_db == ''):
        return (1, '');
        
    (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
    
    #ALTER TABLE
    if(picked_keyword.upper() == 'TABLE'):
        (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
        filename = picked_keyword;
        
        #If no arguments are left 'ALTER TABLE table'
        if(unparsed_keywords == []):
            return (2, '');
        
        #Check if file exists
        if(picked_keyword in os.listdir(language.useful_functions.root_directory + "/" + language.useful_functions.current_db)):
            #Extract header
            with open(language.useful_functions.root_directory + '/' + language.useful_functions.current_db + '/' + filename, 'r') as table:
                header = table.readlines()[0];
                body = table.readlines()[1:];
                table.close();
                
            #Tokenize header
            header_token = header.split('|');
            (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
            
            #ALTER TABLE <tb_name> ADD
            if(picked_keyword.upper() == 'ADD'):
                #If there are not enough arguments 'ALTER TABLE table ADD', 'ALTER TABLE ADD (c5 int, c6)'
                if(len(unparsed_keywords) < 2 or len(unparsed_keywords) % 2 == 1):
                    return (2, '');
                    
                while(unparsed_keywords != []):
                    header_token.append(unparsed_keywords[0] + " " + unparsed_keywords[1]);
                    unparsed_keywords = unparsed_keywords[2:];
                    
            #ALTER TABLE <tb_name> DROP
            elif(picked_keyword.upper() == 'DROP'):
                if(unparsed_keywords == []):
                    return (2, '');
                
                #Removes remaining keywords from the header: Here's how it works
                #x.find(j) - Try to find a column name provided by the SQL statement within a table column
                #[j for j in y if x.find(j) != -1] - For every SQL statement argument, add to the set if it cannot be found within some header column. This returns a set of matching SQL statement arguments.
                # == [] - If that set is empty, return true (otherwise false). If true, this means that the SQL statement does not contain the header column.
                #i for i in header_token if - For every header column, add it to the set if the above condition is true. This returns the set of header_columns not named by the SQL statement arguments.
                header_token = [i for i in header_token if (lambda x, y: [j for j in y if x.find(j) != -1] == [])(i,unparsed_keywords)];
                unparsed_keywords = [];
                
            else:
                return (3, filename);
                
            #Detokenize header
            header = '|'.join(header_token);
            
            #Rewrite with new header
            with open(language.useful_functions.root_directory + '/' + language.useful_functions.current_db + '/' + filename, 'w') as table:
                table.write(header+'\n');
                for bodyline in body:
                    table.write(bodyline + '\n');
                table.close();
            return (0, 'Table ' + filename + ' modified.');

        else:
            return (5, 'alter ' + filename);