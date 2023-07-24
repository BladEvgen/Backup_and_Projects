from random import randint
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2

        self.lb1 = Label(text='Start number')
        self.add_widget(self.lb1)

        self.start_number = TextInput(multiline=False)
        self.add_widget(self.start_number)

        self.lb2 = Label(text='End number')
        self.add_widget(self.lb2)

        self.end_number = TextInput(multiline=False)
        self.add_widget(self.end_number)

        self.start = Button(text='Generate random number')
        self.start.background_color = (1, 1, 255, 1)
        self.start.bind(on_press=self.callback_start)
        self.add_widget(self.start)

        self.result_label = Label(text='', size_hint=(None, None))
        self.add_widget(self.result_label)

    def callback_start(self, instance):
        self.start.disabled = False
        start_number = int(self.start_number.text)
        end_number = int(self.end_number.text)
        random_number = randint(start_number, end_number)
        self.result_label.text = str(random_number)


class MyApp(App):
    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
