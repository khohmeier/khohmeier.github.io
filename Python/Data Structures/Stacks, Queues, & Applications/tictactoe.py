# Kaitlyn Hohmeier
__author__ = 'narayans'
from gameboard import GameBoard
from stack import Stack
import time
import random


# the demo function below provides examples of gameboard usage
# this demo illustrates everything you can do with a gameboard

def demo():
    """
    Demo function to illustrate interactions with the game board

    Parameters:

    Return:
         None
    """

    # get a reference to the GameBoard
    # you will use this reference to communicate with the gameboard
    gb = GameBoard.get_board()

    row = 3
    col = 4

    # Retrieve color of specified cell
    old_color = gb.get_color(row, col)

    # change the color of specified cell
    gb.set_color(row, col, "RED")

    # Retrieve the name of the color of the specified cell
    c = gb.get_color(row, col)
    print("Cell ", row, col, " is colored ", c)

    # wait 5 seconds and then restore color of cell to old_color
    time.sleep(5)
    gb.set_color(row, col, old_color)

    # change the label of the specified cell
    gb.set_label(row, col, "X")

    # Retrieve the label of the specified cell
    letter = gb.get_label(row, col)
    print("Cell ", row, col, " has label ", letter)

    # Retrieve the number of rows in the board
    max_rows = gb.get_row_count()

    # Retrieve the number of columns in the board
    max_cols = gb.get_column_count()

    colors = ["red", "green", "yellow"]
    # Iterate over the board and assign random letters and colors to the cells
    for row in range(max_rows):
        for col in range(max_cols):
            letter = chr(random.randint(ord('A'), ord('Z')))
            gb.set_label(row, col, letter)
            gb.set_color(row, col, colors[random.randint(0,2)])
            time.sleep(0.1)

    time.sleep(5)
    gb.reset() # reset game board to default color and font

    time.sleep(5)
    # resize game board to different dimensions
    gb.set_size(6,8)


def reset_board():
    """
    Reset all cells in the game board to un-highlighted state

    Parameters:

    Return:
        None
    """

    gb = GameBoard.get_board()
    gb.reset()


def __highlight_cells(s:Stack):
    """
    Highlight the cells referenced in the stack

    Parameters:
        s: stack of cell references in the form (row,col)

    Return:
        None
    """

    gb = GameBoard.get_board()
    while not s.is_empty():
        t = s.pop()
        gb.highlight(t[0], t[1])


def search_one_word():
    """
    Prompt user for word to search and search game board for that word. If word is found, display
    cell references where the word is found and highlight those cells. If not, display appropriate message.

    Parameters:

    Return:
        None
    """

    gb = GameBoard.get_board()
    word = input("Enter word for which to search: ")
    s = Stack()
    result = __search_board(gb, word, s)
    if result:
        print("\t" + word + " found at " + str(s))
        __highlight_cells(s)
    else:
        print("\t" + word + " was not found in board")


def search_all_words():
    """
    Prompt user for filename containing words to search and search game board for all words contained in file.
    For each word found, display cell references where the word is found and highlight those cells.
    If not, display appropriate message.

    Parameters:

    Return:
        None
    """

    gb = GameBoard.get_board()

    filename = input("Enter name of file containing words for which to search: ")
    file = open("Resources/"+filename, "r")

    for word in file:
        word = word.strip()
        print("Searching for "+ word)
        s = Stack()
        result = __search_board(gb, word, s)
        if result:
            print("\t" + word + " found at " + str(s))
            __highlight_cells(s)
        else:
            print("\t"+word + " was not found in board")


