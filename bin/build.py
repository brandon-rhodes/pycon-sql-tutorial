#!/usr/bin/env python

import gzip
import shutil
import os
import sqlite3
from csv import DictReader

if __name__ == '__main__':
    db = sqlite3.connect('movie.db')

    db.execute('''
CREATE TABLE actors_and_titles (actor TEXT, title TEXT);
''')

    lines = iter(gzip.open('actors.list.gz'))
    while not next(lines).startswith('Name'):
        continue
    next(lines)   # skip the title underlines
    for line in lines:
        if line.startswith('-----------------------'):
            break
        if line == '\n':
            continue
        line = line.decode('latin-1')
        maybe_actor, title = line.split('\t', 1)
        if maybe_actor:
            actor = maybe_actor
        bi = title.find('[')
        if bi != -1:
            title = title[:bi]
        title = title.strip()
        #print (u'%s|%s' % (actor,title)).encode('utf-8')
        db.execute('INSERT INTO actors_and_titles VALUES'
                   ' (?, ?)', (actor, title))
