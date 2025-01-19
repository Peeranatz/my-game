from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock


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
        print(f"Player {self.player_data[player_index]['name']} selected")
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

        # Add ball image
        self.ball_image = Image(source="footballz.png", size_hint=(None, None))
        self.layout.add_widget(self.ball_image)

        # Add shoe image
        self.shoe_image = Image(source="stusz.png", size_hint=(None, None))
        self.layout.add_widget(self.shoe_image)

        self.add_widget(self.layout)

        # Physics attributes
        self.gravity = -600  # Gravity pulling the ball down (pixels/sec^2)
        self.ball_speed = [0, -200]  # [Horizontal speed, Vertical speed]
        self.ball_position = [Window.width / 2 - 50, Window.height]

        # Shoe position
        self.shoe_position = [Window.width / 2 - 75, Window.height * 0.1]

        # Score
        self.score = 0

        # Schedule update function
        Clock.schedule_interval(self.update, 1 / 60.0)  # 60 FPS

    def set_player(self, player_data):
        self.player_image.source = player_data["image"]
        self.player_image.size = (200, 200)
        self.player_image.pos = (Window.width / 10 - 100, Window.height * 0.7)

        self.score_label.pos = (Window.width * 0.05, Window.height * 0.9)

        self.ball_image.size = (100, 100)
        self.ball_position = [Window.width / 2 - 50, Window.height]
        self.ball_image.pos = tuple(self.ball_position)

        self.shoe_image.size = (150, 100)
        self.shoe_image.pos = tuple(self.shoe_position)

    def update(self, dt):
        # Update ball's speed with gravity
        self.ball_speed[1] += self.gravity * dt

        # Update ball's position
        self.ball_position[0] += self.ball_speed[0] * dt
        self.ball_position[1] += self.ball_speed[1] * dt

        # Apply horizontal drag to slow down the ball
        self.ball_speed[0] *= 0.99

        # Update ball image position
        self.ball_image.pos = tuple(self.ball_position)

        # Check collision with the shoe
        if self.check_collision():
            self.ball_speed[1] = abs(self.ball_speed[1]) * 0.8
            collision_offset = self.ball_position[0] - self.shoe_position[0]
            self.ball_speed[0] += collision_offset * 0.1
            self.score += 1

            # Update the score label
            self.score_label.text = f"Score: {self.score}"

        # Check if the ball hits the sides of the screen
        if (
            self.ball_position[0] <= 0
            or self.ball_position[0] + self.ball_image.width >= Window.width
        ):
            self.ball_speed[0] *= -1  # Reverse horizontal direction

        # Check if the ball hits the bottom of the screen
        if self.ball_position[1] <= 0:
            self.reset_ball()  # Reset ball position and speed

        # Check if the ball hits the top of the screen
        if self.ball_position[1] + self.ball_image.height >= Window.height:
            self.ball_speed[1] *= -1  # Reverse vertical direction

    def check_collision(self):
        # Check if the ball and shoe collide
        ball_bottom = self.ball_position[1]
        ball_top = self.ball_position[1] + self.ball_image.height
        ball_left = self.ball_position[0]
        ball_right = self.ball_position[0] + self.ball_image.width

        shoe_top = self.shoe_position[1] + self.shoe_image.height
        shoe_bottom = self.shoe_position[1]
        shoe_left = self.shoe_position[0]
        shoe_right = self.shoe_position[0] + self.shoe_image.width

        return (
            ball_bottom <= shoe_top
            and ball_top >= shoe_bottom
            and ball_right >= shoe_left
            and ball_left <= shoe_right
        )

    def reset_ball(self):
        # Reset ball position and speed
        self.ball_position = [Window.width / 2 - 50, Window.height]
        self.ball_speed = [0, -200]
        self.score = 0  # Reset the score
        self.score_label.text = f"Score: {self.score}"

    def on_touch_move(self, touch):
        # Update shoe position based on touch movement
        self.shoe_position[0] = touch.x - self.shoe_image.width / 2

        # Ensure the shoe stays within screen bounds
        self.shoe_position[0] = max(
            0, min(self.shoe_position[0], Window.width - self.shoe_image.width)
        )
        # Update shoe image position
        self.shoe_image.pos = tuple(self.shoe_position)


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
        # Switch to the Select Player Screen
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
