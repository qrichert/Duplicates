"""
Main window class

To-do:
- If a folder is selected, give the option to add another one.
  With two folders you don't need to crawl the whole system
  if you know where to look.
- Maybe even make a list of folders to crawl with "+" and "-"
"""

import os
import ntpath
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

LANG = 'en'

if LANG == 'fr':
	import translation.fr as tr
else:  # English is default
	import translation.en as tr

class MainWindow(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

	# Constants
		self.DEFAULT_PADDING = 7

		# Attributes
		self.m_parent = parent
		self.m_folders = []
		self.m_foldersFormattedName = []
		self.m_lastFolder = None

		# Main window layout
		self.m_mainLayout = tk.Frame(self)
		self.m_mainLayout.pack(padx=self.DEFAULT_PADDING, pady=self.DEFAULT_PADDING)

		self.m_helpLabel = tk.Label(self.m_mainLayout, text=tr.SELECT_FOLDER_HELP_LABEL, anchor=tk.W)
		self.m_helpLabel.pack(fill=tk.X, pady=(0, self.DEFAULT_PADDING))

		self.m_foldersListFrame = tk.Frame(self.m_mainLayout, bg='white', bd=0)
		self.m_foldersListFrame.pack(fill=tk.X)

		self.m_foldersList = tk.Listbox(self.m_foldersListFrame, bg='white', bd=0, width=30, selectmode=tk.EXTENDED)
		self.m_foldersList['activestyle'] = 'none'
		self.m_foldersList['selectbackground'] = '#2257c9'
		self.m_foldersList['selectforeground'] = 'white'
		self.m_foldersList['selectborderwidth'] = 0
		self.m_foldersList.pack(fill=tk.BOTH, padx=2, pady=2)
		self.m_foldersList.bind('<BackSpace>', self.removeFolders)
		self.m_foldersList.bind('<Delete>', self.removeFolders)

		self.m_buttonsLayout = tk.Frame(self.m_mainLayout)
		self.m_buttonsLayout.pack(side=tk.RIGHT)

		self.m_removeFolderButton = ttk.Button(self.m_buttonsLayout, text='-')
		self.m_removeFolderButton.pack(side=tk.RIGHT)
		self.m_removeFolderButton.bind('<Button-1>', self.removeFolders)

		self.m_addFolderButton = ttk.Button(self.m_buttonsLayout, text='+')
		self.m_addFolderButton.pack(side=tk.RIGHT)
		self.m_addFolderButton.bind('<Button-1>', self.addFolder)

	def addFolder(self, event=None):
		# Get either user directory or last folder opened if any
		initialdir = self.m_lastFolder or os.path.expanduser('~')

		folder = filedialog.askdirectory(initialdir=initialdir, title=tr.SELECT_FOLDER_DIALOG_TITLE)

		if folder is None or folder == '':
			return

		for f in self.m_folders:
			# Same folder already added
			if folder == f:
				messagebox.showinfo(title=tr.SELECT_FOLDER_ERROR_ALREADY_IN_LIST_DIALOG_TITLE,
				                    message=tr.SELECT_FOLDER_ERROR_ALREADY_IN_LIST_DIALOG_MESSAGE)
				return

			# Child of folder already added
			if folder.startswith(f):
				messagebox.showinfo(title=tr.SELECT_FOLDER_ERROR_PARENT_ALREADY_IN_LIST_DIALOG_TITLE,
				                    message=tr.SELECT_FOLDER_ERROR_PARENT_ALREADY_IN_LIST_DIALOG_MESSAGE)
				return

			# Parent of folder already added -> Remove children
			if f.startswith(folder):
				if messagebox.askyesno(title=tr.SELECT_FOLDER_ERROR_CHILDREN_ALREADY_IN_LIST_DIALOG_TITLE,
				                       message=tr.SELECT_FOLDER_ERROR_CHILDREN_ALREADY_IN_LIST_DIALOG_MESSAGE):
					self.removeChildrenOfFolder(folder)
					break
				else:
					return

		# Append full path to internal list (not displayed)
		self.m_folders.append(folder)

		# Separate path from file/folder name
		# /Users/Quentin/Movies  -> (h: '/Users/Quentin' - t: 'Movies')
		# /Users/Quentin/Movies/ -> (h: '/Users/Quentin/Movies' - t: '')
		head, tail = ntpath.split(folder)  # head = path, tail = folder name (if path ends with /, tail = '')

		# Here we want the selected folder's parent to open next time
		# if tail not empty, head contains parent path
		# if tail empty, head = full path -> get parent path of head
		self.m_lastFolder = head if tail != '' else ntpath.dirname(head)

		# Here we want the selected folder's name for display
		# if tail not empty, tail contains the folder name
		# if tail is empty, head = full path -> get folder name (head doesn't have a trailing / at this point)
		folder = tail if tail != '' else ntpath.basename(head)

		self.m_foldersFormattedName.append(folder)
		self.m_foldersList.insert(tk.END, folder)

	def removeChildrenOfFolder(self, folder):
		foldersToRemove = []
		foldersFormattedNameToRemove = []

		i = 0
		for f in self.m_folders:
			if f.startswith(folder):
				# We don't pop it straight away not to mess up with the loop
				foldersToRemove.append(self.m_folders[i])
				foldersFormattedNameToRemove.append(self.m_foldersFormattedName[i])
			i += 1

		for f in foldersToRemove:
			self.m_folders.remove(f)

		for f in foldersFormattedNameToRemove:
			self.m_foldersFormattedName.remove(f)

		self.rebuildFoldersList()

	def removeFolders(self, event=None):
		foldersToRemoveIndexes = self.m_foldersList.curselection()

		foldersToRemove = []
		foldersFormattedNameToRemove = []

		for f in foldersToRemoveIndexes:
			foldersToRemove.append(self.m_folders[f])
			foldersFormattedNameToRemove.append(self.m_foldersFormattedName[f])

		for f in foldersToRemove:
			self.m_folders.remove(f)

		for f in foldersFormattedNameToRemove:
			self.m_foldersFormattedName.remove(f)

		self.rebuildFoldersList()

	def rebuildFoldersList(self):
		"""Clears the folder list display and re-fills it properly"""
		self.m_foldersList.delete(0, tk.END)

		for f in self.m_foldersFormattedName:
			self.m_foldersList.insert(tk.END, f)
