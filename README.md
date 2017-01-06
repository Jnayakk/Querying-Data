# Querying Data Project

## About
This python program accepts SQuEaL queries from the keyboard, runs them on a database, and outputs the results. For example, below is a table called movies. The table has four columns, one for the year, title, studio and lastly box office gross. Here, each row corresponds to a certain movie.

![table1](https://cloud.githubusercontent.com/assets/24378046/21708690/17691c94-d3a9-11e6-9c2a-b910e5f30f38.png)

Now, this program allows us to perform operations on these types of tables written in SQuEaL. For example considering the movies table (given above), We might be interested in only the names of the movies, so we might want a table with only the m.title column. We could express this in SQuEaL as:
select m.title from movies
and this would give us a table with just one column:

![table2](https://cloud.githubusercontent.com/assets/24378046/21708694/1aa5a814-d3a9-11e6-8948-96a39cadd72a.png)

Or maybe you want only the movie names and year (and not the studio or gross revenue). You'd express this as:
select m.title,m.year from movies
and you'd get a table with two columns, m.title and m.year:

![table3](https://cloud.githubusercontent.com/assets/24378046/21708698/1de346ee-d3a9-11e6-8894-ef78ba3924e8.png)

Additionally, many other operations such as joining two tables, acquiring the cartesian product of two tables and more can be done in this program.

## How the program works
### Part 1: Reading Tables and Databases
First, I created a class that can read tables and databases from any csv files. With this, given any csv file containing any tables or databases of information such as the movies table shown earlier, the class can read it and acquire all of the information from the csv file. 

### Part 2: Building Table and Database Objects
Next I implemented two classes in order to build table and database objects. A table, is represented as a dictionary where each key is the name of a column and each value is the list of items in that column from the top row to the bottom. For example, the movies dictionary would contain four key/value pairs. Here is one of them: the key is 'm.year' and the value is ['1997','2003','2010'], another would have the key 'm.title' mapped to the value ['Titanic','The Lord of the Rings: The Return of the King','Toy Story 3'].

A database can be represented as a dictionary where the keys are table names and the values are table objects.

This is important because it allows me to store all of the information read from csv files as table or database objects, which can later assist me in performing operations on these tables.

### Part 3: Running Queries
Lastly in order to run the queries, squeal.py was created so that it:
1. Reads the database in the current directory.
2. Reads SQuEaL queries from the keyboard until a blank line is entered.

## How this program is useful
The quantity and variety of data generated today requires that we have ways to organize that data and extract pieces of data that are currently of interest. For example, when searching for a certain product to buy online, there might be thousands of similar products however, you have ways of searching, sorting, and filtering that data to find the specific product you were looking for.

Websites like Amazon use databases to store vast amounts of data. They then make queries on that data in order to retrieve data for a variety of purposes. This project is just another example of how databases work in the real world. This python program understands and accepts a SQL-like language, or more specifically, SQuEaL queries from the keyboard, runs them on a database, and outputs the results.
