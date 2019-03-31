import tkinter as tk
from tkinter import ttk

from duplicatescrawler import *

from lang import *


class SearchWindow(tk.Toplevel):
	def __init__(self, parent, folders):
		tk.Toplevel.__init__(self, parent)

		# Constants
		self.DEFAULT_PADDING = 7

		# Attributes
		self.m_parent = parent
		self.m_folders = folders
		self.m_duplicatesCrawler = DuplicatesCrawler(self, self.m_folders)

		# Window configuration
		self.protocol('WM_DELETE_WINDOW', self.cancelProcessing)  # Override default 'Quit Cross' behaviour
		self.bind('<Escape>', self.cancelProcessing)  # Link Esc to quit function

		self.title('Duplicates - ' + tr.SW_TITLE)  # Window title
		self.resizable(False, False)  # Not resizable

		x = int((self.winfo_screenwidth() - self.winfo_reqwidth()) / 2)
		y = int((self.winfo_screenheight() - self.winfo_reqheight()) / 2.5)

		self.geometry("+{}+{}".format(x + 10, y + 10))  # Position window on screen

		# Main window layout
		self.m_mainLayout = tk.Frame(self)
		self.m_mainLayout.pack(padx=self.DEFAULT_PADDING, pady=self.DEFAULT_PADDING)

		self.m_statusLabel = tk.Label(self.m_mainLayout, text=tr.SW_STATUS_LABEL, anchor=tk.W)
		self.m_statusLabel.pack(fill=tk.X, pady=0)

		self.m_progressBar = ttk.Progressbar(self.m_mainLayout, mode='indeterminate', length=270)
		self.m_progressBar['maximum'] = 100
		self.m_progressBar['value'] = 100
		self.m_progressBar.pack(fill=tk.X)

		self.m_cancelButton = ttk.Button(self.m_mainLayout, text=tr.SW_CANCEL_BUTTON)
		self.m_cancelButton['command'] = self.cancelProcessing
		self.m_cancelButton.pack(pady=(self.DEFAULT_PADDING, 0))

	def startProcessing(self):
		self.m_duplicatesCrawler.start()

	def cancelProcessing(self, event=None):
		self.m_duplicatesCrawler.terminate()
		self.destroy()

	def processingEnded(self, duplicates):
		self.m_parent.searchResult(duplicates)
		self.destroy()

if __name__ == '__main__':
	root = tk.Tk()
	root.tk_setPalette(background='#ececec')
	sw = SearchWindow(root)
	sw.pack()
	sw.mainloop()