# all functions named with a leading __ are treated as "for internal use only", and therefore not added to the menu
def __search_board(gb, word, stk):
    """
    Searches the game board for a particular search word by checking the board horizontally (both ways), vertically
    (both ways), and diagonally (both diagonals, both ways). Checks each individual letters in every row and every
    column

    Parameters:
        gb: a Game Board object
        word: the word to be searched for
        stk: a stack

    Return:
        a Boolean value - True if the word is found; False otherwise
    """

    h = gb.get_row_count()
    w = gb.get_column_count()

    for row in range(h):
        for col in range(w):

            result = __search_row_lr(gb, row, col, word, stk)
            if result:
                return True

            result = __search_row_rl(gb, row, col, word, stk)
            if result:
                return True

            result = __search_col_tb(gb, row, col, word, stk)
            if result:
                return True

            result = __search_col_bt(gb, row, col, word, stk)
            if result:
                return True

            result = __search_diag_minor_bt(gb, row, col, word, stk)
            if result:
                return True

            result = __search_diag_minor_tb(gb, row, col, word, stk)
            if result:
                return True

            result = __search_diag_major_tb(gb, row, col, word, stk)
            if result:
                return True

            result = __search_diag_major_bt(gb, row, col, word, stk)
            if result:
                return True

    return False


# all functions named with a leading __ are treated as "for internal use only", and therefore not added to the menu
# recursively search specified row left to right
def __search_row_lr(gb, row, col, word, stk):
    """
    Performs a recursive left-right search of a row for a target word

    Parameters:
        gb: a Game Board object
        row: a row number
        col: a column number
        word: the target word to be searched for
        stk: a stack

    Return:
        A Boolean value - True if word is found; False otherwise. Also returns p, a stack containing tuples of row-
        column number pairs where each letter matching the target word is found on the board.
    """

    if word == "":  # matched all letters of word
        return True
    elif col == gb.get_column_count():
        # reached right end of board
        return False
    elif word[0] != gb.get_label(row, col):
        # character mismatch
        return False
    else:  # letter at (row, col) matches first letter of word. Try matching rest
        stk.push((row,col))
        p = __search_row_lr(gb, row, col + 1, word[1:], stk)
        if not p:
            stk.pop()
        return p


def __search_row_rl(gb, row, col, word, stk):
    """
    Performs a recursive right-left search of a row for a target word

    Parameters:
        gb: a Game Board object
        row: a row number
        col: a column number
        word: the target word to be searched for
        stk: a stack

    Return:
        A Boolean value - True if word is found; False otherwise. Also returns p, a stack containing tuples of row-
        column number pairs where each letter matching the target word is found on the board.
    """

    if word == "":  # matched all letters of word
        return True
    elif col < 0:
        # reached left end of board
        return False
    elif word[0] != gb.get_label(row, col):
        # character mismatch
        return False
    else:  # letter at (row, col) matches first letter of word. Try matching rest
        stk.push((row, col))
        p = __search_row_rl(gb, row, col - 1, word[1:], stk)
        if not p:
            stk.pop()
        return p


def __search_col_tb(gb, row, col, word, stk):
    """
    Performs a recursive top-bottom search of a column for a target word

    Parameters:
        gb: a Game Board object
        row: a row number
        col: a column number
        word: the target word to be searched for
        stk: a stack

    Return:
        A Boolean value - True if word is found; False otherwise. Also returns p, a stack containing tuples of row-
        column number pairs where each letter matching the target word is found on the board.
    """

    if word == '':  # all letters in the word matched
        return True
    elif row == gb.get_row_count():
        # reached the bottom of the board
        return False
    elif word[0] != gb.get_label(row, col):
        # character mismatch
        return False
    else:
        stk.push((row, col))
        p = __search_col_tb(gb, row + 1, col, word[1:], stk)
        if not p:
            stk.pop()
        return p


def __search_col_bt(gb, row, col, word, stk):
    """
    Performs a recursive bottom-top search of a column for a target word

    Parameters:
        gb: a Game Board object
        row: a row number
        col: a column number
        word: the target word to be searched for
        stk: a stack

    Return:
        A Boolean value - True if word is found; False otherwise. Also returns p, a stack containing tuples of row-
        column number pairs where each letter matching the target word is found on the board.
    """

    if word == '':  # all letters in the word matched
        return True
    elif row < 0:
        # reached the top of the board
        return False
    elif word[0] != gb.get_label(row, col):
        # character mismatch
        return False
    else:
        stk.push((row, col))
        p = __search_col_bt(gb, row - 1, col, word[1:], stk)
        if not p:
            stk.pop()
        return p


