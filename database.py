class Table():
    '''A class to represent a SQuEaL table'''

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        self._table_dict = new_dict

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        return self._table_dict

    def get_key_list(self, key):
        '''
        (Table, str) -> list
        returns the list of values that correspond to the given key
        '''
        return self._table_dict[key]

    def get_keys(self):
        '''
        (Table) -> list
        Returns the keys of the dictionary in a list
        '''
        self.key_list = []
        for i in self._table_dict:
            self.key_list.append(i)
        return self.key_list

    def get_row(self, n):
        '''
        (Table, int) -> dict
        returns the nth row of the table in a dictionary, where the key to each
        value is the same as that of the table. Starts at row 0.
        REQ: dictionary in the Table format, which means that all values of
        every key must be a list
        '''
        self.nth_row = {}
        for i in self._table_dict:
            self.nth_row[i] = self._table_dict[i][n]
        return self.nth_row

    def num_rows(self):
        '''
        (Table) -> int
        returns the number of rows in the table
        REQ: dictionary in the Table format, which means that all values of
        every key must be a list
        '''
        self.row_count = 0
        # get a list of own keys first
        a = self.get_keys()
        for i in self._table_dict[a[0]]:
            self.row_count += 1
        return self.row_count

    def choose_keys(self, list_of_keys):
        '''
        (Table, list of keys) -> dict
        returns a dictionary using the keys given from the list
        '''
        self.new_dict = {}
        for i in self._table_dict:
            if (i in list_of_keys):
                self.new_dict[i] = self._table_dict[i]
        return self.new_dict

    def remove_row(self, n):
        '''
        (Table, int) -> NoneType
        removes the nth row from the table
        '''
        for i in self._table_dict:
            self._table_dict[i].pop(n)

    def remove_all_rows(self):
        '''
        (Table) -> NoneType
        remove all rows from table
        '''
        row_num = 0
        for i in range(0, self.num_rows()):
            self.remove_row(0)
            row_num += 1


class Database():
    '''A class to represent a SQuEaL database'''

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        self._data_dict = new_dict

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        return self._data_dict

    def get_table(self, key):
        '''
        (Database) -> table
        returns the table value from the given key
        '''
        return self._data_dict[key]
