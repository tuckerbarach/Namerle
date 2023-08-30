#!/usr/bin/python
# gui.py

'''Name Guessing Game'''

__version__ = "1.1"
__author__ = 'Tucker Barach'

import tkinter as tk
from tkinter import CENTER, HORIZONTAL, colorchooser 
import random
import os
import datetime
import time
from PIL import Image, ImageFont
import high_scores as hs
import switch
import keyboard as k


# Sets up window:
root = tk.Tk()
root.title("Namerle")
path = os.path.dirname(os.path.abspath(__file__))
height = root.winfo_screenheight()
width  = root.winfo_screenwidth()

start = hs.get_category("/res/stats.txt", 4)
if int(start) == 0:
    starting_color = "#ffffff" # light
    text_color     = "#000000"
    outline_color  = "#d4d6da"
    stats_color    = "#787c7e"
else:
    starting_color = "#121213"
    text_color     = "#ffffff"
    outline_color  = "#3a3a3c"
    stats_color    = "#3a3a3c"

hints = int(hs.get_category("/res/stats.txt", 5))

root.geometry(str(width) + "x" + str(height)) # sets fullscreen
root.configure(bg=starting_color)

GUESSES       = 6
PADDING       = 10

current_objs   = []
all_objs       = []
star_bars      = []
letter_ids     = []
keyboard_ids   = []
squares        = []
possible_names = []
used_chars     = []

used_guesses     = 0
origin_x         = 0
origin_y         = 0
animate_index    = 0
past_guesses     = -1
easy_hint_number = 1
hard_hint_number = 1

letter        = ''
answer        = ""
current_word  = ""
final_word    = ""
start_time    = ""
end_time      = ""
total_time    = ""
date          = ""

word_correct  = False
first_game_on = False
info_on       = False
info_rect     = None
info_text     = None
timer_id      = None
mode_switch   = None
hint_switch   = None
names_switch  = None

number_to_words = {
    1: "1st",
    2: "2nd",
    3: "3rd",
    4: "4th",
    5: "5th",
    6: "6th",
    7: "7th",
    8: "8th",
    9: "9th",
    10: "10th",
    11: "11th",
    12: "12th",
    13: "13th"
}

chars = "abcdefghijklmnopqrstuvwxyz"
file  = open(path + "/../res/new_names.txt", "r") # opens all the names

setting_photo = tk.PhotoImage(file=path + "/../res/settings.png")
leader_photo  = tk.PhotoImage(file=path + "/../res/leader_icon.png")
hint_photo    = tk.PhotoImage(file=path + "/../res/hint_button_icon.png")

names = file.read().split("\n") # creates a list of every name
file.close()

length = tk.IntVar(root)

setting_window  = tk.Toplevel(root)
stat_window     = tk.Toplevel(root)
setting_label   = tk.Label(setting_window, text="SETTINGS", font=('Helvetica Neue', 25, 'bold'), fg=text_color, bg=starting_color)
mode_label      = tk.Label(setting_window, text="Dark Theme", font=('Helvetica Neue', 20, 'normal'), fg=text_color, bg=starting_color)
hint_label      = tk.Label(setting_window, text="Easy Hints", font=('Helvetica Neue', 20, 'normal'), fg=text_color, bg=starting_color)
names_label     = tk.Label(setting_window, text="Enter Anything", font=('Helvetica Neue', 20, 'normal'), fg=text_color, bg=starting_color)

name_length = tk.Scale(root, variable=length, from_=2, to=13, length=130, font=('Helvetica Neue', 18, 'normal'), 
                    label="Name Length:", orient=HORIZONTAL, troughcolor=text_color, fg=text_color, bg=starting_color)
name_length.set(6)
name_length.grid(row=0, column=0, sticky=tk.N+tk.W)

title = tk.Label(root, text="Namerle", font=('Helvetica Neue', 50, 'bold'), fg=text_color, bg=starting_color)
title.grid(row=0, column=1, sticky=tk.N+tk.E+tk.S+tk.W)

