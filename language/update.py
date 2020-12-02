#Coded by Chris Parks
#November 27, 2020. due December 3, 2020
#For UNR CS 457

import sys;
import os;
import re;
import language.useful_functions;

def where_val_helper(s):
    try:
        float(s);
        return float(s);
    except ValueError:
        return s;

def action(picked_keyword, unparsed_keywords):
    #Catch using statement too early
    if(language.useful_functions.current_db == ''):
        return (1, '');
    
    if(unparsed_keywords == []):
        return (3, picked_keyword);
    
    (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
    filename = picked_keyword;
    
    #Check if table exists
    try:
        with open(language.useful_functions.root_directory + '/' + language.useful_functions.current_db + '/' + filename, 'r') as table:
            entire_table = table.readlines();
            table.close();
    except FileNotFoundError:
        return (5, 'update table ' + picked_keyword);
    
    #Must have 'SET field = value', optionally 'WHERE field = value'
    if(len(unparsed_keywords) != 4 and len(unparsed_keywords) != 8):
        return (2, '');
    
    fields = [];
    fields_string = '';
    body = [];
    body_string = '';
    
    #Get table schema
    fields = [a.split(' ') for a in entire_table[0].replace('\n','').split('|')];
    all_fields = [a[0] for a in fields];
    body = [a.replace('\n','').split('|') for a in entire_table[1:]];
    modified_body = body.copy();

    #Get set information
    picked_keyword = unparsed_keywords[1:4];
    unparsed_keywords = unparsed_keywords[4:];
    
    set_field_name = picked_keyword[0];
    if(picked_keyword[1] != '='):
        return (3, picked_keyword[0]);
    set_value = picked_keyword[2];
    
    #Do the where clause
    if(unparsed_keywords != []):
        picked_keyword = unparsed_keywords[1:4];
        unparsed_keywords = unparsed_keywords[4:];
        
        #Do the where clause
        where_field_name = picked_keyword[0];
        where_operator = picked_keyword[1];
        where_value = picked_keyword[2];
    
        if(where_operator == '='): where_operator = '==';
        
        #Filter out non-matching records
        for i, a in enumerate(modified_body):
            if(eval('where_val_helper(modified_body[i][all_fields.index(where_field_name)]) ' + where_operator + ' where_val_helper(where_value)')):
                continue;
            else:
                modified_body[i] = '';
    
    #Change values in the modified body and merge
    affected_records = 0;
    for i, a in enumerate(modified_body):
        if(modified_body[i] != ''):
            affected_records = affected_records + 1;
            modified_body[i][all_fields.index(set_field_name)] = set_value;
            body[i] = modified_body[i];

    body_string = '\n'.join(['|'.join(a) for a in body]);
    fields_string = '|'.join([' '.join(a) for a in fields]);
    
    #Edit table contents
    with open(language.useful_functions.root_directory + '/' + language.useful_functions.current_db + '/' + filename, 'w') as table:
        table.write(fields_string);
        table.write('\n');
        table.write(body_string);
        table.close();
    
    if(affected_records == 1):
        return (0, '1 record modified.');
    return (0, str(affected_records) + ' records modified.');