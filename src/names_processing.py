import os

def run():
    """
    Processes file of all names and metadata into just names
    """

    all_names = []
    path = os.path.dirname(os.path.abspath(__file__))
    file  = open(path + "/res/MA.TXT", "r") # opens all the names
    lines = file.read().split("\n") # creates a list of every name
    file.close()

    for line in lines:
        line = line.split(",")
        if int(line[2]) >= 1950 and line[3] not in all_names:
            all_names.append(line[3])

    new_file = open("new_names.txt", "w+")
    for name in all_names:
        new_file.write(name + "\n")
    new_file.close()

run()