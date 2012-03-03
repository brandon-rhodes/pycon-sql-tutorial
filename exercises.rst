
=====================================
 First Steps: SQL Tutorial Exercises
=====================================

:PyCon: 2012
:Where: Santa Clara, California
:Who: Brandon Rhodes


| *Assumption #1: You know Python*
| *Assumption #2: You want to learn SQL*

------------------------------------------------------------------------

Learning the SELECT statement
=============================

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

d. … what about movies with “Yoga” in their title?

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
   which start with the word “Bystander.”

.. SELECT DISTINCT role FROM role WHERE role LIKE 'bystander%';

4. Counting groups
------------------

.. Introduce GROUP BY and show how it can produce multiple rows, all of
   which have a COUNT(*) summary.  Also show SUM().

a. Write a single query that shows how many men, and how many women,
   have ever had roles in film.

.. SELECT gender, count(*) FROM actor GROUP BY 1;

b. What was the average length of a film's name in 1905?  …in 1990?

.. SELECT sum(length(title)) / count(*) FROM movie
   WHERE year = 1990;

c. What is the most common movie name ever?

.. SELECT count(*), title FROM movie GROUP BY 2 ORDER BY 1 DESC LIMIT 10;

d. … character name ever?

.. SELECT count(*), role FROM role GROUP BY 2 ORDER BY 1 DESC LIMIT 10;

5. Joining up
-------------

.. Show how JOIN lets you create an N×M table that combines two real
   tables, but how a WHERE clause can reduce the N×M to an interesting
   set of rows.  Note that field names can (and, in real life, sometimes
   must) now be qualified with their table name.

a. Which movies have featured a character named “King Arthur”?

.. SELECT * FROM movie JOIN role ON (movie.id = movie_id)
   WHERE role = 'King Arthur';

b. Which actors have played a character named “King Arthur”?

.. SELECT * FROM actor JOIN role ON (actor.id = actor_id)
   WHERE role = 'King Arthur';

c. Which movie had the largest cast ever?

.. SELECT COUNT(*), title, movie.id
   FROM movie JOIN role ON (movie.id = movie_id)
   GROUP BY 2 ORDER BY 1 DESC LIMIT 10;

d. Which 12 actors hold the record for being credited in the most
   movies?

.. SELECT COUNT(*), name
   FROM actor JOIN role ON (actor.id = actor_id)
   WHERE role <> ''
   GROUP BY 2 ORDER BY 1 DESC LIMIT 10;

e. Which actors have most often reprised the same role, bringing it back
   in movie after movie?

.. SELECT count(*), name, role FROM actor
   JOIN role ON (actor.id = actor_id)
   WHERE role <> ''
   GROUP BY 2, 3 ORDER BY 1 DESC LIMIT 10;

6. What will you be having?
---------------------------

.. Explain, finally, how HAVING filters rows after aggregation has taken
.. place.  Show how an alias lets you name an aggregate column for
.. easier use in the HAVING clause.

a. Produce a list of actors who have played exactly 99 roles.

.. SELECT COUNT(*) AS role_count, actor_id, name
   FROM actor JOIN role ON (actor.id = actor_id)
   WHERE role <> ''
   GROUP BY 2, 3
   HAVING role_count = 99;

b. Produce a list of actors who have been in exactly 99 films.

.. SELECT COUNT(DISTINCT movie_id) AS movie_count,
     actor_id, name
   FROM actor
     JOIN role ON (actor.id = actor_id)
   WHERE role <> ''
   GROUP BY 2, 3
   HAVING movie_count = 99;

c. In which years was the average length of a film title greater than 20
   characters?

.. SELECT year, AVG(LENGTH(title)) AS average
   FROM movie GROUP BY 1 HAVING average > 20;

Further topics
--------------

| Subqueries
| Inserting and updating data
| Transactions

| *Break*

| Indexes and performance
| The DB-API and batch operations
| The SQLAlchemy ORM, and others

Quick Reference
===============

::

 Table                                       Result
 -----                                       ------

  row       x
  row      row      row -> row      row  ->  row A
  row       x
  row       x
  row      row      row -> row      row  ->  row B
  row      row      row /
  row       x
  row      row      row \
  row      row      row -> row       x
  row       x

          WHERE      GROUP BY      HAVING   ORDER BY


The chart above is designed to help you remember
the order in which the major operations of a SELECT take place.
The “paging” restrictions LIMIT and OFFSET occur last,
after all of the steps above have already taken place.

The SQL language supports several basic expressions.
Several that you will be using in this tutorial are::

 a + b, a - b, a * b, a / b, et cetera
 a = b, a < b, a > b, a <> b
 COUNT(), SUM()
 LENGTH(string)
 string [NOT] LIKE '%case insensitive pattern%'
 string [NOT] GLOB 'Case sensitive pattern*'
 cond1 AND cond2
 cond1 OR cond2

The basic CRUD (create, read, update, delete) operations are::

 1.  INSERT INTO table VALUES (a, b, ...);
     INSERT INTO table SELECT ...;
 2.  SELECT expr, expr, ... FROM table JOIN table ... WHERE ...;
 3.  UPDATE table SET field = value, ... WHERE ...;
 4.  DELETE FROM table WHERE ...;

.. 1. The Basics
.. -------------

.. * CREATE TABLE
.. * DROP TABLE
.. * CRUD operations: insert, select, update, delete
.. * INSERT
.. * UPDATE
.. * DELETE
.. * Batching operations

.. 2. Relational Algebra
.. ---------------------

.. * FOREIGN KEY
.. * PRIMARY KEY

.. 3. Indexing
.. -----------

.. * DB-API
.. * CREATE INDEX
.. * DROP INDEX
.. * Speed of inserting with index vs creating index afterward

.. 4. Transactions
.. ---------------

.. * Consistency models
.. * BEGIN
.. * COMMIT
.. * ROLLBACK
.. * CREATE TEMPORARY TABLE

.. 5. Aggregation
.. --------------

.. * HAVING
.. * GROUP BY
.. * OFFSET / LIMIT
.. * SELECT DISTINCT is like GROUP BY but lacks ability to compute SUM() etc

.. 6. ORMs
.. -------

.. * Models
.. * Relations
.. * Lazy vs eager loading
.. * Units of work
