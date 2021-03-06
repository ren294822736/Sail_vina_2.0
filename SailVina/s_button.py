from tkinter import *
from tkinter.ttk import *
import s_file
from tkinter import messagebox


class SButton(object):
    def __init__(self, root, text, x, y):
        self.root = root
        self.text = text
        self.x = x
        self.y = y

        self.button = Button(self.root, text=self.text)
        self.button.place(x=self.x, y=self.y)

        self.entry_text = None
        self.initial_dir = None
        self.title = None
        self.file_type = None
        self.parent = None

    def _bind_open_file(self, event):
        self.initial_dir = self.entry_text.get()
        filename = s_file.SFile().open_file(self.initial_dir, self.title, self.file_type, parent=self.parent)
        self.entry_text.set(filename)

    def bind_open_file(self, entry_text, title, file_type, parent=""):
        self.entry_text = entry_text
        self.title = title
        self.file_type = file_type
        self.parent = parent
        self.button.bind("<Button-1>", self._bind_open_file)

    def _bind_open_dir(self, event):
        self.initial_dir = self.entry_text.get()
        dir_name = s_file.SFile().open_dir(initial_dir=self.initial_dir, title=self.title)
        self.entry_text.set(dir_name)

    def bind_open_dir(self, entry_text, title):
        self.entry_text = entry_text
        self.title = title
        self.button.bind("<Button-1>", self._bind_open_dir)

    def _bind_open_files(self, event):
        self.initial_dir = self.entry_text.get()
        try:
            file_type = self.file_type.get()
        except AttributeError:
            file_type = self.file_type
        self.filename_text = s_file.SFile().open_files(initial_dir=self.initial_dir, title=self.title,
                                                       file_type=file_type)
        self.entry_text.set(self.filename_text)

    def bind_open_files(self, entry_text, title, file_type):
        self.entry_text = entry_text
        self.title = title
        self.file_type = file_type
        self.button.bind("<Button-1>", self._bind_open_files)


class HelpButton(object):

    def __init__(self, root, help_text, x, y, width):
        self.root = root
        self.help_text = help_text
        self.x = x
        self.y = y
        self.width = width

        self.help_button = Button(self.root, text="帮助", command=self.show_help)
        self.help_button.place(x=self.x, y=self.y, width=self.width)

    def show_help(self):
        messagebox.showinfo("帮助", self.help_text)
