#!/usr/bin/env python

import gzip
import sqlite3

def import_actors(filename):
    lines = iter(gzip.open(filename))
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
            bj = title.find(']')
            role = title[bi + 1:bj - 1]
            title = title[:bi]
        else:
            role = ''
        title = title.strip()
        if '{' in title:  # TV episode
            continue
        db.execute('INSERT INTO actor_title_role VALUES'
                   ' (?, ?, ?)', (actor, title, role))
    db.commit()

if __name__ == '__main__':
    db = sqlite3.connect('movie.db')
    db.execute('''
CREATE TABLE actor_title_role (actor TEXT, title TEXT, role TEXT);
''')
    import_actors('actors.list.gz')
    import_actors('actresses.list.gz')
#    db.execute('''
    ('''

CREATE TABLE movie (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT);
CREATE TABLE actor (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);
CREATE TABLE role (movie_id INTEGER, actor_id INTEGER, role TEXT);

INSERT INTO movie (title) SELECT title FROM actor_title_role;
INSERT INTO actor (name) SELECT actor FROM actor_title_role;

CREATE INDEX movie_id ON movie (id);
CREATE INDEX movie_title ON movie (title);

CREATE INDEX actor_id ON actor (id);
CREATE INDEX actor_name ON actor (name);

INSERT INTO role (movie_id, actor_id, role)
  SELECT movie.id, actor.id, role FROM actor_title_role
   JOIN movie USING (title)
   JOIN actor ON (actor.name = actor_title_role.actor);

''')
