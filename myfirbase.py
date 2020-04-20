import requests
import json
from kivy.app import App


class MyFirebase():
    wak = "AIzaSyBNJHHa0TXRRQSG0AwJ-yqVwDyATsUPtuY" # web api keys
    
    def sign_up(self, email, password):
        app = App.get_running_app()
        # send email and password to fire base 
        # and firebase return something like localId, authToken, refereshToken
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.wak
        signup_data = {"email" : email, "password" : password, "returnSecureToken" : True}
        sign_up_request = requests.post(signup_url, data=signup_data)
        # print(sign_up_request.ok)
        # print(sign_up_request.content.decode())
        sign_up_data = json.loads(sign_up_request.content.decode())

        if sign_up_request.ok == True:
            refresh_token = sign_up_data['refreshToken']
            localId = sign_up_data['localId']
            idToken = sign_up_data['idToken']
            
            # save refresh Token  to a file
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)

            # save localId in a main app class
            app.local_id = localId
            app.id_token = idToken

            # Get Friend ID 
            # Get Request on firebase to create next friend id 
            friend_get_req = requests.get("https://fitness-app-2c083.firebaseio.com/next_friend_id.json?auth=" + idToken)
            my_friend_id = friend_get_req.json()
            friend_patch_data = '{"next_friend_id" : %s}' % str(my_friend_id + 1)
            friend_patch_req = requests.patch("https://fitness-app-2c083.firebaseio.com/.json?auth=" + idToken, data=friend_patch_data)
            print(friend_get_req.json())

            # create new database in a firebase
            my_data = '{"avatar" : "staff.png", "friends" : "", "steak" : "", "workouts" : "", my_friend_id" : "%s" }' % my_friend_id
            requests.patch("https://fitness-app-2c083.firebaseio.com/" + localId + ".json?auth=" + idToken, data=my_data)

            app.change_screen("home_screen")

        if sign_up_request.ok == False:
            error_data = json.loads(sign_up_request.content.decode())
            error_message = error_data["error"]["message"]
            app.root.ids['login_screen'].ids['error_message'].text = error_message

        
        pass

    def exchange_refresh_token(self, refresh_token):
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.wak
        refresh_playload = '{"grant_type" : "refresh_token", "refresh_token" : "%s"}' % refresh_token
        refresh_req = requests.post(refresh_url, data=refresh_playload)
        # print("REFRESH OK", refresh_req.ok)
        # print(refresh_req.json())
        id_token = refresh_req.json()['id_token']
        local_id = refresh_req.json()['user_id']
        return id_token, local_id
