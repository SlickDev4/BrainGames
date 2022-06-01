from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from .oxford_dictionary import dictionary

kv = Builder.load_file("classGames/WordsGame/words_build.kv")

EASY = False
MEDIUM = False
HARD = False
EXPERT = False


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

    def test(self):

        characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                      'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-', 'z']
        characters_set = set(characters)
        dc = []

        for word in dictionary:
            word = word.lower()
            if all(char in characters_set for char in set(word)):
                dc.append(word)

        print(len(dc))
        print(len(dictionary))


