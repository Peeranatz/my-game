from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen


class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        # Background
        self.background = Image(
            source="main_bk_football.jpg",
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False,
        )
        layout.add_widget(self.background)

        # Start Button
        start_button = Button(
            text="Play",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        start_button.bind(on_release=self.start_game)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def start_game(self, instance):
        # Change to the SelectPlayerScreen
        self.manager.current = "select_player"


class SelectPlayerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Background for the player selection screen
        self.background = Image(
            source="selec_player_bk.jpg",
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False,
        )
        layout.add_widget(self.background)

        self.add_widget(layout)


class SoccerJuggleApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name="menu"))
        sm.add_widget(SelectPlayerScreen(name="select_player"))
        return sm


if __name__ == "__main__":
    SoccerJuggleApp().run()
