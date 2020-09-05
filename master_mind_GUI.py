from graphics import *

##########################-Constants-#########################################
BLANK = 0
BLANK_DOT = -1
COLORS = ["cyan", "purple", "blue", "green", "yellow", "red"]
PEGS = ["grey", "white", "black"]
GAME_SIZE = 7
ROW_SIZE = 4
LINE_X_START = 3.5
LINE_Y_START = 2
LINE_DISTANCE = 3
DOT_SIZE = 1
DOT_DISTANCE = 2.5
PEG_BOX_X = 12.7
PEG_BOX_Y = 1
BOX_SIZE = 2
PEGS_START_POS_X = 13.2
PEGS_START_POS_Y = 1.5
PEG_SIZE = 0.4
BUTTON_X = 15.5
BUTTON_WIDTH = 3
BUTTON_Y = 1.2
BUTTON_HEIGHT = 1.6
BUTTON_TEXT_POS = 17
BUTTON_TEXT_SIZE = 2
NR_POS_X = 1.5
NR_POS_Y = 2
RIGHT_PLACE = 2
WRONG_PLACE = 1


##########################-Visuals-#########################################
def create_dots():
    """Create all colored dots to be on the board"""
    hidden_dots = []
    for i in range(GAME_SIZE):
        row = []
        for x in range(ROW_SIZE):
            row.append(Circle(Point(LINE_X_START + DOT_DISTANCE * x,
                                    LINE_Y_START + LINE_DISTANCE * i), DOT_SIZE))
        hidden_dots.append(row)
    #dot_map will track the color of each result dot as
    #the graphics package offers no getColor function
    #NOTE: Global structures are normally not good practice, 
    #its only purpose here is to simplify call interface for students
    global dot_map
    dot_map = []
    for _ in range(GAME_SIZE):
        row = []
        for _ in range(ROW_SIZE):
            row.append(BLANK_DOT)
        dot_map.append(row)
    return hidden_dots


