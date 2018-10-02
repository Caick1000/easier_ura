from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
Window.clearcolor = (0, 0.05, 0.1, 0)

from modules import header, body, footer
from datetime import datetime

current_date = datetime.now().strftime("%Y/%m/%d")

def validations(gender, context, path, custom_path, debug):
    if gender == 'Female':
        gender = 'f'

    elif gender == 'Male':
        gender = 'm'
        
    else: gender = 'f'

    if context == '':
        context = 'no_name'

    if path == '':
        path = 'global/{}'.format(gender)

    if custom_path == '':
        custom_path = path

    if debug == False:
        debug = '0'
    else:
        debug = '1'

    return(gender, context, path, custom_path, debug)

class CreateUra(GridLayout):

    def uraConfig(self):
        debug = self.ids.check_debug.active
        gender = self.ids.gender.text
        #ura_file_name = self.ids.ura_file_name.text
        context = self.ids.context_input.text
        ip = self.ids.ip_input.text
        path =self.ids.path_input.text
        custom_path = self.ids.custom_path_input.text

        
        # if self.ids.btn.text == 'Female':
        #     gender = 'f'
        # elif self.ids.btn.text == 'Male':
        #     gender = 'm'
        # else:
        #     gender = 'f'

        # if self.ids.check_debug.active:
        #     debug = 1

        gender, context, path, custom_path, debug = validations(gender, context, path, custom_path, debug)

        ura_header = header(context, ip, path, custom_path, gender)

        with open("ura_file_name" + '.conf', 'w+') as f:
            f.write(str(ura_header) + '\n')



class UraApp(App):

    def build(self):
        return CreateUra()

if __name__ == "__main__":
    UraApp().run()
