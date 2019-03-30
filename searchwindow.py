import tkinter as tk
from tkinter import ttk

LANG = 'en'

if LANG == 'fr':
	import translation.fr as tr
else:  # English is default
	import translation.en as tr


class SearchWindow(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		# Constants
		self.DEFAULT_PADDING = 7

		# Attributes
		self.m_parent = parent
		self.m_progress = 100

		# Window configuration
		self.m_parent.protocol('WM_DELETE_WINDOW', self.cancelProcessing)  # Override default 'Quit Cross' behaviour
		self.m_parent.bind('<Escape>', self.cancelProcessing)  # Link Esc to quit function

		self.m_parent.title('Duplicates - ' + tr.SW_TITLE)  # Window title
		self.m_parent.resizable(False, False)  # Not resizable

		x = int((self.m_parent.winfo_screenwidth() - self.m_parent.winfo_reqwidth()) / 2)
		y = int((self.m_parent.winfo_screenheight() - self.m_parent.winfo_reqheight()) / 2.5)

		self.m_parent.geometry("+{}+{}".format(x + 10, y + 10))  # Position window on screen

		# Main window layout
		self.m_mainLayout = tk.Frame(self)
		self.m_mainLayout.pack(padx=self.DEFAULT_PADDING, pady=self.DEFAULT_PADDING)

		self.m_statusLabel = tk.Label(self.m_mainLayout, text=tr.SW_STATUS_LABEL, anchor=tk.W)
		self.m_statusLabel.pack(fill=tk.X, pady=0)

		self.m_progressBar = ttk.Progressbar(self.m_mainLayout, mode='indeterminate', length=270)
		self.m_progressBar['maximum'] = 100
		self.m_progressBar['value'] = 100
		self.m_progressBar['variable'] = self.m_progress
		self.m_progressBar.pack(fill=tk.X)

		self.m_cancelButton = ttk.Button(self.m_mainLayout, text=tr.SW_CANCEL_BUTTON)
		self.m_cancelButton['command'] = self.cancelProcessing
		self.m_cancelButton.pack(pady=(self.DEFAULT_PADDING, 0))

	def startProcessing(self, folders):
		print('start')
		# ...
		# self.processingEnded()

	def cancelProcessing(self, event=None):
		print('stop')
		self.m_parent.destroy()

	def processingEnded(self):
		print('end')
		self.m_parent.destroy()

if __name__ == '__main__':
	root = tk.Tk()
	root.tk_setPalette(background='#ececec')
	sw = SearchWindow(root)
	sw.pack()
	sw.mainloop()
