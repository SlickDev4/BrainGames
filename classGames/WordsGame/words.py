from kivy.lang import Builder
from kivy.metrics import sp
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from random import shuffle
from .oxford_dictionary import dictionary
from .buttons_position import character_buttons_easy_position, character_buttons_medium_position, \
    character_buttons_hard_position, character_buttons_expert_position

kv = Builder.load_file("classGames/WordsGame/words_build.kv")

EASY = False
MEDIUM = False
HARD = False
EXPERT = False

DISABLED = True
ENABLED = False

BUTT_SIZE = (0.15, 0.07)
LEVEL_BUTTONS_SIZE = (0.8, 0.1)

ZERO_SIZE = (0, 0)
ZERO_POS = {'x': 0, 'y': 0}

INVISIBLE = 0
VISIBLE = 1

number_of_buttons = 0
number_of_index = 0

characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                      'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-', 'z']

character_buttons_ids = []
selected_characters = []
available_words = []


class Words(Screen):
    def initiate_level(self, difficulty):
        global EASY, MEDIUM, HARD, EXPERT

        if difficulty == 'easy':
            EASY = True
        if difficulty == 'medium':
            MEDIUM = True
        if difficulty == 'hard':
            HARD = True
        if difficulty == 'expert':
            EXPERT = True

        self.start()

    def start(self):
        self.create_buttons()
        self.assign_characters()
        self.level_buttons_manager(ZERO_SIZE, INVISIBLE, DISABLED)
        self.character_buttons_manager(BUTT_SIZE, VISIBLE, ENABLED)

    def create_buttons(self):
        global number_of_buttons, BUTT_SIZE

        if EASY:
            number_of_buttons = 12
        if MEDIUM:
            number_of_buttons = 10
        if HARD:
            number_of_buttons = 8
        if EXPERT:
            number_of_buttons = 6

        if len(character_buttons_ids) == 0:
            for i in range(1, number_of_buttons + 1):
                char_buttons = Button(size_hint=ZERO_SIZE, opacity=INVISIBLE, disabled=DISABLED,
                                            font_size=sp(20), disabled_color=[1, 1, 1, 1],
                                            background_disabled_normal='atlas://data/images/defaulttheme/button')

                self.add_widget(char_buttons)
                character_buttons_ids.append(char_buttons)

    def character_buttons_manager(self, size_hint, opacity, disabled):
        for self.button in character_buttons_ids:
            self.button.size_hint = size_hint
            self.button.opacity = opacity
            self.button.disabled = disabled

        if not len(character_buttons_ids) == 0:
            for index, self.button in enumerate(character_buttons_ids):
                if character_buttons_ids[0].opacity == VISIBLE:
                    if EASY:
                        self.button.pos_hint = character_buttons_easy_position[index]
                    if MEDIUM:
                        self.button.pos_hint = character_buttons_medium_position[index]
                    if HARD:
                        self.button.pos_hint = character_buttons_hard_position[index]
                    if EXPERT:
                        self.button.pos_hint = character_buttons_expert_position[index]
                else:
                    self.button.pos_hint = ZERO_POS

    def level_buttons_manager(self, size, opacity, disabled):
        self.ids.easy.size_hint = size
        self.ids.easy.opacity = opacity
        self.ids.easy.disabled = disabled

        self.ids.medium.size_hint = size
        self.ids.medium.opacity = opacity
        self.ids.medium.disabled = disabled

        self.ids.hard.size_hint = size
        self.ids.hard.opacity = opacity
        self.ids.hard.disabled = disabled

        self.ids.expert.size_hint = size
        self.ids.expert.opacity = opacity
        self.ids.expert.disabled = disabled

        # If Statement to ensure that when the Buttons are Hidden, their Position is Zero
        if opacity == INVISIBLE:
            self.ids.easy.pos_hint = ZERO_POS
            self.ids.medium.pos_hint = ZERO_POS
            self.ids.hard.pos_hint = ZERO_POS
            self.ids.expert.pos_hint = ZERO_POS

        # Else Positions the Buttons Properly
        else:
            self.ids.easy.pos_hint = {'x': 0.1, 'y': 0.8}
            self.ids.medium.pos_hint = {'x': 0.1, 'y': 0.65}
            self.ids.hard.pos_hint = {'x': 0.1, 'y': 0.5}
            self.ids.expert.pos_hint = {'x': 0.1, 'y': 0.35}

    def assign_characters(self):
        global number_of_index

        shuffle(characters)

        selected_characters.clear()
        available_words.clear()

        for index, char in enumerate(characters):
            if EASY:
                number_of_index = 12
            if MEDIUM:
                number_of_index = 10
            if HARD:
                number_of_index = 8
            if EXPERT:
                number_of_index = 6

            if index < number_of_index:
                selected_characters.append(char)
                character_buttons_ids[index].text = selected_characters[index]
            else:
                break

        for word in dictionary:
            word = word.lower()
            if all(char in selected_characters for char in set(word)):
                available_words.append(word)

        print(len(available_words))

        if len(available_words) < number_of_index * 2:
            self.assign_characters()

    def back(self):
        global EASY, MEDIUM, HARD, EXPERT

        self.level_buttons_manager(LEVEL_BUTTONS_SIZE, VISIBLE, ENABLED)
        self.character_buttons_manager(ZERO_SIZE, INVISIBLE, DISABLED)

        character_buttons_ids.clear()

        EASY = False
        MEDIUM = False
        HARD = False
        EXPERT = False


