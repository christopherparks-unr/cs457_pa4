#Coded by Chris Parks
#November 27, 2020. due December 3, 2020
#For UNR CS 457

import language.commit;

def action():
    print('All done.');
    language.commit.remove_locks();
    exit();
    return (0, 'All done.');
    