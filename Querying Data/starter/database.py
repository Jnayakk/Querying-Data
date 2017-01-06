# The token where one can declare which tables to acquire.
FROM_TOKEN = "from"

# The token for selecting all columns
ALL_COLUMNS_TOKEN = '*'

# The delimiter which is a comma for sql purposes.
COMMA_DELIMETER = ','

# The operator representing equal
EQUALS_OPERATOR = '='

# The operator representing greater than.
GREATER_OPERATOR = '>'

# The delimeter which is a space
SPACE_DELIMETER = ' '


class Table():
    '''A class to represent a SQuEaL table'''

    def save_to_table(self, given_dict):
        '''(Table, dict of {str: list of str}) -> NoneType
        Takes the given dictionary and saves it to the table class
        '''
        self._table = given_dict

    def share_table(self):
        '''(Table) -> dict of {str: list of str}

        Returns the table stored in the table class represented as a
        dictionary
        '''
        return self._table

    def count_rows(self):
        '''(Table) -> int
        Return the number of rows in the table
        '''
        res = 0
        # go to the first key and check the length of values in the list
        # that it is mapped to, that is the amount of rows there are in the
        # dictionary
        for i in self._table:
            res = len(self._table[i])
        return res

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        self._table = new_dict

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        return self._table

    def cartesian_product(self, second_table):
        '''(Table, Table) -> Table

        Computes the cartesian product of the first and second table and
        returns it. That is where each row in the first table is paired
        with every row in the second table.
        '''
        # count the number of rows in both given tables
        table_1_rows = self.count_rows()
        table_2_rows = second_table.count_rows()

        # get the dictionary representations of the tables
        table_1 = self.share_table()
        table_2 = second_table.share_table()

        # create a new dictionary for the cartesian product of the two tables
        new_dict = dict()

        # for each value of each key in the first table (represented as
        # a dictionary)
        for key in table_1:
            for value in table_1[key]:
                # if the key is in the new dictionary
                if (key in new_dict):
                    # multiply each key values by the number of
                    # rows in the second table and add them to the
                    # key values in the new dict
                    new_dict[key] += (table_2_rows*[value])
                else:
                    # create a new key as an empty list and do the
                    # same as above if the key is not in the new dictionary.
                    new_dict[key] = []
                    new_dict[key] += (table_2_rows*[value])

        # for each key in the second table (represented as a dictionary)
        for key in table_2:
            # the key values in the new dicitionary is the product of the
            # number of rows in the first table and the key values in the
            # second table
            new_dict[key] = table_1_rows*table_2[key]

        table = Table()
        table.save_to_table(new_dict)
        return table


class Database():
    '''A class to represent a SQuEaL database'''

    def obtain_table_from_db(self, table_name):
        '''(Database, str) -> Table

        Returns a table object from a database.
        '''
        # obtain the database represented as a dictionary.
        database_dict = self.share_database()

        # acquire the table object from the database by using its name
        # then return it.
        table_object = database_dict.get(table_name)
        return table_object

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        self._database = new_dict

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        return self._database

    def save_to_database(self, given_dict):
        '''(Table, dict of {str: list of str}) -> NoneType
        Takes the given dictionary and saves it to the database class
        '''
        self._database = given_dict

    def share_database(self):
        '''(Table) -> dict of {str: list of str}

        Returns the dictionary stored in the database class
        '''
        return self._database

    def sql_syntax_from(self, from_clause):
        '''(Database, str) -> Table
        Returns a table containing all of the columns from all of the
        tables that are involved in the query. Which is the cartesian
        product of all of the tables involved in the query.
        '''
        list_of_table_names = from_clause.split(COMMA_DELIMETER)

        # remove the first table name and make that the base table
        base_table_name = list_of_table_names.pop(0)

        # get the table object from the base table name
        my_table = self.obtain_table_from_db(base_table_name)

        # for each table in the from clause, compute the cartesian product
        # of the base table (my_table) and the table after it.
        for each_table in list_of_table_names:
            my_table = (my_table.cartesian_product
                        (self.obtain_table_from_db(each_table)))

        return my_table

    def process_all_where_constraints(self, all_where_clause):
        '''(Database, str) -> (str, str, str)

        Returns a list of tuples that contain two operands and one
        operator for the amount of where clauses given.
        '''
        # split all the where clauses with the delimeter being a comma.
        list_of_where_clause = all_where_clause.split(COMMA_DELIMETER)

        list_of_operators_and_operands = []

        # for each where clause, in the list
        for each_where_clause in list_of_where_clause:

            # find the index of the operators, whether they are = or >
            equals_operator_index = each_where_clause.find(EQUALS_OPERATOR)
            greater_than_operator_index = (each_where_clause.find
                                           (GREATER_OPERATOR))

            # if the equals operator is found, then that is the operator
            # being used in the where clause.
            if (equals_operator_index != -1):
                operator_index = equals_operator_index
            # if the greater-than operator index is found, then that is the
            # operator being used in the where clause.
            elif (greater_than_operator_index != -1):
                operator_index = greater_than_operator_index

            # the result will be a tuple containing the first operand, then
            # the operator and then the second operand.
            list_of_operators_and_operands.append(
                (each_where_clause[:operator_index], each_where_clause
                 [operator_index], each_where_clause[operator_index + 1:]))

        return list_of_operators_and_operands

    def get_cartesian_table(self, query):
        '''(Database, str) -> Table

        From the given query, returns a table that is the cartesian
        product of all tables listed in the query.
        '''
        # split the query with the delimeter being a space
        formatted_query = query.split(SPACE_DELIMETER)

        # find one index above the index of the first occurence
        # of the string "from".
        from_clause_index = formatted_query.index(FROM_TOKEN) + 1
        cartesian_table = (self.sql_syntax_from
                           (formatted_query[from_clause_index]))

        return cartesian_table
