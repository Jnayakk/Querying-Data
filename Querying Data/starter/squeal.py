from reading import *
from database import *

# The delimiter which is a comma for sql purposes.
COMMA_DELIMETER = ','

# The operator representing equal
EQUALS_OPERATOR = '='

# The operator representing greater than.
GREATER_OPERATOR = '>'

# The delimeter which is a space
SPACE_DELIMETER = ' '

# The token where one can declare which tables to acquire.
FROM_TOKEN = "from"

# The token where one can declare which columns to acquire
SELECT_TOKEN = "select"

# The input prompt
INPUT_PROMT = "Enter a SQuEaL query, or a blank line to exit:"

ALL_TOKEN = '*'
# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results


def print_csv(table):
    '''(Table) -> NoneType
    Print a representation of table.
    '''
    dict_rep = table.get_dict()
    columns = list(dict_rep.keys())
    print(','.join(columns))
    rows = table.count_rows()
    for i in range(rows):
        cur_column = []
        for column in columns:
            cur_column.append(dict_rep[column][i])
        print(','.join(cur_column))


def cartesian_product(first_table, second_table):
    '''(Table, Table) -> Table

    Computes the cartesian product of the first and second table and
    returns it. That is where each row in the first table is paired
    with every row in the second table.
    '''
    # look in database.py file for how this was calculated.
    return first_table.cartesian_product(second_table)


def format_query(query):
    '''(str) -> dict

    Whatever query is entered as a string, this function takes it and
    returns it as a dictionary where select and from are keys and
    their values are columns and tables.
    REQ: query is in proper sql syntax

    >>> format_query('select books.title from books')
    {'from': ['books'], 'select': ['books.title']}

    >>> format_query("select o.category, m.title from movies,oscar")
    {'from': ['movies', 'oscar'], 'select': ['o.category', 'm.title']}
    '''
    formatted_query = {}

    # split query by using a white space as the delimeter
    query = query.split(SPACE_DELIMETER)

    # get the select and from values, since the sql syntax will always be
    # in correct form, the values for select will be the string after
    # the 0th index and the values for from will be the string after
    # the 3rd index
    select_values = query[1].split(COMMA_DELIMETER)
    from_values = query[3].split(COMMA_DELIMETER)

    # map the string "select" to the values after select in the query
    formatted_query[SELECT_TOKEN] = select_values
    # map the string "from" to the values after select in the query
    formatted_query[FROM_TOKEN] = from_values

    return formatted_query


def run_query(db, query):
    '''(Database, str) -> Table

    Given a Database object and a query in the form of a string. This
    function runs the query on the database and returns a table
    representing the resulting table.

    r = ({'b.title': ['The Maze Runner', 'Dusk'], 'b.category':
         ['Mystery', 'Thriller'], 'b.movies': ['yes', 'no']})
    d = Database()
    d.save_to_database(r)
    res = run_query(db, "select b.title,b.movies from ratings").get_dict()
    res == ({'b.title': ['The Maze Runner', 'Dusk'], 'b.movies':
             ['yes', 'no']})
    True
    '''
    # format the query to know for sure what token wants what.
    formatted_query = format_query(query)

    # get the cartesian table of all the tables listed in query after from
    # look in database.py to see how that happens.
    table = db.get_cartesian_table(query)

    # whichever columns were selected in the query thats what is going
    # to be in the final table.
    final_table = sql_syntax_select(table, formatted_query)
    return final_table


def sql_syntax_select(table, formatted_query):
    '''(Table, dict) -> Table

    From the formatted query, find select and its values and only return
    them in a new table

    >>> t = Table()
    >>> t.set_dict({'b.title': ['The Maze Runner', 'Dusk'], 'b.category':
         ['Mystery', 'Thriller'], 'b.movies': ['yes', 'no']})
    res = sql_syntax_select(t, {'from': [t],
                            'select': ['b.title']}
    res.get_dict() == {'b.title': ['The Maze Runner', 'Dusk']}
    True
    '''

    # find the select key and declare its values as list of columns
    list_of_columns = formatted_query[SELECT_TOKEN]

    # get the table represented as a dictionary from the table object
    my_table = table.share_table()

    selected = {}
    # create a table
    select_table = Table()

    # get all of the columns if the value in select key is '*'
    if list_of_columns == [ALL_TOKEN]:
        list_of_columns = [(my_table.keys())]

    # if the query is not selecting all of the values, then go through
    # each column and get its values to store in the new dictionary.
    else:
        for column in list_of_columns:
            selected[column] = my_table[column]

    # save the dictionary to the table and then return it.
    select_table.save_to_table(selected)
    return select_table


if(__name__ == "__main__"):
    # ask the input prompt and read the database
    query = input(INPUT_PROMT)
    database = read_database()

    # while a blank line is not entered, keep showing the input prompt
    while (query != ""):
        print_csv(run_query(database, query))
        query = input(INPUT_PROMT)
