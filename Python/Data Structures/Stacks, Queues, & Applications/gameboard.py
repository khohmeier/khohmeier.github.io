from tkinter import *
import tkinter as tk
from tkinter import filedialog
#import winsound
import threading

import time
import inspect
import imp
import functools
from os import path


class GameCell(Label):

    def __init__(self, root, label="?"):
        self.baseFont = ("Times", 10)
        self.textFont = ("Arial", 14)
        self.root = root
        # Call the constructor in the parent class Button
        Button.__init__(self, root, width=3, height=2, relief=GROOVE, font=self.baseFont)
        self.label = label
        self.color = root.cget('bg')  # default tkinter root window color
        self.default_color = self.color
        self.show(root)

    def reset(self):
        self.color = self.default_color
        self.configure(bg=self.root.cget('bg'))
        self.configure(font=self.textFont)

    def set_color(self, c):
        self.color = c
        self.configure(bg=self.color)

    def highlight(self):
        self.color = "YELLOW"
        self.configure(bg=self.color)
        self.configure(font=('helvetica', 20, 'italic'))

    def get_color(self):
        return self.color

    def set_label(self, label):
        self.label = label
        self.config(text=self.label)

    def get_label(self):
        return self.label

    def upSize(self):
        self.configure(width=15, height=5)

    def downSize(self):
        self.configure(width=10, height=5, font=self.baseFont)

    def show(self, root):
        self.isFaceUp = True
        self.config(text=self.label, font=self.textFont)
        root.update()  # update root so that the cell is repainted immediately

    def hide(self):
        self.configure(text="", bg='LIGHT GRAY')
        self.isFaceUp = False


