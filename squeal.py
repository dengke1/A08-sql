from reading import *
from database import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results


def merge(dict1, dict2):  # check
    '''
    (dict, dict) -> dict
    combines two dictionaries together into a single one. The new one is then
    returned.
    >>> a = merge({'a':1, 'b':2, 'c':3}, {'d':4, 'e':5})
    a == {'a':1, 'b':2, 'c':3, 'd':4, 'e':5}
    True
    '''
    dict1.update(dict2)
    return dict1


def combine_dict(dict1, dict2):
    '''
    (dict, dict) -> dict
    takes 2 dictionaries from the table objects and merges the values of
    each key into a list, which becomes the new value of the shared key. The
    values of the latter dictionary are inserted after the first.
    If keys are not shared, they are discarded. Basically it stacks rows
    on top of each other and creates a new dictionary.
    REQ: values need to be lists, strings, floats, integers or boolean
    REQ: the 2 dictionaries need to have the same keys

    >>> a = combine_dict({'a': [1, 2], 'c': False, 'b': 'g'},\
    {'a': [1, 1], 'c': [3, 3], 'b': [2, 2]})
    a == {'a': [1, 2, 1, 1], 'c': [False, 3, 3], 'b': ['g', 2, 2]}
    True
    '''
    # create a dictionary with the shared keys, with empty lists as values
    ret_dict = {}
    for i in dict1:
        ret_dict[i] = []
    # stick the values of the two dicts into corresponding lists
    for i in dict1:
        if (not isinstance(dict1[i], list)):
            ret_dict[i].append(dict1[i])
        else:
            ret_dict[i].extend(dict1[i])
    # .extend() the values of the second dictionary into new dict
    for i in dict2:
        if (not isinstance(dict2[i], list)):
            ret_dict[i].append(dict2[i])
        else:
            ret_dict[i].extend(dict2[i])
    return ret_dict


def cartesian_product(table1, table2):
    '''
    (Table, Table) -> Table
    Each row of the first table is stuck together with each row of the second
    table. The new table will have all of the column names of each table.
    This should result in (# of rows in table1) x (# of rows in table2) rows
    in the returned table. If one table is empty, then the resultant product
    will have no values in each of its keys.
    REQ: Tables given must be in proper Table format (column name as list,
    rest of column in list as a value, unique column names)

    >>> a = Table()
    >>> b = Table()
    >>> a.set_dict({1:[1, 2], 2:[2, 3], 3:[3, 4]})
    >>> b.set_dict({'a':['a', 'b'], 'b':['b','c']})
    >>> l = cartesian_product(a, b)
    >>> l.get_dict() == {1: [1, 1, 2, 2], 2: [2, 2, 3, 3], 3: [3, 3, 4, 4],\
    'a': ['a', 'b', 'a', 'b'], 'b': ['b', 'c', 'b', 'c']}
    True

    >>> a = Table()
    >>> b = Table()
    >>> a.set_dict({1:[], 2:[], 3:[]})
    >>> b.set_dict({'a':['a', 'b'], 'b':['b','c']})
    >>> l = cartesian_product(a, b)
    >>> l.get_dict() == {1: [], 2: [], 3: [],'a': [], 'b': []}
    True
    '''
    list_of_dict = []
    product = {}
    # merge all the rows in the two tables, stick into list
    for i in range(0, table1.num_rows()):
        for o in range(0, table2.num_rows()):
            list_of_dict.append(merge(table1.get_row(i), table2.get_row(o)))

    try:
        # start off the product of the dictonaries
        product = combine_dict(list_of_dict[0], list_of_dict[1])
        # combine everything after
        for i in range(2, len(list_of_dict)):
            product = combine_dict(product, list_of_dict[i])

    # if there aren't any rows in one table then all lists in dict are emptied
    except IndexError:
        keys = merge(table1.get_dict(), table2.get_dict())
        for i in keys:
            product[i] = []

    product_table = Table()
    product_table.set_dict(product)
    return product_table


def instruction_list(info):
    '''
    (str) -> list of list
    takes the given query in the SQuEaL and translates the stuff into computer
    friendly list of terms. First item in the list describes which columns,
    second describes which tables, and third item are some restrictions.
    REQ: given string must be in proper SQuEaL syntax

    >>> instruction_list("select m.title,m.studio,m.gross,m.year from movies\
     where m.title=o.title")
    [['m.title', 'm.studio', 'm.gross', 'm.year'], ['movies'],\
    ['m.title=o.title']]
    '''
    from_index = info.find('from')
    where_index = info.find('where')  # if it's -1 then where is not there
    instruction_list = []
    # create some strings to hold parts of the query
    select_info = info[6:from_index]
    if (where_index == -1):
        from_info = info[from_index + 4:]
    else:
        from_info = info[from_index + 4:where_index]
        where_info = info[where_index + 5:]

    ret_list = []
    # stick these lnstructions into a common list
    instruction_list.append(select_info)
    instruction_list.append(from_info)
    if (where_index != -1):
        instruction_list.append(where_info)
    for i in instruction_list:
        i = i.strip()
        i = i.split(',')
        ret_list.append(i)
    return ret_list


