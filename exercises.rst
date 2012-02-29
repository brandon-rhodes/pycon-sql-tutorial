
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

.. Introduce the idea of a table with “.table” and “.schema”, using both
   the terminology “column/row” and “record/field.”  Mention that
   migration is problematic.  Show them SELECT, SELECT-WHERE, COUNT(*),
   LIMIT, and the operators “=”, “<>”, “[NOT] LIKE”, “[NOT] GLOB”,
   “AND”, and “OR”.

a. In what year was “Double Indemnity” released?

.. SELECT year FROM movie WHERE title = 'Double Indemnity';

b. How many movies were released in 1929?  What about 1930?  1931?

.. SELECT COUNT(*) FROM movie WHERE year = 1929;
   SELECT COUNT(*) FROM movie WHERE year = 1930;
   SELECT COUNT(*) FROM movie WHERE year = 1931;

c. How many movies ever have been released to theaters, and how many
   were instead released direct-to-video?

.. SELECT COUNT(*) FROM movie WHERE for_video = 0;
   SELECT COUNT(*) FROM movie WHERE for_video = 1;

d. … what, specifically, about movies with “Yoga” in their title?

.. SELECT COUNT(*) FROM movie WHERE title LIKE '%yoga%' AND for_video = 0;
   SELECT COUNT(*) FROM movie WHERE title LIKE '%yoga%' AND for_video = 1;

e. Draw a two-circle Venn diagram showing how many movies have the word
   “life” in their title and how many include the word “death.”

.. SELECT COUNT(*) FROM movie
     WHERE title LIKE '%life%' AND title LIKE '%death%';
   SELECT COUNT(*) FROM movie
     WHERE title NOT LIKE '%life%' AND title LIKE'%death%';
   SELECT COUNT(*) FROM movie
     WHERE title LIKE '%life%' AND title NOT LIKE '%death%';

2. Putting things well in order
-------------------------------

.. Show how ORDER BY can be used with table column names and with
   expressions.  Explain that SELECT and, thus, LIMIT is normally random
   in its delivery of rows, but that ORDER can make them stable, and
   thus make OFFSET interesting for paging through data.

a. What was the year that the very first movies were released, and what
   were their titles?

.. SELECT * FROM movie ORDER BY year ASC LIMIT 10;

b. What movie has the longest title ever?

.. SELECT * FROM movie ORDER BY LENGTH(title) DESC LIMIT 3;
   or, for clarity, and to lead into next topic:
   SELECT LENGTH(title), * FROM movie ORDER BY 1 DESC LIMIT 3;

c. ... which actor or actress?

.. SELECT * FROM actor ORDER BY LENGTH(name) DESC LIMIT 3;

d. Which movie(s), not counting movies whose titles start with
   punctuation, come first in alphabetical order, and which come last?

.. SELECT * FROM movie WHERE title GLOB 'A*' ORDER BY title ASC LIMIT 10;
   SELECT * FROM movie WHERE title GLOB 'Z*' ORDER BY title DESC LIMIT 10;
   SELECT * FROM movie WHERE title GLOB 'ZZ*' ORDER BY title DESC LIMIT 10;

e. If someone searched your movie database for movies with “gun” in
   their title and you displayed them in the order they were released,
   which movies would be on the second page of 10 results each?

.. SELECT * FROM movie WHERE title LIKE '%gun%'
   ORDER BY year LIMIT 10 OFFSET 10;

3. Making distinctions
----------------------

.. Now replace the “*” in SELECT with explicit field names.  Show that
   because we now get less information, running DISTINCT on the output
   gives us a smaller result set.

a. Create a query which, as a sanity check, outputs the two genders
   represented in the ``actor`` table.

.. SELECT DISTINCT gender FROM actor;

b. Which years in human history have seen at least one movie released?

.. SELECT DISTINCT year FROM movie;

c. Produce a list of role names, with each name appearing only once,
   that start with the word “Bystander.”

.. SELECT DISTINCT role FROM role WHERE role LIKE 'bystander%';

4. Counting groups
------------------

.. Introduce GROUP BY and show how it can produce multiple rows, all of
   which have a COUNT(*) summary.  Also show SUM().

a. Write a single query 

average length of film name in different decades?

most common movie name

c. What is the maximum number of movies to share a single name?

d. Following up on (3b): In how many years has there been at least one
   movie released?

e. Which character name is the most common out of all of the roles ever
   played in a movie?
   

4. Joining up
-------------

.. Show how JOIN lets you create an N×M table that combines two real
   tables, but how a WHERE clause can reduce the N×M to an interesting
   set of rows.  Note that field names can (and sometimes must) now be
   qualified with their table name.

a. Which movies have featured a character named “King Arthur”?

b. Which actors have played a character named “King Arthur”?

c. 

d. 

e. 

5. what
-------

.. But full N×M JOINs are rarely useful

In what year was the first movie made?

Who were the actors in the movie 1972 movie “Sleuth”?

In how many movies has the famous Michael Caine acted?

Using a single query: Were more movies were released in
1928, 1929, or 1930?

Using a single query: What is one of the least common last names in Hollywood?

How many movies share their name with at least one other movie?

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
* UPDATE
* DELETE
* Batching operations

2. Relational Algebra
---------------------

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
