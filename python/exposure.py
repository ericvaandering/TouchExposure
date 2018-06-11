#! /usr/bin/env/python3

"""
The class implementing the various exposure functions
"""

from __future__ import print_function

import math

# The set of classic f-stops in full, half, and third stops
F_STOPS = {
    1: [0.7, 1.0, 1.4, 2, 2.8, 4, 5.6, 8, 11, 16, 22, 32, 45, 64, 90],
    2: [0.7, 0.8, 1.0, 1.2, 1.4, 1.7, 2, 2.4, 2.8, 3.3, 4, 4.8, 5.6, 6.7, 8, 9.5, 11, 13, 16, 19,
        22, 27, 32, 38, 45, 54, 64, 76, 90],
    3: [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.5, 2.8, 3.2, 3.5, 4, 4.5, 5.0, 5.6,
        6.3, 7.1, 8, 9, 10, 11, 13, 14, 16, 18, 20, 22, 25, 29, 32, 36, 40, 45, 51, 57, 64, 72, 80,
        90],
}

SHUTTERS = {
    1: [1 / t for t in [8000, 4000, 2000, 1000, 500, 250, 125, 60, 30, 15, 8, 4, 2]]
       + [1, 2, 4, 8, 15, 30, 60],
    3: [1 / t for t in [8000, 6400, 5000, 4000, 3200, 2500, 2000, 1600, 1250, 1000, 800, 640, 500,
                        400, 320, 250, 200, 160, 125, 100, 80, 60, 50, 40, 30, 25, 20, 15, 13, 10,
                        8, 6, 5, 4, 3, 2.5, 2, 1.6, 1.25]]
       + [1, 1.3, 1.6, 2, 2.5, 3.2, 4, 5, 6, 8, 10, 13, 15, 20, 25, 30, 40, 50, 60],
}


class Exposure:
    """
    The class implementing the various exposure functions
    """

    def __init__(self,
                 min_f=F_STOPS[1][0], max_f=F_STOPS[1][-1], step_f=3,
                 min_t=SHUTTERS[1][0], max_t=SHUTTERS[1][-1], step_t=3,
                 ):
        """
        Init
        """

        self.min_f = min_f
        self.max_f = max_f
        self.step_f = step_f

        self.min_t = min_t
        self.max_t = max_t
        self.step_t = step_t

        self.bias = None

        self.f = 8
        self.t = 1 / 100
        self.iso = 100
        self.lv = 0

    def calcluate_lv(self):
        self.lv = math.log(self.f * self.f / self.t, 2) + math.log(self.iso / 100, 2)

    def x_to_fstop(self, x):
        """
        Convert 0 < x < 1 into a classic f-stop value
        """
        print('x to fstop called')
        min_value = math.log(self.min_f, 2)
        max_value = math.log(self.max_f, 2)
        steps = round(2 * (max_value - min_value) * self.step_f)

        # Which f stops are valid for the list? Quantize x.
        valid_f = [f for f in F_STOPS[self.step_f] if self.max_f >= f >= self.min_f]
        x = round(x * steps) / steps

        self.f = math.pow(2, (max_value - min_value) * x + min_value)
        # self.calcluate_lv()

        display_f = min(valid_f, key=lambda test: abs(test - self.f))

        return str(display_f), self.f

    def fstop_to_x(self, f):
        """
        Convert shutter t into 0 < x < 1
        """

        min_value = math.log(self.min_f, 2)
        max_value = math.log(self.max_f, 2)

        if f < self.min_f:
            return 0
        if f > self.max_f:
            return 1
        x = (math.log(f, 2) - min_value) / (max_value - min_value)
        return x

    def x_to_shutter(self, x):
        """
        Convert 0 < x < 1 into a classic shutter speed value
        """
        print('x to shutter called')

        min_value = math.log(self.min_t, 2)
        max_value = math.log(self.max_t, 2)
        steps = round((max_value - min_value) * self.step_t)

        # Which shutter values are valid for the list? Quantize x.
        valid_t = [t for t in SHUTTERS[self.step_t] if self.max_t >= t >= self.min_t]
        x = round(x * steps) / steps

        self.t = math.pow(2, (max_value - min_value) * x + min_value)
        # self.calcluate_lv()

        best_off_by = 1e9
        closest_t = None
        for test_t in valid_t:
            off_by = abs(test_t - self.t) / test_t
            if off_by < best_off_by:
                best_off_by = off_by
                closest_t = test_t

        if closest_t <= 0.5:
            return f'1/{int(1/closest_t)}', self.t
        elif closest_t < 4:
            return f'{closest_t: .1f}', self.t
        else:
            return f'{int(closest_t)}', self.t

    def get_display_t(self):
        valid_t = [t for t in SHUTTERS[self.step_t] if self.max_t >= t >= self.min_t]

        best_off_by = 1e9
        closest_t = None
        for test_t in valid_t:
            off_by = abs(test_t - self.t) / test_t
            if off_by < best_off_by:
                best_off_by = off_by
                closest_t = test_t

        if closest_t <= 0.5:
            return f'1/{int(1/closest_t)}'
        elif closest_t < 4:
            return f'{closest_t: .1f}'
        else:
            return f'{int(closest_t)}'

    def shutter_to_x(self, t):
        """
        Convert shutter t into 0 < x < 1
        """

        min_value = math.log(self.min_t, 2)
        max_value = math.log(self.max_t, 2)

        if t < self.min_t:
            return 0
        if t > self.max_t:
            return 1
        x = (math.log(t, 2) - min_value) / (max_value - min_value)
        return x

    def set_exposure(self, f=None, t=None, iso=None, bias=None):
        """
        Set the exposure and adjust other parameters
        :param f: New f-stop
        :param t: New shutter
        :param iso: New ISO value
        :param bias: New exposure bias
        :return: a 4-tuple of f, t, iso, and the bias
        """

        if f and t and iso and bias is not None:
            self.f = f
            self.t = t
            self.iso = iso
            self.bias = bias
            self.calcluate_lv()
            return (self.f, self.t, self.iso, self.bias)

        if f:
            self.f = f
            self.t = (self.iso * self.f * self.f) / (100 * pow(2, self.lv))
            return (self.f, self.t, self.iso, self.bias)

        if t:
            self.t = t
            self.f = math.sqrt(100 * self.t / self.iso * pow(2, self.lv))
            return (self.f, self.t, self.iso, self.bias)

    def ev_value(self):  # FIXME: Refactor
        return self.lv
