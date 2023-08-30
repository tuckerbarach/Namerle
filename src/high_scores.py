#!/usr/bin/python
# high_scores.py

'''Leaderboard Methods'''

__version__ = "1.1"
__author__ = 'Tucker Barach'

import tkinter as tk
import os

class Score():
    def __init__(self, id, date, answer, guesses, time):
        """
        creates Score object

        :param id: an int for starting ID of score
        :param date: a String for current date of game played 
        :param answer: a String for correct answer of game
        :param guesses: an int for how many guesses it took to win
        :param time: a float for seconds to complete game
        """

        self.id      = id
        self.date    = date
        self.answer  = answer
        self.guesses = guesses
        self.time    = time

    def __str__(self):
        """
        how a Score object should be printed neatly
        """

        return "ID: " + self.id + " " + self.date + ": " + self.answer + ", " + self.guesses + ", " + self.time


def read_scores(file_name):
    """
    reads the contents of a file with values seperated by commas

    :param filename: a String for local file path
    """

    path = os.path.dirname(os.path.abspath(__file__)) # gets absolute file path

    with open(path + "/.." + file_name) as f:
        contents = f.readlines()[1:]
    
    scores = []
    for line in contents:
        values = line.split(",")
        scores.append(Score(values[0], values[1], values[2], values[3], values[4])) # creates new score object
    
    return scores


def show_scores(file_name):
    """
    prints the contents of a file with values seperated by commas

    :param filename: a String for local file path
    """

    path = os.path.dirname(os.path.abspath(__file__)) # gets absolute file path
    for score in read_scores(path + file_name):
        print(score)


def show_scores_GUI(file_name):
    """
    shows the contents of a file with values seperated by commas in a GUI

    :param filename: a String for local file path
    """

    root = tk.Tk()
    root.title("High Scores")

    scores = read_scores(file_name) # gets contents of file

    id_list      = tk.Listbox(root)
    date_list    = tk.Listbox(root)
    answer_list  = tk.Listbox(root)
    guesses_list = tk.Listbox(root)
    time_list    = tk.Listbox(root)

    # appending all items to list boxes:
    for item in scores:
        id_list.insert(tk.END, item.id)
        date_list.insert(tk.END, item.date)
        answer_list.insert(tk.END, item.answer)
        guesses_list.insert(tk.END, item.guesses)
        time_list.insert(tk.END, item.time)

    # displaying list boxes:  
    id_list.grid(row=0, column=0)
    date_list.grid(row=0, column=1)
    answer_list.grid(row=0, column=2)
    guesses_list.grid(row=0, column=3)
    time_list.grid(row=0, column=4)

    root.mainloop()


def add_score(file_name, data):
    """
    adds a new score to the contents of a file

    :param filename: a String for local file path
    :param data: a String for new data to be added
    """

    path = os.path.dirname(os.path.abspath(__file__)) # gets absolute file path
    file = open(path + file_name, "a")
    file.write("\n" + str(data))                      # adds new score to end of file
    file.close()


def clear_scores(file_name, first_line):
    """
    clears the contents of a file and keeps first line

    :param filename: a String for local file path
    :param first_line: a String for first line of file
    """

    file = open(file_name, "w")
    file.write(first_line) # keeps the first line which isn't score data
    file.close()


def next_id(file_name):
    """
    returns the next ID for new data to be added

    :param filename: a String for local file path
    :return: an int for next ID
    """

    returns = get_item(file_name, 0)
    return int(returns[-1]) + 1


def remove(file_name, id_to_delete):
    """
    removes a specific line to delted from an ID

    :param filename: a String for local file path
    :param id_to_delete: an int for ID to delete
    """

    scores     = read_scores(file_name) # gets contents of file
    id_removed = False
    file       = open(file_name, "w")

    file.write("ID, Date, Name, Gusses, Time:\n") # keeps first line of file
    for score in scores:
        if score.id == str(id_to_delete):
            id_removed = True
        else:
            if id_removed:
                score.id = str(int(score.id) - 1) # changes ID after deleted item by one
            file.write(score.id + "," + score.date + "," + score.answer + "," + score.guesses + "," + score.time)
    file.close()


def get_item(file_name, index):
    """
    returns a list of a Score variable

    :param filename: a String for local file path
    :param index: an int for which parameter to return
    :return: list of a file's category
    """

    path = os.path.dirname(os.path.abspath(__file__)) # gets absolute file path

    with open(path + "/.." + file_name) as f:
        contents = f.readlines()[1:]

    returns = []
    for line in contents:
        values = line.split(",")
        returns.append(values[index])
    
    return returns


def get_length(file_name):
    """
    returns the length of file which is how many score entries there are

    :param filename: a String for local file path
    :return: an int of length of file
    """

    path = os.path.dirname(os.path.abspath(__file__)) # gets absolute file path
    with open(path + "/.." + file_name) as f:
        contents = f.read()

    return contents.count("\n")
        

def get_category(file_name, line_number):
    """
    returns the value of a category

    :param filename: a String for local file path
    :param line_number: an int of line number of the stat to return
    :return: a String of the value stored on line_number line
    """

    path = os.path.dirname(os.path.abspath(__file__)) # gets absolute file path
    with open(path + "/.." + file_name) as f:
        contents = f.readlines()[1:]

    for i, line in enumerate(contents):
        if line_number == i + 1:
            return line.split(",")[1].replace("\n", "")
    return -1


def edit_category(file_name, line_number, change, to_zero):
    """
    edits a line number with the new statsitic to be written

    :param filename: a String for local file path
    :param line_number: an int of line number of the stat to overwrite
    :param change: an int for the change of value to write
    :param to_zero: a boolean if the stat should be changed to 0
    """

    path = os.path.dirname(os.path.abspath(__file__)) # gets absolute file path

    with open(path + "/.." + file_name) as f:
        contents = f.readlines()[1:]

    file = open(path + "/.." + file_name, "w")
    file.write("Statistics:")

    for i, line in enumerate(contents):

        line = line.replace("\n", "")
        if line_number == i + 1:
            split = line.split(",")
            if not to_zero:
                file.write("\n" + split[0] + "," + str(int(split[1]) + change))
            else:
                file.write("\n" + split[0] + ",0")
        else:
            file.write("\n" + line)

    file.close()