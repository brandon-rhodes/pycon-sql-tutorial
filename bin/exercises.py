#!/usr/bin/env python

from unittest import TestCase

class Case(TestCase):
    def runTest(self):
        pass

case = Case()

if __name__ == '__main__':
    import sqlite3
    db = sqlite3.connect('movie.db')
    c = db.cursor()
    with open('exercise1.sql') as f:
        command = f.read()
    c.execute(command)
    result = c.fetchall()
    # "How many movies are in the database?"
    case.assertEqual(result, [(530257,)])
