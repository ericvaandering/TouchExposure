#! /usr/bin/env python3

# ToughExposure


'''An exposure suggestor and calculator'''

from collections import deque

import ui
import clipboard
from console import hud_alert

from exposure import Exposure

exp = Exposure(2.0, 32.0)
last_adjusted = deque([None, None], maxlen=5)  # Initialize the list of last clicked switches with two items


def slider_toggle(sender):
    """
    The user has clicked a switch. Set the last two switches to have been clicked to on
    and enable the corresponding sliders. Disable the other sliders.
    :param sender: The switch object which was clicked
    :return:
    """
    v = sender.superview
    name = sender.name

    aperture_slider = v['slider1']
    shutter_slider = v['slider2']
    iso_slider = v['slider3']

    slider_map = {'iso_switch': iso_slider, 'aperture_switch': aperture_slider, 'shutter_switch': shutter_slider}

    if name != last_adjusted[-1]:  # Make sure the last two entries are unique
        last_adjusted.append(name)

    switches = {'iso_switch', 'aperture_switch', 'shutter_switch'}
    enabled_switches = {last_adjusted[-1], last_adjusted[-2]}

    for switch in switches:
        if switch in enabled_switches:
            v[switch].value = True
            enable_slider(slider_map[switch])
        else:
            v[switch].value = False
            disable_slider(slider_map[switch])


def enable_slider(slider):
    """
    Turn a slider back on (undo disable_slider)
    :param slider:
    :return:
    """
    slider.touch_enabled = True
    slider.alpha = 1
    slider.tint_color = None


def disable_slider(slider):
    """
    Disable a slider
    :param slider: the slider to disable
    :return:
    """

    # How gray and transparent we want the disabled controls
    GRAY = (0.5, 0.5, 0.5)
    ALPHA = 0.5

    slider.touch_enabled = False
    slider.alpha = ALPHA
    slider.tint_color = GRAY


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
