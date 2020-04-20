
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: n10103881
#    Student name: MARY TERESA JOSEPH
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Task Description-----------------------------------------------#
#
#  NOT CONNECT-4
#
#  This assignment tests your skills at processing data stored in
#  lists, creating reusable code and following instructions to display
#  a complex visual image.  The incomplete Python program below is
#  missing a crucial function, "play_game".  You are required to
#  complete this function so that when the program is run it fills
#  a grid with various rectangular tokens, using data stored in a
#  list to determine which tokens to place and where.  See the
#  instruction sheet accompanying this file for full details.
#
#  Note that this assignment is in two parts, the second of which
#  will be released only just before the final deadline.  This
#  template file will be used for both parts and you will submit
#  your final solution as a single Python 3 file, whether or not you
#  complete both parts of the assignment.
#
#--------------------------------------------------------------------#  



#-----Preamble-------------------------------------------------------#
#
# This section imports necessary functions and defines constant
# values used for creating the drawing canvas.  You should not change
# any of the code in this section.
#

# Import the functions needed to complete this assignment.  You
# should not need to use any other modules for your solution.  In
# particular, your solution must NOT rely on any non-standard Python
# modules that need to be downloaded and installed separately,
# because the markers will not have access to such modules.
from turtle import *
from math import *
from random import *
import time

# Define constant values for setting up the drawing canvas
cell_size = 100 # pixels (default is 100)
num_columns = 7 # cells (default is 7)
num_rows = 6 # cells (default is 6)
x_margin = cell_size * 2.75 # pixels, the size of the margin left/right of the board
y_margin = cell_size // 2 # pixels, the size of the margin below/above the board
canvas_height = num_rows * cell_size + y_margin * 2
canvas_width = num_columns * cell_size + x_margin * 2

# Validity checks on board size
assert cell_size >= 80, 'Cells must be at least 80x80 pixels in size'
assert num_columns >= 7, 'Board must be at least 7 columns wide'
assert num_rows >= 6, 'Board must be at least 6 rows high'

#
#--------------------------------------------------------------------#



#-----Functions for Creating the Drawing Canvas----------------------#
#
# The functions in this section are called by the main program to
# manage the drawing canvas for your image.  You should not change
# any of the code in this section.
#

