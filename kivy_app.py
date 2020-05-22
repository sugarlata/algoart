from kivy.config import Config
Config.set('graphics', 'position', 'custom')

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


class FilterMenuItem(MDMenuItem):
    filter_object = None


class FilterListItem(OneLineListItem):
    filter_object = None


class MainScreen(Screen):
    color_models = []
    select_color_model = None
    img_background = None
    sel_background = None
    fn_background = ''
    img_foreground = None
    hsv = False
    background_type = ''
    selected_filter = ObjectProperty(None)
    filter_list = [
        {'viewclass': 'FilterMenuItem',
         'text': 'Square Pattern',
         'filter_object': squarePattern},
        {'viewclass': 'FilterMenuItem',
         'text': 'Sinusoidal Pattern',
         'filter_object': sinusoidalPattern},
        {'viewclass': 'FilterMenuItem',
         'text': 'Paraboloid Pattern',
         'filter_object': paraboloidPattern},
        {'viewclass': 'FilterMenuItem',
         'text': 'ReverseParaboloid Pattern',
         'filter_object': reverseParaboloidPattern},
        {'viewclass': 'FilterMenuItem',
         'text': 'Point Parabolic',
         'filter_object': pointParabolic},
        {'viewclass': 'FilterMenuItem',
         'text': 'Point Reverse Parabolic',
         'filter_object': pointReverseParabolic},
        {'viewclass': 'FilterMenuItem',
         'text': 'Point Linear',
         'filter_object': pointLinear},
        {'viewclass': 'FilterMenuItem',
         'text': 'Point Sinusoidal',
         'filter_object': pointSinusoidal},
        {'viewclass': 'FilterMenuItem',
         'text': 'Point Damped',
         'filter_object': pointDamped},

    ]
    selected_filter_list = ListProperty({})

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

        self.load_foreground_image(self.img_background)

    def load_foreground_image(self, img):

        # Change Contrast & Brightness
        if self.ids.brightness_level.text != '':
            try:
                value = int(self.ids.brightness_level.text)
                img_bright = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
                img_bright[:, :, 2] += value
                img = cv2.cvtColor(img_bright.astype(np.uint8), cv2.COLOR_HSV2BGR)
            except Exception as e:
                print 'Could not change brightness'
                print e

        if self.ids.contrast_switch.active:
            try:
                img_contrast = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
                img_contrast[:, :, 0] = cv2.equalizeHist(img_contrast[:, :, 0])
                img = cv2.cvtColor(img_contrast, cv2.COLOR_YUV2BGR)
            except:
                print 'Could not change contrast'

        # print
        # print 'Cartoonify Picture'
        # # 1) Edges
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray = cv2.medianBlur(gray, 5)
        # edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        #
        # # 2) Color
        # color = cv2.bilateralFilter(img, 9, 300, 300)
        #
        # # 3) Cartoon
        # img = cv2.bitwise_and(color, color, mask=edges)

        print
        print 'Beginning Remap Color'

        if self.hsv:
            img_orig = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        else:
            img_orig = img

        # Get list of colors
        print "Getting set of in image colors"

        unq_col = np.asarray(img_orig).reshape((img_orig.shape[0] * img_orig.shape[1], 3))

        print 'Colors:', unq_col.shape
        print "Remapping Colors..."
        col_index, color_array = self.select_color_model.match_color(unq_col)

        print 'Color Remapped'
        recolored_array = color_array[col_index[:]]
        recolored = recolored_array.reshape(img_orig.shape[0], img_orig.shape[1], img_orig.shape[2])

        if self.hsv:
            recolored = cv2.cvtColor(recolored, cv2.COLOR_HSV2BGR)

        self.img_foreground = recolored
        print 'Finished'

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

    def on_selected_filter_list(self, context, instance):

        for c in self.ids.list_filters.children:

            if c.filter_object not in self.selected_filter_list:
                self.ids.list_filters.remove_widget(c)

        for f in self.selected_filter_list:

            is_in = False
            for c in self.ids.list_filters.children:
                if c.filter_object is f:
                    is_in = True

            if not is_in:
                fo = FilterListItem(on_release=self.change_selected_filter)
                fo.filter_object = f
                fo.text = f.str_text
                self.ids.list_filters.add_widget(fo)

    def add_filter(self, filter_type):

        if self.img_background is None:
            print "Please select a background image first"
            return

        try:
            ft = filter_type()
            ft.shape = self.img_background.shape
            self.selected_filter_list.append(ft)
        except Exception as e:
            print "An error occurred add filter"
            print e

    def change_selected_filter(self, context):
        self.selected_filter = context.filter_object

    def disable_settings(self):

        self.ids.cut_before.disabled = True
        self.ids.tf_a.disabled = True
        self.ids.slider_a.disabled = True
        self.ids.tf_f.disabled = True
        self.ids.slider_f.disabled = True
        self.ids.tf_o.disabled = True
        self.ids.slider_o.disabled = True
        self.ids.tf_s.disabled = True
        self.ids.slider_s.disabled = True
        self.ids.tf_r.disabled = True
        self.ids.slider_r.disabled = True
        self.ids.tf_mode.disabled = True
        self.ids.tf_x.disabled = True
        self.ids.slider_x.disabled = True
        self.ids.tf_y.disabled = True
        self.ids.slider_y.disabled = True

    def on_selected_filter(self, context, instance):
        self.reset_settings()
        self.change_attrs_settings(instance.vars_allowed)
        self.load_settings(instance)

    def change_attrs_settings(self, vars_allowed):

        if vars_allowed['cut_before']:
            self.ids.cut_before.disabled = False
        else:
            self.ids.cut_before.disabled = True

        if vars_allowed['a']:
            self.ids.tf_a.disabled = False
        else:
            self.ids.tf_a.disabled = True

        if vars_allowed['f']:
            self.ids.tf_f.disabled = False
        else:
            self.ids.tf_f.disabled = True

        if vars_allowed['o']:
            self.ids.tf_o.disabled = False
        else:
            self.ids.tf_o.disabled = True

        if vars_allowed['s']:
            self.ids.tf_s.disabled = False
        else:
            self.ids.tf_s.disabled = True

        if vars_allowed['r']:
            self.ids.tf_r.disabled = False
        else:
            self.ids.tf_r.disabled = True

        if vars_allowed['mode']:
            self.ids.tf_mode.disabled = False
        else:
            self.ids.tf_mode.disabled = True

        if vars_allowed['x']:
            self.ids.tf_x.disabled = False
        else:
            self.ids.tf_x.disabled = True

        if vars_allowed['y']:
            self.ids.tf_y.disabled = False
        else:
            self.ids.tf_y.disabled = True

    def reset_settings(self):
        self.ids.tf_mode.text = ''
        self.ids.tf_a.text = ''
        self.ids.tf_f.text = ''
        self.ids.tf_o.text = ''
        self.ids.tf_s.text = ''
        self.ids.tf_x.text = ''
        self.ids.tf_y.text = ''
        self.ids.tf_r.text = ''
        self.ids.cut_before.active = False

    def load_settings(self, instance):

        instance.shape = self.img_background.shape

        try:
            self.ids.tf_mode.text = str(instance.mode)
        except:
            pass
        try:
            self.ids.tf_a.text = str(instance.a)
        except:
            pass

        try:
            self.ids.tf_f.text = str(instance.f)
        except:
            pass

        try:
            self.ids.tf_o.text = str(instance.o)
        except:
            pass

        try:
            self.ids.tf_s.text = str(instance.s)
        except:
            pass

        try:
            self.ids.tf_x.text = str(instance.x)
        except:
            pass

        try:
            self.ids.tf_y.text = str(instance.y)
        except:
            pass

        try:
            self.ids.tf_r.text = str(instance.r)
        except:
            pass

        try:
            self.ids.cut_before.active = instance.cut_before
        except:
            pass

    def remove_filter(self):
        try:
            widget_to_delete = None
            for i in range(len(self.selected_filter_list)):
                if self.selected_filter_list[i] == self.selected_filter:
                    widget_to_delete = self.selected_filter_list[i]

            if widget_to_delete is not None:
                self.selected_filter_list.remove(widget_to_delete)
        except Exception as e:
            print 'Could not remove filter'
            print e

    def foreground_enter(self):
        if self.img_foreground is not None:
            self.open_image_np(self.img_foreground)

    def change_mode_settings(self, instance, attr):

        value = instance.active
        setattr(self.selected_filter, attr, value)

    def change_cut_settings(self, instance, attr):

        try:
            value = str(instance.text)
        except:
            return

        if value not in ['reflect', 'constant', 'nearest', 'mirror', 'wrap']:
            print 'Please select correct setting'
            return

        if self.selected_filter is None:
            print "Please select a filter"
            return

        setattr(self.selected_filter, attr, value)

    def change_filter_settings(self, instance, attr):

        try:
            value = int(instance.text)
        except:
            return

        if self.selected_filter is None:
            print "Please select a filter"
            return

        setattr(self.selected_filter, attr, value)

    def compile_masks(self):

        mask_list = []

        for mask in self.selected_filter_list:

            mask.recalc()
            mask_list.append(mask.get_matrix())

        if len(mask_list) == 0:
            print 'Need to create a filter'
            return

        if len(mask_list) > 0:

            if self.ids.add_mult.active:
                # Multiply
                mask_matrix = np.ones(mask_list[0].shape)
                for mask in mask_list:
                    mask_matrix = np.multiply(mask_matrix, mask)

            else:
                # Add
                mask_matrix = np.zeros(mask_list[0].shape)
                for mask in mask_list:
                    mask_matrix = np.add(mask_matrix, mask)

                mask_mask = np.greater(mask_matrix, 1)
                mask_matrix = np.where(mask_mask, 1, mask_matrix)

        return mask_matrix

    def reload_filters(self):

        mask = self.compile_masks()

        # if self.background_type is None:
        #     self.background_type == 'picture'
        #
        # if self.background_type == '':
        #     self.background_type == 'picture'
        #
        # if self.background_type == 'picture':
        print 'Min', np.min(mask)
        print 'Max', np.max(mask)
        combine = np.multiply(mask.astype(np.float32), self.img_foreground.astype(np.float32)).astype(np.uint8)
        ## + np.multiply(1 - mask, self.img_background)

        print self.img_foreground.shape
        print combine[:,250]
        self.open_image_np(combine)
        # combine = np.multiply(stacked_mask, recolored) + np.multiply(1 - stacked_mask, bgr_img_orig)
        #
        # cv2.imwrite('recolored.png', combine)
        # # cv2.imshow('image', recolored)
        # # cv2.waitKey(0)
        # # cv2.destroyAllWindows()
        #
        # print "Finish"





class ImageApp(App):

    theme_cls = ThemeManager()

    def build(self):
        return Builder.load_file('kivy_app.kv')

    def on_start(self):
        self.root.on_enter()




if __name__ == "__main__":
    ImageApp().run()

