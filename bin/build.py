#!/usr/bin/env python

POSTGRES=False or True

import gzip
import os
import re
import sqlite3
import sys

if POSTGRES:
    import psycopg2

line_re = re.compile(r'''
    (?P<actor_name>[^\t]+)?
    \t+
    (?P<is_televsion>")?(?P<movie_title>[^"]+?)"?
    \ +\((?P<year>[\d?]{4})(/(?P<nth_movie_that_year>[IVX]+))?\)
    (\ +\{(?P<episode>[^}]+)\})?
    (\ *(
        \((?P<as>as\ [^)]+( \([IV]+\))?)\)\)?
      | \((?P<also_as>also\ as\ [^)]+)\)
      | \((?P<attached>attached)\)
      | \((?P<archive_footage>.*archive\ footage[^)]*)\)
      | \((?P<archive_sound>.*archive\ sound[^)]*)\)
      | (?P<bare_number>7|30)
      | (?P<compound_guard_number_3>Compound\ Guard\ \#3)
      | \((?P<credit_only>credit\ only[^)]*)\)
      | \((?P<from>from [^)]*)\)
      | (?P<hunter_number_2>Hunter\ \#2)
      | \((?P<in_talks>in\ talks|in\ negotiations)\)
      | \((?P<episode_details>(\d+\ )?episode[^)]*)\)
      | \((?P<made_for_video>V)\)
      | \((?P<rumored>rumored)\)
      | \((?P<scenes_deleted>scenes\ deleted)\)
      | \((?P<segment>segment [^)]*)\)
      | \((?P<singing_voice>singing\ voice[^)]*)\)
      | \((?P<song>song:? [^)]+)\)
      | \((?P<songs>songs?)\)
      | \{\{(?P<suspended>SUSPENDED)\}\}
      | \((?P<television>TV)\)
      | \((?P<unconfirmed>unconfirmed)\)
      | \((?P<uncredited>uncredited[^)]*)\)\ ?\)?
      | \((?P<videogame>VG)\)
      | \(?(?P<voice>voice[^)]*)\)
      | \(?(?P<voice2>;\ \(voice\))\)
      | \((?P<year_scenes>\d\d\d\d\ scenes)\)
      | \((?P<years>\d\d\d\d\ ?-?\ ?[?\d]?[?\d]?[?\d]?[?\d]?)\)
      | Chris
    ))*
    (\ +\[(?P<role>.+?)\] )?
    (\ +<(?P<rank>\d+)>)?
    \n$
    ''', re.X)

def import_actors(committer, db, filename, gender):

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

        m = line_re.match(line)
        if m is None:
            print 'Could not parse %r' % line
            continue

        g = m.groupdict()

        if g['actor_name']:
            actor = g['actor_name']

        if (g['archive_footage']
            or g['archive_sound']
            or g['credit_only']
            or g['episode']
            or g['in_talks']
            or g['is_televsion']
            or g['rumored']
            or g['scenes_deleted']
            or g['song']
            or g['songs']
            or g['suspended']
            or g['television']
            or g['unconfirmed']
            or g['uncredited']
            or g['videogame']
            ):
            continue

        nth = g['nth_movie_that_year'] or ''
        made_for_video = bool(g['made_for_video'])

        if POSTGRES:
            s = 'INSERT INTO actor_title_role VALUES (%s,%s,%s,%s,%s,%s,%s)'
            if g['year'] == '????':
                g['year'] = None
        else:
            s = 'INSERT INTO actor_title_role VALUES (?, ?, ?, ?, ?, ?, ?)'
        db.execute(s,
                   (actor, gender,
                    g['movie_title'], g['year'], nth, made_for_video,
                    g['role']))

    committer.commit()

if __name__ == '__main__':
    if POSTGRES:
        connection = psycopg2.connect('dbname=movie')
        db = connection.cursor()
    else:
        if os.path.exists('movie.db'):
            print 'Error: database already exists'
            sys.exit(1)
        connection = db = sqlite3.connect('movie.db')
    db.execute('''
CREATE TABLE actor_title_role (
    actor_name TEXT, gender TEXT,
    title TEXT, year INTEGER, nth TEXT, for_video BOOLEAN,
    role_name TEXT
);
''')
    import_actors(connection, db, 'cache/actors.list.gz', 'm')
    import_actors(connection, db, 'cache/actresses.list.gz', 'f')

    for cmd in '''

CREATE TABLE movie (
  id SERIAL, title TEXT, year INTEGER, nth TEXT, for_video BOOLEAN
  );
CREATE TABLE actor (
  id SERIAL, name TEXT, gender TEXT
  );
CREATE TABLE role (
  movie_id INTEGER, actor_id INTEGER, name TEXT
  );

INSERT INTO movie (title, year, nth, for_video)
  SELECT DISTINCT title, year, nth, for_video
    FROM actor_title_role;

INSERT INTO actor (name, gender)
  SELECT DISTINCT actor_name, gender
    FROM actor_title_role;

CREATE INDEX tmp1 ON movie (title, year);
CREATE INDEX tmp2 ON actor (name);

INSERT INTO role (movie_id, actor_id, name)
  SELECT movie.id, actor.id, role_name
    FROM actor_title_role
    JOIN movie ON (
      movie.title = actor_title_role.title AND
      movie.year = actor_title_role.year AND
      movie.nth = actor_title_role.nth
    )
    JOIN actor ON (
      actor.name = actor_title_role.actor_name AND
      actor.gender = actor_title_role.gender
    );

DROP TABLE actor_title_role;
DROP INDEX tmp1;
DROP INDEX tmp2;

VACUUM;

'''.split(';'):
        db.execute(cmd)
        connection.commit()

# CREATE INDEX role_unique ON role (role, movie_id, actor_id);
# TODO: why is there a movie from year 7? Fix my RE.
