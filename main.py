
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from datetime import datetime
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
import speech_recognition as sr
from kivy.uix.image import Image
from kivy.uix.label import Label
import arabic_reshaper
import bidi.algorithm
from bidi.algorithm import get_display

Builder.load_file('main.kv')

class HomeScreen(Screen):
    def to_login_page(self):
        self.manager.current = "login_screen"

    def sign_up(self):
        self.manager.current = "sign_up_screen"

class LoginScreen(Screen):


    def sign_up(self):
        self.manager.current= "sign_up_screen"

    def login(self,uname, pword):
        # read the file
        with open("users.json") as file:
            users=json.load(file)
        if self.ids.username.text== "" or self.ids.password.text == "":
            self.ids.login_wrong.text = "You can't leave one or both of the fields empty"
        else:

            if uname in  users and users[uname]['password']== pword:
                self.manager.current= "speech_to_text"
            else:
                self.ids.login_wrong.text ="Wrong username or password"



class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def to_login_page(self):
        self.manager.current = "login_screen"
    def add_user(self, uname, pword):

        with open("users.json") as file:
            users = json.load(file)

        if self.ids.username.text == "" or self.ids.password.text == "":
            self.ids.signup_wrong.text = "You can't leave one or both of the fields empty"
        else:
            users[uname]={"username":uname, "password":pword ,"created": datetime.now().strftime("%Y-%m-%d %H %M %S")}
            if uname in users:
                self.ids.signup_wrong.text = "This username is already taken. Please choose another name"
            else:

                with open("users.json", "w") as file:
                    json.dump(users, file)
                    self.ids.signup_wrong.text = "Sign Up Successful!"



class SpeechToText(Screen):
    def logout(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    Status = StringProperty("Arabic")
    Status2 = StringProperty("English")
    Status3 = StringProperty("Microphone")
    Status4 = StringProperty("File")

    def arabicSelected(self):
        self.ids.arabic.state = 'down'

    def englishSelected(self):
        self.ids.english.state = 'down'

    def microSelected(self):
        self.ids.microphone.state = 'down'

    def fileSelected(self):
        self.ids.file.state = 'down'

    def startRecording(self, fileInput):
        #Arabic & Microphone
        if (self.ids.arabic.state == 'down') and (self.ids.microphone.state=='down'):
            self.ids.englishLabel.text=""
            self.ids.say.text =""

            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)

            # Speech recognition using Google SpeechRecognition
            try:
                self.ids.say.text = 'You said:'
                reshaped_text = arabic_reshaper.reshape(r.recognize_google(audio, language="ar-AR"))
                bidi_text = get_display(reshaped_text)
                self.ids.arabicLabel.text = bidi_text

            except sr.UnknownValueError:
                self.ids.englishLabel.text="Could not understand audio"
            except sr.RequestError as e:
                self.ids.englishLabel.text="Could not request results"
        else:
        #------------------------------------------------------------------------
        # English & Microphone
            if (self.ids.english.state == 'down') and (self.ids.microphone.state == 'down'):
                self.ids.arabicLabel.text =""
                self.ids.say.text = ""

                r = sr.Recognizer()
                with sr.Microphone() as source:
                    audio = r.listen(source)

            # Speech recognition using Google SpeechRecognition
                try:
                    self.ids.say.text = 'You said:'
                    self.ids.englishLabel.text = f'{r.recognize_google(audio)}'
                except sr.UnknownValueError:
                    self.ids.englishLabel.text = "Could not understand audio"
                except sr.RequestError as e:
                    self.ids.englishLabel.text = "Could not request results"
            else:
        # ------------------------------------------------------------------------
        # English & File
                if (self.ids.english.state == 'down') and (self.ids.file.state == 'down'):
                    self.ids.arabicLabel.text =""
                    self.ids.say.text = ""
                    r = sr.Recognizer()
                    AUDIO_FILE=(fileInput)
                    with sr.AudioFile(AUDIO_FILE) as source:
                        audio = r.listen(source)
                    try:
                        self.ids.say.text = 'You said:'
                        text = r.recognize_google(audio)
                        self.ids.englishLabel.text = text
                    except sr.UnknownValueError:
                        self.ids.englishLabel.text = "Could not understand audio"
                    except sr.RequestError as e:
                        self.ids.englishLabel.text = "Could not request results"
                else:
                    # ------------------------------------------------------------------------
                    # Arabic & File
                    if (self.ids.arabic.state == 'down') and (self.ids.file.state == 'down'):
                        self.ids.englishLabel.text=""
                        self.ids.say.text = ""
                        r = sr.Recognizer()
                        AUDIO_FILE = (fileInput)
                        with sr.AudioFile(AUDIO_FILE) as source:
                            audio = r.listen(source)
                        try:
                            self.ids.say.text = 'You said:'
                            reshaped_text = arabic_reshaper.reshape(r.recognize_google(audio, language="ar-AR"))
                            bidi_text = get_display(reshaped_text)
                            self.ids.arabicLabel.text=bidi_text

                        except sr.UnknownValueError:
                            self.ids.englishLabel.text = "Recognition could not understand audio"
                        except sr.RequestError as e:
                            self.ids.englishLabel.text = "Could not request results"
                    else:
                        self.ids.say.text = "You have to choose first!"



class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainApp().run()