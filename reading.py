# Functions for reading tables and databases

import glob
from database import *

# a table is a dict of {str:list of str}.
# The keys are column names and the values are the values
# in the column, from top row to bottom row.

# A database is a dict of {str:table},
# where the keys are table names and values are the tables.

# YOU DON'T NEED TO KEEP THE FOLLOWING CODE IN YOUR OWN SUBMISSION
# IT IS JUST HERE TO DEMONSTRATE HOW THE glob CLASS WORKS. IN FACT
# YOU SHOULD DELETE THE PRINT STATEMENT BEFORE SUBMITTING
file_list = glob.glob('*.csv')

# Write the read_table and read_database functions below


def read_table(file_name):
    '''
    (str) -> table
    opens up a .csv file and creates a Table object from it, which is a dict
    of {str:list of str}. The keys are the column names and the values are
    the values in the object.
    REQ: file must be a properly formatted .csv file (no blank lines, etc)
    '''
    file = open(file_name, 'r')

    line = file.readlines()
    # some initiations and stuff
    new_list = []
    value_list = []
    new_dict = {}
    # creates a new_list with each element being a list of a line in the file
    for element in line:
        element = element.replace('\n', '')
        element = element.strip()
        element = element.split(',')
        new_list.append(element)

    # creates the dictionary
    for o in range(0, len(new_list[0])):
        # creates a value list for the dictionary keys
        for i in range(1, len(new_list)):
            value_list.append(new_list[i][o])
        new_dict[new_list[0][o]] = value_list[:]
        # sets the value list back to nothing and repeats with each key
        value_list = []

    file.close()
    new_table = Table()
    new_table.set_dict(new_dict)
    return new_table


def read_database():
    '''
    () -> Database
    returns a database, which is a list in the form of (table name : Table).
    The table names and Tables are taken from all the csv files in the same
    file directory as reading.py
    '''
    dat_dict = {}
    # create the database dictionary
    for p in range(0, len(file_list)):
        # removes the .csv part of the names for the key
        dat_dict[file_list[p].replace('.csv', '')] = read_table(file_list[p])
    new_database = Database()
    new_database.set_dict(dat_dict)
    return new_database
