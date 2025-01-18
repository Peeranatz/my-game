from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen


class SelectPlayerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        # Bind window size to update positions
        Window.bind(size=self.on_window_resize)

        # Background
        self.background = Image(
            source="selec_player_bk.jpg",
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False,
        )
        self.layout.add_widget(self.background)

        # Title
        self.title = Label(
            text="Select Your Player", font_size="48sp", size_hint=(None, None)
        )
        self.layout.add_widget(self.title)

        # Player data setup
        self.player_data = {
            0: {
                "image": "Ronaldo-re.png",
                "name": "Ronaldo",
                "preview": "ronaldo-re.png",
            },
            1: {"image": "Messi-re.png", "name": "Messi", "preview": "messi-re.png"},
            2: {"image": "Mbape-re.png", "name": "Mbappe", "preview": "Mbape-re.png"},
            3: {
                "image": "Haaland-re.png",
                "name": "Haaland",
                "preview": "haaland-re.png",
            },
            4: {"image": "Bruno-re.png", "name": "Bruno", "preview": "bruno-re.png"},
            5: {"image": "Son-re.png", "name": "Son", "preview": "son-re.png"},
            6: {"image": "Salah-re.png", "name": "Salah", "preview": "salah-re.png"},
        }

        # Create containers for dynamic elements
        self.player_cards = []
        self.create_player_cards()

        self.add_widget(self.layout)

        # Initial update of positions
        self.on_window_resize(Window, Window.size)

    def create_player_cards(self):
        for i in range(7):
            card_container = FloatLayout(size_hint=(None, None))

            # Player preview image
            player_image = Image(
                source=self.player_data[i]["preview"], size_hint=(None, None)
            )

            # Player name label
            name_label = Label(
                text=self.player_data[i]["name"],
                font_size="16sp",
                size_hint=(None, None),
            )

            # Selection button
            select_button = Button(text="Select", size_hint=(None, None))
            select_button.bind(on_release=lambda btn, i=i: self.select_player(i))

            card_container.add_widget(player_image)
            card_container.add_widget(name_label)
            card_container.add_widget(select_button)

            self.player_cards.append(
                {
                    "container": card_container,
                    "image": player_image,
                    "label": name_label,
                    "button": select_button,
                }
            )
            self.layout.add_widget(card_container)

    def on_window_resize(self, instance, size):
        width, height = size

        # Update title position
        self.title.pos = (width * 0.5 - self.title.width * 0.5, height * 0.85)

        # Calculate card dimensions and spacing
        card_width = width * 0.12
        card_height = height * 0.3
        card_spacing = width * 0.02

        # Calculate starting position to center all cards
        total_width = (card_width + card_spacing) * 7 - card_spacing
        start_x = (width - total_width) / 2

        # Update each player card
        for i, card in enumerate(self.player_cards):
            # Container position
            x_pos = start_x + (card_width + card_spacing) * i
            y_pos = height * 0.3
            card["container"].size = (card_width, card_height)
            card["container"].pos = (x_pos, y_pos)

            # Image position and size
            card["image"].size = (card_width, card_width)
            card["image"].pos = (x_pos, y_pos + card_height * 0.3)

            # Label position
            card["label"].size = (card_width, card_height * 0.2)
            card["label"].pos = (x_pos, y_pos + card_height * 0.2)

            # Button position and size
            card["button"].size = (card_width, card_height * 0.15)
            card["button"].pos = (x_pos, y_pos)

    def select_player(self, player_index):
        # Go to game screen or start game with the selected player
        print(f"Player {self.player_data[player_index]['name']} selected")
        # Add your game start logic here, e.g., set the player's image and start the game
        self.manager.current = "game"
        self.manager.get_screen("game").set_player(self.player_data[player_index])


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        # Background
        self.background = Image(
            source="bk_stadium.jpg",
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False,
        )
        self.layout.add_widget(self.background)

        # Player image placeholder
        self.player_image = Image(size_hint=(None, None))
        self.layout.add_widget(self.player_image)

        # Score label
        self.score_label = Label(
            text="Score: 0", font_size="32sp", size_hint=(None, None)
        )
        self.layout.add_widget(self.score_label)

        self.add_widget(self.layout)

    def set_player(self, player_data):
        # Set player image and position it
        self.player_image.source = player_data["image"]
        self.player_image.size = (200, 200)
        self.player_image.pos = (Window.width / 2 - 100, Window.height * 0.6)

        # Position score label
        self.score_label.pos = (Window.width * 0.05, Window.height * 0.9)


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

        # Title
        title = Label(
            text="Foot Bounce Game",
            font_size="48sp",
            size_hint=(None, None),
            pos=(Window.width / 2 - 200, Window.height * 0.7),
        )
        layout.add_widget(title)

        # Start Button
        start_button = Button(
            text="Start Game",
            size_hint=(None, None),
            size=(200, 50),
            pos=(Window.width / 2 - 100, Window.height / 2 - 25),
        )
        start_button.bind(on_release=self.start_game)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = "select_player"


class SoccerJuggleApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name="menu"))
        sm.add_widget(SelectPlayerScreen(name="select_player"))
        sm.add_widget(GameScreen(name="game"))
        return sm


if __name__ == "__main__":
    SoccerJuggleApp().run()
