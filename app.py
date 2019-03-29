"""
Main window class

To-do:
- If a folder is selected, give the option to add another one.
  With two folders you don't need to crawl the whole system
  if you know where to look.
- Maybe even make a list of folders to crawl with "+" and "-"
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

LANG = 'en'

if LANG == 'fr':
	import translation.fr as tr
else:  # English is default
	import translation.en as tr

class App(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.pack()

		# Attributes
		self.CURRENT_FOLDER = None
		self.DEFAULT_PADDING = 7

		self.master.protocol('WM_DELETE_WINDOW', self.appQuit)  # Override default 'Quit Cross' behaviour
		self.master.bind('<Escape>', self.appQuit)  # Link Esc to quit function

		self.master.title('Duplicates')  # Window title
		self.master.resizable(False, False)  # Not resizable
		self.master.tk_setPalette(background='#ececec')  # Main widget background color

		x = int((self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2)
		y = int((self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 2.5)

		self.master.geometry("+{}+{}".format(x, y))  # Position window on screen
		self.master.config(menu=tk.Menu(self.master))  # Remove default Python menu

		# Main window layout
		mainLayout = tk.Frame()
		mainLayout.pack(padx=self.DEFAULT_PADDING, pady=self.DEFAULT_PADDING)

		# Folder selection Label & Dialog
		folderSelectionLayout = tk.Frame(mainLayout)
		folderSelectionLayout.grid(sticky=tk.W)

		self.selectFolderButton = ttk.Button(folderSelectionLayout, text=tr.SELECT_FOLDER_BUTTON)
		self.selectFolderButton.bind('<Button-1>', self.selectFolder)
		self.selectFolderButton.grid(row=0, column=0)

		self.currentFolderLabel = tk.Label(folderSelectionLayout, text=tr.CURRENT_FOLDER_LABEL)
		self.currentFolderLabel.grid(row=0, column=1, padx=(self.DEFAULT_PADDING, 0))

		# self.messageBox = tk.Text(mainLayout, width=50, height=10, bg='white', highlightthickness=0, font=('Arial', 14), padx=self.DEFAULT_PADDING, pady=self.DEFAULT_PADDING)
		# self.messageBox.grid(pady=(self.DEFAULT_PADDING, 0))

	def appQuit(self, event=None):
		self.master.quit()

	def selectFolder(self, event=None):
		folder = filedialog.askdirectory(title=tr.SELECT_FOLDER_DIALOG_TITLE)
		self.setCurrentFolder(folder)

	def setCurrentFolder(self, folder):
		self.CURRENT_FOLDER = folder

		if self.CURRENT_FOLDER is None:
			self.currentFolderLabel['text'] = tr.CURRENT_FOLDER_LABEL
		else:
			if len(self.CURRENT_FOLDER) <= 42:
				self.currentFolderLabel['text'] = self.CURRENT_FOLDER
			else:
				self.currentFolderLabel['text'] = '...' + self.CURRENT_FOLDER[-39:]
