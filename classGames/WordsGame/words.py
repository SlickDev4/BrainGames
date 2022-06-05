from kivy.lang import Builder
from kivy.metrics import sp
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from random import shuffle
from .oxford_dictionary import dictionary
from .buttons_position import character_buttons_position

kv = Builder.load_file("classGames/WordsGame/words_build.kv")

EASY = False
MEDIUM = False
HARD = False
EXPERT = False

DISABLED = True
ENABLED = False

BUTT_SIZE = (0.15, 0.07)
LEVEL_BUTTONS_SIZE = (0.8, 0.1)
MAIN_LABEL_SIZE = (0.9, 0.4)
CURRENT_LABEL_SIZE = (0.9, 0.07)
CONFIRM_REMOVE_BUTT_SIZE = (0.3, 0.07)

MAIN_LABEL_POS = {'x': 0.05, 'y': 0.2}
CURRENT_LABEL_POS = {'x': 0.05, 'y': 0.7}
CONFIRM_BUTT_POS = {'x': 0.05, 'y': 0.62}
REMOVE_BUTT_POS = {'x': 0.35, 'y': 0.62}
DELETE_BUTT_POS = {'x': 0.65, 'y': 0.62}

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

        self.load_level()

    def load_level(self):
        self.create_buttons()
        self.assign_characters_to_buttons()

        self.character_buttons_manager(BUTT_SIZE, VISIBLE, ENABLED)
        self.level_buttons_manager(ZERO_SIZE, INVISIBLE, DISABLED)
        self.confirm_remove_delete_buttons_manager(CONFIRM_REMOVE_BUTT_SIZE, VISIBLE, ENABLED)
        self.labels_manager(MAIN_LABEL_SIZE, CURRENT_LABEL_SIZE, VISIBLE)

    def create_buttons(self):

        if len(character_buttons_ids) == 0:
            for i in range(1, 13):
                char_buttons = Button(size_hint=ZERO_SIZE, opacity=INVISIBLE, disabled=DISABLED,
                                            font_size=sp(20), disabled_color=[1, 1, 1, 1],
                                            background_disabled_normal='atlas://data/images/defaulttheme/button')

                self.add_widget(char_buttons)
                character_buttons_ids.append(char_buttons)

        for self.button in character_buttons_ids:
            self.button.bind(on_press=self.assign_characters_to_label)

    def character_buttons_manager(self, size, opacity, disabled):
        for self.button in character_buttons_ids:
            self.button.size_hint = size
            self.button.opacity = opacity
            self.button.disabled = disabled

        if not len(character_buttons_ids) == 0:
            for index, self.button in enumerate(character_buttons_ids):
                if character_buttons_ids[0].opacity == VISIBLE:
                    self.button.pos_hint = character_buttons_position[index]
                else:
                    self.button.pos_hint = ZERO_POS

    def confirm_remove_delete_buttons_manager(self, size, opacity, disabled):
        self.ids.confirm_button.size_hint = size
        self.ids.confirm_button.opacity = opacity
        self.ids.confirm_button.disabled = disabled

        self.ids.remove_button.size_hint = size
        self.ids.remove_button.opacity = opacity
        self.ids.remove_button.disabled = disabled

        self.ids.delete_button.size_hint = size
        self.ids.delete_button.opacity = opacity
        self.ids.delete_button.disabled = disabled

        if opacity == VISIBLE:
            self.ids.confirm_button.pos_hint = CONFIRM_BUTT_POS
            self.ids.remove_button.pos_hint = REMOVE_BUTT_POS
            self.ids.delete_button.pos_hint = DELETE_BUTT_POS
        else:
            self.ids.confirm_button.pos_hint = ZERO_POS
            self.ids.remove_button.pos_hint = ZERO_POS
            self.ids.delete_button.pos_hint = ZERO_POS

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

    def labels_manager(self, big_size, small_size, opacity):

        self.ids.word_label.size_hint = big_size
        self.ids.word_label.opacity = opacity

        self.ids.current_word_label.size_hint = small_size
        self.ids.current_word_label.opacity = opacity

        if opacity == VISIBLE:
            self.ids.word_label.pos_hint = MAIN_LABEL_POS
            self.ids.current_word_label.pos_hint = CURRENT_LABEL_POS
        else:
            self.ids.word_label.pos_hint = ZERO_POS
            self.ids.current_word_label.pos_hint = ZERO_POS

    def assign_characters_to_buttons(self):
        shuffle(characters)

        selected_characters.clear()
        available_words.clear()

        for index, char in enumerate(characters):
            selected_characters.append(char)
            character_buttons_ids[index].text = selected_characters[index]

            if index == 11:
                break

        for word in dictionary:
            word = word.lower()
            if all(char in selected_characters for char in set(word)):
                available_words.append(word)

        if len(available_words) < 20:
            self.assign_characters_to_buttons()

    def assign_characters_to_label(self, *args):
        for self.button in character_buttons_ids:
            if self.button.state == 'down':
                self.ids.current_word_label.text += self.button.text

    def confirm_word_and_add_to_main_label(self):
        if self.ids.current_word_label.text in available_words:
            self.ids.word_label.text += f'{self.ids.current_word_label.text}\n'
        else:
            print('no such word')

    def remove_characters_from_label(self):
        self.ids.current_word_label.text = self.ids.current_word_label.text[:-1]

    def delete_word_from_current_label(self):
        self.ids.current_word_label.text = ''

    def back(self):
        global EASY, MEDIUM, HARD, EXPERT

        self.character_buttons_manager(ZERO_SIZE, INVISIBLE, DISABLED)
        self.level_buttons_manager(LEVEL_BUTTONS_SIZE, VISIBLE, ENABLED)
        self.confirm_remove_delete_buttons_manager(ZERO_SIZE, INVISIBLE, DISABLED)
        self.labels_manager(ZERO_SIZE, ZERO_SIZE, INVISIBLE)

        character_buttons_ids.clear()

        EASY = False
        MEDIUM = False
        HARD = False
        EXPERT = False