def do_from(data, table_list):  # examples
    '''
    (Database, list of str) -> table
    returns a cartesian product for all the tables mentioned in the table list.
    If only one is present that table is returned. If more than one table is
    given, all the tables are stuck together with every other table using
    the cartesian_product function(see REQ for cartesian_product).
    REQ: given list must contain correct table names. Extra names may not be
    given.

    >>> a = Table()
    >>> b = Table()
    >>> c = Table()
    >>> data = Database()
    >>> a.set_dict({'11': ['a', 'b'], '22': ['a', 'b'], '33': ['a', 'b']})
    >>> b.set_dict({'aa': ['1', '2'], 'bb': ['1', '2']})
    >>> c.set_dict({'88':['7'], '99':['8'], '55':['4']})
    >>> data.set_dict({'one': a, 'two':b, 'three': c})
    >>> list1 = ['one', 'two', 'three']
    >>> n = do_from(data, list1)
    >>> n == {'99': ['8', '8', '8', '8'], 'bb': ['1', '2', '1', '2'],\
    '33': ['a', 'a', 'b', 'b'], '11': ['a', 'a', 'b', 'b'],\
    'aa': ['1', '2', '1', '2'], '88': ['7', '7', '7', '7'],\
    '22': ['a', 'a', 'b', 'b'], '55': ['4', '4', '4', '4']}
    True

    >>> a = Table()
    >>> b = Table()
    >>> c = Table()
    >>> data = Database()
    >>> a.set_dict({'11': ['a', 'b'], '22': ['a', 'b'], '33': ['a', 'b']})
    >>> b.set_dict({'aa': ['1', '2'], 'bb': ['1', '2']})
    >>> c.set_dict({'88':['7'], '99':['8'], '55':['4']})
    >>> data.set_dict({'one': a, 'two':b, 'three': c})
    >>> list1 = ['one']
    >>> n = do_from(data, list1)
    >>> n == {'11': ['a', 'b'], '22': ['a', 'b'], '33': ['a', 'b']}
    True
    '''
    # set the temporary table to the first given table
    temp_table = data.get_table(table_list[0])
    try:
        if (len(table_list) > 1):
            for i in range(1, len(table_list)):
                temp_table = cartesian_product(temp_table,
                                               data.get_table(table_list[i]))
    # if there aren't any rows in one table then all lists are emptied
    except IndexError:
        temp_table.remove_all_rows()
    return temp_table


def do_constraint(table, constraint):  # value iS HARDCODED, NOT NUMERICAL
    '''
    (Table, str) -> Table
    takes instructions in the constraint list returns a table based on
    what is given.
    'column_name1=column_name2' returns a table with only identical rows
    in both columns
    'column_name1>column_name2' returns a table with only rows with values
    in column1 that are bigger than those in column2. Has to actually
    compare floats/ints.
    'column_name1='value' returns a table only where values in rows
    in column_name1 are equal to the given value
    'column_name1>'value' returns a table only where values in rows
    in column_name1 are greater than the given value. Has to actually
    compare floats/ints.
    REQ: constraint has to be in one of these formats
    REQ: actual column names must be given.
    REQ: 'value' has to be a hardcoded and has to be between the single quotes

    >>> a = Table()
    >>> a.set_dict({'11': ['a', 'b'], '22': ['a', 'b'], '33': ['a', 'b']})
    >>> n = do_constraint(a, "11='a'")
    >>> n == {'11' : ['a'], '22' :['a'], '33' :['a']}
    True

    >>> a = Table()
    >>> a.set_dict({'11': ['1', '2'], '22': ['0', '0'], '33': ['a', 'b']})
    >>> n = do_constraint(a, "22>11")
    >>> n == {'11' : [], '22' :[], '33' :[]}
    True

    >>> a = Table()
    >>> a.set_dict({'11': ['1', '2'], '22': ['2', '2'], '33': ['a', 'b']})
    >>> n = do_constraint(a, "11=22")
    >>> n == {'11' : ['2'], '22' :['2'], '33' :['b']}
    True
    '''
    equal = constraint.find('=')
    greater = constraint.find('>')
    key1 = ''
    key2 = ''
    row_num = 0
    # check if I have to work with a hardcoded value
    # if I do, value is set to a variable
    value_given = False
    try:
        a = constraint.index("'")
        value = constraint[a + 1:len(constraint) - 1]
        value_given = True
    except:
        value_given = False

    # if we have to work with hardcoded value
    if (value_given):
        # remove rows that aren't equal
        if (equal != -1):
            key1 = constraint[0:equal]
            row_num = 0
            for i in range(0, table.num_rows()):
                if (table.get_key_list(key1)[row_num] != value):
                    table.remove_row(row_num)
                    row_num -= 1
                row_num += 1
        # remove rows that aren't greater than numerical hardcoded value
        elif (greater != -1):
            key1 = constraint[0:greater]
            row_num = 0
            for i in range(0, table.num_rows()):
                if (float(table.get_key_list(key1)[row_num]) <= float(value)):
                    table.remove_row(row_num)
                    row_num -= 1
                row_num += 1

    # if we do not have to work with value but only columns
    else:
        try:
            # remove rows that aren't equal from both columns
            if (equal != -1):
                row_num = 0
                key1 = constraint[0:equal]
                key2 = constraint[equal + 1:]
                for i in range(0, table.num_rows()):
                    if (table.get_key_list(key1)[row_num] !=
                            table.get_key_list(key2)[row_num]):
                        table.remove_row(row_num)
                        row_num -= 1
                    row_num += 1
            # remove rows that aren't greater from both columns
            elif (greater != -1):
                row_num = 0
                key1 = constraint[0:greater]
                key2 = constraint[greater + 1:]
                for i in range(0, table.num_rows()):
                    if (float(table.get_key_list(key1)[row_num]) <=
                            float(table.get_key_list(key2)[row_num])):
                        table.remove_row(row_num)
                        row_num -= 1
                    row_num += 1
        except:  # remove all the rows from table if column2 is not found
            table.remove_all_rows()
    return table


