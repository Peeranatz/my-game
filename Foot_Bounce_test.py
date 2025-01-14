from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

# Screen dimensions
WIDTH, HEIGHT = 800, 600
Window.size = (WIDTH, HEIGHT)


class SoccerJuggleGame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = None
        self.selected_player = None
        self.score = 0

        # Background
        self.background = Image(
            source="bk_stadium.jpg",
            size_hint=(None, None),
            size=(WIDTH, HEIGHT),
            pos=(0, 0),
        )
        self.add_widget(self.background)


class SoccerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SoccerJuggleGame(name="Foot Bounce_game"))
        return sm


if __name__ == "__main__":
    SoccerApp().run()
