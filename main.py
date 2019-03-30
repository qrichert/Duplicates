#!/usr/local/bin/python3

import tkinter as tk
from mainwindow import *

class App(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.pack()

		self.m_parent = parent

		self.m_parent.protocol('WM_DELETE_WINDOW', self.appQuit)  # Override default 'Quit Cross' behaviour
		self.m_parent.bind('<Escape>', self.appQuit)  # Link Esc to quit function

		self.m_parent.title('Duplicates')  # Window title
		# self.parent.resizable(False, False)  # Not resizable

		self.m_parent.tk_setPalette(background='#ececec')  # Main widget background color

		x = int((self.m_parent.winfo_screenwidth() - self.m_parent.winfo_reqwidth()) / 2)
		y = int((self.m_parent.winfo_screenheight() - self.m_parent.winfo_reqheight()) / 2.5)

		self.m_parent.geometry("+{}+{}".format(x, y))  # Position window on screen
		self.m_parent.config(menu=tk.Menu(self.m_parent))  # Remove default Python menu

		self.m_mainWindow = MainWindow(self)
		self.m_mainWindow.pack()

	def appQuit(self, event=None):
		self.m_parent.quit()


if __name__ == '__main__':
	root = tk.Tk()
	app = App(root)
	app.mainloop()
