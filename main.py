#Coded by Chris Parks
#November 27, 2020. due December 3, 2020
#For UNR CS 457

import sys;
import os;
import re;

import language.useful_functions;

operation_sequence = [];


#First, read input and turn it into a list to iterate upon
create_set_mode = False;
token_input = [];
for std_input in sys.stdin:
    if(std_input[0:2] == '--' or std_input == '\n'): continue;
    if(std_input.strip().lower() == '.exit'): operation_sequence.append(['.exit']); break;
    
    #Tokenize the input line
    for i in re.split(' |,',std_input):
        i = i.lower();
        i = i.replace('\t','').replace('\n','').replace(';','').replace('\'','');
        if(i[0:2] == '--'):
            language.useful_functions.execute_operation([a for a in token_input if a != '']);
            token_input = [];
            break;
        if(i != '\n' and i != ''):
            if(not create_set_mode and i.find('(') != -1):
                j = i[i.index('(')+1:]
                i = i[:i.index('(')];
                create_set = [j];
                create_set_mode = True;
            elif(create_set_mode and i.find('(') != -1 and i.find(')') != -1):
                if(i.count(')') == 1):
                    create_set.append(i);
                else:
                    create_set.append(i[:i.index(')')+1]);
                    create_set_mode = False;
                    token_input.append(create_set);
                continue;
            elif(create_set_mode and i.find(')') == -1):
                create_set.append(i);
                continue;
            elif(create_set_mode and i.find(')') != -1):
                j = i[:i.index(')')];
                i = i[i.index(')')+1:]
                create_set.append(j);
                create_set_mode = False;
                token_input.append(create_set);
                
            token_input.append(i);
    if(std_input.replace('\n','')[-1:] == ';'):
        language.useful_functions.execute_operation([a for a in token_input if a != '']);
        token_input = [];

#Parse operation sequence and perform statements
#for this_operation in operation_sequence:
#    language.useful_functions.execute_operation(this_operation);
    
    