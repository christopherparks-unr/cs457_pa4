#Coded by Chris Parks
#November 27, 2020. due December 3, 2020
#For UNR CS 457

import sys;
import os;
import re;
import language.useful_functions;

def remove_locks():
    for i in language.useful_functions.table_locks:
        #Remove file if it exists
        if(i + '_lock' in os.listdir(language.useful_functions.root_directory + '/' + language.useful_functions.current_db)):
            os.remove(language.useful_functions.root_directory + '/' + language.useful_functions.current_db + '/' + i + '_lock');
    
    language.useful_functions.table_locks = [];

def action(picked_keyword, unparsed_keywords):
    #Catch arguments after end of statement
    if(unparsed_keywords != []):
        return (3, unparsed_keywords[0:1]);
    
    if(not language.useful_functions.transactioning):
        return (99, '!No transaction in progress.')
    
    language.useful_functions.transactioning = False;
    #Perform operations, checking for locks along the way
    for this_operation in language.useful_functions.transactions:
        check_locks = [a for a in language.useful_functions.analyze(this_operation) if a not in language.useful_functions.table_locks];
        if(check_locks == []):
            language.useful_functions.execute_operation(this_operation);
        else:
            remove_locks();
            return (99, 'Transaction abort.');
            
    
    remove_locks();
    
    return (0, 'Transaction committed.');