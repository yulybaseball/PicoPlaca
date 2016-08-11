"""
    Testing units for PREDICTOR
"""

import unittest

from predictor import PPpredictor

class Test_PPpredictor(unittest.TestCase):
    """ Tests for predictor.py """

    def setUp(self):
        self.predictor = PPpredictor()
        super(Test_PPpredictor, self).setUp()

    def test_day_of_week(self):
        """ Asserts _day_of_week method returns the good day. """
        # monday
        self.assertEqual(self.predictor._day_of_week('2002-10-14'), 0)
        # tuesday
        self.assertEqual(self.predictor._day_of_week('2006-04-25'), 1)
        # ... and so with another days...
        # not so important to test another days: _day_of_week method uses a
        # buit-in method...

    def test_not_valid_date(self):
        """ Asserts an exception is raised. """
        with self.assertRaises(Exception):
            self.assertEqual(self.predictor._day_of_week('2016-18-10'), 2)

    def test_plate_belongs2day(self):
        """ Asserts a plate's last digit is restricted in a given date. """
        self.assertTrue(self.predictor._plate_belongs2day('DFS982',
                                                          '2016-08-08'))

    def test_plate_doesnt_belong2day(self):
        """ Asserts a plate doesn't have the last number in correspondence with
        a given date. """
        self.assertFalse(self.predictor._plate_belongs2day('AAC-20',
                                                           '2016-08-10'))

    def test_plate_is_not_correct(self):
        """ Asserts plate is in a bad format: raises an exception. """
        with self.assertRaises(Exception):
            self.assertFalse(self.predictor._plate_belongs2day('SDJHH',
                                                               '2016-08-08'))
        with self.assertRaises(Exception):
            self.assertFalse(self.predictor._plate_belongs2day('',
                                                               '2016-08-08'))

    def test_date_is_not_correct(self):
        """ Asserts date is in a bad format: raises an exception. """
        with self.assertRaises(Exception):
            self.assertFalse(self.predictor._plate_belongs2day('SDJH8',
                                                               '2016-02-30'))
    def test_is_restricted_time(self):
        """ Asserts time is between restricted ones. """
        self.assertTrue(self.predictor._is_restricted_time('16:00'))
        self.assertTrue(self.predictor._is_restricted_time('09:29'))

    def test_is_not_restricted_time(self):
        """ Asserts given time is not restricted. """
        self.assertFalse(self.predictor._is_restricted_time('00:00'))
        self.assertFalse(self.predictor._is_restricted_time('23:59'))

    def test_is_permitted2circulate(self):
        """ Asserts a given plate is allowed to be on road in a given date and
        time. """
        self.assertTrue(self.predictor.permitted2circulate(
                                            'HGF-121', '2016-08-10', '12:00'))
        # restricted date, but no-restricted time
        self.assertTrue(self.predictor.permitted2circulate(
                                            'HGF-121', '2016-08-08', '12:00'))
        # restricted time, but no-restricted date
        self.assertTrue(self.predictor.permitted2circulate(
                                            'HGF-121', '2016-08-18', '16:00'))

    def test_is_not_permitted2circulate(self):
        """ Asserts a given plate is NOT allowed to be on road in a given
        date and time. """
        self.assertFalse(self.predictor.permitted2circulate(
                                            'HGF-125', '2016-08-10', '16:00'))

    def test_is_permitted2circulate_exception(self):
        """ Asserts an exception is raised when any of the parameters is not
        correct. """
        # Plate is not correct
        with self.assertRaises(Exception):
            self.assertFalse(self.predictor.permitted2circulate('SAXC',
                '2016-08-08', '16:00'))
        # Date is not correct
        with self.assertRaises(Exception):
            self.assertFalse(self.predictor.permitted2circulate('SAXC-9',
                '2016-18-08', '16:00'))

if __name__ == '__main__':
    unittest.main()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