def __search_diag_minor_bt(gb, row, col, word, stk):
    """
    Performs a recursive bottom-top search of the minor diagonal (/) for a target word

    Parameters:
        gb: a Game Board object
        row: a row number
        col: a column number
        word: the target word to be searched for
        stk: a stack

    Return:
        A Boolean value - True if word is found; False otherwise. Also returns p, a stack containing tuples of row-
        column number pairs where each letter matching the target word is found on the board.
    """

    if word == '':  # all letters in the word matched
        return True
    elif row < 0 or col == gb.get_column_count():
        # out of bounds check
        return False
    elif word[0] != gb.get_label(row, col):
        # character mismatch
        return False
    else:
        stk.push((row, col))
        p = __search_diag_minor_bt(gb, row - 1, col + 1, word[1:], stk)
        if not p:
            stk.pop()
        return p


def __search_diag_minor_tb(gb, row, col, word, stk):
    """
    Performs a recursive top-bottom search of the minor diagonal (/) for a target word

    Parameters:
        gb: a Game Board object
        row: a row number
        col: a column number
        word: the target word to be searched for
        stk: a stack

    Return:
        A Boolean value - True if word is found; False otherwise. Also returns p, a stack containing tuples of row-
        column number pairs where each letter matching the target word is found on the board.
    """

    if word == '':  # all letters in the word matched
        return True
    elif row == gb.get_row_count() or col < 0:
        # out of bounds check
        return False
    elif word[0] != gb.get_label(row, col):
        # character mismatch
        return False
    else:
        stk.push((row, col))
        p = __search_diag_minor_tb(gb, row + 1, col - 1, word[1:], stk)
        if not p:
            stk.pop()
        return p


def __search_diag_major_tb(gb, row, col, word, stk):
    """
    Performs a recursive top-bottom search of the major diagonal (\) for a target word

    Parameters:
        gb: a Game Board object
        row: a row number
        col: a column number
        word: the target word to be searched for
        stk: a stack

    Return:
        A Boolean value - True if word is found; False otherwise. Also returns p, a stack containing tuples of row-
        column number pairs where each letter matching the target word is found on the board.
    """

    if word == '':  # all letters in the word matched
        return True
    elif row == gb.get_row_count() or col == gb.get_column_count():
        # out of bounds check
        return False
    elif word[0] != gb.get_label(row, col):
        # character mismatch
        return False
    else:
        stk.push((row, col))
        p = __search_diag_major_tb(gb, row + 1, col + 1, word[1:], stk)
        if not p:
            stk.pop()
        return p


def __search_diag_major_bt(gb, row, col, word, stk):
    """
    Performs a recursive bottom-top search of the major diagonal (\) for a target word

    Parameters:
        gb: a Game Board object
        row: a row number
        col: a column number
        word: the target word to be searched for
        stk: a stack

    Return:
        A Boolean value - True if word is found; False otherwise. Also returns p, a stack containing tuples of row-
        column number pairs where each letter matching the target word is found on the board.
    """

    if word == '':  # all letters in the word matched
        return True
    elif row < 0 or col < 0:
        # out of bounds check
        return False
    elif word[0] != gb.get_label(row, col):
        # character mismatch
        return False
    else:
        stk.push((row, col))
        p = __search_diag_major_bt(gb, row - 1, col - 1, word[1:], stk)
        if not p:
            stk.pop()
        return p


def read_puzzle():
    """
    Prompt user for puzzle file name and read and display characters contained in file on the game board

    Parameters:

    Return:
        None
    """

    filename = input("Enter name of puzzle file: ")
    file = open("Resources/"+filename, "r")

    # Read the text in the puzzle file
    # Determine the number of rows and columns in the puzzle
    # Resize game board to corresponding size
    # set the label of each cell in the game board to the corresponding letter in the puzzle

    lines = []
    for line in file:
        line = line.strip()
        lines.append(line.split())

    h = len(lines)
    w = len(lines[0])

    gb = GameBoard.get_board()
    gb.set_size(h, w)

    for row in range(h):
        for col in range(w):
            letter = lines[row][col]
            gb.set_label(row, col, letter)


if __name__ == '__main__':
    GameBoard()
