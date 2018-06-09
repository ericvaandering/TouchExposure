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

    def test_x_to_fstop(self):
        """
        Test the f stop conversion function
        """

        exposure = Exposure(min_f=2, max_f=4)
        self.assertEqual(exposure.x_to_fstop(0), '2')
        self.assertEqual(exposure.x_to_fstop(0.5), '2.8')
        self.assertEqual(exposure.x_to_fstop(1.0), '4')

        exposure = Exposure(min_f=2, max_f=5.6)
        self.assertEqual(exposure.x_to_fstop(0), '2')
        self.assertEqual(exposure.x_to_fstop(0.33), '2.8')
        self.assertEqual(exposure.x_to_fstop(0.67), '4')
        self.assertEqual(exposure.x_to_fstop(1.0), '5.6')

    def test_fstop_to_x(self):
        """
        Test the shutter speed to (0, 1) conversion function
        """

        # Can ony test to one place since stop values are not accurate

        exposure = Exposure(min_f=2, max_f=4)
        self.assertEqual(exposure.fstop_to_x(2), 0.0)
        self.assertEqual(exposure.fstop_to_x(4), 1.0)
        self.assertAlmostEqual(exposure.fstop_to_x(2.8), 0.5, 1)

        exposure = Exposure(min_f=2, max_f=5.6)
        self.assertAlmostEqual(exposure.fstop_to_x(2.8), 1 / 3, 1)
        self.assertAlmostEqual(exposure.fstop_to_x(4), 2 / 3, 1)

    def test_x_to_shutter(self):
        """
        Test the shutter speed conversion function
        """

        exposure = Exposure(min_t=1 / 500, max_t=1 / 125)
        self.assertEqual(exposure.x_to_shutter(0), '1/500')
        self.assertEqual(exposure.x_to_shutter(0.5), '1/250')
        self.assertEqual(exposure.x_to_shutter(1.0), '1/125')

        exposure = Exposure(min_t=1 / 1000, max_t=1 / 125)
        self.assertEqual(exposure.x_to_shutter(0), '1/1000')
        self.assertEqual(exposure.x_to_shutter(0.33), '1/500')
        self.assertEqual(exposure.x_to_shutter(0.67), '1/250')
        self.assertEqual(exposure.x_to_shutter(1.0), '1/125')

        exposure = Exposure()
        self.assertEqual(exposure.x_to_shutter(0), '1/8000')
        self.assertEqual(exposure.x_to_shutter(1.0), '60')

    def test_shutter_to_x(self):
        """
        Test the shutter speed to (0, 1) conversion function
        """

        exposure = Exposure(min_t=1 / 500, max_t=1 / 125)
        self.assertEqual(exposure.shutter_to_x(1 / 500), 0.0)
        self.assertEqual(exposure.shutter_to_x(1 / 125), 1.0)
        self.assertAlmostEqual(exposure.shutter_to_x(1 / 250), 0.5, 6)

        exposure = Exposure(min_t=1 / 1000, max_t=1 / 125)
        self.assertAlmostEqual(exposure.shutter_to_x(1 / 500), 1 / 3, 6)
        self.assertAlmostEqual(exposure.shutter_to_x(1 / 250), 2 / 3, 6)

        exposure = Exposure()
        self.assertEqual(exposure.shutter_to_x(1 / 8000), 0.0)
        self.assertEqual(exposure.shutter_to_x(60), 1.0)

    def test_set_exposure(self):
        """
        Test the function to set and change exposure
        """

        exposure = Exposure(min_t=1 / 500, max_t=1 / 125)
        (f, t, iso, bias) = exposure.set_exposure(4.0, 1 / 100, 100, 0)
        self.assertEqual(f, 4.0)
        self.assertEqual(t, 1 / 100)

        (f, t, iso, base) = exposure.set_exposure(f=5.6)
        self.assertAlmostEqual(t, 1 / 50, 1)

        (f, t, iso, base) = exposure.set_exposure(t=1 / 200)
        self.assertAlmostEqual(f, 2.8, 1)


if __name__ == '__main__':
    unittest.main()
