#!/usr/bin/env python

import os
import shutil
from urllib2 import urlopen

ftp = 'ftp://ftp.fu-berlin.de/pub/misc/movies/database/'

if __name__ == '__main__':
    for filename in 'actors.list.gz', 'actresses.list.gz', 'movies.list.gz':
        shutil.copyfileobj(
            urlopen(ftp + filename),
            open(os.path.join('cache', filename), 'w'),
            )
