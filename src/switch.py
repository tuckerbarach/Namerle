import tkinter as tk


class Switch():
    """
    Creates a custom switch with an off and on mode
    """

    def __init__(self, window, width, height, off_color, on_color, bg_color, is_on, command, bounds=()):
        self.window = window
        self.width     = width
        self.height    = height
        self.off_color = off_color
        self.on_color  = on_color
        self.bg_color  = bg_color
        self.is_on     = is_on
        self.area      = []
        self.ball      = None
        self.command   = command
        self.bounds    = bounds

    def change_canvas_color(self, color):
        """
        Changes the background of the switch
        """

        self.area[0].config(bg=color)

    def change_bg(self, color):
        """
        Changes the color of the switch
        """

        for i in range(1, len(self.area)):
            self.area[0].itemconfig(self.area[i], fill=color)

    def switch_clicked(self, e):
        """
        Calls for the background of switch to be changed, switch to slide over, and call function
        :param e: automatically sent Event object
        """

        self.is_on = not self.is_on
        move_distance = self.width // 2.5 - self.width // 8

        if self.is_on:
            self.change_bg(self.on_color)
            self.area[0].move(self.ball, move_distance, 0)
        else:
            self.change_bg(self.off_color)
            self.area[0].move(self.ball, -1 * (move_distance), 0)

        self.command() # runs switch's function


    def create_switch(self):
        """
        Creates switch object
        :return: Canvas object which displays a switch
        """

        canvas = tk.Canvas(self.window, width=self.width, height=self.height, bg=self.bg_color, highlightthickness=0)
        canvas.pack()
        canvas.update()
        canvas_width = canvas.winfo_width()
        bulge = self.height // 20

        if self.is_on:
            filler = self.on_color
            ball_pos = self.width // 2.5
        else:
            filler = self.off_color
            ball_pos = canvas_width // 8

        left_coord  = (2, 0, canvas_width // 2, self.height) # 134
        right_coord = (canvas_width // 2, 0, canvas_width - 2, self.height) 

        left_arc    = canvas.create_arc(left_coord, start=90, extent=180, width=0, fill=filler)   # left side of switch
        right_arc   = canvas.create_arc(right_coord, start=-90, extent=180, width=0, fill=filler) # right side of switch
        
        self.area.append(canvas)
        self.area.append(left_arc)
        self.area.append(right_arc)
 
        self.square = canvas.create_rectangle(canvas_width // 4, bulge, int(canvas_width / 4 * 3), self.height, width=0, fill=filler)
        self.area.append(self.square)
        diameter = (self.width // 2 - self.width // 8) * 1.25
        on_off = canvas.create_oval(ball_pos, self.height // 6, ball_pos + diameter, self.height // 6 + diameter, width=0, fill="white")
        self.ball = on_off

        # binds switch to run a function if clicked:
        canvas.tag_bind(left_arc, "<ButtonRelease-1>", self.switch_clicked)
        canvas.tag_bind(right_arc, "<ButtonRelease-1>", self.switch_clicked)
        canvas.tag_bind(self.square, "<ButtonRelease-1>", self.switch_clicked)
        canvas.tag_bind(self.ball, "<ButtonRelease-1>", self.switch_clicked)

        return canvas