def create_pegs():
    """Create dots for result display"""
    hidden_pegs = []
    for _ in range(GAME_SIZE):
        row = []
        for _ in range(ROW_SIZE):
            row.append(BLANK)
        hidden_pegs.append(row)
    #Make circle and set initial color assignments for peg dots.
    for i in range(GAME_SIZE):
        for x in range(ROW_SIZE):
            hidden_pegs[i][x] = Circle(Point(PEGS_START_POS_X + (x%2),
                                             PEGS_START_POS_Y + i * LINE_DISTANCE + x//2), PEG_SIZE)
            hidden_pegs[i][x].setFill(PEGS[BLANK])
    #peg_map will track the color of each result dot as
    #the graphics package offers no getColor function
    #NOTE: Global structures are normally not good practice, 
    #its only purpose here is to simplify call interface for students
    global peg_map
    peg_map = []
    for _ in range(GAME_SIZE):
        row = []
        for _ in range(ROW_SIZE):
            row.append(BLANK)
        peg_map.append(row)
    return hidden_pegs


#This will draw four colored dots to represent guess.
def make_guess(guess, win):
    """The chooses a guessed color code line by clicking the dots"""
    draw_line(guess, win)
    submit_guess = False
    while not submit_guess:
        click = win.getMouse()
        edit_dot = -1
        for i in range(ROW_SIZE):
            if click.x >= LINE_X_START - DOT_SIZE + i*DOT_DISTANCE and \
                click.x <= LINE_X_START + DOT_SIZE + i*DOT_DISTANCE:
                edit_dot = i
                break

        if edit_dot != -1:
            dots[guess][edit_dot].undraw()
            dot_map[guess][edit_dot] = (dot_map[guess][edit_dot] + 1) % len(COLORS)
            color = COLORS[dot_map[guess][edit_dot]]
            dots[guess][edit_dot].setFill(color)
            dots[guess][edit_dot].draw(win)

        if (click.x >= BUTTON_X and click.x <= BUTTON_X + BUTTON_WIDTH)\
            and (BLANK_DOT not in dot_map[guess]):
            if click.y >= BUTTON_Y and click.y <= BUTTON_Y + BUTTON_HEIGHT:
                submit_guess = True
        new_guess = dot_map[guess].copy()

    return new_guess


def draw_submit_button(win):
    """Draws "submit button" in lower right corner"""
    Rectangle(Point(BUTTON_X, BUTTON_Y),
              Point(BUTTON_X + BUTTON_WIDTH, BUTTON_Y + BUTTON_HEIGHT)).draw(win)
    Text(Point(BUTTON_TEXT_POS, LINE_Y_START), "Submit").draw(win)


def draw_line(guess, win):
    """Draws the visual objects for a guess line beside."""
    Text(Point(NR_POS_X, NR_POS_Y + LINE_DISTANCE * guess), str(guess+1)).draw(win)
    Rectangle(Point(PEG_BOX_X, PEG_BOX_Y + guess * LINE_DISTANCE),
              Point(PEG_BOX_X + BOX_SIZE,
                    PEG_BOX_Y + BOX_SIZE + guess * LINE_DISTANCE)).draw(win)
    for i in range(ROW_SIZE):
        dots[guess][i].setFill("white")
        dots[guess][i].draw(win)
    for i in range(ROW_SIZE):
        pegs[guess][i].draw(win)


def peg_feedback(guess, correct, wrong_place, win):
    """Draws the result pegs for a guess line"""
    for i in range(correct):
        peg_map[guess][i] = 2
    for i in range(correct, correct + wrong_place):
        peg_map[guess][i] = 1
    for i in range(ROW_SIZE):
        color = PEGS[peg_map[guess][i]]
        pegs[guess][i].undraw()
        pegs[guess][i].setFill(color)
        pegs[guess][i].draw(win)


def welcome_window():
    welcome = GraphWin("Welcome to Mastermind, DV1574 edition", 500, 300)
    welcome.setCoords(0, 0, 10, 10)
    welcome.setBackground("light yellow")
    Text(Point(5, 9),
         "Guess my secret 4-dot color code by clicking the dots").draw(welcome)
    Text(Point(5, 8),
         "The available colors are cyan, purple, blue, green, yellow, red").draw(welcome)
    Text(Point(5, 7),          
         "I will guide you using the small circle dots next to the code").draw(welcome)
    Text(Point(5, 6),
         "A black dot means you have a correct color in the correct spot").draw(welcome)
    Text(Point(5, 5),
         " A white dot means you have a correct color but in the wrong spot").draw(welcome)
    Text(Point(5, 3), "CLICK to continue.").draw(welcome)
    welcome.getMouse()
    welcome.close()


def create_GUI():
    welcome_window()

    win = GraphWin("Mastermind, DV1574 edition", 466, 550)
    win.setCoords(0.0, 0.0, 19.6, 23.5)
    win.setBackground("gray")

    global pegs
    pegs = create_pegs()

    global dots
    dots = create_dots()

    play_box = Rectangle(Point(.25, .25), Point(19.5, 23.25))
    play_box.setFill("white")
    play_box.draw(win)
    Text(Point(1.5, 21), "Guess #").draw(win)

    #Display Banner on top of display.
    banner = Text(Point(9, 22), "Master Mind!")
    banner.setFace("times roman")
    banner.setSize(15)
    banner.setStyle("bold")
    banner.setFill("Black")
    banner.draw(win)

    start_text = Text(Point(10, 15), "CLICK to start the game!")
    start_text.draw(win)

    win.getMouse()
    start_text.undraw()
    draw_submit_button(win)
    return win


def gameover_screen(guesses, string):
    win = GraphWin("Game Over!", 500, 500)
    win.setCoords(0.0, 0.0, 30.0, 30.0)
    if string == "Winner":

        win.setBackground("light green")

        message = Text(Point(11, 29), "You guessed the code in only")
        message.setFace("times roman")
        message.setSize(15)
        message.setStyle("bold")
        message.draw(win)

        message2 = Text(Point(15, 27), (guesses, "guesses!!!"))
        message2.setFace("times roman")
        message2.setSize(20)
        message2.setStyle("bold")

    else:
        win.setBackground("red")
        message = Text(Point(11, 29), "Sorry")
        message.setFace("times roman")
        message.setSize(15)
        message.setStyle("bold")
        message.draw(win)

        message2 = Text(Point(15, 27), "You Lost!!!")
        message2.setFace("times roman")
        message2.setSize(20)
        message2.setStyle("bold")

    message2.draw(win)

    quit_box = Rectangle(Point(25, .25), Point(29.75, 2))
    quit_box.setFill("black")
    quit_box.draw(win)

    quit_mess = Text(Point(27, 1), "Quit")
    quit_mess.setFill("white")
    quit_mess.setStyle("bold")
    quit_mess.draw(win)

    closing = False
    while not closing:
        click = win.getMouse()
        if click.y >= .25 and click.y <= 2:
            closing = True
    win.close()
    return
