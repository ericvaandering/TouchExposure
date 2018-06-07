#! /usr/bin/env python3

# ToughExposure


'''An exposure suggestor and calculator'''

import ui
import clipboard
from console import hud_alert
from exposure import Exposure

exp = Exposure(2.0, 32.0)


def slider_action(sender):
    # Get the root view:
    v = sender.superview
    # Get the sliders:
    f_stop = v['slider1'].value
    seconds = v['slider2'].value
    iso_setting = v['slider3'].value



    f = exp.f_stop(f_stop)
    # Update the text from the new values
    v['label1'].text = f'f/{f} {int(seconds * 255)}s ISO {int(iso_setting * 255)} EV={exp.ev_value():4.1f}'


v = ui.load_view('ToughExposure')
slider_action(v['slider1'])
if ui.get_screen_size()[1] >= 768:
    # iPad
    v.present('sheet')
else:
    # iPhone
    v.present()
