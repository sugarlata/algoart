from kivy.config import Config
Config.set('graphics', 'position', 'custom')

import os
import cv2
import sys
import kivy
import numpy as np

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
from service_color_matching import ColorMatch


kivy.require('1.9.2')


class ScreenImage(Image):

    img = ObjectProperty()
    image_fn = ''

    def __init__(self, **kwargs):
        super(ScreenImage, self).__init__(**kwargs)

    def load_image_np(self, img):
        self.img = img

    def load_image(self, fn):
        if self.image_fn == fn:
            return
        else:
            self.image_fn = fn

        self.img = cv2.imread(fn)

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
    select_color_model = None
    img_background = None
    sel_background = None
    fn_background = ''
    img_foreground = None
    hsv = False
    background_type = ''

    def on_enter(self, *args):

        self.load_models()

    def load_models(self):
        del self.color_models[:]
        self.color_models = os.listdir('model-images/')
        try:
            self.color_models.remove('.DS_Store')
        except:
            pass
        self.update_color_models()

    def update_color_models(self):
        for c in self.ids.list_color_models.children:
            self.ids.list_color_models.remove(c)

        for k in self.color_models:
            self.ids.list_color_models.add_widget(
                OneLineListItem(text=k, on_release=self.load_color_model)
            )

    def load_color_model(self, context):
        self.open_image(os.path.join('model-images', context.text))

    def open_image(self, fn):
        self.ids.mainImage.load_image(fn)

    def open_image_np(self, img):
        self.ids.mainImage.load_image_np(img)

    def reload_color_model(self, hsv, pix_blob_limit):
        try:
            int(pix_blob_limit)
        except:
            print "Couldn't get pix blob limit - not int"
            return
        print "Please wait, creating color model"
        self.select_color_model = ColorMatch()
        self.select_color_model.create_model(hsv, int(pix_blob_limit))
        print "Finished"

    def save_color_model_file(self, fn):
        if fn == '':
            print 'Need a filename'
            return

        if self.select_color_model is None:
            print 'There is no model to save'
        else:
            print 'Saving Color Model'
            fn = '%s.npy' % fn
            self.select_color_model.save_model(os.path.join('color-models', fn))
            print 'Saved'

    def load_color_model_file(self, fn):
        if fn == '':
            print 'Need a filename'
            return

        self.select_color_model = None
        self.select_color_model = ColorMatch()

        print 'Loading Color Model'
        fn = '%s.npy' % fn
        try:
            self.select_color_model.load_model(os.path.join('color-models', fn))
        except Exception as e:
            print 'There was an error'
            print e
            return
        print 'Loaded'

    def load_background_image(self, fn, hsv):
        if fn == '':
            print "Need to input a Filename"
            return

        if self.select_color_model is None:
            print "Please select a color model first"
            return

        self.fn_background = str(os.path.join('raw-images', fn))
        try:
            self.open_image(self.fn_background)
        except Exception as e:
            print "Issue loading image"
            print e
            return

        try:
            self.img_background = None
            img_background = cv2.imread(self.fn_background)

            if hsv:
                print 'Loading HSV'
                self.img_background = cv2.cvtColor(img_background, cv2.COLOR_BGR2HSV)
                self.hsv = True
            else:
                print 'Loading BGR'
                self.img_background = img_background
                self.hsv = False

        except Exception as e:
            print "There was an error loading image into OpenCV"
            print e

    def change_background_type(self, context, value):
        if context.state == 'down':
            self.background_type = value
        else:
            self.background_type = ''

    def background_ok_click(self):
        if self.background_type == '':
            print 'Please select a background type'
            return

        if self.img_background is None:
            print "Please select a background image first"
            return

        shape = self.img_background.shape

        if self.background_type == 'white':
            self.sel_background = None
            self.sel_background = np.copy(self.img_background)
            self.sel_background[:, :, :] = 255
            self.open_image_np(self.sel_background)

        if self.background_type == 'black':
            self.sel_background = None
            self.sel_background = np.copy(self.img_background)
            self.sel_background[:, :, :] = 0
            self.open_image_np(self.sel_background)

        if self.background_type == 'picture':
            self.sel_background = None
            self.sel_background = np.copy(self.img_background)
            self.open_image_np(self.sel_background)




class ImageApp(App):

    theme_cls = ThemeManager()

    def build(self):
        return Builder.load_file('kivy_app.kv')

    def on_start(self):
        self.root.on_enter()


if __name__ == "__main__":
    ImageApp().run()

