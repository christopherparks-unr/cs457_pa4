#Coded by Chris Parks
#November 27, 2020. due December 3, 2020
#For UNR CS 457

import sys;
import os;
import re;
import language.useful_functions;


tr_st_1 = ['from']
tr_st_2 = ['left', 'right', 'cross', 'full', 'inner', 'outer', 'join'];
tr_st_3 = ['on'];
tr_st_4 = ['where'];

#Converts strings into floats during the WHERE clause to properly implement comparison operators
def where_val_helper(s):
    try:
        float(s);
        return float(s);
    except ValueError:
        return s;

#Uses the tr_st_# lists to break the statement into several stages
def get_form(picked_keyword, unparsed_keywords):

    
    statement = [[],[],[],[],[]];
    state = 0;
    
    for i in range(0, 4 + 1):
        while(state == i):
            statement[i].append(picked_keyword);
            if(unparsed_keywords == []): break;
            (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
            for j in range(i+1,4 + 1):
                if(eval('picked_keyword in tr_st_' + str(j))):
                    state = j;
                    break;
    
    return statement;

#Grabs table from DB
def get_table(table_name):
    try:
        with open(language.useful_functions.root_directory + '/' + language.useful_functions.current_db + '/' + table_name, 'r') as table:
            entire_table = table.readlines();
            table.close();
    except FileNotFoundError:
        return None;
    
    return entire_table;

#Splits table into a fields list and a 2D data array
def split_entire_table(entire_table):
    fields = [a.split(' ') for a in entire_table[0].replace('\n','').split('|')];
    body = [a.replace('\n','').split('|') for a in entire_table[1:]];
    return (fields, body);
    
#Returns a list that is 1 if the element in the source list is a table, and 0 if the element is not
def get_num_tables(arr):
    return [1 if a in os.listdir(language.useful_functions.root_directory + '/' + language.useful_functions.current_db) else 0 for a in arr];

def action(picked_keyword, unparsed_keywords):
    #Catch using statement too early
    if(language.useful_functions.current_db == ''):
        return (1, '');
            
    (picked_keyword, unparsed_keywords) = language.useful_functions.get_next_keyword(unparsed_keywords);
    
    statement = get_form(picked_keyword, unparsed_keywords);
    #print(statement)

    if(statement[0] == []):
        return (2, '');
    
    fields_list = statement[0];
    
    if(statement[1] + statement[2] + statement[3] + statement[4] == []):
        return (3, picked_keyword);

    #Begin Stage 1 (from)
    #Remove 'from'
    statement[1] = statement[1][1:];
    if(statement[1] == []):
        return (3, 'from');
    
    #Dictionary that stores table nicknames
    table_name_dict = {};
    
    #Get table(s) within stage 1 and its nickname(s), if any
    tmp_num_tables = get_num_tables(statement[1]);
    for i, a in enumerate(tmp_num_tables):
        if(a == 1):
            table_name_dict[statement[1][i]] = statement[1][i];
        elif(a == 0 and tmp_num_tables[i-1] == 1):
            table_name_dict[statement[1][i]] = statement[1][i-1];
            del table_name_dict[statement[1][i-1]];
        else:
            return (3, statement[1][i-1]);
    
    table_name_pos = [a for a in table_name_dict.keys()]
    
    #Detect cross-join syntax, then fix
    #Can not handle more than one cross join -- should re-work Stage 2 and 3 to be one stage with multiple '<join type> join <table> on <criteria>' entries
    if(len(table_name_dict) == 2):
        statement[2].append('cross');
        statement[2].append('join');
        statement[2].append(table_name_dict[table_name_pos[1]]);
        statement[2].append(table_name_pos[1]);
        table_name_dict.pop(table_name_pos[1]);
        del statement[1][2:4];
    elif(len(table_name_dict) > 2):
        return(99, '!Statement is joining too many tables.');
    
    #Begin Stage 2 (join)
    #get table name from join, and store what kind of join
    table_joins = [''];
    join_number = 0;
    if(statement[2] != []):
        #Only append join as a left join if it's the first keyword
        if(statement[2][0] == 'join'):
            table_joins.append('left');
            join_number += 1;
            
        #Determine type of join
        tmp_num_tables = get_num_tables(statement[2]);
        for i, a in enumerate(statement[2]):
            if(a == 'join'):
                join_number += 1;
            elif(a == 'outer'):
                continue;
            elif(a in tr_st_2):
                table_joins.append(a);
                join_number += 1;
            else:
                #Argument is either a table or a table nickname
                if(tmp_num_tables[i] == 1):
                    table_name_dict[a] = a;
                elif(tmp_num_tables[i] == 0 and tmp_num_tables[i-1] == 1):
                    table_name_dict[a] = statement[2][i-1];
                    del table_name_dict[statement[2][i-1]];
                else:
                    return (3, statement[2][i-1]);
                    
    table_name_pos = [a for a in table_name_dict.keys()]
    
    #At this point, table_name_dict should contain references to every table needed for the operation, and table_joins should have a type of join for each table
    
    #Begin Stage 3 (on)
    join_criteria = [('', '', '')];
    
    if(statement[3] != [] and table_joins != ['']):
        #Remove 'on'
        statement[3] = statement[3][1:];
        tmp_on_clause = statement[3].copy();
        #Add join clauses
        while(len(tmp_on_clause) >= 3):
            if(tmp_on_clause[1] == '='): tmp_on_clause[1] = '==';
            join_criteria.append((tmp_on_clause[0],tmp_on_clause[1],tmp_on_clause[2]));
            tmp_on_clause = tmp_on_clause[3:];

    #Begin Stage 4 (where)
    where_criteria = [];
    if(statement[4] != []):
        #Remove 'where'
        statement[4] = statement[4][1:];
        tmp_where_clause = statement[4].copy();
        #Add where clauses
        while(len(tmp_where_clause) >= 3):
            if(tmp_where_clause[1] == '='): tmp_where_clause[1] = '==';
            where_criteria.append((tmp_where_clause[0],tmp_where_clause[1],tmp_where_clause[2]));
            tmp_where_clause = tmp_where_clause[3:];
    
    #At this point, the following should be true:
    #table_name_dict contains references to every table needed for the operation
    ###The first entry is the source table, and every subsequent entry
    #table_joins contains the type of join for each table
    #join_criteria contains the join clause criteria for each join
    #where_criteria contains the where clause criteria for the table
    
    #This means we are ready to parse all the information
    #print(statement)
    #print(fields_list)
    #print(table_name_dict)
    #print(table_name_pos)
    #print(table_joins)
    #print(join_criteria)
    #print(where_criteria)
    
    table = [];
    fields = [];
    all_fields = [];
    body = [];
    
    final_fields = [];
    final_all_fields = [];
    final_body = [];
    
    #Begin combining data into one big table
    for i, table_nickname in enumerate(table_name_pos):
        table.append(None);
        fields.append(None);
        all_fields.append(None);
        body.append(None);
        #Get table
        table[i] = get_table(table_name_dict[table_name_pos[i]]);
        if(table[i] == None):
            return (5, 'query table ' + table_name_dict[table_name_pos[i]]);

        #Split into fields list and data
        (fields[i], body[i]) = split_entire_table(table[i]);
        fields[i] = [[table_name_pos[i] + '.' + a[0], a[1]] for a in fields[i]];

        all_fields[i] = [a[0] for a in fields[i]];

        #Perform the join and add it to the final table
        if(table_joins[i] == ''):
            final_fields = fields[i].copy();
            final_all_fields = all_fields[i].copy();
            final_body = body[i].copy();
            
        #Cross join
        elif(table_joins[i] == 'cross'):
            final_fields.extend(fields[i]);
            final_all_fields.extend(all_fields[i]);
            
            combined_body = [];
            
            for j in final_body:
                for k in body[i]:
                    tmp = j.copy();
                    tmp.extend(k.copy());
                    combined_body.append(tmp);
            
            final_body = combined_body.copy();
           
        #Inner join
        elif(table_joins[i] == 'inner'):
            final_fields.extend(fields[i]);
            final_all_fields.extend(all_fields[i]);
            
            combined_body = [];
            
            for j in final_body:
                #added_record = False;
                for k in body[i]:
                    tmp = j.copy();
                    tmp.extend(k.copy());
                    
                    if(eval('where_val_helper(j[final_all_fields.index(join_criteria[i][0])]) ' + join_criteria[i][1] + ' where_val_helper(k[all_fields[i].index(join_criteria[i][2])])')):
                        combined_body.append(tmp);
                        #added_record = True;
            
            final_body = combined_body.copy();
        
        #Left join
        elif(table_joins[i] == 'left'):
            final_fields.extend(fields[i]);
            final_all_fields.extend(all_fields[i]);
            
            combined_body = [];
            
            for j in final_body:
                added_record = False;
                for k in body[i]:
                    tmp = j.copy();
                    tmp.extend(k.copy());
                    
                    if(eval('where_val_helper(j[final_all_fields.index(join_criteria[i][0])]) ' + join_criteria[i][1] + ' where_val_helper(k[all_fields[i].index(join_criteria[i][2])])')):
                        combined_body.append(tmp);
                        added_record = True;
                if(added_record == False):
                    tmp = j.copy();
                    tmp.extend(['']*len(all_fields[i]));
                    combined_body.append(tmp);
            
            final_body = combined_body.copy();

        else:
            break;
        
    #Now we have a big table (source_body) containing every table merged together. Time to reduce the columns.
    
    #Fix the fields_list to remove * fields
    if(fields_list == ['*']):
        fields_list = final_all_fields;
    for i, a in enumerate(fields_list):
        if(a.find('*') != -1):
            #Must be of the form '<table>.*'
            fields_list[i] = all_fields[table_name_pos.index(a[:-2])]

    #Now pull the arrays out while preserving order
    tmp_fields_list = [];
    for a in fields_list:
        if(type(a) is list):
            for b in a:
                tmp_fields_list.append(b);
        else:
            tmp_fields_list.append(a);
    fields_list = tmp_fields_list;
    
    #Make remapping list for combined table
    remapping_list = [final_all_fields.index(b) for b in fields_list];

    #Filter down fields and body
    #Remove columns
    if(fields_list != all_fields):
        #Drop the extra fields from the fields list and re-order
        final_fields = [final_fields[i] for i in remapping_list];
        
    #Do the where clause    
    for where_field_name, where_operator, where_value in where_criteria:
        for i, a in enumerate(final_body):
            if(eval('where_val_helper(final_body[i][final_all_fields.index(where_field_name)]) ' + where_operator + ' where_val_helper(final_body[i][final_all_fields.index(where_value)])')):
                
                continue;
            else:
                final_body[i] = '';
        
        final_body = [i for i in final_body if i != ''];
        
    #Drop the extra info from the body and re-order
    for i, f in enumerate(final_body):
        final_body[i] = [final_body[i][j] for j in remapping_list];
    
    #Lastly, strip the table name from the fields if there is no naming conflict
    tmp_final_fields = final_fields.copy();
    for i, a in enumerate(tmp_final_fields):
        tmp_final_fields[i] = a.copy();
    
    #Lastly, strip the table name from the fields if there is no naming conflict
    for i, a in enumerate([k[0] for k in final_fields]):
        include_table_name = False;
        for j, b in enumerate([k[0] for k in final_fields]):
            if i != j:
                if(a[a.index('.')+1:] == b[b.index('.')+1:]):
                    include_table_name = True;
                    break;
        if(include_table_name == False):
            tmp_final_fields[i][0] = a[a.index('.')+1:];
    
    final_fields = tmp_final_fields;
    
    #Return result
    
    body_string = '\n'.join(['|'.join(a) for a in final_body]);
    fields_string = '|'.join([' '.join(a) for a in final_fields]);
    return (0, fields_string + '\n' + body_string);