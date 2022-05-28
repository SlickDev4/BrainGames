from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import Screen
from random import sample

global board

kv = Builder.load_file("classGames/SudokuGame/sudoku_build.kv")

# Global Variables
minutes = 0
seconds = 0

EASY = False
MEDIUM = False
HARD = False
EXPERT = False

VISIBLE = 1
INVISIBLE = 0

BACKGROUND_LABEL_SIZE = (0.93, 0.48)
FIELDS_SIZE = (0.1, 0.05)
ACTION_BUTTONS_SIZE = (0.1, 0.05)
LEVEL_BUTTONS_SIZE = (0.8, 0.1)

ZERO_SIZE = (0, 0)

ENABLED = False
DISABLED = True

# List for the Solution to be Saved so that we can make Checks when the User is Inputting Numbers
solution = []

# Lists for Storing the IDs of Buttons created with For Loops
grid_buttons_ids = []
action_buttons_ids = []

# List for Checking if All Buttons have text in them in order to Complete the Level
grid_buttons_text = []


class Sudoku(Screen):

    empties = NumericProperty(None)

    # ----------------------------------- Initiate Level by Difficulty -------------------------------------

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

        self.initiate_grid()
        Clock.schedule_interval(self.timer, .1)

    # ----------------------------------- Initiate the Sudoku / Widgets -------------------------------------

    # Main Init Function
    def initiate_grid(self):

        # Creates the Grid and the Action Buttons
        self.create_the_grid()
        self.create_the_action_buttons()

        # Initiates the Labels, Fields and Action Buttons SIZE/VISIBILITY and ENABLES them

        self.labels_manager(BACKGROUND_LABEL_SIZE, VISIBLE)
        self.fields_manager(FIELDS_SIZE, VISIBLE, ENABLED)
        self.action_buttons_manager(ACTION_BUTTONS_SIZE, VISIBLE, ENABLED)

        # Hides the Level Buttons after Initiating the needed Widgets
        self.level_buttons_manager(ZERO_SIZE, INVISIBLE, DISABLED)

        # Generates the Sudoku and Fills the Board with some Numbers
        self.sudoku_generator()
        self.fill_board_with_numbers()

        # Prevents the user from clicking Buttons that have Numbers
        self.block_occupied_buttons()

    # Creating the 9x9 Grid Buttons
    def create_the_grid(self):
        # Condition to check if the Buttons are already created
        if len(grid_buttons_ids) == 0:

            # For Loop to Create the Buttons if they are not created
            for i in range(1, 82):
                grid_buttons = ToggleButton(size_hint=FIELDS_SIZE, opacity=INVISIBLE, disabled=DISABLED, group='board',
                                            font_size=sp(20), disabled_color=[1, 1, 1, 1],
                                            background_disabled_normal='atlas://data/images/defaulttheme/button')

                self.add_widget(grid_buttons)

                # Adding the Buttons Instance to a List so that we can reference it later
                grid_buttons_ids.append(grid_buttons)

    # Creating the Action Buttons
    def create_the_action_buttons(self):
        # Condition to check if the Buttons are already created
        if len(action_buttons_ids) == 0:

            # For Loop to Create the Buttons if they are not created
            for i in range(1, 10):
                action_buttons = Button(size_hint=ACTION_BUTTONS_SIZE, opacity=INVISIBLE, disabled=DISABLED,
                                      font_size=sp(20), text=f'{i}')

                self.add_widget(action_buttons)

                # Adding the Buttons Instance to a List so that we can reference it later
                action_buttons_ids.append(action_buttons)

        # For Loop to Assign the On Press Function in order to be able to assign Numbers on the Grid
        for button in action_buttons_ids:
            button.bind(on_press=self.action_buttons)

    # ------------------------------------------ Widget Managers ----------------------------------------------

    # Manages the Size / Visibility / Position of the Labels
    def labels_manager(self, background_size, opacity):

        self.ids.background.size_hint = background_size
        self.ids.background.opacity = opacity

        if opacity == VISIBLE:
            self.ids.background.pos_hint = {'x': 0.035, 'y': 0.425}
        else:
            self.ids.background.pos_hint = {'x': 0, 'y': 0}

    # Manages the Size / Visibility / Position of the 9x9 Grid
    def fields_manager(self, size_hint, opacity, disabled):

        def init_pos():
            x = 0.04
            y = 0.85

            # For Loop to Set the Grid with some Spaces in between the Cubes

            for self.button in grid_buttons_ids:
                x = round(x, 2)
                y = round(y, 2)

                if x == 0.34 or x == 0.65:
                    x += 0.01
                    x = round(x, 2)

                if x == 0.96:
                    x = 0.04
                    y -= 0.05
                    y = round(y, 2)

                if y == 0.70 or y == 0.54:
                    y -= 0.01
                    y = round(y, 2)

                self.button.pos_hint = {'x': x, 'y': y}
                x += 0.1

        def zero_pos():

            # For Loop to Hide all the 9x9 Grid Buttons
            for self.button in grid_buttons_ids:
                self.button.pos_hint = {'x': 0, 'y': 0}

        # For Loop to Set the Size, Visibility and Enables the Buttons

        for self.button in grid_buttons_ids:
            self.button.size_hint = size_hint
            self.button.opacity = opacity
            self.button.disabled = disabled

        # Condition to Position the Buttons if they are Visible

        if not len(grid_buttons_ids) == 0:
            if grid_buttons_ids[0].opacity == VISIBLE:
                init_pos()
            else:
                zero_pos()

    # Manages the Size / Visibility / Position of the Action Buttons
    def action_buttons_manager(self, size_hint, opacity, disabled):

        def init_pos():
            x = 0.04
            y = 0.35

            for self.button in action_buttons_ids:
                x = round(x, 2)

                if x == 0.34 or x == 0.65:
                    x += 0.01
                    x = round(x, 2)

                self.button.pos_hint = {'x': x, 'y': y}
                x += 0.1

        def zero_pos():
            # For Loop to Hide all the Action Buttons
            for self.button in action_buttons_ids:
                self.button.pos_hint = {'x': 0, 'y': 0}

        for self.button in action_buttons_ids:
            self.button.size_hint = size_hint
            self.button.opacity = opacity
            self.button.disabled = disabled

        if opacity == VISIBLE:
            init_pos()
        else:
            zero_pos()

    # Manages the Size / Visibility / Position of the Level Buttons
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
        self.ids.hard.disabled = disabled

    # ----------------------------------- Generate the Sudoku Puzzle ------------------------------------------

    # Fill the Board with a whole Solution and then Remove some numbers depending on the difficulty
    def sudoku_generator(self):
        global board, solution

        base = 3
        side = base * base

        # Pattern for a baseline valid solution
        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side

        def shuffle_the_board(s):
            return sample(s, len(s))

        r_base = range(base)

        rows = [g * base + r for g in shuffle_the_board(r_base) for r in shuffle_the_board(r_base)]
        cols = [g * base + c for g in shuffle_the_board(r_base) for c in shuffle_the_board(r_base)]
        nums = shuffle_the_board(range(1, base * base + 1))

        # Produce board using Randomized Baseline Pattern
        board = [[nums[pattern(r, c)] for c in cols] for r in rows]
        solution = [[nums[pattern(r, c)] for c in cols] for r in rows]

        # for line in board:
        #     print(line)

        squares = side * side
        self.empties = 0

        # Defines how many Numbers to Remove depending on the Difficulty
        if EASY:
            self.empties = 31

        if MEDIUM:
            self.empties = 39

        if HARD:
            self.empties = 43

        if EXPERT:
            self.empties = 55

        # For Loop to Remove the Numbers
        for p in sample(range(squares), self.empties):
            board[p // side][p % side] = ''

    # Assign the prepared Numbers to the Board Buttons
    def fill_board_with_numbers(self):

        x = 0
        y = 0

        # For Loop to Assign the Numbers on the Buttons
        for self.button in grid_buttons_ids:

            if y == 9:
                x += 1
                y = 0

            self.button.text = str(board[x][y])
            y += 1

    # ----------------------------------- Action Buttons Functions ---------------------------------------------

    # Main Function to assign numbers
    def action_buttons(self, number):

        # For Loop to Iterate through the Grid Buttons and Detect which Button is in a Down State
        for self.button in grid_buttons_ids:

            # If Statement to take the ID of the Button
            if self.button.state == 'down':
                action_id = number

                # For Loop to Iterate through the Action Buttons and Detect which Action Button is Pressed
                for self.action in action_buttons_ids:

                    # If Statement to assign the Number from the Action Button to the Grid Button
                    if self.action == action_id:
                        self.button.text = self.action.text

        self.check_for_mistakes()
        self.complete_level()

    # Checking Every Field for a Mistake after Inputting a Number
    def check_for_mistakes(self):

        x = 0
        y = 0

        # For Loop to Iterate through the Grid Buttons and check if their State is Down
        for self.button in grid_buttons_ids:

            if y == 9:
                x += 1
                y = 0

            # If Statement to check if the State is Down
            if self.button.state == 'down':

                # If yes, it checks the User Input with the Solution
                if self.button.text != str(solution[x][y]):
                    self.button.text = ''
                else:
                    self.button.disabled = True

                self.button.state = 'normal'

            y += 1

    # Blocks a button if it already has a number
    def block_occupied_buttons(self):

        for self.button in grid_buttons_ids:
            if not self.button.text == '':
                self.button.disabled = True

    # ---------------------------------- Timer / Tries Left / End of Level ---------------------------------------

    # Timer Function
    def timer(self, dt):
        global minutes, seconds

        # Showing the Timer
        self.ids.timer.opacity = VISIBLE

        # Incrementing the seconds variable and rounding it
        seconds += .1
        seconds = round(seconds, 1)

        # Some If Statements to make the Label more user Friendly
        if seconds < 10:
            self.ids.timer.text = f'{minutes}:0{seconds}'

        if 10 <= seconds <= 60:
            self.ids.timer.text = f'{minutes}:{seconds}'

        if seconds > 60:
            minutes += 1
            seconds = 0
            self.ids.timer.text = f'{minutes}:{seconds}'

    def reset_timer(self):
        global minutes, seconds

        Clock.unschedule(self.timer)
        minutes = 0
        seconds = 0

    # Needs to be Done
    def tries_left(self):
        pass

    def complete_level(self):

        grid_buttons_text.clear()

        for self.button in grid_buttons_ids:
            grid_buttons_text.append(self.button.text)

        if '' not in grid_buttons_text:
            print('level completed')
            self.reset_timer()
            grid_buttons_text.clear()

    # ----------------------------------- Reset Level / Back to Games Page ---------------------------------------

    def back(self):
        global EASY, MEDIUM, HARD, EXPERT

        self.level_buttons_manager(LEVEL_BUTTONS_SIZE, VISIBLE, ENABLED)
        self.action_buttons_manager(ZERO_SIZE, INVISIBLE, DISABLED)
        self.fields_manager(ZERO_SIZE, INVISIBLE, DISABLED)

        self.labels_manager(ZERO_SIZE, INVISIBLE)

        EASY = False
        MEDIUM = False
        HARD = False
        EXPERT = False

        self.ids.easy.pos_hint = {'x': 0.1, 'y': 0.8}
        self.ids.medium.pos_hint = {'x': 0.1, 'y': 0.65}
        self.ids.hard.pos_hint = {'x': 0.1, 'y': 0.5}
        self.ids.expert.pos_hint = {'x': 0.1, 'y': 0.35}

        self.reset_timer()
        self.ids.timer.text = ''

        grid_buttons_text.clear()
