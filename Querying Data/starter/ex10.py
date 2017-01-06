from squeal import cartesian_product
from database import *
import unittest


class TestCartesianProduct(unittest.TestCase):

    def test_two_tables(self):
        self.table1 = {'book.title': ['The Maze Runner', 'Dusk']}
        self.table2 = {'book.year': ['2014', '2015']}
        t1 = Table()
        t2 = Table()
        t1.set_dict(self.table1)
        t2.set_dict(self.table2)
        self.res = cartesian_product(t1, t2)
        self._dict = self.res.get_dict()
        self.exp = {'book.title': ['The Maze Runner', 'The Maze Runner',
                    'Dusk', 'Dusk'], 'book.year': ['2014',
                    '2015', '2014', '2015']}
        self.assertTrue(self.res)

    def test_expected(self):
        self.table1 = {'book.title': ['The Maze Runner', 'Dusk']}
        self.table2 = {'book.year': ['2014', '2015']}
        t1 = Table()
        t2 = Table()
        t1.set_dict(self.table1)
        t2.set_dict(self.table2)
        self.res = cartesian_product(t1, t2)
        self._dict = self.res.get_dict()
        self.exp = {'book.title': ['The Maze Runner', 'The Maze Runner',
                    'Dusk', 'Dusk'], 'book.year': ['2014',
                    '2015', '2014', '2015']}
        self.assertEqual(self._dict, self.exp)

    def test_same(self):
        self.table1 = {'book.title': ['The Maze Runner', 'Dusk']}
        self.table2 = {'book.title': ['Dusk', 'The Maze Runner']}
        t1 = Table()
        t2 = Table()
        t1.set_dict(self.table1)
        t2.set_dict(self.table2)
        self.res = cartesian_product(t1, t2)
        self._dict = self.res.get_dict()
        self.exp = {'book.title': ['Dusk', 'The Maze Runner',
                    'Dusk', 'The Maze Runner']}
        self.assertEqual(self._dict, self.exp)

    def test_one(self):
        self.table1 = {'book.title': [2014, 2015]}
        self.table2 = {'book.year': []}
        t1 = Table()
        t2 = Table()
        t1.set_dict(self.table1)
        t2.set_dict(self.table2)
        self.res = cartesian_product(t1, t2)
        self._dict = self.res.get_dict()
        self.exp = {'book.title': [], 'book.year': []}
        self.assertEqual(self._dict, self.exp)

    def test_empty(self):
        self.table1 = {}
        self.table2 = {}
        t1 = Table()
        t2 = Table()
        t1.set_dict(self.table1)
        t2.set_dict(self.table2)
        self.res = cartesian_product(t1, t2)
        self._dict = self.res.get_dict()
        self.exp = {}
        self.assertFalse(self._dict, self.exp)

    def test_empty(self):
        self.table1 = {'y': ['', '', '']}
        self.table2 = {'b': ['', '', '', '', '']}
        t1 = Table()
        t2 = Table()
        t1.set_dict(self.table1)
        t2.set_dict(self.table2)
        self.res = cartesian_product(t1, t2)
        self._dict = self.res.get_dict()
        self.exp = {'y': ['', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', ''], 'b': ['', '', '', '', '', '', '',
                    '', '', '', '', '', '', '', '']}
        self.assertEqual(self._dict, self.exp)

    def test_two_tables_dicts(self):
        self.table1 = {'book.title': ['The Maze Runner', 'Dusk'],
                       'book.grade': ['A', 'A+']}
        self.table2 = {'book.year': ['2014', '2015', '1979'],
                       'book.age': ['24', '25', '18']}
        t1 = Table()
        t2 = Table()
        t1.set_dict(self.table1)
        t2.set_dict(self.table2)
        self.res = cartesian_product(t1, t2)
        self._dict = self.res.get_dict()
        self.exp = {'book.year': ['2014', '2015', '1979', '2014',
                    '2015', '1979'],
                    'book.title': ['The Maze Runner', 'The Maze Runner',
                                   'The Maze Runner', 'Dusk', 'Dusk', 'Dusk'],
                    'book.grade': ['A', 'A', 'A', 'A+', 'A+', 'A+'],
                    'book.age': ['24', '25', '18', '24', '25', '18']}
if __name__ == '__main__':
    unittest.main(exit=False)
