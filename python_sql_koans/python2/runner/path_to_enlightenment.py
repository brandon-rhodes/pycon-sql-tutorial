#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The path to enlightenment starts with the following:

import unittest

#from koans.about_asserts import AboutAsserts
from koans.about_select import AboutSelect
from koans.about_where import AboutWhere
from koans.about_groupby import AboutGroupBy
from koans.about_having import AboutHaving
from koans.about_orderby import AboutOrderBy
from koans.about_select_sa import AboutSelectInSqlAlchemy
from koans.about_where_sa import AboutWhereInSqlAlchemy
from koans.about_groupby_sa import AboutGroupByInSqlAlchemy
from koans.about_having_sa import AboutHavingInSqlAlchemy
from koans.about_orderby_sa import AboutOrderByInSqlAlchemy



def koans():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    loader.sortTestMethodsUsing = None
    suite.addTests(loader.loadTestsFromTestCase(AboutAsserts))
    suite.addTests(loader.loadTestsFromTestCase(AboutSelect))
    suite.addTests(loader.loadTestsFromTestCase(AboutWhere))
    suite.addTests(loader.loadTestsFromTestCase(AboutHaving))
    suite.addTests(loader.loadTestsFromTestCase(AboutOrderBy))
    suite.addTests(loader.loadTestsFromTestCase(AboutGroupBy))
    suite.addTests(loader.loadTestsFromTestCase(AboutSelectInSqlAlchemy))
    suite.addTests(loader.loadTestsFromTestCase(AboutWhereInSqlAlchemy))
    suite.addTests(loader.loadTestsFromTestCase(AboutHavingInSqlAlchemy))
    suite.addTests(loader.loadTestsFromTestCase(AboutOrderByInSqlAlchemy))
    suite.addTests(loader.loadTestsFromTestCase(AboutGroupByInSqlAlchemy))

    return suite
