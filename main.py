from kivy.config import Config
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 200)
Config.set('graphics', 'top', 100)

import os
import cv2
import sys
import kivy
import time
import numpy as np

from kivy.app import App
from kivy.lang import Builder
from kivymd.theming import ThemeManager
from kivy.clock import mainthread
from kivymd.tabs import MDTabbedPanel
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.properties import ObjectProperty, ListProperty
from kivymd.list import OneLineListItem
from kivymd.button import MDRaisedButton
from kivymd.selectioncontrols import MDSwitch, MDCheckbox
from kivymd.textfields import MDTextField
from kivymd.slider import MDSlider
from kivy.uix.screenmanager import Screen
from service_color_matching import ColorMatch
from kivymd.menu import MDMenuItem, MDDropdownMenu
from service_masks import squarePattern, sinusoidalPattern, paraboloidPattern,\
    reverseParaboloidPattern, pointParabolic, pointReverseParabolic,\
    pointLinear, pointSinusoidal, pointDamped

from screen_color_select import ScreenColorSelect


kivy.require('1.9.2')


class MainScreen(Screen):
    pass


class ImageApp(App):

    theme_cls = ThemeManager()

    def build(self):
            return Builder.load_file('main.kv')

    def on_start(self):
        pass


if __name__ == '__main__':
    ImageApp().run()