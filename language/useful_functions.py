#Coded by Chris Parks
#November 27, 2020. due December 3, 2020
#For UNR CS 457

import os;

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py' or module == 'useful_functions.py':
        continue
    exec('import language.' + module[:-3] + ' as ' + module[:-3]);
del module;

global root_directory;
global current_db;
global transactioning;

global transactions;
global table_locks;

root_directory = os.getcwd();
current_db = '';
transactioning = False;

transactions = [];
table_locks = [];

#Get next keyword from list
def get_next_keyword(unparsed_keywords):
    return (unparsed_keywords[0:1][0], unparsed_keywords[1:]);

def get_lock(table_name):
    global root_directory;
    global current_db;

    try:
        with open(root_directory + '/' + current_db + '/' + table_name + '_lock', 'r') as table:
            #entire_table = table.readlines();
            table.close();
    except FileNotFoundError:
        return False;
    
    return True;
    
#Analyze operation; returns lists of tables referenced by operation
def analyze(this_operation):
    if(this_operation[0] == 'select'):
        tr_st_1 = ['from']
        tr_st_2 = ['left', 'right', 'cross', 'full', 'inner', 'outer', 'join'];
        tr_st_3 = ['on'];
        tr_st_4 = ['where'];
        
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
        
        return statement[1];
    elif(this_operation[0] == 'update'):
        return [this_operation[1]];
    else:
        return [];
    
#Parses and performs one operation, returning an error code
def parse_operation(unparsed_keywords):
    (picked_keyword, unparsed_keywords) = get_next_keyword(unparsed_keywords);
    
    action_keywords = ['select', 'create', 'use', 'alter', 'drop', 'insert', 'update', 'delete', 'begin', 'commit']
    
    if(picked_keyword.lower() in action_keywords):
        return eval(picked_keyword.lower() + '.action(picked_keyword, unparsed_keywords)');

    #.EXIT
    elif(picked_keyword.lower() == '.exit'):
        return exit.action();
    
    else: return (0, '');

#Performs an operation and prints the error code
def execute_operation(this_operation):
    global root_directory;
    global current_db;
    global transactioning;

    global transactions;
    global table_locks;
    
    #print(this_operation)
    if(transactioning and this_operation[0] != 'commit'):
        transactions.append(this_operation);
        for i in analyze(this_operation):    
            try:
                #Create lock
                with open(root_directory + '/' + current_db + '/' + i + '_lock', 'x') as table:
                    table.close();
                
                #Add table to list; this instance has control of lock
                if(i not in table_locks):
                    table_locks.append(i);
            except FileExistsError:
                print('Error: Table ' + i + ' is locked!');
            
    else:
        return_code = parse_operation(this_operation);
        if(return_code[0] == 0): #Success
            print(return_code[1]);
            if(len(return_code) == 3):
                current_db = return_code[2];
            
        elif(return_code[0] == 1): #DB not selected
            print('!No database selected. Execute \'USE <db_name>\' first.');
            
        elif(return_code[0] == 2): #Invalid # of operations
            print('!Syntax error, invalid number of arguments.');
            
        elif(return_code[0] == 3): #Syntax error, unexpected symbol after ''
            print('!Syntax error, unexpected symbol after \'' + return_code[1] + '\'');
            
        elif(return_code[0] == 4): #Database/Table already exists
            print('!Failed to create ' + return_code[1] + ' because it already exists.');
            
        elif(return_code[0] == 5): #It does not exist
            print('!Failed to ' + return_code[1] + ' because it does not exist.');
            
        elif(return_code[0] == 99): #Unique errors
            print(return_code[1]);
        return return_code;