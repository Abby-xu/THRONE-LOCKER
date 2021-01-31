'''
Author: Abby
Date: 2021-01-30 18:46:31
LastEditTime: 2021-01-31 05:55:32
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /Hackathon/an_app/main.py
'''

import time
import kivy
import webbrowser
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Line, Color
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.relativelayout import RelativeLayout  
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.storage.jsonstore import JsonStore
from kivy.properties import NumericProperty
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from multiprocessing.pool import ThreadPool


class LoginErrorPopup(Popup):
    def __init__(self, msg: str, **kw):
        self.msg = msg
        self.title = 'Login Error'
        self.size_hint = (.5, .5)
        super().__init__(**kw)
        self.open()


class LoginForm(BoxLayout):
    username = StringProperty()
    password = StringProperty()
    # remember_me = BooleanProperty(False)
    def website_function(self):
        webbrowser.open('https://www.aa.com/travelInformation/flights/status')


    def __init__(self, on_success, on_error, **kw):
        self.on_success = on_success
        self.on_error = on_error
        super().__init__(**kw)
        self.load_login_info()

    def load_login_info(self):
        if app.store.exists('login'):
            self.username = app.store.get('login')['username']
            self.password = app.store.get('login')['password']
            # self.remember_me = app.store.get('login')['rememberMe']
            self.ids['usernameField'].text = self.username
            self.ids['passwordField'].text = self.password
            # self.ids['rememberMe'].active = self.remember_me

    def submit(self, username: str, password: str):
        self._block_inputs()
        self.username, self.password = username, password

        # if self.remember_me:
        #     self.save_login_info()
        if app.store.exists('login'):
            app.store.clear()

        pool = ThreadPool(processes=1)
        pool.apply_async(self.do_login, callback=self._on_success, error_callback=self._on_error)

    def shop_submit(self):
        time.sleep(1)
        app.root.current = 'Shop'

    def aircraft_function(self):
        app.root.current = 'Aircraft'

    def save_login_info(self):
        app.store.put('login', username=self.username, password=self.password) 
        # rememberMe=self.remember_me

    def do_login(self):
        time.sleep(2)
        #print(self.username, self.password, self.remember_me)

    def _block_inputs(self):
        self.ids['submit'].text = 'Loading...'
        #self.ids['submit'].disabled = self.ids['rememberMe'].disabled = True
        self.ids['usernameField'].disabled = self.ids['passwordField'].disabled = True

    def _unblock_inputs(self):
        self.ids['submit'].text = 'Submit'
        #self.ids['submit'].disabled = self.ids['rememberMe'].disabled = False
        self.ids['usernameField'].disabled = self.ids['passwordField'].disabled = False

    def _on_success(self, e):
        self._unblock_inputs()
        self.on_success(e)

    def _on_error(self, e):
        self._unblock_inputs()
        self.on_error(e)

    @classmethod
    def on_success(cls, e):
        pass

    @classmethod
    def on_error(cls, e):
        pass


class SuccessScreen(Screen):
    pass

class Shop_Screen(Screen):
    pass

class Aircraft_Screen(Screen):
    pass

class Reserved_Screen(Screen):
    pass

class Take_Screen(Screen):
    pass

class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(LoginForm(on_success=self.success, on_error=self.display_error))

    @classmethod
    def success(cls, e):
        app.manager.current = 'success'

    @classmethod
    def display_error(cls, e):
        LoginErrorPopup(msg='Unable to login at this time.')



class AAApp(App):

    store = ObjectProperty(JsonStore('storage.json'))
    manager = ObjectProperty(ScreenManager())

    def build(self):
        # Config.set('graphics', 'width', '600')
        # Config.set('graphics', 'height', '900')
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (600, 900)
        img = Image(source = 'a.png')
        # self.draw_canvas_widget = DrawCanvasWidget()
        self.manager.add_widget(LoginScreen(name='login'))
        self.manager.add_widget(SuccessScreen(name='success'))
        self.manager.add_widget(Shop_Screen(name="Shop"))
        self.manager.add_widget(Aircraft_Screen(name='Aircraft'))
        self.manager.add_widget(Reserved_Screen(name='Reserved'))
        self.manager.add_widget(Take_Screen(name='Take'))
        
        # return AAPage()
        return self.manager


if __name__ == '__main__':

    app = AAApp()
    app.run()