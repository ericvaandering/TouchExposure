#! /usr/bin/env/python3

"""
The class implementing the various exposure functions
"""

from __future__ import print_function

import math

# The set of classic f-stops in full, half, and third stops
F_STOPS = {
    1: [0.7, 1.0, 1.4, 2, 2.8, 4, 5.6, 8, 11, 16, 22, 32, 45, 64, 90],
    2: [0.7, 0.8, 1.0, 1.2, 1.4, 1.7, 2, 2.4, 2.8, 3.3, 4, 4.8, 5.6, 6.7, 8, 9.5, 11, 13, 16, 19, 22, 27, 32, 38, 45,
        54, 64, 76, 90],
    3: [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.5, 2.8, 3.2, 3.5, 4, 4.5, 5.0, 5.6, 6.3, 7.1, 8, 9, 10,
        11, 13, 14, 16, 18, 20, 22, 25, 29, 32, 36, 40, 45, 51, 57, 64, 72, 80, 90],
}

SHUTTERS = {
    1: {'frac': [8000, 4000, 2000, 1000, 500, 250, 125, 60, 30, 15, 8, 4, 2], 'whole': [1, 2, 4, 8, 15, 30, 60]},
    3: {'frac': [8000, 6400, 5000, 4000, 3200, 2500, 2000, 1600, 1250, 1000, 800, 640, 500, 400, 320, 250, 200, 160,
                 125, 100, 80, 60, 50, 40, 30, 25, 20, 15, 13, 10, 8, 6, 5, 4, 3, 2.5, 2, 1.6, 1.25],
        'whole': [1, 1.3, 1.6, 2, 2.5, 3.2, 4, 5, 6, 8, 10, 13, 15, 20, 25, 30, 40, 50, 60]},
}

class Exposure:
    """
    The class implementing the various exposure functions
    """

    def __init__(self, min_f=F_STOPS[1][0], max_f=F_STOPS[1][-1], step_f=3):
        """
        Init
        """

        self.min_f = min_f
        self.max_f = max_f
        self.step_f = step_f

        self.f = 8
        self.t = 1 / 100
        self.iso = 100
        self.lv = 0

    def f_stop(self, x):
        """
        Convert 0 < x < 1 into a classic f-stop value
        """

        fmin = math.log(self.min_f, 2)
        fmax = math.log(self.max_f, 2)
        steps = round(2 * (fmax - fmin) * self.step_f)

        # Which f stops are valid for the list
        valid_f = [f for f in F_STOPS[self.step_f] if self.max_f >= f >= self.min_f]
        x = round(x * steps) / steps

        self.f = math.pow(2, (fmax - fmin) * x + fmin)
        self.lv = math.log(self.f * self.f / self.t, 2) + math.log(self.iso / 100, 2)
        display_f = min(valid_f, key=lambda t: abs(t - self.f))

        return str(display_f)

    def ev_value(self):  # FIXME: Refactor
        return self.lv