# Set up the canvas and draw the background for the overall image
def create_drawing_canvas(mark_legend_spaces = True, # show text for legend
                          mark_axes = True, # show labels on axes
                          bg_colour = 'light grey', # background colour
                          line_colour = 'slate grey'): # line colour for board
    
    # Set up the drawing canvas with enough space for the board and
    # legend
    setup(canvas_width, canvas_height)
    bgcolor(bg_colour)

    # Draw as quickly as possible
    tracer(False)

    # Get ready to draw the board
    penup()
    color(line_colour)
    width(2)

    # Determine the left-bottom coords of the board
    left_edge = -(num_columns * cell_size) // 2 
    bottom_edge = -(num_rows * cell_size) // 2

    # Draw the horizontal grid lines
    setheading(0) # face east
    for line_no in range(0, num_rows + 1):
        penup()
        goto(left_edge, bottom_edge + line_no * cell_size)
        pendown()
        forward(num_columns * cell_size)
        
    # Draw the vertical grid lines
    setheading(90) # face north
    for line_no in range(0, num_columns + 1):
        penup()
        goto(left_edge + line_no * cell_size, bottom_edge)
        pendown()
        forward(num_rows * cell_size)

    # Mark the centre of the board (coordinate [0, 0])
    penup()
    home()
    dot(10)

    # Optionally label the axes
    if mark_axes:

        # Define the font and position for the labels
        small_font = ('Arial', (18 * cell_size) // 100, 'normal')
        y_offset = (27 * cell_size) // 100 # pixels

        # Draw each of the labels on the x axis
        penup()
        for x_label in range(0, num_columns):
            goto(left_edge + (x_label * cell_size) + (cell_size // 2), bottom_edge - y_offset)
            write(chr(x_label + ord('a')), align = 'center', font = small_font)

        # Draw each of the labels on the y axis
        penup()
        x_offset, y_offset = 7, 10 # pixels
        for y_label in range(0, num_rows):
            goto(left_edge - x_offset, bottom_edge + (y_label * cell_size) + (cell_size // 2) - y_offset)
            write(str(y_label + 1), align = 'right', font = small_font)

    # Optionally mark the spaces for drawing the legend
    if mark_legend_spaces:
        # Font for marking the legend's position
        big_font = ('Arial', (24 * cell_size) // 100, 'normal')
        # Left side
        goto(-(num_columns * cell_size) // 2 - 50, -25)
        write('Put your token\ndescriptions here', align = 'right', font = big_font)    
        # Right side
        goto((num_columns * cell_size) // 2 + 50, -25)
        write('Put your token\ndescriptions here', align = 'left', font = big_font)    

    # Reset everything ready for the student's solution
    pencolor('black')
    width(1)
    penup()
    home()
    tracer(True)
   

# End the program and release the drawing canvas to the operating
# system.  By default the cursor (turtle) is hidden when the
# program ends.  Call the function with False as the argument to
# prevent this.
def release_drawing_canvas(hide_cursor = True):
    tracer(True) # ensure any drawing still in progress is displayed
    if hide_cursor:
        hideturtle()
    done()
    
#
#--------------------------------------------------------------------#



#-----Test Data for Use During Code Development----------------------#
#
# The "fixed" data sets in this section are provided to help you
# develop and test your code.  You can use them as the argument to
# the "play_game" function while perfecting your solution.  However,
# they will NOT be used to assess your program.  Your solution will
# be assessed using the "random_game" function appearing below.
# Your program must work correctly for any data set that can be
# generated by the "random_game" function.
#
# Each of the data sets is a list of instructions, each specifying
# in which column to drop a particular type of game token.  The
# general form of each instruction is
#
#     [column, token_type]
#
# where the columns range from 'a' to 'g' and the token types
# range from 1 to 4.
#
# Note that the fixed patterns below all assume the board has its
# default dimensions of 7x6 cells.
#

# The following data sets each draw just one token type once
fixed_game_a0 = [['a', 1]]
fixed_game_a1 = [['b', 2]]
fixed_game_a2 = [['c', 3]]
fixed_game_a3 = [['d', 4]]

# The following data sets each draw just one type
# of token multiple times
fixed_game_a4 = [['c', 1], ['f', 1], ['g', 1], ['c', 1]] 
fixed_game_a5 = [['d', 2], ['d', 2], ['a', 2], ['c', 2]] 
fixed_game_a6 = [['c', 3], ['f', 3], ['g', 3], ['c', 3]] 
fixed_game_a7 = [['f', 4], ['f', 4], ['c', 4], ['c', 4]]

# The following small data sets each draw all four kinds
# of token
fixed_game_a8 = [['e', 3], ['e', 4], ['f', 3], ['e', 1],
                 ['c', 2], ['g', 4]]
fixed_game_a9 = [['g', 3], ['d', 4], ['b', 3], ['e', 1],
                 ['f', 2], ['g', 4], ['c', 2], ['g', 4]]
fixed_game_a10 = [['f', 3], ['d', 1], ['c', 3], ['c', 4],
                  ['e', 2], ['b', 1], ['b', 3]]
fixed_game_a11 = [['e', 3], ['c', 3], ['d', 3], ['c', 2],
                  ['c', 3], ['d', 4], ['a', 4], ['f', 1]]
fixed_game_a12 = [['f', 1], ['b', 4], ['f', 1], ['f', 4],
                  ['e', 2], ['a', 3], ['c', 3], ['b', 2],
                  ['a', 2]]
fixed_game_a13 = [['b', 3], ['f', 4], ['d', 4], ['b', 1],
                  ['b', 4], ['f', 4], ['b', 2], ['c', 4],
                  ['d', 3], ['a', 1], ['g', 3]]
fixed_game_a14 = [['c', 1], ['c', 4], ['g', 2], ['d', 4],
                  ['d', 1], ['f', 3], ['f', 4], ['f', 1],
                  ['g', 2], ['c', 2]]
fixed_game_a15 = [['d', 3], ['d', 4], ['a', 1], ['c', 2],
                 ['g', 3], ['d', 3], ['g', 1], ['a', 2],
                 ['a', 2], ['f', 4], ['a', 3], ['c', 2]]

# The following large data sets are each a typical game
# as generated by the "play_game" function.  (They are
# divided into five groups whose significance will be
# revealed in Part B of the assignment.)
fixed_game_b0_0 = [['d', 4], ['e', 1], ['f', 1], ['d', 1],
                   ['e', 2], ['c', 3], ['a', 2], ['e', 4],
                   ['g', 1], ['d', 4], ['a', 2], ['f', 2]]
fixed_game_b0_1 = [['f', 3], ['a', 2], ['d', 2], ['f', 4],
                   ['b', 2], ['a', 2], ['f', 3], ['f', 3],
                   ['e', 1], ['b', 2], ['e', 1], ['c', 1],
                   ['a', 3], ['d', 3], ['f', 1], ['f', 4],
                   ['b', 4], ['b', 1], ['c', 4], ['d', 1],
                   ['a', 3], ['e', 1], ['b', 2], ['c', 3],
                   ['d', 3], ['c', 2], ['c', 1], ['a', 2],
                   ['d', 4], ['b', 4], ['g', 2]]
fixed_game_b0_2 = [['d', 3], ['d', 4], ['a', 4], ['g', 3],
                   ['d', 2], ['g', 2], ['f', 1], ['b', 2],
                   ['a', 1], ['a', 3], ['a', 4], ['c', 3],
                   ['f', 3], ['b', 2], ['c', 3], ['a', 4],
                   ['g', 1]]

fixed_game_b1_0 = [['e', 3], ['a', 4], ['c', 2], ['f', 1],
                   ['a', 1], ['c', 4], ['g', 3], ['d', 1],
                   ['f', 3], ['d', 1], ['f', 1], ['g', 1],
                   ['e', 3], ['f', 3], ['f', 3], ['e', 4],
                   ['b', 2], ['a', 2], ['g', 1], ['d', 1],
                   ['a', 1], ['a', 1]]
fixed_game_b1_1 = [['f', 3], ['g', 1], ['g', 2], ['b', 1],
                   ['c', 2], ['c', 2], ['f', 3], ['g', 3],
                   ['b', 4], ['g', 4], ['d', 4], ['b', 1],
                   ['e', 3], ['e', 3], ['a', 2], ['c', 1],
                   ['f', 4], ['f', 3], ['e', 3], ['a', 2],
                   ['f', 4], ['g', 1], ['f', 4], ['a', 1]]
fixed_game_b1_2 = [['d', 2], ['f', 1], ['f', 1], ['c', 1],
                   ['c', 4], ['c', 4], ['d', 1], ['d', 4],
                   ['b', 2], ['d', 4], ['b', 1], ['d', 3],
                   ['d', 1], ['a', 1], ['f', 2], ['c', 2],
                   ['c', 4], ['c', 1], ['g', 1], ['g', 1],
                   ['g', 4], ['g', 2], ['a', 1], ['g', 1],
                   ['f', 2], ['e', 4], ['b', 1], ['e', 3],
                   ['b', 4], ['a', 4], ['b', 1], ['a', 4],
                   ['f', 2], ['g', 2], ['a', 1], ['f', 4],
                   ['e', 1], ['b', 4], ['a', 4], ['e', 2],
                   ['e', 3], ['e', 1]]

fixed_game_b2_0 = [['g', 2], ['d', 2], ['f', 2], ['f', 2],
                   ['b', 2], ['e', 1], ['d', 1], ['d', 3],
                   ['e', 1], ['e', 1], ['b', 1], ['b', 1],
                   ['d', 3], ['f', 3], ['d', 3]]
fixed_game_b2_1 = [['c', 2], ['g', 3], ['e', 4], ['g', 2],
                   ['a', 2], ['f', 2], ['f', 2], ['c', 1],
                   ['d', 2], ['b', 3], ['f', 2], ['d', 4],
                   ['b', 4], ['e', 2], ['g', 3], ['b', 4],
                   ['a', 1], ['g', 3], ['f', 1], ['e', 4],
                   ['d', 3], ['a', 1], ['a', 1], ['d', 2],
                   ['g', 3], ['d', 2], ['c', 4], ['f', 2],
                   ['g', 1], ['e', 4], ['f', 3], ['e', 3],
                   ['e', 3], ['b', 1], ['d', 2], ['c', 1],
                   ['c', 3]]
fixed_game_b2_2 = [['e', 2], ['b', 2], ['e', 2], ['g', 2],
                   ['f', 3], ['e', 3], ['e', 2], ['g', 2],
                   ['d', 2], ['e', 2], ['a', 1], ['c', 2],
                   ['e', 2], ['a', 3], ['f', 1], ['a', 3],
                   ['d', 2], ['g', 3], ['b', 4], ['b', 2],
                   ['f', 2], ['g', 4], ['d', 3], ['f', 1],
                   ['d', 3], ['a', 1], ['a', 4], ['g', 1],
                   ['f', 3], ['b', 3], ['c', 4], ['a', 3],
                   ['g', 2], ['c', 1], ['f', 3], ['b', 2],
                   ['b', 4], ['c', 3], ['d', 4], ['c', 4],
                   ['d', 1], ['c', 1]]

fixed_game_b3_0 = [['b', 2], ['d', 4], ['g', 2], ['e', 3],
                   ['d', 3], ['f', 4], ['g', 3], ['a', 3],
                   ['g', 2], ['d', 4], ['g', 4], ['f', 4],
                   ['a', 4], ['a', 4], ['f', 2], ['b', 1]]
fixed_game_b3_1 = [['d', 2], ['b', 2], ['e', 4], ['e', 3],
                   ['d', 3], ['c', 2], ['e', 3], ['b', 4],
                   ['b', 4], ['d', 4], ['f', 1], ['c', 2],
                   ['a', 1], ['e', 3], ['b', 4], ['f', 3],
                   ['c', 3], ['b', 3], ['c', 2], ['b', 2],
                   ['d', 3], ['e', 4], ['f', 2], ['g', 3],
                   ['g', 4], ['e', 2], ['c', 1], ['d', 3],
                   ['d', 1], ['f', 3], ['g', 3], ['f', 3],
                   ['c', 3], ['g', 4], ['g', 3], ['g', 3]]
fixed_game_b3_2 = [['a', 2], ['c', 1], ['f', 2], ['d', 2],
                   ['a', 3], ['c', 2], ['b', 3], ['e', 3],
                   ['e', 3], ['f', 4], ['a', 1], ['a', 2],
                   ['b', 1], ['c', 3], ['a', 2], ['c', 2],
                   ['g', 3], ['g', 3], ['d', 3], ['b', 2],
                   ['c', 4], ['g', 3], ['f', 3], ['a', 3],
                   ['f', 2], ['f', 1], ['d', 4], ['d', 4],
                   ['g', 2], ['e', 3], ['e', 4], ['f', 3],
                   ['d', 3], ['e', 4], ['g', 4], ['c', 3],
                   ['d', 1], ['e', 2], ['b', 2], ['b', 1],
                   ['g', 1]]

fixed_game_b4_0 = [['g', 3], ['f', 3], ['e', 4], ['a', 4],
                   ['a', 4], ['c', 4], ['e', 3], ['e', 4],
                   ['a', 4], ['a', 2], ['a', 2], ['c', 4],
                   ['f', 4], ['d', 4], ['c', 4], ['f', 3],
                   ['e', 1], ['b', 2], ['c', 2], ['a', 3],
                   ['g', 4], ['d', 3], ['f', 1], ['f', 2],
                   ['e', 2], ['d', 1], ['c', 4]]
fixed_game_b4_1 = [['a', 3], ['d', 4], ['g', 4], ['b', 3],
                   ['e', 1], ['b', 4], ['e', 3], ['f', 1],
                   ['f', 4], ['b', 4], ['d', 2], ['e', 4],
                   ['g', 4], ['d', 2], ['c', 3], ['b', 2],
                   ['f', 4], ['d', 2], ['b', 2], ['e', 4],
                   ['c', 3], ['d', 2], ['a', 1], ['e', 1],
                   ['d', 2], ['g', 1], ['g', 3]]
fixed_game_b4_2 = [['c', 1], ['c', 4], ['d', 1], ['c', 2],
                   ['d', 3], ['d', 4], ['g', 3], ['e', 1],
                   ['g', 4], ['c', 3], ['f', 1], ['b', 4],
                   ['a', 3], ['c', 4], ['e', 2], ['e', 3],
                   ['b', 3], ['d', 1], ['c', 3], ['f', 4],
                   ['e', 1], ['g', 4], ['b', 4], ['g', 3],
                   ['b', 4], ['b', 3], ['b', 3], ['g', 3],
                   ['e', 3], ['f', 1], ['e', 1], ['a', 1],
                   ['a', 4], ['a', 1], ['f', 4], ['f', 2],
                   ['f', 3], ['d', 1], ['d', 3], ['a', 3],
                   ['a', 1], ['g', 2]]

# If you want to create your own test data sets put them here,
# otherwise call function random_game to obtain data sets.
 
#
#--------------------------------------------------------------------#



#-----Function for Assessing Your Solution---------------------------#
#
# The function in this section will be used to assess your solution.
# Do not change any of the code in this section.

# The following function creates a random data set describing a
# game to draw.  Your program must work for any data set that
# can be returned by this function.  The results returned by calling
# this function will be used as the argument to your "play_game"
# function during marking.  For convenience during code development
# and marking this function also prints each move in the game to the
# shell window.  NB: Your code should not print anything else to
# the shell.  Make sure any debugging calls to the "print" function
# are disabled before you submit your solution.
#
# To maximise the amount of "randomness" the function makes no attempt
# to give each of the four "players" the same number of turns.  (We
# assume some other random mechanism, such as rolling a die, determines
# who gets to drop a token into the board at each turn.)  However the
# function has been designed so that it will never attempt to overfill
# a column of the board.  Also, the function will not necessarily
# generate enough moves to fill every cell in the board.
#
def random_game():
    # Welcoming message
    print('Welcome to the game!')
    print('Here are the randomly-generated moves:')
    # Initialise the list of moves
    game = []
    # Keep track of free spaces
    vacant = [["I'm free!"] * num_rows] * num_columns
    # Decide how many tokens to insert
    num_tokens = randint(0, num_rows * num_columns * 1.5)
    # Drop random tokens into the board, provided they won't
    # overfill a column
    for move in range(num_tokens):
        # Choose a random column and token type
        column_num = randint(0, num_columns - 1)
        column = chr(column_num + ord('a'))
        token = randint(1, 4)
        # Add the move, provided it won't overfill the board
        if vacant[column_num] != []:
            # Display the move
            print([column, token])
            # Remember it
            game.append([column, token])
            vacant[column_num] = vacant[column_num][1:]
    # Print a final message and return the completed game
    print('Game over!')
    if len(game) == 0:
        print('Zero moves were generated')
    elif len(game) == 1:
        print('Only one move was generated')
    else:
        print('There were', len(game), 'moves generated')
    return game

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
#  Complete the assignment by replacing the dummy function below with
#  your own "play_game" function.
#

# Draw tokens on the board as per the provided data set

create_drawing_canvas(False)

#define and draw the 100*100 pixel box
def square(length):#square has four sides
    for i in range(4):
        width(3)
        forward(length)
        left(90)
        
#define star for the winner
def star(height, colour):

    left_angle = 72 # degrees, for left turns
    right_angle = 144  # degrees, for right turns
    line_size = height * 0.409 # length of each of the ten lines

    # Draw a five-pointed, filled star as five concave segments
    setheading(-left_angle) # pointing down from top point
    #pencolor=("black")
    width(1)
    color("black",colour) # use the given fill colour
    pendown()
    begin_fill()
    segment_numbers = range(5)
    for seg_no in segment_numbers: # draw each of the segments
      forward(line_size)
      left(left_angle)
      forward(line_size)
      right(right_angle)
    end_fill()
    
#position of token 1
goto(-550,100)
speed("fastest")

#draw token 1 - Mitsubushi
        
def Mitsubushi():
    color("black","light blue")
    begin_fill()
    square(100)
    end_fill()

    #top diamond
    penup()
    width(1)
    forward(50)
    left(90)
    forward(50)
    right(45)
    pendown()
    color("red","red")
    begin_fill()
    square(30)
    end_fill()
    
    #remaining diamonds
    color("red","red")
    begin_fill()
    left(180)
    forward(28)
    right(45)
    forward(28)
    right(130)
    forward(28)
    right(50)
    forward(56)
    right(45)
    forward(28)
    right(135)
    forward(28)
    right(45)
    forward(28)
    end_fill()
    
Mitsubushi()


#print the token number and description of token
penup()
goto(-550,50)
pendown()
pencolor("black")
width(0.5)
write("Token 1:\nMitsubushi", align = 'left', font =('Times New Roman',16,'normal'))

#define token 2 - Suzuki

penup()
home()
goto(-550,-195)#position of token 2
pendown()

def Suzuki():
    color("black","yellow")
    begin_fill()
    square(100)
    end_fill()
    
    #draw s symbol
    penup()
    pencolor('red')
    width(16)
    left(90)
    forward(40)
    right(90)
    forward(30)
    right(45)
    pendown()
    forward(35)
    left(90)
    width(9)
    forward(25)
    left(90)
    width(16)
    forward(56)
    right(90)
    width(9)
    forward(25)
    width(16)
    right(90)
    forward(35)
     
Suzuki()
    
#print the token number and description of token
penup()
goto(-550,-250)
pendown()
pencolor("black")
width(0.5)
write("Token 2:\nSuzuki", align = 'left', font =('Times New Roman',16,'normal'))

#define token 3 - toyota

penup()
home()
goto(450,100)#position of token 3
pendown()

def toyota():
    color("black","light green")
    begin_fill()
    square(100)
    end_fill()
    penup()
    forward(60)
    left(90)
    forward(25)
    right(90)
    pendown()
    pencolor('navy blue')
    
    #Verticle oval
    def talloval(r):
        width(6)
        left(45)
        for loop in range(2):      
            circle(r,90)    
            circle(r/4,90)  
    talloval(40)

    penup()
    right(45)
    backward(35)
    left(90)
    forward(34)
    right(90)
    pendown()

    #small horizontal oval
    def flatoval(r):               
        right(45)
        for loop in range(2):
            circle(r,90)
            circle(r/4,90)
    flatoval(40)

    penup()
    right(45)
    forward(20)
    left(90)
    backward(5)
    pendown()

    #big horizontal oval
    def flatoval1(r):              
        right(45)
        for loop in range(2):
            circle(r,90)
            circle(r/2,90)
    flatoval1(46)

toyota()

#print the token number and description of token
penup()
goto(450,50)
pendown()
pencolor("black")
width(0.5)
write("Token 3:\nToyota", align = 'left', font =('Times New Roman',16,'normal'))

#define token 4

penup()
home()
goto(450,-200)#position of token 4
pendown()
radius=[45,40]

def volkswagen():
    color("black","gold")
    begin_fill()
    square(100)
    end_fill()
    
    #draw outer circle
    penup()
    forward(50)
    left(90)
    forward(50)
    right(90)
    forward(radius[0])
    left(90)
    pencolor('blue')
    fillcolor('blue')
    begin_fill()
    pendown()
    circle(radius[0])
    end_fill()

    #draw inner circle
    left(90)
    forward(radius[0])
    right(180)
    penup()
    forward(radius[1])
    left(90)
    pencolor('white')
    width(5)
    pendown()
    circle(radius[1])

    #top V
    penup()
    pencolor('white')
    width(7)
    circle(radius[1],extent=50)
    left(100)
    pendown()
    forward(30)
    right(60)
    forward(10)
    right(65)
    forward(35)
    penup()

    #bottom W
    backward(35)
    right(25)
    backward(6)
    right(90)
    forward(radius[1])
    left(90)
    pendown()
    circle(radius[1],extent=25)
    left(130)
    forward(50)
    right(138)
    forward(25)
    left(70)
    forward(10)
    left(70)
    forward(27)
    right(138)
    forward(52)
       
volkswagen()

#print the token number and description of token
penup()
goto(450,-250)
pendown()
pencolor("black")
width(0.5)
write("Token 4:\nVolkswagen", align = 'left', font =('Times New Roman',16,'normal'))

#define a number for each token
def callToken(token):
    # print(token)
    if(token==1):
        Mitsubushi()
    elif(token==2):
        Suzuki()
    elif(token==3):
        toyota()
    elif(token==4):
        volkswagen()
    return 

def callPenupHome(logo):
    callToken(logo)
    penup()
    home()
    return

#for a clear single winner - gold star
def check_winner(top_token):
    print("top_token",top_token)
    # loop for a single winner - gold star
    for i in top_token.values():#i defines the topmost tokens     
        print("value is ",i)
        if i != 0:
            count_of_possible_winner = sum(value == i for value in top_token.values())
            possible_winner=i
            print("value is", i)
            print("count_possible_winner is", count_of_possible_winner)
            if count_of_possible_winner >=4:
                winner = i
                print(winner)
                if winner == 1:
                    goto(-464,230)#positioning gold star for winning token
                    star(70, "gold")
                elif winner == 2:
                    goto(-464,-50)
                    star(70, "gold")
                elif winner == 3:
                    goto(550,230)
                    star(70, "gold")
                elif winner == 4:
                    goto(550,-50)
                    star(70, "gold")
               #function to stop the game with a single winner
                time.sleep(15)
                exit()
            # else:
            #     return
    return

def play_game(moves):
    a_y_axis = -300
    b_y_axis = -300
    c_y_axis = -300
    d_y_axis = -300
    e_y_axis = -300
    f_y_axis = -300
    g_y_axis = -300

    top_token = {'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0}
    # print(top_token)
    
    # print(moves)
    for i in moves:#i defines the various moves
        if str(i[0]) == "a":
            goto(-350, a_y_axis)
            a_y_axis+=100
            top_token['a']=i[1]
            callPenupHome(i[1])
            check_winner(top_token)
            
        elif str(i[0]) == "b":
            goto(-250, b_y_axis)
            b_y_axis+=100
            top_token['b']=i[1]
            callPenupHome(i[1])
            check_winner(top_token)

        elif str(i[0]) == "c":
            goto(-150, c_y_axis)
            c_y_axis+=100
            top_token['c']=i[1]
            callPenupHome(i[1])
            check_winner(top_token)

        elif str(i[0]) == "d":
            goto(-50, d_y_axis)
            d_y_axis+=100
            top_token['d']=i[1]
            callPenupHome(i[1])
            check_winner(top_token)

        elif str(i[0]) == "e":
            goto(50, e_y_axis)
            e_y_axis+=100
            top_token['e']=i[1]
            callPenupHome(i[1])
            check_winner(top_token)
            
        elif str(i[0]) == "f":
            goto(150, f_y_axis)
            f_y_axis+=100
            top_token['f']=i[1]
            callPenupHome(i[1])
            check_winner(top_token)

        elif str(i[0]) == "g":
            goto(250, g_y_axis)
            g_y_axis+=100
            top_token['g']=i[1]
            callPenupHome(i[1])
            check_winner(top_token)
    #positioning the silver star for a tie game
    goto(-464,230)
    star(70, "silver")
    penup()
    goto(-464,-50)
    pendown()
    star(70, "silver")
    penup()
    goto(550,230)
    pendown()
    star(70, "silver")
    penup()
    goto(550,-50)
    pendown()
    star(70, "silver")
    
    return







#
#--------------------------------------------------------------------#



#-----Main Program---------------------------------------------------#
#
# This main program sets up the background, ready for you to start
# drawing your solution.  Do not change any of this code except
# as indicated by the comments marked '*****'.
#

# Set up the drawing canvas
# ***** You can change the background and line colours, and choose
# ***** whether or not to label the axes and mark the places for the
# ***** legend, by providing arguments to this function call
create_drawing_canvas(False)

# Control the drawing speed
# ***** Change the following argument if you want to adjust
# ***** the drawing speed
speed('fastest')

# Decide whether or not to show the drawing step-by-step
# ***** Set the following argument to False if you don't want to wait
# ***** forever while the cursor moves slowly around the screen
tracer(True)

# Give the drawing canvas a title
# ***** Replace this title with a description of your solution's
# ***** theme and its tokens
title("Car company logo (Mitsubushi, Suzuki, Toyota and Volkswagen)")

### Call the student's function to play the game
### ***** While developing your program you can call the "play_game"
### ***** function with one of the "fixed" data sets, but your
### ***** final solution must work with "random_game()" as the
### ***** argument.  Your "play_game" function must work for any data
### ***** set that can be returned by the "random_game" function.
#play_game(fixed_game_a0) # <-- use this for code development only

play_game(random_game()) # <-- this will be used for assessment
# play_game(not_working)

# Exit gracefully
# ***** Change the default argument to False if you want the
# ***** cursor (turtle) to remain visible at the end of the
# ***** program as a debugging aid
release_drawing_canvas()

#
#--------------------------------------------------------------------#

