# KIVY imports
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, ScreenManagerException
from kivy.properties import StringProperty

# Mysc imports
from modules import localizacao
from validations import validations
from datetime import datetime

#Color of the window
Window.clearcolor = (0, 0.05, 0.1, 0)



class Localizacao(Screen):
    button_text = StringProperty('Gender')

    def __init__(self, **kwargs):
        super(Localizacao, self).__init__(**kwargs)
        self.dropdown = CustomDropDown(self)


    def uraConfig(self):
        debug = self.ids.check_debug.active
        gender = self.ids.gender.text
        ura_file_name = self.ids.ura_file_name.text
        context = self.ids.context_input.text
        ip = self.ids.ip_input.text
        path =self.ids.path_input.text
        custom_path = self.ids.custom_path_input.text

        gender, context, path, custom_path, debug, ip, ura_file_name = validations(gender, context, path, custom_path, debug, ip, ura_file_name)

        ura_header = localizacao(context, ip, path, custom_path, gender, debug)

        with open(ura_file_name + '.conf', 'w+') as f:
            f.write(ura_header + '\n')



class Preventiva(Screen):
    button_text = StringProperty('Gender')

    def __init__(self, **kwargs):
        super(Preventiva, self).__init__(**kwargs)
        self.dropdown = CustomDropDown(self)


    def uraConfig(self):
        debug = self.ids.check_debug.active
        gender = self.ids.gender.text
        ura_file_name = self.ids.ura_file_name.text
        context = self.ids.context_input.text
        ip = self.ids.ip_input.text
        path =self.ids.path_input.text
        custom_path = self.ids.custom_path_input.text

        gender, context, path, custom_path, debug, ip, ura_file_name = validations(gender, context, path, custom_path, debug, ip, ura_file_name)

        ura_header = localizacao(context, ip, path, custom_path, gender, debug)

        with open(ura_file_name + '.conf', 'w+') as f:
            f.write(ura_header + '\n')

class MenuScreen(Screen):
    type_ura = StringProperty(None)
    error_text = StringProperty('')

    def checkUraType(self):
        type_localizacao = self.ids.type_localizacao.active
        type_preventiva = self.ids.type_preventiva.active
        type_negociacao = self.ids.type_negociacao.active
        type_pesquisa = self.ids.type_pesquisa.active
        
        if (type_localizacao):
            self.type_ura = 'localizacao'
        elif(type_preventiva):
            self.type_ura = 'preventiva'
        elif(type_negociacao):
            self.type_ura = 'negociacao'
        elif(type_pesquisa):
            self.type_ura = 'pesquisa'
        else:
            self.type_ura = 'localizacao'



class CustomDropDown(DropDown):
    def __init__(self, genders, **kwargs):
        super(CustomDropDown, self).__init__(**kwargs)
        self.gender = genders


    def on_select(self, data):
        self.gender.button_text = data



class My_manager(ScreenManager):
    pass



class UraApp(App):
    def build(self):
        return My_manager()

    def clear_inputs(self, text_inputs):
        for text_input in text_inputs:
            text_input.text = ''

if __name__ == '__main__':
    UraApp().run()
