#!/usr/local/bin/python3

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

DEFAULT_PADDING = 7

class App(ttk.Frame):
	def __init__(self, master):
		ttk.Frame.__init__(self, master)
		self.pack()

		self.master.protocol('WM_DELETE_WINDOW', self.buttonClickQuit)  # Override default 'Quit Cross' behaviour
		self.master.bind('<Escape>', self.buttonClickQuit)  # Link Esc to quit function

		self.master.title('hello, world!')  # Window title
		self.master.resizable(False, False)  # Not resizable
		self.master.tk_setPalette(background='#ececec')  # Main widget background color

		x = int((self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2)
		y = int((self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 2.5)

		self.master.geometry("+{}+{}".format(x, y))  # Position window on screen
		self.master.config(menu=tk.Menu(self.master))  # Remove default Python menu

		# Main window layout
		mainLayout = ttk.Frame(self)
		mainLayout.pack(padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)

		self.labelHello = ttk.Label(mainLayout, text='Hi, what do we code today?')  # There is a more flexible widget called Message
		self.labelHello.pack() # pack(fill = X || Y) : width || height : 100%

		# Layout for the buttons inside mainLayout
		buttonsLayout = ttk.Frame(mainLayout)
		buttonsLayout.pack(side=tk.RIGHT, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)

		self.buttonOk = ttk.Button(buttonsLayout, text='OK', default=tk.ACTIVE, command=self.buttonClickOk)
		self.buttonOk.pack(side=tk.RIGHT)
		self.buttonQuit = ttk.Button(buttonsLayout, text='Quit', command=self.buttonClickQuit)
		self.buttonQuit.pack(side=tk.RIGHT)

	def buttonClickOk(self):
		print('User clicked OK')
		messagebox.showinfo('User clicked OK', 'The user clicked OK, do something, bro!')

	def buttonClickQuit(self, event=None):  # event = None is for bind() which sends 2 parameters
		print('User wants to Quit')
		self.master.quit()


if __name__ == '__main__':
	root = tk.Tk()
	app = App(root)
	app.mainloop()
