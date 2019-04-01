import tkinter as tk
from tkinter import ttk

from lang import *


class DuplicatesWindow(tk.Toplevel):
	def __init__(self, parent, duplicates, nbFilesProcessed):
		tk.Toplevel.__init__(self, parent)

		# Constants
		self.DEFAULT_PADDING = 7

		# Attributes
		self.m_parent = parent
		self.m_duplicates = duplicates
		self.m_nbFilesProcessed = nbFilesProcessed

		# Window configuration
		self.protocol('WM_DELETE_WINDOW', self.closeDialog)  # Override default 'Quit Cross' behaviour
		self.bind('<Escape>', self.closeDialog)  # Link Esc to quit function

		self.title('Duplicates - ' + tr.DW_TITLE)  # Window title
		#self.resizable(False, False)  # Not resizable

		x = int((self.winfo_screenwidth() - self.winfo_reqwidth()) / 2)
		y = int((self.winfo_screenheight() - self.winfo_reqheight()) / 2.5)

		self.geometry("+{}+{}".format(x + 10, y + 10))  # Position window on screen

		# Main window layout
		self.m_mainLayout = tk.Frame(self)
		self.m_mainLayout.pack(fill=tk.BOTH, expand=1)

		self.m_textFrame = tk.Frame(self.m_mainLayout)
		self.m_textFrame.pack(fill=tk.BOTH, expand=1)
		self.m_textFrame.columnconfigure(0, weight=1)
		self.m_textFrame.rowconfigure(0, weight=1)

		self.m_text = tk.Text(self.m_textFrame, bg='white', wrap='none', highlightthickness=0)
		self.m_text.grid(row=0, column=0, sticky=tk.NSEW)

		self.m_textVScrollbar = tk.Scrollbar(self.m_textFrame, orient=tk.VERTICAL)
		self.m_textVScrollbar['command'] = self.m_text.yview
		self.m_textVScrollbar.grid(row=0, column=1, sticky=tk.NS)
		self.m_text['yscrollcommand'] = self.m_textVScrollbar.set

		self.m_textHScrollbar = tk.Scrollbar(self.m_textFrame, orient=tk.HORIZONTAL)
		self.m_textHScrollbar['command'] = self.m_text.xview
		self.m_textHScrollbar.grid(row=1, column=0, sticky=tk.EW)
		self.m_text['xscrollcommand'] = self.m_textHScrollbar.set

		nbUniqueFiles = len(self.m_duplicates)
		nbDuplicates = sum(len(duplicates) for __, duplicates in self.m_duplicates.items())

		self.m_text.insert(tk.END, tr.DW_NB_FILES_PROCESSED.format(self.m_nbFilesProcessed) + '\n')
		self.m_text.insert(tk.END, tr.DW_UNIQUE_FILES_AND_DUPLICATES.format(nbUniqueFiles, nbDuplicates) + '\n')
		self.m_text.insert(tk.END, '--------------------------------------------------------------\n')

		# Populating text field
		for __, duplicates in self.m_duplicates.items():
			for duplicate in duplicates:
				self.m_text.insert(tk.END, duplicate + '\n')

			self.m_text.insert(tk.END, '--------------------------------------------------------------\n')

		self.m_closeButton = ttk.Button(self.m_mainLayout, text=tr.DW_CLOSE_BUTTON)
		self.m_closeButton['command'] = self.closeDialog
		self.m_closeButton.pack(padx=self.DEFAULT_PADDING, pady=self.DEFAULT_PADDING)


	def closeDialog(self, event=None):
		self.destroy()
