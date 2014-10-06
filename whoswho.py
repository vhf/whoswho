import json
import random
import sys
from hs_oauth import get_access_token, request

from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout


def process_cmd(cmd):
    if cmd == 'exit()':
        sys.exit()
    response = request(access_token, HS_BASE_URL + cmd)
    return json.dumps(response, indent=4)

HS_BASE_URL = 'https://www.hackerschool.com/api/v1'
access_token, refresh_token = get_access_token()


people = json.loads(process_cmd('/batches/14/people'))


class GuessScreen(GridLayout):
    def __init__(self, **kwargs):
        super(GuessScreen, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 4
        self.someone = self.get_someone()

        self.photo = AsyncImage(source=self.someone['image'])
        self.add_widget(self.photo)

        self.guess = TextInput(multiline=False, focus=True )
        self.guess.bind(on_text_validate=self.on_enter)
        self.add_widget(self.guess)

    def get_someone(self):
        n_people = random.randint(0,len(people)-1)
        return people[n_people]

    def on_enter(self, value):
        print "Now guessing: ", self.someone['first_name']
        if self.guess.text == self.someone['first_name']:
            print "Yay"
            self.someone = self.get_someone()
            self.photo.source = self.someone['image']
            self.guess.text = ""
        else:
            print 'Boooo'


class WhoswhoApp(App):
    def build(self):
        guess = GuessScreen()
        return guess

WhoswhoApp().run()
