from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, NoTransition, CardTransition
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from workoutbanner import WorkoutBanner
from myfirbase import MyFirebase
from os import walk
from functools import partial
import requests
import json

class LabelButton(ButtonBehavior, Label):
    pass

class ImageButton(ButtonBehavior, Image):
    pass


class HomeScreen(Screen):
    pass

class SettingScreen(Screen):
    pass

class ChangeAvatarScreen(Screen):
    pass

class LoginScreen(Screen):
    pass


GUI = Builder.load_file('main.kv')
class MainApp(App):
    my_friend_id = 1
    def build(self):
        self.my_firebase = MyFirebase()
        return GUI

    def on_start(self):

         # populate avatar grid 
        avatar_grid = self.root.ids['change_avatar_screen'].ids['avatar_grid']
        for root_dir, folders, files in walk("icons/avatars/"):
            for f in files:
                img = ImageButton(source="icons/avatars/" + f, on_release=partial(self.change_avatar, f))
                avatar_grid.add_widget(img)

        try : 
            with open("refresh_token.txt", "r") as f:
                refresh_token = f.read()

            id_token, local_id =  self.my_firebase.exchange_refresh_token(refresh_token)


            # Get database to data
            result = requests.get("https://fitness-app-2c083.firebaseio.com/" + local_id + ".json?auth=" + id_token)
            # print("RESULT OK", result.ok)
            data = json.loads(result.content.decode())
            # print(data)
            avatar_image = self.root.ids['avatar_image']
            avatar_image.source = "icons/avatars/" + data['avatar']

            # now get and update steak labels
            steak_label = self.root.ids['home_screen'].ids['steak_label']
            steak_label.text  = str(data['steak']) + " day steaks."

            # Get and update Friend ID 
            friend_id_label = self.root.ids['setting_screen'].ids['friend_id_label']
            friend_id_label.text = "Friend ID : " + str(self.my_friend_id)

            banner_grid = self.root.ids['home_screen'].ids['banner_grid']
            workouts = data['workouts'] [1:]
            for workout in workouts:
                for i in range(5):
                    W = WorkoutBanner(workout_image=workout['workout_image'], description=workout['description'], type_image=workout['type_image'], number=workout['number'], units=workout['units'], likes=workout['likes']) 
                    banner_grid.add_widget(W)

                # print(workout['workout_image'])
                # print(workout['units'])
            self.root.ids['screen_manager'].transition = NoTransition()
            self.change_screen("home_screen")
            self.root.ids['screen_manager'].transition = CardTransition()

        except Exception as e:
            print(e)
            pass

    def change_avatar(self, image, widget_id):
        # change avatar image in app
        avatar_image = self.root.ids['avatar_image']
        avatar_image.source = "icons/avatars/" + image
        # change avatar image in firebase data
        my_data = '{"avatar" : "%s"}' % image
        requests.patch("https://fitness-app-2c083.firebaseio.com/" + str(self.my_friend_id) + ".json", data=my_data)
        
        self.change_screen("setting_screen")

        # populate workout grid in home
    def change_screen(self, screen_name):
        # get screen from kv file
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name
        

MainApp().run()