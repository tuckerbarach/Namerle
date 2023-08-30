import tkinter as tk

class LetterButton():
    """
    Creates a button that has a keyboard key
    """

    dark_mode_square_color  = "#818384"
    dark_mode_letter_color  = "#ffffff"
    light_mode_square_color = "#d4d6da"
    light_mode_letter_color = "#000000"


    def letter_pressed(self, event):
        """
        Calls function when letter is pressed
        :param event: automatically sent Event object
        """

        self.command(self.letter)

    def __init__(self, canvas, x_loc, y_loc, width, height, is_dark, command, is_correct, letter=""):
        self.canvas = canvas
        self.x_loc  = x_loc
        self.y_loc  = y_loc
        self.width  = width
        self.height = height
        self.is_dark  = is_dark
        self.command = command
        self.is_correct = is_correct
        self.letter = letter

        rect_color   = self.light_mode_square_color
        letter_color = self.light_mode_letter_color
        if is_dark:
            rect_color   = self.dark_mode_square_color
            letter_color = self.dark_mode_letter_color

        size = 15
        # reduces size of non-letter keys so they fit:
        if letter == "ENTER" or letter == "BACK":
            size = 12
        self.rect   = self.canvas.create_rectangle(x_loc, y_loc, x_loc + width, y_loc + height, fill=rect_color, width=0)
        self.text = self.canvas.create_text(x_loc + width // 2, y_loc + height // 2,
         fill=letter_color, text=letter, font=('Helvetica', size, 'bold'))

        self.canvas.tag_bind(self.rect, "<ButtonRelease-1>", self.letter_pressed)
        self.canvas.tag_bind(self.text, "<ButtonRelease-1>", self.letter_pressed)

    def update_color(self, rect_color, text_color):
        """
        Calculates which pixel to start drawing on to align keyboard center
        :param rect_color: String for what color to change the key
        :param text_color: String for what color to change the text on the key
        """

        self.canvas.itemconfigure(self.rect, fill=rect_color)
        self.canvas.itemconfigure(self.text, fill=text_color)
