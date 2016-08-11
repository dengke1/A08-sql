def constraint_with_value(table, constraint, value, equal, greater):
    '''
    (Table, constraint, float, int, int) -> Table
    '''
    key1 = ''
    key2 = ''
    if (is_value):
        # remove rows that aren't equal
        if (equal != -1):
            key1 = constraint[0:equal]
            row_num = 0
            for i in range(0, table.num_rows()):
                if (float(table.get_key_list(key1)[row_num]) != value):
                    table.remove_row(row_num)
                    row_num -= 1
                row_num += 1
        # remove rows that aren't greater
        elif (greater != -1):
            key1 = constraint[0:greater]
            row_num = 0
            for i in range(0, table.num_rows()):
                if (float(table.get_key_list(key1)[row_num]) <= value):
                    table.remove_row(row_num)
                    row_num -= 1
                row_num += 1
    return table

def constraint_without(table, constraint, equal, greater):
    '''
    (Table, constraint, int, int) -> Table
    '''
    key1 = ''
    key2 = ''
    # if value isnt given do this
    if (equal != -1):
        row_num = 0
        key1 = constraint[0:equal]
        key2 = constraint[equal + 1:]
        try:
            for i in range(0, table.num_rows()):
                if (table.get_key_list(key1)[row_num] !=
                    table.get_key_list(key2)[row_num]):
                    table.remove_row(row_num)
                    row_num -= 1
                row_num += 1                        
        except:
            for i in range(0, table.num_rows()):
                if (table.get_key_list(key1)[row_num] != key2):
                    table.remove_row(row_num)
                    row_num -= 1
                row_num += 1

    # remove rows that aren't greater
    elif (greater != -1):
        row_num = 0
        key1 = constraint[0:greater]
        key2 = constraint[greater + 1:]
        for i in range(0, table.num_rows()):
            if (float(table.get_key_list(key1)[row_num]) <=
                float(table.get_key_list(key2)[row_num])):
                table.remove_row(row_num)
                row_num -= 1
            row_num += 1-
    return table
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
    REQ: 'value' has to be a hardcoded and has to be between the single quotes

    >>> a = Table()
    >>> a.set_dict({'11': ['a', 'b'], '22': ['a', 'b'], '33': ['a', 'b']})
    >>> n = do_constraint(a, "11=a")
    >>> n == {'11' : ['a'], '22' :['a'], '33' :['a']}
    True

    >>> a = Table()
    >>> a.set_dict({'11': ['1', '2'], '22': ['a', 'b'], '33': ['a', 'b']})
    >>> n = do_constraint(a, "11>'1'")
    >>> n == {'11' : ['2'], '22' :['b'], '33' :['b']}
    True

    >>> a = Table()
    >>> a.set_dict({'11': ['1', '2'], '22': ['a', 'b'], '33': ['a', 'b']})
    >>> n = do_constraint(a, "11=fortytwo")
    >>> n == {'11' : [], '22' :[], '33' :[]}
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
        a = constraint.find("'")
        value = constraint[a + 1:len(constraint) - 1]
        value_given = True
    except:
        value_given = False

    # if we have to work with hardcoded value
    if (value_given):
        # remove rows that aren't equal
        if (equal != -1):
            key1 = constraint[0:equal]
            for i in range(0, table.num_rows()):
                if (table.get_key_list(key1)[row_num]) != value):
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
          
    return table


def do_constraint(table, constraint):  # examples
    '''
    (Table, str) -> Table
    takes instructions in the constraint list returns a table based on
    what is given.
    'column_name1=column_name2' returns a table with only identical rows
    in both columns
    'column_name1>column_name2' returns a table with only rows with values
    in column1 that are bigger than those in column2
    'column_name1='value' returns a table only where values in rows
    in column_name1 are equal to the given value
    'column_name1>'value' returns a table only where values in rows
    in column_name1 are greater than the given value
    REQ: constraint has to be in one of these formats
    REQ: 'value' has to be a number as well as the all the values in the
    given column name
    '''
    equal = constraint.index('=')
    greater = constraint.index('>')
    key1 = ''
    key2 = ''
    # check if I have to work with numbers
    # if I do, value is set to a float version
    is_value = False
    try:
        a = constraint.index("'")
        value = float(constraint[a + 1:len(constraint) - 1])
        is_value = True
    except:
        is_value = False

    # if value is given do this
    if (is_value):
        table = constraint_with_value(table, constraint, value, equal, greater)
    # if value isnt given do this
    else:
        table = constraint_without(table, constraint, equal, greater)
    return table


## print(isinstance(query, str))
#a = Table()
#b = Table()
#c = Table()
#data = Database()
#a.set_dict({'11': [], '22': [], '33': []})
#b.set_dict({'aa': ['a', 'b', 'c'], 'bb': ['1', '2', '3']})
#c.set_dict({'88':['7', '8'], '99':['8', '9'], '55':['4', '8']})
#data.set_dict({'one': a, 'two':b, 'three': c})
#list1 = ['one', 'two', 'three']
###l = float(b.key_list('aa')[0])
###print(b.num_rows())
#l = run_query(data, "select aa,bb,88 from three,two")
#print_csv(l)
###l = do_constraint(b, "bb=1")
###print_csv(l)
###{1: [1, 1, 2, 2], 2: [2, 2, 3, 3], 3: [3, 3, 4, 4],\
###'a': ['a', 'b', 'a', 'b'], 'b': ['b', 'c', 'b', 'c']}