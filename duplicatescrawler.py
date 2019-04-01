"""
This class looks for duplicates in 3 passes:
	- First pass: Compares files by size, files that have the same size may be duplicates
	- Second pass: Compares the hashes of the files on the first kb
	- Third pass: Compares the hashes of the entire files where the first kb hashes matches

Going through passes makes the algorithm more efficient. Instead of hashing every single file
(heavy on processing power), we just compare their sizes. If the sizes don't match, the files
are different anyway. If they match, we hash just the 1st kb (fast, and only on select files
that have the same size). Only if the first kb matches do we hash the entire files.

See https://stackoverflow.com/a/36113168/10775702 for more info

This works in a separate thread.
Call DuplicatesCrawler.start().
"""

import threading
import os
import hashlib


class ThreadEndRequested(Exception):
	pass


class DuplicatesCrawler(threading.Thread):
	def __init__(self, parent, folders):
		threading.Thread.__init__(self)

		self.m_parent = parent
		self.m_folders = folders
		self.m_requestThreadEnd = False

	def run(self):
		# Dictionaries are more efficient than lists, especially large ones

		# hashesBySize = {
		#   456544 = [file1, file2, file3], -> Duplicates
		#   865 = [file1] -> Single
		# }
		hashesBySize = {}
		hashesByFirstKB = {}
		hashesByFile = {}

		# 1st Pass: By File Size
		i = 0  # Number of files processed
		self.m_parent.updateStatus(step=1, progress=0)
		for folder in self.m_folders:
			# os.walk(): Lists files in a folder recursively (one iteration for the given folder + 1 for each sub folder, etc.)
			# dirpath = Path of current directory (one per iteration)
			# dirnames = Names of folders in that directory
			# filenames = Names of files in that directory

			for dirpath, dirnames, filenames in os.walk(folder):
				# For each file in the directory
				for fileName in filenames:
					if self.m_requestThreadEnd is True:
						return

					fullPath = os.path.join(dirpath, fileName)
					try:
						# Replace symlinks by real file & Get file size
						fullPath = os.path.realpath(fullPath)
						fileSize = os.path.getsize(fullPath)
					except (OSError,):
						# File cannot be accessed or whatever
						continue

					# If file size already in dictionary it will return it, else fail
					duplicate = hashesBySize.get(fileSize)

					if not duplicate:
						hashesBySize[fileSize] = []  # Create a list of files that have that size

					hashesBySize[fileSize].append(fullPath)  # And append the current file to the dictionary, indexed by file size

					# Updating status
					i += 1  # One more file
					self.m_parent.updateStatus(step=1, progress=i)

		nbFilesProcessed = i

		# 2nd Pass: By 1st kb Hash
		# dictionary.items() returns a list of tuples (key, value)
		# Every iteration is a list of files having the same size (__ = (unused) size)
		i = 0
		nbFilesToProcess = sum(len(files) for __, files in hashesBySize.items())
		self.m_parent.updateStatus(step=2, progress=0, total=nbFilesToProcess)
		for __, files in hashesBySize.items():
			# Single files have no duplicates
			if len(files) < 2:
				i += 1
				self.m_parent.updateStatus(step=2, progress=i, total=nbFilesToProcess)
				continue

			for fullPath in files:
				if self.m_requestThreadEnd is True:
					return

				# Updating status
				i += 1  # One more file
				self.m_parent.updateStatus(step=2, progress=i, total=nbFilesToProcess)

				try:
					smallHash = self.getFileHash(fullPath, firstChunkOnly=True)
				except (OSError, ThreadEndRequested):
					# File access & shit
					continue

				duplicate = hashesByFirstKB.get(smallHash)

				if not duplicate:
					hashesByFirstKB[smallHash] = []

				hashesByFirstKB[smallHash].append(fullPath)

		# 3rd Pass: By File Hash
		# Same as 2nd pass, only for entire file instead of chunk
		i = 0
		nbFilesToProcess = sum(len(files) for __, files in hashesByFirstKB.items())
		self.m_parent.updateStatus(step=3, progress=0, total=nbFilesToProcess)
		for __, files in hashesByFirstKB.items():
			if len(files) < 2:
				i += len(files)
				self.m_parent.updateStatus(step=3, progress=i, total=nbFilesToProcess)
				continue

			for fullPath in files:
				if self.m_requestThreadEnd is True:
					return

				# Updating status
				i += 1  # One more file
				self.m_parent.updateStatus(step=3, progress=i, total=nbFilesToProcess)

				try:
					fullHash = self.getFileHash(fullPath)
				except (OSError, ThreadEndRequested):
					continue

				duplicate = hashesByFile.get(fullHash)

				if not duplicate:
					hashesByFile[fullHash] = []

				hashesByFile[fullHash].append(fullPath)

		# Final step, cleaning the dictionary
		keysToRemove = []
		for key, files in hashesByFile.items():
			if self.m_requestThreadEnd is True:
				return

			if len(files) < 2:
				keysToRemove.append(key)

		for key in keysToRemove:
			if self.m_requestThreadEnd is True:
				return

			if key in hashesByFile:
				del hashesByFile[key]  # del does not return the value like pop()

		if self.m_requestThreadEnd is False:
			# Contains duplicates sorted by hash
			self.m_parent.processingEnded(hashesByFile, nbFilesProcessed)

	def getFileHash(self, fileName, firstChunkOnly=False, chunkSize=1024):
		hashObj = hashlib.sha1()
		fileObj = open(fileName, 'rb')

		if firstChunkOnly:
			hashObj.update(fileObj.read(chunkSize))
		else:
			for chunk in self.readFileByChunk(fileObj, chunkSize):
				hashObj.update(chunk)

		hashed = hashObj.digest()

		fileObj.close()

		return hashed

	def readFileByChunk(self, fileObj, chunkSize):
		while True:
			if self.m_requestThreadEnd is True:
				raise ThreadEndRequested

			# At each iteration we read the next chunk of chunkSize bytes
			chunk = fileObj.read(chunkSize)

			# If chunk is empty we have read the whole file and return
			if not chunk:
				return

			# yield returns the value of the chunk without terminating the function
			# Each yield is read as an item of an array in for chunk in self.readFileByChunk(fileObj, chunkSize):
			# The benefit over returning a list is that we only keep a chunk in memory, and not an entire file
			yield chunk

	def terminate(self):
		"""
		Threads can't be terminated, so we fake it using self.m_requestThreadEnd.
		At every stage of the process, we check self.m_requestThreadEnd and quit
		if it is set to True.
		"""
		self.m_requestThreadEnd = True
