# ------------ Imports ------------
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from random import randint


# ------------ Main Menu Screen ------------
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

        # Exit Button
        exit_button = Button(
            text="Exit",
            size_hint=(None, None),
            size=(200, 50),
            pos=(Window.width / 2 - 100, Window.height / 2 - 100),
        )
        exit_button.bind(on_release=self.exit_game)
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = "select_player"

    def exit_game(self, instance):
        App.get_running_app().stop()


# ------------ Select Player Screen ------------
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
        player_image_path = self.player_data[player_index]["image"]
        self.manager.get_screen("game").start_game(player_image_path)
        self.manager.current = "game"


# ------------ Main Game Screen ------------
class SoccerJuggleGame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # เพิ่ม attribute ใหม่สำหรับการเปลี่ยนลูกฟุตบอล
        self.ball_images = [
            "footballz.png",
            "mudeng-re.png",  # เพิ่มรูปลูกฟุตบอลประเภทใหม่
            "pigpig-re.png",  # เพิ่มรูปลูกฟุตบอลประเภทใหม่
            "bowling-re.png",  # เพิ่มรูปลูกฟุตบอลประเภทใหม่
            "footgold.png",  # เพิ่มรูปลูกฟุตบอลประเภทใหม่
        ]
        self.current_ball_image_index = 0

        self.game_state = None
        self.selected_player = None
        self.score = 0
        self.high_score = 0

        # Bind window size to update positions
        Window.bind(size=self.on_window_resize)

        # Load sounds
        self.hit_sound = SoundLoader.load("sound_bounce.mp3")
        self.game_over_sound = SoundLoader.load("gameOver.mp3")

        # Create layout
        self.layout = FloatLayout()

        # Background
        self.background = Image(
            source="bk_stadium.jpg",
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False,
        )
        self.layout.add_widget(self.background)

        # Ball properties
        self.ball = Image(source="footballz.png", size_hint=(None, None))
        self.layout.add_widget(self.ball)

        # Shoe properties
        self.shoe = Image(source="stusz.png", size_hint=(None, None))
        self.layout.add_widget(self.shoe)

        # Hitbox for the shoe
        self.shoe_hitbox = Widget(size_hint=(None, None))
        self.layout.add_widget(self.shoe_hitbox)

        # Player image
        self.player_image = Image(size_hint=(None, None))
        self.layout.add_widget(self.player_image)

        # Score label
        self.score_label = Label(
            text=f"Score: {self.score}",
            font_size="30sp",
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            pos_hint={"center_x": 0.08, "center_y": 0.8},
        )
        self.layout.add_widget(self.score_label)

        # Game Over label
        self.game_over_label = Label(
            text="Game Over",
            font_size="72sp",
            color=(1, 0, 0, 1),  # สีแดง
            size_hint=(None, None),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            opacity=0,  # ซ่อนไว้ตอนเริ่มเกม
        )
        self.layout.add_widget(self.game_over_label)

        # เพิ่ม Label สำหรับข้อความ You Win
        self.win_label = Label(
            text="You Win!",
            font_size="72sp",
            color=(0, 1, 0, 1),  # สีเขียว
            size_hint=(None, None),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            opacity=0,
        )
        self.layout.add_widget(self.win_label)

        # Restart button
        self.restart_button = Button(text="Restart", size_hint=(None, None))
        self.restart_button.bind(on_release=self.show_game_over)
        self.restart_button.opacity = 0
        self.restart_button.disabled = True
        self.layout.add_widget(self.restart_button)

        self.add_widget(self.layout)

        # Initial update of positions
        self.on_window_resize(Window, Window.size)

        # Game loop
        Clock.schedule_interval(self.update, 1 / 60.0)

    def start_game(self, player_image_path):
        self.game_state = "WAITING"
        self.score = 0
        self.ball.pos = (
            Window.width // 2 - self.ball.width // 2,
            Window.height // 2 - self.ball.height // 2,
        )
        self.ball_speed_y = -5
        self.ball_speed_x = randint(-3, 3) or 1
        self.gravity = -0.2
        self.player_image.source = player_image_path
        self.update_score()
        self.restart_button.opacity = 0
        self.restart_button.disabled = True
        self.game_over_label.opacity = 0

        # รีเซ็ตการตั้งค่าเมื่อเริ่มเกมใหม่
        self.current_ball_image_index = 0
        self.ball.source = self.ball_images[0]
        self.win_label.opacity = 0

        # เรียกใช้เมธอดเดิม
        super().start_game(player_image_path)

        # กำหนด game loop กลับมา
        Clock.schedule_interval(self.update, 1 / 60.0)

    def start_playing(self):
        self.game_state = "PLAYING"

    def show_game_over(self, instance):
        self.manager.get_screen("game_over").display_results(
            self.score, self.high_score
        )
        self.manager.current = "game_over"

    def update(self, dt):
        # เพิ่มเงื่อนไขสำหรับสถานะ WIN
        if self.game_state == "WIN":
            return

        if self.game_state == "PLAYING":
            self.ball.y += self.ball_speed_y
            self.ball.x += self.ball_speed_x
            self.ball_speed_y += self.gravity

            # Ball collision with shoe
            if self.check_collision():
                self.ball_speed_y = 8
                self.ball_speed_x = randint(-3, 3)
                self.score += 1
                self.update_score()

                # Play hit sound
                if self.hit_sound:
                    self.hit_sound.play()

                # Increase difficulty
                if self.score % 5 == 0:
                    self.ball_speed_y -= 0.5
                    self.gravity -= 0.05

            # Ball falls off screen
            if self.ball.y < 0:
                self.game_state = "GAME_OVER"

                # Update high score
                if self.score > self.high_score:
                    self.high_score = self.score

                # Play game over sound
                if self.game_over_sound:
                    self.game_over_sound.play()

                # แสดง Game Over label
                self.game_over_label.opacity = 1

                self.restart_button.opacity = 1
                self.restart_button.disabled = False

            # Ball bounces off walls
            if self.ball.x <= 0 or self.ball.x + self.ball.width >= Window.width:
                self.ball_speed_x *= -1

    def check_collision(self):
        ball_bottom = self.ball.y
        ball_center_x = self.ball.x + self.ball.width / 2
        return (
            self.shoe_hitbox.x
            < ball_center_x
            < self.shoe_hitbox.x + self.shoe_hitbox.width
            and self.shoe_hitbox.y
            < ball_bottom
            < self.shoe_hitbox.y + self.shoe_hitbox.height
            and self.ball_speed_y < 0
        )

    def update_score(self):
        self.score_label.text = f"Score: {self.score}"

        # ตรวจสอบและเปลี่ยนลูกฟุตบอล
        if self.score == 10 or self.score == 20 or self.score == 30 or self.score == 40:
            self.current_ball_image_index += 1
            if self.current_ball_image_index < len(self.ball_images):
                self.ball.source = self.ball_images[self.current_ball_image_index]

        # แสดงข้อความ You Win เมื่อเดาะครบ 50 ครั้ง
        if self.score == 50:
            self.win_label.opacity = 1
            self.game_state = "WIN"
            # หยุดการเคลื่อนที่ของลูกฟุตบอล
            Clock.unschedule(self.update)

    def on_touch_down(self, touch):
        if self.game_state == "WAITING":
            self.start_playing()

    def on_touch_move(self, touch):
        if self.game_state == "PLAYING":
            self.shoe.x = touch.x - self.shoe.width / 2
            self.shoe_hitbox.x = touch.x - self.shoe_hitbox.width / 2

    def on_window_resize(self, instance, size):
        width, height = size

        # Update ball size and position
        ball_size = (width * 0.08, height * 0.08)
        self.ball.size = ball_size
        if self.game_state is None or self.game_state == "WAITING":
            self.ball.pos = (
                width // 2 - ball_size[0] // 2,
                height // 2 - ball_size[1] // 2,
            )

        # Update shoe size and position
        shoe_width = width * 0.25
        shoe_height = height * 0.1
        self.shoe.size = (shoe_width, shoe_height)
        self.shoe.pos = (width // 2 - shoe_width // 2, height * 0.1)

        # Update shoe hitbox
        hitbox_width = shoe_width * 0.5
        hitbox_height = shoe_height * 0.2
        self.shoe_hitbox.size = (hitbox_width, hitbox_height)
        self.shoe_hitbox.pos = (width // 2 - hitbox_width // 2, height * 0.12)

        # Update player image size and position
        player_size = (width * 0.1, height * 0.15)
        self.player_image.size = player_size
        self.player_image.pos = (width * 0.02, height * 0.8)
        # ต่อจาก on_window_resize ของ SoccerJuggleGame
        player_size = (width * 0.1, height * 0.15)
        self.player_image.size = player_size
        self.player_image.pos = (width * 0.02, height * 0.8)

        # Update score label position
        self.score_label.pos = (width * 0.02, height * 0.95)

        # Update restart button size and position
        button_width = width * 0.2
        button_height = height * 0.08
        self.restart_button.size = (button_width, button_height)
        self.restart_button.pos = (
            width // 2 - button_width // 2,
            height // 2 - button_height // 2,
        )


# ------------ Game Over Screen ------------
class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        # Background
        self.background = Image(
            source="gameover.jpg",
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False,
        )
        layout.add_widget(self.background)

        # Results label
        self.results_label = Label(
            text="",
            font_size="24sp",
            color=(1, 1, 1, 1),
            size_hint=(None, None),
        )
        layout.add_widget(self.results_label)

        # Restart button
        restart_button = Button(
            text="Restart",
            size_hint=(None, None),
            size=(200, 50),
            pos=(Window.width / 2 - 100, Window.height / 2 - 25),
        )
        restart_button.bind(on_release=self.restart_game)
        layout.add_widget(restart_button)
        self.add_widget(layout)

    def display_results(self, score, high_score):
        self.results_label.text = f"Your Score: {score}\nHigh Score: {high_score}"
        self.results_label.pos = (Window.width / 2 - 100, Window.height / 2 + 50)

    def restart_game(self, instance):
        print("Restart button clicked")
        self.manager.current = "select_player"


# ------------ Main App Class ------------
class SoccerJuggleApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name="menu"))
        sm.add_widget(SelectPlayerScreen(name="select_player"))
        sm.add_widget(SoccerJuggleGame(name="game"))
        sm.add_widget(GameOverScreen(name="game_over"))
        return sm


# ------------ Main Entry Point ------------
if __name__ == "__main__":
    SoccerJuggleApp().run()
