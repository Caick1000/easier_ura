# KIVY imports
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout

# Misc imports
from modules import header, body, footer
from datetime import datetime

current_date = datetime.now().strftime("%Y/%m/%d")


# Function to check if a parameter is wrong or empty
def validations(gender, context, path, custom_path, debug, ip):
    gender = 'f' if gender == 'Female' else 'm' if gender == 'Male' else 'f'
    context = 'missing_context' if context == '' else context
    path = 'global/{}'.format(gender) if path == '' else path
    custom_path = path if custom_path == '' else custom_path
    debug = '0' if debug == False else '1'
    ip = 'missing_ip' if ip == '' else ip

    if custom_path[:-1] == '/' or custom_path[:-1] == '\\':
        custom_path = custom_path[:-1]

    if custom_path[0:] == '/' or custom_path[0:] == '\\':
        custom_path = custom_path[0:]

    if path[:-1] == '/' or path[:-1] == '\\':
        path = path[:-1]

    if path[0:] == '/' or path[0:] == '\\':
        path = path[0:]

    return(gender, context, path, custom_path, debug, ip)


class CreateUra(GridLayout):

    def clear_inputs(self, *args):
        for item in args:
            item = ''

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

        with open(str(ura_file_name) + '.conf', 'w+') as f:
            f.write(str(ura_header) + '\n')
    


class UraApp(App):

    def build(self):
        return CreateUra()

if __name__ == "__main__":
    UraApp().run()
