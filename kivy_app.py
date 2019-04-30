from kivy.config import Config
Config.set('graphics', 'position', 'custom')

import cv2
import sys
import kivy

from kivy.app import App
from kivy.lang import Builder
from kivymd.theming import ThemeManager
from kivy.clock import mainthread
from kivymd.tabs import MDTabbedPanel
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivymd.list import OneLineListItem
from kivymd.button import MDRaisedButton
from kivymd.selectioncontrols import MDSwitch, MDCheckbox
from kivymd.textfields import MDTextField
from kivymd.slider import MDSlider
from kivy.uix.screenmanager import Screen


kivy.require('1.9.2')


class ScreenImage(Image):

    img = ObjectProperty()

    def __init__(self, **kwargs):
        super(ScreenImage, self).__init__(**kwargs)

    def on_img(self, context, instance):
        self.update()

    def update(self):
        # convert it to texture
        buf1 = cv2.flip(self.img, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(
            size=(self.img.shape[1], self.img.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture


class MainScreen(Screen):
    color_models = []

    def update_color_models(self):
        for c in self.root_window.ids.list_color_models.children:
            self.root_window.ids.list_color_models.remove(c)

        for k in self.color_models:
            self.root_window.ids.list_color_models.add_widget(
                OneLineListItem(text=k)
            )


class ImageApp(App):

    theme_cls = ThemeManager()

    def build(self):
        return Builder.load_file('kivy_app.kv')

    def on_start(self):
        pass


if __name__ == "__main__":
    ImageApp().run()

