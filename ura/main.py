# KIVY imports
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty

# Mysc imports
from modules import header, body, footer
from validations import validations
from datetime import datetime

#Color of the window
Window.clearcolor = (0, 0.05, 0.1, 0)



class CreateUra(GridLayout):
    button_text = StringProperty('Gender')

    def __init__(self, **kwargs):
        super(CreateUra, self).__init__(**kwargs)
        self.dropdown = CustomDropDown(self)

        
    def clear_inputs(self, text_inputs):
        for text_input in text_inputs:
            text_input.text = ''


    def uraConfig(self):
        debug = self.ids.check_debug.active
        gender = self.ids.gender.text
        ura_file_name = self.ids.ura_file_name.text
        context = self.ids.context_input.text
        ip = self.ids.ip_input.text
        path =self.ids.path_input.text
        custom_path = self.ids.custom_path_input.text
        bt_create = self.ids.bt_create.on_press

        gender, context, path, custom_path, debug, ip = validations(gender, context, path, custom_path, debug, ip)

        ura_header = header(context, ip, path, custom_path, gender)

        with open(ura_file_name + '.conf', 'w+') as f:
            f.write(ura_header + '\n')
    


class CustomDropDown(DropDown):
    def __init__(self, genders, **kwargs):
        super(CustomDropDown, self).__init__(**kwargs)
        self.gender = genders

    def on_select(self, data):
        self.gender.button_text = data


class UraApp(App):

    def build(self):
        return CreateUra()

if __name__ == "__main__":
    UraApp().run()
