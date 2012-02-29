
========================
 SQL Tutorial Exercises
========================

:PyCon: 2012
:Place: Santa Clara, California
:By: Brandon Rhodes


| *Assumption #1: You know Python*
| *Assumption #2: You want to learn SQL*

------------------------------------------------------------------------

First Half
==========

1. Getting our feet wet
-----------------------

.. Introduce the idea of a table, using both the terminology
   “column/row” and of “record/field.”  Mention that migration is
   problematic.  Show them SELECT, SELECT-WHERE, SELECT-LIMIT, COUNT(),
   and the operators “=”, “LIKE”, “ILIKE”, “AND”, and “OR”.

a. In what year was “A Fist Full of Dollars” released?

b. How many movies were released in 1929 compared to 1930 and 1931?

c. How many movies have the word “Amazon” in their name?

d. 

e. 

2. what
-------

.. Now replace the “*” in SELECT with explicit field names.  Show that
   because we now get less information, running DISTINCT on the output
   gives us a smaller result set.  Contrast COUNT() with the DISTINCT
   qualified with COUNT(DISTINCT), using the 'm' and 'f' genders.

a. How many men have acted in movies?

b. … how many women?

c. 

d. In how many years has there been at least one movie released?

e. 

3. what
-------

Who were the actors in the movie 1972 movie “Sleuth”?

In how many movies has the famous Michael Caine acted?

Using a single query: Were more movies were released in
1928, 1929, or 1930?

Using a single query: What is one of the least common last names in Hollywood?

a. In what year was the first movie made?

b.

c. 

d. 

e. 

4. what
-------

a. 

b. 

c. 

d. 

e. 

5. what
-------

a. 

b. 

c. 

d. 

e. 

6. what
-------

a. 

b. 

c. 

d. 

e. 

7. what
-------

a. 

b. 

c. 

d. 

e. 

8. what
-------

a. 

b. 

c. 

d. 

e. 

9. what
-------

a. 

b. 

c. 

d. 

e. 

a. x
b. yu

------------------------------------------------------------------------

Second Half
===========

1. Getting our feet wet
-----------------------

a. 

b. 

c. 

d. 

e. 

2. what
-------

a. 

b. 

c. 

d. 

e. 

3. what
-------

a. 

b. 

c. 

d. 

e. 

4. what
-------

a. 

b. 

c. 

d. 

e. 

5. what
-------

a. 

b. 

c. 

d. 

e. 

6. what
-------

a. 

b. 

c. 

d. 

e. 

7. what
-------

a. 

b. 

c. 

d. 

e. 

8. what
-------

a. 

b. 

c. 

d. 

e. 

9. what
-------

a. 

b. 

c. 

d. 

e. 


1. The Basics
-------------

* CREATE TABLE
* DROP TABLE
* CRUD operations: insert, select, update, delete
* INSERT 
* SELECT *
* UPDATE
* DELETE
* SELECT … WHERE
* SELECT … ORDER BY
* Batching operations

2. Relational Algebra
---------------------

* SELECT … JOIN
* FOREIGN KEY
* PRIMARY KEY

3. Indexing
-----------

* DB-API
* CREATE INDEX
* DROP INDEX
* Speed of inserting with index vs creating index afterward

4. Transactions
---------------

* Consistency models
* BEGIN
* COMMIT
* ROLLBACK
* CREATE TEMPORARY TABLE

5. Aggregation
--------------

* HAVING
* GROUP BY
* OFFSET / LIMIT
* SELECT DISTINCT is like GROUP BY but lacks ability to compute SUM() etc

6. ORMs
-------

* Models
* Relations
* Lazy vs eager loading
* Units of work
