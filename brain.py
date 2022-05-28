from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from classGames.games import Games
from classHome.home import Home
from classScoreboard.scoreboard import Scoreboard
from classSettings.settings import SettingsPage

from classGames.PuzzleGame.puzzle import Puzzle
from classGames.SudokuGame.sudoku import Sudoku


class MainWindow(ScreenManager):
    pass


kv = Builder.load_file("build.kv")
sm = MainWindow()

screens = [Home(name='home'), Games(name='games'), Scoreboard(name='scoreboard'), SettingsPage(name='settings'),
           Puzzle(name='puzzle'), Sudoku(name='sudoku')]

for screen in screens:
    sm.add_widget(screen)


class BrainApp(App):

    def build(self):
        Window.size = (360, 700)
        Window.top = 27
        Window.left = 500
        return sm


if __name__ == '__main__':
    BrainApp().run()