buttons_panel = tk.PanedWindow(root, bg=starting_color)
buttons_panel.grid(row=0, column=2, sticky=tk.N+tk.E)

canvas = tk.Canvas(root, width=width, height=height // 5 * 3, bg=starting_color, highlightbackground=starting_color)
canvas.grid(row=1, column=0, columnspan=3)

canvas.update()
x_bound = canvas.winfo_width()
y_bound = canvas.winfo_screenheight() - canvas.winfo_y() - (length.get() * PADDING) # calculates canvas height after manipulation

square_size  = y_bound // 4 * 3 // (GUESSES * 2.5)
starting_pos = (x_bound - square_size * length.get()) // 2 # calculates starting position to draw squares

start = hs.get_category("/res/stats.txt", 4)
is_dark = True
if int(start) == 0:
    is_dark = False

names_num = int(hs.get_category("/res/stats.txt", 6))
names_on = False
if names_num == 0:
    names_on = True


class StatButton():
    """
    Converts a drawn rectangle into a button
    """

    def __init__(self, rect_obj, guesses):
        self.rect_obj = rect_obj
        self.guesses  = guesses


def display_stats(event):
    """
    Opens a GUI with all the data in a preset file
    """

    hs.show_scores_GUI("/res/scores.txt")


def change_bg():
    """
    Changes the background from dark to light mode
    """

    global starting_color, text_color, outline_color, stats_color, start

    start = hs.get_category("/res/stats.txt", 4) # 0 (light) or 1 (dark) resembling which mode to start on
    if int(start) == 0:
        hs.edit_category("/res/stats.txt", 4, 1, False)
        starting_color = "#121213" # dark color
        text_color     = "#ffffff"
        outline_color  = "#3a3a3c" # dark gray
        stats_color    = "#3a3a3c"
        start = 1

        keyboard_obj.is_dark = True
    else:
        hs.edit_category("/res/stats.txt", 4, 1, True)
        starting_color = "#ffffff"
        text_color     = "#000000"
        outline_color  = "#d4d6da" # light gray
        stats_color    = "#787c7e"
        start = 0

        keyboard_obj.is_dark = False
    
    # changes every widgit and object's background:
    root.config(bg=starting_color)
    canvas.config(bg=starting_color, highlightbackground=starting_color)
    stat_window.config(bg=starting_color)
    name_length.config(bg=starting_color, fg=text_color, troughcolor=text_color)
    buttons_panel.config(bg=starting_color)
    title.config(fg=text_color, bg=starting_color)
    setting_window.config(bg=starting_color)
    setting_label.config(bg=starting_color, fg=text_color)
    mode_label.config(bg=starting_color, fg=text_color)
    hint_label.config(bg=starting_color, fg=text_color)
    names_label.config(bg=starting_color, fg=text_color)
    keyboard.config(bg=starting_color, highlightbackground=starting_color)
    canvas.itemconfig(info_rect, fill=text_color)
    canvas.itemconfig(info_text, fill=starting_color)
    keyboard_obj.change_key_colors()
    mode_switch.change_canvas_color(starting_color)
    hint_switch.change_canvas_color(starting_color)
    names_switch.change_canvas_color(starting_color)

    root.update()

    squares_copy = squares.copy()
    letters_copy = letter_ids.copy()

    # if rect or letter is in a word that has been guessed, remove from lists: 
    for obj in all_objs:
        if obj.rect_id in squares_copy:
            squares_copy.remove(obj.rect_id)
        if obj.letter_id in letters_copy:
            letters_copy.remove(obj.letter_id)

    for square in squares_copy:
        canvas.itemconfigure(square, fill=starting_color, outline=outline_color)

    for letter_id in letters_copy:
        canvas.itemconfigure(letter_id, fill=text_color)


def easy_hint():
    """
    Displays a hint which is the letter in the ith position
    """

    global easy_hint_number

    if easy_hint_number == length.get() + 1:
        easy_hint_number = 1
    letter = answer.upper()[easy_hint_number - 1]
    display_info("The " + number_to_words.get(easy_hint_number) + " letter is: " + letter)

    easy_hint_number += 1


def hard_hint():
    """
    Displays a hint which removes a letter that's not in name
    """

    global hard_hint_number

    try:
        all_letters = [x for x in chars.upper() if x not in answer.upper() and x not in used_chars] # adds all letters not in name to list
        letter = random.choice(all_letters) # picks random letter
        used_chars.append(letter)

        display_info(letter + " is not in the name")
        button = keyboard_obj.get_button(letter)
        button.update_color("#3a3a3c", "#ffffff") # turns digital key dark
        button.is_correct = True
        hard_hint_number += 1
    except IndexError:
        display_info("All remaining letters are in the name")


def pick_hint():
    """
    Picks a hint dependant on which type of hint is selected
    """

    if hints == 0:
        hard_hint()
    else:
        easy_hint()


def call_hint():
    """
    Updates which hint mode is selected
    """

    global hints

    # easy hints on:
    if hints == 0:
        hints = 1
        hs.edit_category("/res/stats.txt", 5, 1, False)
    # easy hints off:
    else:
        hints = 0
        hs.edit_category("/res/stats.txt", 5, 1, True)


def change_answers():
    """
    Updates if allowed all letter combinations to be entered or just names
    """

    global names_num, names_on
    if names_num == 0:
        names_num = 1
        names_on = False
        hs.edit_category("/res/stats.txt", 6, 1, False)
    else:
        names_num = 0
        names_on = True
        hs.edit_category("/res/stats.txt", 6, 1, True)


def show_settings():
    """
    Opens a GUI with switch(s) that commit actions
    """

    global setting_window, setting_label, mode_label, hint_label, names_label, names_on, mode_switch, hint_switch, names_switch

    setting_window  = tk.Toplevel(root)
    setting_label   = tk.Label(setting_window, text="SETTINGS", font=('Helvetica Neue', 25, 'bold'), fg=text_color, bg=starting_color)
    mode_label      = tk.Label(setting_window, text="Dark Theme", font=('Helvetica Neue', 20, 'normal'), fg=text_color, bg=starting_color)
    hint_label      = tk.Label(setting_window, text="Easy Hints", font=('Helvetica Neue', 20, 'normal'), fg=text_color, bg=starting_color)
    names_label     = tk.Label(setting_window, text="Enter Anything", font=('Helvetica Neue', 20, 'normal'), fg=text_color, bg=starting_color)
   
    setting_window.title("Settings")

    # https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter:
    size = tuple(int(_) for _ in setting_window.geometry().split('+')[0].split('x'))
    x = int((width / 2 - size[0] / 2) // 2)
    y = int((height / 2 - size[1] / 2) // 3)

    setting_window.geometry("+%d+%d" % (x, y))
    setting_window.geometry("{}x{}".format(width - 2 * x, height // 4))
    setting_window.configure(bg=starting_color)

    setting_label.pack()
    mode_label.pack()

    # choosing which direction switches will open in:
    is_on = True
    if int(start) == 0:
        is_on = False
    easy_on = True
    if hints == 0:
        easy_on = False
    names_on = True
    if names_num == 0:
        names_on = False

    mode_switch = switch.Switch(setting_window, 35, 22, "gray", "#538d4e", starting_color, is_on, command=change_bg)
    mode_switch.create_switch()

    hint_label.pack()

    hint_switch = switch.Switch(setting_window, 35, 22, "gray", "#538d4e", starting_color, easy_on, command=call_hint)
    hint_switch.create_switch()

    names_label.pack()
    names_switch = switch.Switch(setting_window, 35, 22, "gray", "#538d4e", starting_color, names_on, command=change_answers)
    names_switch.create_switch()

settings = tk.Button(buttons_panel, image=setting_photo, bg="white", padx=PADDING, background="black", command=show_settings)
settings.grid(row=0, column=2, sticky=tk.N+tk.E)


def show_stats():
    """
    Opens a GUI that displays statistics of the user's game-playing history
    """

    global stat_bars, stat_window

    stat_window = tk.Toplevel(root)
    stat_window.title("Statistics")

    # https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter:
    size = tuple(int(_) for _ in stat_window.geometry().split('+')[0].split('x'))
    x = (width / 2 - size[0] / 2) // 2
    y = (height / 2 - size[1] / 2) // 3

    stat_window.geometry("+%d+%d" % (x, y))
    stat_window.configure(bg=starting_color)

    stat_label = tk.Label(stat_window, text="STATISTICS", font=('Helvetica Neue', 25, 'bold'), fg=text_color, bg=starting_color)
    stat_label.pack()

    games_played   = hs.get_length("/res/scores.txt") + int(hs.get_category("/res/stats.txt", 1))         # determines games played
    win_percent    = int(games_played / (games_played + int(hs.get_category("/res/stats.txt", 1))) * 100) # calculates winning percentage
    current_streak = hs.get_category("/res/stats.txt", 2)
    max_streak     = hs.get_category("/res/stats.txt", 3)

    stats_panel  = tk.PanedWindow(stat_window, bg=starting_color)
    played_num   = tk.Label(stats_panel, text=str(games_played), font=('Helvetica Neue', 50, 'normal'), fg=text_color, bg=starting_color)
    win_num      = tk.Label(stats_panel, text=str(win_percent), font=('Helvetica Neue', 50, 'normal'), fg=text_color, bg=starting_color)
    streak_num   = tk.Label(stats_panel, text=str(current_streak), font=('Helvetica Neue', 50, 'normal'), fg=text_color, bg=starting_color)
    max_num      = tk.Label(stats_panel, text=str(max_streak), font=('Helvetica Neue', 50, 'normal'), fg=text_color, bg=starting_color)
    played_label = tk.Label(stats_panel, text="Played", font=('Helvetica Neue', 15, 'normal'), fg=text_color, bg=starting_color)
    win_label    = tk.Label(stats_panel, text="Win %", font=('Helvetica Neue', 15, 'normal'), fg=text_color, bg=starting_color)
    streak_label = tk.Label(stats_panel, text="Current\nStreak", font=('Helvetica Neue', 15, 'normal'), fg=text_color, bg=starting_color)
    max_label    = tk.Label(stats_panel, text="Max\nStreak", font=('Helvetica Neue', 15, 'normal'), fg=text_color, bg=starting_color)

    played_num.grid(row=0, column=0)
    win_num.grid(row=0, column=1)
    streak_num.grid(row=0, column=2)
    max_num.grid(row=0, column=3)
    played_label.grid(row=1, column=0)
    win_label.grid(row=1, column=1)
    streak_label.grid(row=1, column=2)
    max_label.grid(row=1, column=3)

    stats_panel.pack()

    guess_label = tk.Label(stat_window, text="GUESS DISTRIBUTION", font=('Helvetica Neue', 25, 'bold'), fg=text_color, bg=starting_color)
    guess_label.pack()

    stat_canvas = tk.Canvas(stat_window, width=width // 2, height=height // 2, bg=starting_color, highlightbackground=starting_color)
    stat_canvas.pack()

    stat_canvas.update()
    x_canvas = stat_canvas.winfo_width()
    y_canvas = stat_canvas.winfo_height()
    
    counts      = hs.get_item("/res/scores.txt", 3)      # gets list of all guesses
    maximum     = max(set(counts), key=counts.count)     # determines which guesss amount is the maximum
    num         = counts.count(maximum)                  # finds how many guesses in the maximum
    rect_length = (x_canvas - x_canvas // 4) // int(num) # sets standard length

    count_x = x_canvas // 10
    count_y = y_canvas // GUESSES

    # displays number in front of rectangle:
    for i in range(GUESSES):
        stat_canvas.create_text(count_x, count_y + (i * count_y // 1.5), text=str(i + 1),
         fill=text_color, font=('Helvetica', 20, 'normal'))

    stat_bars = []

    for i, num in enumerate(set(counts)):
        amt = counts.count(num)
        filler = stats_color
        if int(num) == past_guesses:
            filler = "#538d4e"
        bar = stat_canvas.create_rectangle(count_x + count_x // 4, count_y - 15 + ((int(num) - 1) * count_y // 1.5),
             count_x + count_x // 2 + amt * rect_length, count_y + ((int(num) - 1) * count_y // 1.5 + 15),
              fill=filler, width=0, activefill="#b59f3a")
        
        stat_bars.append(StatButton(bar, num))
        stat_canvas.tag_bind(bar, "<Button-1>", display_stats)
        stat_canvas.create_text(count_x + count_x // 4 + amt * rect_length, count_y + ((int(num) - 1) * count_y // 1.5),
                                text=str(counts.count(num)), fill="white", font=('Helvetica', 20, 'bold'))


hint_button = tk.Button(buttons_panel, image=hint_photo, bg="white", padx=PADDING, command=pick_hint)

leaderboard = tk.Button(buttons_panel, image=leader_photo, bg="white", padx=PADDING, command=show_stats)
leaderboard.grid(row=0, column=1)


def new_game(event):
    """
    Clears the canvas and generates a new template for a new name

    :param event: automatically sent Event object
    """

    global answer, current_word, used_guesses, origin_x, origin_y, letter_ids, easy_hint_number, hard_hint_number
    global squares, start_time, square_size, starting_pos, all_objs, word_correct, possible_names, used_chars, first_game_on
    
    word_correct  = False
    first_game_on = True

    easy_hint_number = 1
    hard_hint_number = 1
    used_guesses     = 0

    used_chars = []
    letter_ids = []
    squares    = []
    all_objs   = []
    
    keyboard_obj.reset_keyboard()
    keyboard.grid(row=2, column=0, columnspan=3)
    hint_button.grid(row=0, column=0, sticky=tk.W)

    current_word = ""
    canvas.delete("all")

    letters  = length.get()
    origin_x = (x_bound - (letters * PADDING)) // letters
    origin_y = y_bound // 5 * 3 // GUESSES


    square_size  = y_bound // 4 * 3 // (GUESSES * 1.35)
    starting_pos = (x_bound - square_size * length.get()) // 2

    x_loc = square_size
    y_loc = y_bound // 20

    # creates grid of squares: 
    for r in range(GUESSES):
        for i in range(length.get()):
            square = canvas.create_rectangle(starting_pos + (x_loc * i) + PADDING, y_loc + PADDING,
            starting_pos + (square_size * (i + 1)), y_loc + square_size, fill=starting_color, outline=outline_color, width=3)
            squares.append(square)
        y_loc += square_size

    possible_names = []

    # adds as names with given name length to list:
    for name in names:
        if len(name) == letters:
            possible_names.append(name)
    
    answer     = random.choice(possible_names)
    start_time = datetime.datetime.now()

    print("Answer: " + answer)


def display_letter():
    """
    Displays a letter onto the canvas fit into a box
    """

    if len(current_word) > 0:
        row = used_guesses
        col = len(current_word)
        x   = starting_pos + (square_size // 2) + ((col - 1) * square_size + PADDING // 2) # gets the X value for which square to fit
        y   = y_bound // 20 + (square_size // 2) + (row * square_size + PADDING)           # gets the Y value for which square to fit
        id  = canvas.create_text(x, y, text=letter, fill=text_color, font=('Helvetica', 30, 'bold'))
        letter_ids.append(id)


def remove_letter():
    """
    Removes the last letter typed from the canvas
    """

    canvas.delete(letter_ids[-1])
    letter_ids.pop()


class SquareLetter:
    """
    Object for every square after name is submitted in that row
    """

    def __init__(self, rect_id, ans_letter, guess_letter, color, is_correct, letter_id):
        self.rect_id      = rect_id
        self.ans_letter   = ans_letter
        self.guess_letter = guess_letter
        self.color        = color
        self.is_correct   = is_correct
        self.letter_id    = letter_id

    def __str__(self):
        return "Rect ID: " + str(self.rect_id) + "\n" +\
                "Color: " + self.color + "\n" +\
                "Correct? " + str(self.is_correct) + "\n" +\
                "Answer Letter: " + self.ans_letter + "\n" +\
                "Guess Letter: " + self.guess_letter + "\n" +\
                "Letter ID: " + str(self.letter_id) + "\n"


def color_squares():
    """
    Colors the squares of each box containing a new letter
    """

    global index, animate_index
    canvas.itemconfigure(current_objs[index].rect_id, fill=current_objs[index].color, outline=current_objs[index].color)
    canvas.itemconfigure(current_objs[index].letter_id, fill="#ffffff")
    canvas.update()

    if index < len(current_objs) - 1:
        root.after(250, color_squares)
    elif final_word == answer.upper():
        animate_index = 0
        animate_answer()

    index += 1


def animate_answer():
    """
    Moves the correct answer boxes up and down
    """

    global animate_index

    for i in range(30):
        canvas.move(current_objs[animate_index].rect_id, 0, -2)
        canvas.move(current_objs[animate_index].letter_id, 0, -2)
        canvas.update()
        
    for i in range(30):
        canvas.move(current_objs[animate_index].rect_id, 0, 2)
        canvas.move(current_objs[animate_index].letter_id, 0, 2)
        canvas.update()
    
    if animate_index < len(answer) - 1:
        root.after(100, animate_answer)
    else:
        show_stats()

    animate_index += 1


def remove_info():
    """
    Removes the instructions from display
    """

    global info_rect, info_text, timer_id, info_on

    # to prevent spamming instructions:
    try:
        canvas.delete(info_rect)
        canvas.delete(info_text)
        root.after_cancel(timer_id)
        info_on = False
    except ValueError:
        pass


def display_info(text, remain_on=False):
    """
    Displays text centered onto the screen
    """

    global info_rect, info_text, timer_id, info_on

    if info_on:
        remove_info()

    info_on = True

    characters = list(text)

    rect_length = len(characters) * 18 # 18 is width of each character

    x_val = x_bound // 2  - rect_length // 2
    y_val = y_bound // 25

    info_rect = canvas.create_rectangle(x_val, y_val, x_val + rect_length, y_val * 2, fill=text_color)
    info_text = canvas.create_text(x_val, y_val + y_val // 2, text=text, fill=starting_color, font=('Menlo', 30, 'bold'), anchor=tk.W)

    if not remain_on:
        timer_id = root.after(1000, remove_info) # instructions disappear after a second


def calculate_time():
    """
    Calculates the total time taken from when game is created to answer is guessed
    """

    global total_time
    total_time = end_time - start_time
    total_time = round(total_time.total_seconds(), 3)


def check_guess():
    """
    Determines whether the user's guess matches the answer
    """

    global used_guesses, current_word, end_time, final_word, date, past_guesses, word_correct

    if not names_on or current_word.lower().capitalize() in possible_names:

        final_word = current_word.upper()
        calculate_colors()

        if current_word.upper() == answer.upper():
            word_correct = True
            past_guesses = used_guesses + 1

            end_time =  datetime.datetime.now()
            date     = time.asctime(time.localtime(time.time()))

            calculate_time()

            id = str(hs.next_id("/res/scores.txt"))

            hs.add_score("/res/scores.txt", id + "," + date + "," + answer + "," + str(past_guesses) + "," + str(total_time))
            hs.edit_category("/res/stats.txt", 2, 1, False)

            current_max    = int(hs.get_category("/res/stats.txt", 3))
            current_streak = int(hs.get_category("/res/stats.txt", 2))

            if current_streak > current_max:
                hs.edit_category("/res/stats.txt", 3, 1, False)

        elif used_guesses + 1 >= GUESSES:
            print("Game Over!\nCorrect Word: " + answer)
            end_time =  datetime.datetime.now()
            calculate_time()
            display_info(answer)
            hs.edit_category("/res/stats.txt", 1, 1, False)
            hs.edit_category("/res/stats.txt", 2, 0, True)
            past_guesses = -1
            
        used_guesses += 1
        current_word = "" # resets typed guessed
    
    else:
        display_info("Not a real name!")


def keyboard_pressed(l):
    """
    Operates digital keyboard

    :param l: String for the letter of digital key that was pressed
    """

    global letter, current_word

    if l == "BACK":
        if len(current_word) > 0:
            remove_letter()
            current_word = current_word[:-1]

    elif l.lower() in chars and len(current_word) < length.get() and not word_correct:
        letter = l.upper()
        current_word += letter.upper()
        display_letter()
    
    elif l == "ENTER":
        if len(current_word) == length.get():
            remove_info()
            check_guess()


def letter_pressed(event):
    """
    Operates phyiscal keyboard

    :param event: an Event object automatically sent
    """

    global letter, current_word

    if event.keysym == "BackSpace":
        if len(current_word) > 0:
            remove_letter()
            current_word = current_word[:-1]

    elif first_game_on and event.char in chars and len(current_word) < length.get() and not word_correct:
        letter = event.char.upper()
        current_word += letter.upper()
        display_letter()
    
    elif event.keysym == "Return":
        if len(current_word) == length.get():
            remove_info()
            check_guess()

keyboard_obj = k.Keyboard(root, 44, 58, width, height, is_dark, keyboard_pressed, 6)
keyboard = keyboard_obj.create_keyboard()
root.update()


def calculate_colors():
    """
    Calculates the colors of each square based off the letter inside the square
    """

    global current_objs, index
    index = 0

    remain_answer = answer.upper()
    remain_guess = current_word.upper()

    current_objs = []
    current_squares = squares[0: length.get()]
    for i in range(len(answer)):
        rect_id = current_squares[i] + (length.get() * used_guesses)
        letter_id = letter_ids[i + length.get() * used_guesses]
        ans_letter = answer.upper()[i]
        guess_letter = current_word.upper()[i]

        letter_obj = SquareLetter(rect_id, ans_letter, guess_letter, "#3a3a3c", False, letter_id)
        current_objs.append(letter_obj)
        all_objs.append(letter_obj)

    for letter in current_word.upper():
        if letter not in remain_answer.upper():
            button = keyboard_obj.get_button(letter)
            button.update_color("#3a3a3c", "#ffffff")
            button.is_correct = True

    objs_copy = current_objs.copy()
    for i, square in enumerate(current_objs): # green:
        if square.guess_letter == square.ans_letter:
            square.color = "#538d4e"
            square.is_correct = True
            button = keyboard_obj.get_button(square.guess_letter)
            button.update_color("#538d4e", "#ffffff")
            button.is_correct = True

    remain_objs = [x for x in objs_copy if not x.is_correct]
    remain_answer = "".join([x.ans_letter for x in objs_copy if not x.is_correct])
    remain_guess = "".join([x.guess_letter for x in objs_copy if not x.is_correct])

    for i, square in enumerate(remain_objs):
        remain_count = remain_guess.count(square.guess_letter)

        if remain_count > 0 and square.guess_letter in remain_answer.upper():
            square.color = "#b59f3a"
            square.is_correct = True
            remain_answer = remain_answer.replace(square.guess_letter, "", 1)
            remain_guess = "".join([x.guess_letter for x in objs_copy if not x.is_correct])
            button = keyboard_obj.get_button(square.guess_letter)
            if not button.is_correct:
                button.update_color("#b59f3a", "#ffffff")
                button.is_correct = True


    color_squares()


name_length.bind("<ButtonRelease-1>", new_game)
root.bind("<KeyRelease>", letter_pressed)

display_info("Select name length in top left corner to begin!", remain_on=True)

root.mainloop()