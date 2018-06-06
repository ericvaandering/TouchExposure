#! /usr/bin/env python3
"""
Test cases for the Exposure class
"""

import unittest
from unittest import TestCase

from exposure import Exposure


class TestExposure(TestCase):
    """
    Test cases for the Exposure class
    """

    def test_f_stop(self):
        """
        Test the f stop conversion function
        """

        exposure = Exposure(min_f=2, max_f=4)
        self.assertEquals(exposure.f_stop(0), '2')
        self.assertEquals(exposure.f_stop(0.5), '2.8')
        self.assertEquals(exposure.f_stop(1.0), '4')

        exposure = Exposure(min_f=2, max_f=5.6)

        self.assertEquals(exposure.f_stop(0), '2')
        self.assertEquals(exposure.f_stop(0.33), '2.8')
        self.assertEquals(exposure.f_stop(0.67), '4')
        self.assertEquals(exposure.f_stop(1.0), '5.6')


if __name__ == '__main__':
    unittest.main()
