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

# The delimiter which is a comma at the moment
DELIMETER = ','

# Used to read the file
READING_FILE = 'r'

# The extensions of each table file that we have to read from.
EXTENSION = ".csv"

# Write the read_table and read_database functions below


def format_msg(sentance):
    '''(str) -> list of str
    Given a sentance with words split by commas and spaces and lines,
    the function returns the the sentance in a format of a list of
    strings for each word so that it could be read easier.

    REQ: sentance is a string

    >>> format_msg("book.title\n,book.year,book.author\n")
    ['book.title', 'book.year', book.author']
    >>> format_msg("hello\n,s,how\n,you, doing?")
    ['hello', 's', 'how', 'you', 'doing?']
    '''
    # split each element in the message with a comma
    for element in sentance:
        # contain each splitted word in a list
        list_of_words = sentance.split(DELIMETER)

    formatted_list = []
    # clean up the words and strip the new line from each line if there
    # is one.
    for word in range(len(list_of_words)):
        messege = list_of_words[word].strip()
        # add the cleaned words into a new formatted list
        formatted_list.append(messege)

    return formatted_list


def read_table(file):
    '''(str) -> Table
    Reads the table in the file given in the parameter and returns a Table
    object.

    REQ: file should be a comma seperated file (csv format)

    >>> read_table("books.csv")
    <database.Table object at 0x01D723F0>
    >>> t = read_table("books.csv")
    >>> t.share_table()
    {'book.author': ['Douglas Hofstadter', 'Randall Munroe',
    'Randall Munroe', 'Andrew Hodges'], 'book.title': ['Godel Escher Bach',
    'What if?', 'Thing Explainer', 'Alan Turing: The Enigma'], 'book.year':
    ['1979', '2014', '2015', '2014']}
    '''
    # list for all the values in the columns
    values = []
    count = 0

    # open the file for reading and format and clean the first line to
    # put all the columns in a list.
    table_file = open(file, READING_FILE)
    columns = format_msg(table_file.readline())

    # create empty lists for each column in the table
    while (count < (len(columns))):
        values.append([])
        count += 1

    # format the rest of the lines in the file using the format_msg function
    for line in table_file:
        formatted_lines = format_msg(line)
        index = 0

        # go through each empty list and add the corresponding values in
        # them, so that each list contains the values under the same column.
        # do this only for lines that contain values, not empty lines.
        if (formatted_lines != ['']):
            for index in range(len(columns)):
                values[index].append(formatted_lines[index])
                index += 1

            table_dict = dict()
            # map each list of values to the columns with the same index for
            # ex, book.title will contain a list of the titles of books.
            for index in range(len(columns)):
                table_dict[columns[index]] = values[index]

    table = Table()
    table.save_to_table(table_dict)
    table_file.close()
    return table


def read_database():
    '''() -> Database
    Reads the database (i.e: all tables in their .csv files) in the directory.

    >>> read_database()
    <database.Database object at 0x01C32350>
    >>> d = read_database()
    >>> d.share_database()
    {'seinfeld-episodes': <database.Table object at 0x03644AB0>,
    'oscar-film': <database.Table object at 0x03644830>,
    'imdb': <database.Table object at 0x01D0DBF0>,
    'boxoffice': <database.Table object at 0x01D09770>}
    '''
    list_of_table_names = []
    # for each file in the database
    for file_name in file_list:
        # take the file names that contain the extension ".csv" and put
        # them into a list
        list_of_table_names += [file_name[:file_name.find(EXTENSION)]]

    # add each of the tables into the database and return a database
    # object representing all of the data in all of the csv files.
    return add_table_to_database(list_of_table_names)


def add_table_to_database(list_of_table_file_names):
    '''(list_of_str) -> Database
    Given a list of file names containing tables, this function returns
    a database object.

    >>> add_table_to_database(['books.csv', 'imdb.csv'])
    <database.Database object at 0x03BB2350>
    >>> add_table_to_database(['movies.csv', 'boxoffice.csv', 'imdb.csv'])
    <database.Database object at 0x010C00B0>
    '''
    # create a empty dictionary and database
    db = {}
    final_database = Database()

    # map each table name to a table object in the database for each table
    # name in the list of table file names.
    for name in range(len(list_of_table_file_names)):
        db[list_of_table_file_names[name]] = read_table(file_list[name])

    # save the dictionary to the database
    final_database.save_to_database(db)
    return final_database
