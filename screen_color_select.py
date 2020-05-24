import requests
import matplotlib
from bs4 import BeautifulSoup

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.selectioncontrols import MDSwitch, MDCheckbox
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty, DictProperty, ListProperty, StringProperty
from kivymd.textfields import MDTextField
from kivymd.snackbar import Snackbar
from kivymd.button import MDRaisedButton
from kivy.uix.gridlayout import GridLayout
from kivymd.dialog import MDDialog
from kivy.metrics import dp
from kivymd.label import MDLabel
from os import path as os_path
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.menu import MDDropdownMenu
from kivy.network.urlrequest import UrlRequest
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import NoTransition
from kivy.graphics.texture import Texture


COLOR_MAPPING = {
    'red': 0,
    'green': 1,
    'blue':2
}


Builder.load_string("""

<ScreenColorSelect>

    GridLayout:
        cols: 1
        rows: 4

        GridLayout:
            cols: 1
            size_hint: 1, None
            height: dp(200)

            AnchorLayout:
                center_x: True
                MDLabel:
                    size_hint: None, None
                    height: dp(30)
                    width: dp(250)
                    text: 'Load from Color Hunter Website'

            AnchorLayout:
                center_x: True

                GridLayout:
                    size_hint: None, None
                    size: dp(250), dp(50)
                    cols: 2

                    MDLabel:
                        text: 'Dull / Vibrant'

                    MDSwitch:
                        id: dull_palette
                        size_hint: None, None
                        size: dp(36), dp(48)
                        pos_hint: {'center_x': 0.75, 'center_y': 0.5}
                        active: True

            AnchorLayout:
                center_x: True
                MDTextField:
                    id: colorhunter_id
            
            AnchorLayout:
                center_x: True
                MDRaisedButton:
                    id: load_colorhunter
                    on_release: root.load_colorhunter(colorhunter_id.text, dull_palette.active)
                    text: 'Load Color Scheme'


        GridLayout:
            cols: 1
            size_hint: 1, None
            height: dp(100)

            GradientWidget:
                id: gradient_rect


        GridLayout:
            cols: 1
            size_hint: 1, 1

            MDTextField:
                id: palette_list_text
                multiline: True

            AnchorLayout:
                center_x: True
                MDRaisedButton:
                    id: reload_button
                    on_release: root.reload_button_release()
                    text: 'Reload'




        GridLayout:
            size_hint: 1, None
            rows: 1
            height: dp(50)


            AnchorLayout:
                center_x: True
                MDRaisedButton:
                    id: next_button
                    on_release: root.next_button_release()
                    text: 'Next'






""")


def hex_to_rgb(value, index):
    value = value.replace('#', '')
    value = value.upper()
    return ([int(value[i:i+2], 16) for i in (0, 2, 4)][index]) / 255.


class ScreenColorSelect(Screen):
    pass

    def next_button_release(self):

        print('Done')

    def load_colorhunter(self, colorhunter_id, dull_palette):

        if dull_palette:
            palette_type = 'vibrant0'
        else:
            palette_type = 'dull0'

        r = requests.get('http://www.colorhunter.com/palette/%s' % colorhunter_id)
        soup = BeautifulSoup(r.text, 'lxml')
        raw_color_list = soup.find_all('div', {'class': 'palettecolors', 'id': palette_type})[0].find_all('div', {'class': 'color'})


        list_colors = []
        for color_line in raw_color_list:
            list_colors.append(color_line.a['title'])

        color_string = ""
        for color_text in list_colors:
            color_string += color_text
            color_string += '\n'

        self.ids.palette_list_text.text = color_string

        self.load_list_colors(list_colors)
        
    def load_list_colors(self, list_colors):

        gradient_list = [[hex_to_rgb(list_color, i) for i in range(0,3)] for list_color in list_colors]

        self.ids.gradient_rect.update_gradient(gradient_list)

        cdict = {k: [(float(i) / float(len(list_colors) - 1.), hex_to_rgb(list_colors[i], v), hex_to_rgb(list_colors[i], v)) for i in range(0,len(list_colors))] for k, v in COLOR_MAPPING.items()}
        cmap = matplotlib.colors.LinearSegmentedColormap('cmap1', cdict, 256)

        palette = []
        for i in range(0,256):
            
            cmap_resp = cmap(i/255.0)
            palette = palette + list(cmap_resp[:3])

    def reload_button_release(self):

        list_colors = self.ids.palette_list_text.text.split('\n')
        if '' in list_colors:
            list_colors.remove('')
        self.load_list_colors(list_colors)


class GradientWidget(Widget):

    def __init__(self, **args):

        super(GradientWidget, self).__init__(**args)

        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(size=self.update_rect)
        self.bind(pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_gradient(self, color_list):
        self.texture = Texture.create(size=(len(color_list), 1), colorfmt='rgb')
        p = [y for x in color_list for y in x]
        p = [chr(int(v*255)) for v in p]
        
        buf = ''.join(p)
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.rect.texture = self.texture        
