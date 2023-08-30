import tkinter as tk
import letter_button as lb

class Keyboard():
    """
    Creates a digital keyboard 
    """

    dark_mode_background  = "#121213"
    light_mode_background = "#ffffff"

    def __init__(self, root, width, height, screen_width, screen_height, is_dark, command, spacing):
        self.row1 = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]
        self.row2 = ["A", "S", "D", "F", "G", "H", "J", "K", "L"]
        self.row3 = ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "BACK"]
        self.row1_buttons = []
        self.row2_buttons = []
        self.row3_buttons = []
        self.root = root
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_dark = is_dark
        self.command = command
        self.spacing = spacing

    def calculate_starting_position(self):
        """
        Calculates which pixel to start drawing on to align keyboard center
        :return: int for which pixel to start on
        """

        keyboard_width = 9 * self.spacing + 10 * self.width
        middle = self.screen_width // 2
        return middle - keyboard_width // 2

    def create_keyboard(self):
        """
        Creates digial keyboard
        :return: Canvas object which displays a keyboard
        """

        bg_color = self.light_mode_background
        if self.is_dark:
            bg_color = self.dark_mode_background

        canvas = tk.Canvas(self.root, width=self.screen_width, height=self.screen_height)
        canvas.config(bg=bg_color, highlightbackground=bg_color)
        starting_pos = self.calculate_starting_position()

        # creates first row buttons:
        for i, letter in enumerate(self.row1):
            btn = lb.LetterButton(canvas, starting_pos + i * (self.width + self.spacing),
             self.spacing, self.width, self.height, self.is_dark, self.command, False, letter)
            self.row1_buttons.append(btn)
        
        # creates second row buttons:
        for i, letter in enumerate(self.row2):
            btn = lb.LetterButton(canvas, starting_pos + self.width // 2 + i * (self.width + self.spacing),
             self.spacing * 2 + self.height, self.width, self.height, self.is_dark, self.command, False, letter)
            self.row2_buttons.append(btn)

        # creates third row buttons:
        for i, letter in enumerate(self.row3):
            btn = lb.LetterButton(canvas, starting_pos + self.width // 2 +i * (self.width + self.spacing),
             self.spacing * 3 + self.height * 2, self.width, self.height, self.is_dark, self.command, False, letter)
            self.row3_buttons.append(btn)

        self.all_buttons = self.row1_buttons + self.row2_buttons + self.row3_buttons
        return canvas


    def get_button(self, letter):
        """
        Finds which button to return based off given letter
        :param letter: String for which letter on keyboard to find
        :return: LetterButton object
        """

        for button in self.all_buttons:
            if button.letter == letter:
                return button

    def change_key_colors(self):
        """
        Changes color of digital keyboard if key not already correct
        """

        for button in self.all_buttons:
            if not button.is_correct:
                text_color = "#000000"
                rect_color = "#d4d6da"
                if self.is_dark:
                    text_color = "#ffffff"
                    rect_color = "#818384"
                button.update_color(rect_color, text_color)

    def reset_keyboard(self):
        """
        Resets every key to default color
        """
        
        for button in self.all_buttons:
            button.is_correct = False
        self.change_key_colors()