class GameBoard(object):
    """
    :author: Sridhar Narayan
    :version: 1.1 - March 2019

    :contact: narayans@uncw.edu
    :organization: University of North Carolina Wilmington

    :summary: Support for a gameboard-like interface

    """
    __gameboard = None

    @staticmethod
    def get_board():
        return GameBoard.__gameboard

    def get_row_count(self):
        return self.num_rows

    def get_column_count(self):
        return self.num_columns

    def reset(self):
        for c in self.cells:
            c.reset()

    def set_color(self, r, c, color):
        cell_offset = r * self.num_columns + c
        self.cells[cell_offset].set_color(color)

    def highlight(self, r, c):
        cell_offset = r * self.num_columns + c
        self.cells[cell_offset].highlight()

    def get_color(self, r, c):
        cell_offset = r * self.num_columns + c
        return self.cells[cell_offset].get_color()

    def set_label(self, r, c, label):
        cell_offset = r * self.num_columns + c
        self.cells[cell_offset].set_label(label)

    def get_label(self, r, c):
        cell_offset = r * self.num_columns + c
        return self.cells[cell_offset].get_label()

    def set_size(self, num_rows, num_cols):
        self.CardType = GameCell  # what kind of card
        self.num_rows = num_rows
        self.num_columns = num_cols

        self.__buildUI()
        self.__maybe_load_code()

    def __init__(self, num_rows=10, num_columns=10, title="Game Board"):

        self.__main_root = Tk()
        self.__main_root.config(width=600, height=400)
        # Disable resizing
        self.__main_root.resizable(0, 0)
        self.__main_root.title(title)

        self.opsMenu = None
        self.__active_key = None
        GameBoard.__gameboard = self

        self.set_size(num_rows, num_columns)

        self.__main_root.mainloop()

    # returns current list of labels under menu option opsMenu
    @staticmethod
    def __menu_options(menu_item):
        mx = menu_item.index(tk.END)
        if mx is None:
            return []
        else:
            return [menu_item.entrycget(i, 'label') for i in range(mx + 1)]

    # open specified file and determine module
    def __load_file(self, code_file_name, message):
        folder, filename = code_file_name.rsplit('/', 1)
        if folder not in sys.path:
            sys.path.append(folder)
        module_name = filename.split('.')[0]
        self.currentModuleName = module_name

        open_file, file_name, description = imp.find_module(module_name)
        module = imp.load_module(code_file_name, open_file, file_name, description)

        self.__load_functions(module, message)

    # load student code
    def __load_code(self):
        code_file_types = [("Python files", "*.py")]
        code_file_name = filedialog.askopenfilename(filetypes=code_file_types)
        if len(code_file_name) > 0:
            self.currentCodeFileName = code_file_name
            self.__load_file(code_file_name, "Loaded ")

    # reload the currently loaded code file
    def __reload_code(self):
        if self.currentCodeFileName is not None:
            # noinspection PyTypeChecker
            # self.__show_message("Reloaded code from " + self.currentCodeFileName)
            self.__load_file(self.currentCodeFileName, "Reloaded ")

    # update the code binding (definition) for the specified function
    def __update_func_def(self, func_to_update):
        functions = inspect.getmembers(self.currentModule, inspect.isfunction)

        for f in functions:
            func_name = f[0]
            func_code = f[1]
            w_list = str(func_to_update).split()
            if func_name == w_list[1]:  # have we found the function def of interest?
                return func_code  # if so, return the current definition for that function

    # create and start a threaded task when called
    def __exec_task(self, f):
        self.__reload_code()  # reload the function definition file
        f = self.__update_func_def(f)  # update the binding of the function of interest
        threading.Thread(target=f).start()  # execute that function

    # load the user code contained in the file from which the viewer was instantiated
    def __maybe_load_code(self):
        main_mod = sys.modules['__main__']
        self.currentModule = main_mod

        if hasattr(main_mod, '__file__'):  # launched by executing a Python script
            self.currentCodeFileName = path.abspath(sys.modules['__main__'].__file__)
            self.currentCodeFileName = self.currentCodeFileName.replace('\\', '/')
            self.__load_functions(main_mod, "Loaded ")

    # add functions defined in specified file to myOps menu
    def __load_functions(self, module, message):
        self.currentModule = module
        functions = inspect.getmembers(module, inspect.isfunction)

        current_menu_options = self.__menu_options(self.opsMenu)

        for f in functions:
            f_label = f[0]
            if f_label[0:2] == '__':
                continue  # skip over the 'private' functions
            f_name = f[1]
            # command associated with this menu option includes the function to be
            # executed as a part of the task as a parameter
            # functools.partial is necessary for this
            # since it allows a partially specified command to be set as the target of the menu action
            # duplicate labels not allowed
            if f_label in current_menu_options:  # delete option before updating
                index = current_menu_options.index(f_label)
                self.opsMenu.delete(index)
                current_menu_options.remove(f_label)

            # update existing option, or add new one
            self.opsMenu.add_command(label=f_label, command=functools.partial(self.__exec_task, f_name))

    # start a new game
    def newGame(self, CardType):
        for child in self.__main_root.winfo_children():
            child.destroy()  # remove all old cards

        GameBoard(self.num_rows, self.num_columns)

    def __buildMenu(self, root):
        menubar = Menu(root)

        gameMenu = Menu(menubar, tearoff=0)

        load_menu = Menu(menubar, tearoff=0)
        load_menu.add_command(label="Load", command=self.__load_code)
        load_menu.add_command(label="Reload", command=self.__reload_code)

        gameMenu.add_command(label="Exit", command=root.destroy)
        menubar.add_cascade(label="Game", menu=gameMenu)
        menubar.add_cascade(label="MyCode", menu=load_menu)

        self.opsMenu = Menu(menubar, tearoff=0)

        # add sub-menus to menubar
        menubar.add_cascade(label="MyFuncs", menu=self.opsMenu)

        root.config(menu=menubar)

    def __buildUI(self):
        for child in self.__main_root.winfo_children():
            child.destroy()  # remove all old card
        self.cells = []

        count = 0
        for r in range(self.num_rows):
            for c in range(self.num_columns):
                c1 = GameCell(self.__main_root)

                self.cells.append(c1)  # add card to the cells list

                self.cells[count].grid(row=r, column=c, padx=5, pady=5)
                count = count + 1

        self.__buildMenu(self.__main_root)


# #only do this if invoked as application
if __name__ == '__main__':
    GameBoard(3, 3)
