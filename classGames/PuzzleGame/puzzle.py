from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from random import shuffle
from .data import *

kv = Builder.load_file("classGames/PuzzleGame/puzzle_build.kv")

# Global Variables
count = 0
minutes = 0
seconds = 0

# Constants
BUTTON_SIZE = (0.2, 0.1)
LEVEL_BUTTON_SIZE = (0.8, 0.2)
ZERO_SIZE = (0, 0)
ZERO_POS = {'x': 0, 'y': 0}
VISIBLE = 1
INVISIBLE = 0
DISABLED = True
ENABLED = False

# Lists to store dynamic information
images = []
button_ids = []
pressed_buttons = []


class Puzzle(Screen):

    # ----------------------------------------- Main Init Functions ---------------------------------------------

    # Function to Create the Buttons with a For Loop
    def create_buttons(self):

        # Creating the Buttons if they are not already created
        if len(button_ids) == 0:
            for i in range(1, 25):
                buttons = ToggleButton(size_hint=ZERO_SIZE, pos_hint=ZERO_POS, opacity=0,
                                       background_normal='images/puzzle_images/question_mark.jpg', border=[0, 0, 0, 0])
                self.add_widget(buttons)
                button_ids.append(buttons)

            # Binding the On_Press Function
            for self.button in button_ids:
                self.button.bind(on_press=self.buttons_press)

    # Load the Level Depending on the Difficulty chosen by the User
    def initiate_level(self, difficulty):

        # Function to Load the Widgets - Buttons and Images
        self.initiate_widgets()

        # For Loop to Iterate through the Buttons and Set their Images Depending on the chosen Level
        for index, self.button in enumerate(button_ids):

            # Easy Level
            if difficulty == 'easy':
                self.button.background_down = easy_images[index]

            # Medium Level
            if difficulty == 'medium':
                self.button.background_down = medium_images[index]

            # Hard Level
            if difficulty == 'hard':
                self.button.background_down = hard_images[index]

    # Initiate the Widgets
    def initiate_widgets(self):
        # Creating the Buttons
        self.create_buttons()

        # Initiating the Buttons Size / Pos / Visibility
        self.action_buttons_manager(BUTTON_SIZE, VISIBLE, ENABLED)

        # Hide the Easy / Medium / Hard Buttons
        self.ids.easy.pos_hint = ZERO_POS
        self.ids.medium.pos_hint = ZERO_POS
        self.ids.hard.pos_hint = ZERO_POS
        self.level_buttons_manager(ZERO_SIZE, INVISIBLE, DISABLED)

        # Initiate the Progress Bar and Timer
        self.ids.progress.opacity = VISIBLE
        self.ids.timer.opacity = VISIBLE

        # Scheduling the Timer to be Count the Time for Completing the Level
        Clock.schedule_interval(self.timer, .1)

    # ------------------------------------------- Widget Managers ------------------------------------------------

    # Level Buttons Manager - Controls the Size / Pos / Visibility of the Level Buttons
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

        # If Statement to ensure that when the Buttons are Hidden, their Position is Zero
        if opacity == INVISIBLE:
            self.ids.easy.pos_hint = ZERO_POS
            self.ids.medium.pos_hint = ZERO_POS
            self.ids.hard.pos_hint = ZERO_POS

    # Action Buttons Manager - Controls the Size / Pos / Visibility of the Action Buttons
    def action_buttons_manager(self, size, opacity, disabled):

        # Shuffles the Position of the Buttons so the User can have different Levels every time
        shuffle(button_position)

        # For Loop to Iterate through the List with the Button Positions and place them randomly
        for index, self.button in enumerate(button_ids):
            self.button.pos_hint = button_position[index]

        # For Loop to Iterate through the Buttons and to manage their Size and Visibility
        for self.button in button_ids:
            self.button.size_hint = size
            self.button.opacity = opacity

            # If Statement to ensure that when the Buttons are Hidden, their Position is Zero
            if opacity == INVISIBLE:
                self.button.pos_hint = ZERO_POS
                self.button.disabled = disabled
                self.button.state = 'normal'

    # ----------------------------------------- User Functions ---------------------------------------------------

    # Buttons On_Press Function
    def buttons_press(self, *args):
        global count

        # For Loop to Iterate through the Buttons
        for self.button in button_ids:

            # If Statement to Detect which Button is Pressed
            if self.button.state == 'down' and self.button not in pressed_buttons:
                # Adding the Pressed Button to a List, and it's Image to another List
                pressed_buttons.append(self.button)
                images.append(self.button.background_down)
                count += 1

            # If Statement to Detect if the Button is Unpressed
            if self.button.state == 'normal' and self.button in pressed_buttons:
                # Removing the Unpressed Button and it's Image from the Lists
                pressed_buttons.remove(self.button)
                images.remove(self.button.background_down)
                count -= 1

            # If Statement to Check if Two Buttons are pressed
            if count == 2:

                # If Statement to Check for Success or Fail
                if images[0] == images[1]:
                    Clock.schedule_once(self.success, 1)
                else:
                    Clock.schedule_once(self.fail, 1)
                break

        # Blocking All the Buttons if Two of them are Pressed
        self.block_buttons()

    # Function to ensure that if 2 Buttons are Pressed, the User can't press a Third One
    def block_buttons(self):
        global count

        def block_butts(blocked):

            # For Loop to Iterate through the Buttons and Block all of them if 2 are Pressed
            for self.button in button_ids:
                self.button.background_disabled_normal = self.button.background_normal
                self.button.background_disabled_down = self.button.background_down
                self.button.disabled = blocked

        if count == 2:
            block_butts(True)

        if count < 2:
            block_butts(False)

    # ----------------------------------------- Timer and Mistake Checks -----------------------------------------

    # Timer Function
    def timer(self, dt):
        global minutes, seconds

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

    # Success Function - Checking if the User has guessed Correctly
    def success(self, dt):
        global images, count

        count = 0

        # For Loop to Iterate through the Pressed Buttons
        for self.button in pressed_buttons:

            # If Statement to Check if the Pressed Buttons have the Same Image
            if self.button.background_down == images[0]:
                self.button.opacity = 0
                self.button.size_hint = ZERO_SIZE
                self.button.pos_hint = ZERO_POS
                self.button.disabled = True
                self.button.state = 'normal'

        # If the Statement above is True - Clearing the Image and Pressed Buttons List and Incrementing the Progress
        images.clear()
        pressed_buttons.clear()
        self.block_buttons()
        self.ids.progress.value += 8.34

        # If Statement to check if all the Tiles are Guessed - If Yes, the Level is complete!
        if self.ids.progress.value >= 100:
            self.complete_level()

    # Fail Function - Checking if the User has guessed Wrongly
    def fail(self, dt):
        global count

        count = 0

        # For Loop to Iterate through the Buttons List
        for self.button in button_ids:

            # If the Button is visible, it turns it's state to normal and Hides the Image
            if self.button.opacity == VISIBLE:
                self.button.state = 'normal'

        # Clears the Images and Pressed Buttons List
        images.clear()
        pressed_buttons.clear()

        # Unblocks the Buttons after the Wrong Guess - The count will be 0 so the Function will unblock the buttons
        self.block_buttons()

    # ----------------------------------------------- End Of Level -----------------------------------------------

    # Complete Level Function - Stops the Timer, Gives the User Congratulations and the Level is Finished
    def complete_level(self):
        global minutes, seconds

        # Unschedule the Timer
        Clock.unschedule(self.timer)

        # Provides the User with Feedback on how long it took them to complete the level
        self.ids.level_complete.opacity = 1
        self.ids.level_complete.text = f'Congratulations!\n\nYou completed this level for ' \
                                       f'{minutes} minutes and {seconds} seconds.'

    # Reset Level/Back to Games Page
    def back(self):
        global minutes, seconds

        # Unschedule the Timer
        Clock.unschedule(self.timer)

        # Reset Minutes / Seconds / Timer Text
        minutes = 0
        seconds = 0
        self.ids.timer.text = ''

        # Returns the Level Buttons in a Normal State - Size / Visibility
        self.level_buttons_manager(LEVEL_BUTTON_SIZE, VISIBLE, ENABLED)

        # Returns the Level Buttons in a Normal State - Position
        self.ids.easy.pos_hint = {'x': 0.1, 'y': 0.75}
        self.ids.medium.pos_hint = {'x': 0.1, 'y': 0.5}
        self.ids.hard.pos_hint = {'x': 0.1, 'y': 0.25}

        # Hides the Timer, Progress Bar and Level Complete Label
        self.ids.progress.opacity = INVISIBLE
        self.ids.timer.opacity = INVISIBLE
        self.ids.level_complete.opacity = INVISIBLE

        # Resets the Progress Bar Value to 0
        self.ids.progress.value = 0

        # Hides the Action Buttons - Size / Visibility
        self.action_buttons_manager(ZERO_SIZE, INVISIBLE, DISABLED)

        # Using the Fail Function to Reset the Count and Clear the Lists
        Clock.schedule_once(self.fail, 0)
