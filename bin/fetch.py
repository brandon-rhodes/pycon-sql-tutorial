#!/usr/bin/env python

import os
import shutil
from urllib2 import urlopen

base = 'http://www2.census.gov/econ/susb/data'
ftp = 'ftp://ftp.fu-berlin.de/pub/misc/movies/database/'

if __name__ == '__main__':
    for filename in 'actors.list.gz', 'actresses.list.gz', 'movies.list.gz':
        shutil.copyfileobj(
            urlopen(ftp + filename),
            open(filename, 'w'),
            )

if False:
    os.chdir(os.path.dirname(__file__))  # /bin directory
    os.chdir('..')                       # main directory
    if not os.path.isdir('cache'):
        os.mkdir('cache')
    for year in range(1998, 2010): #1998
        naic = 'naics' if 1998 < year < 2007 else '6digitnaics'
        name = 'us_state_%s_%s.txt' % (naic, year)
        print '%s/%s/%s' % (base, year, name)
        u = urlopen('%s/%s/%s' % (base, year, name))
        f = open('cache/%s' % name, 'w')
        shutil.copyfileobj(u, f)
        u.close()
        f.close()