def run_query(DATABASE, string):
    '''
    (Database, string) -> Table
    Takes a database and given query and creates a table based on the
    instructions in the query.
    REQ: query must follow correct SQuEaL syntax

    >>> a = Table()
    >>> b = Table()
    >>> c = Table()
    >>> data = Database()
    >>> a.set_dict({'11': [], '22': [], '33': []})
    >>> b.set_dict({'aa': ['a', 'b', 'c'], 'bb': ['1', '2', '3']})
    >>> c.set_dict({'88':['7', '8'], '99':['8', '9'], '55':['4', '8']})
    >>> data.set_dict({'one': a, 'two':b, 'three': c})
    >>> query = "select aa,bb,88 from two,three"
    >>> l = run_query(data, query)
    >>> l.get_dict() == {'aa' : ['a', 'b', 'c', 'a', 'b', 'c']\
    'bb':['1', '2', '3', '1', '2', '3'], '88':['7', '7', '7', '8', '8', '8']}
    True

    >>> a = Table()
    >>> b = Table()
    >>> c = Table()
    >>> data = Database()
    >>> a.set_dict({'11': [], '22': [], '33': []})
    >>> b.set_dict({'aa': ['a', 'b', 'c'], 'bb': ['1', '2', '3']})
    >>> c.set_dict({'88':['7', '8']})
    >>> data.set_dict({'one': a, 'two':b, 'three': c})
    >>> query = "select * from two,three where 88=7,aa=a"
    >>> l = run_query(data, query)
    >>> l.get_dict() == {'aa' : ['a'], 'bb':['1'], '88':['7']}
    True
    '''
    # turn the query into a list of parts
    query = instruction_list(string)
    # does cartesian product on every single given table
    temp_table = do_from(DATABASE, query[1])
    # try to do the where statements, otherwise ignore
    try:
        for i in query[2]:
            temp_table = do_constraint(temp_table, i)
    except:
        pass

    # choose which keys to keep, also checks if asterik is given
    if (query[0] == ['*']):
        pass
    else:
        temp_table = temp_table.choose_keys(query[0])
    # gotta change it back to a table if it isn't one
    if not(isinstance(temp_table, Table)):
        actual_table = Table()
        actual_table.set_dict(temp_table)
    else:
        actual_table = temp_table
    return actual_table


def print_csv(table):
    '''(Table) -> NoneType
    Print a representation of table.
    >>> c.set_dict({'88':['7', '8'], '99':['8', '9'], '55':['4', '8']})
    >>> print_csv(c)
    '''
    dict_rep = table.get_dict()
    columns = list(dict_rep.keys())
    print(','.join(columns))
    rows = table.num_rows()
    for i in range(rows):
        cur_column = []
        for column in columns:
            cur_column.append(dict_rep[column][i])
        print(','.join(cur_column))

if(__name__ == "__main__"):
    query = input("Enter a SQuEaL query, or a blank line to exit:")
    database = read_database()
    while (query != ''):
        print_csv(run_query(database, query))
        query = input("Enter a SQuEaL query, or a blank line to exit:")

    # a = run_query(database, "select b.title,b.studio,b.gross,f.category\
    # from boxoffice,oscar-film where b.title=f.title")
    # print_csv(a)
