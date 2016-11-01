#!/usr/bin/env python

import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
import json

from io import StringIO
# from PyQt4 import QtGui


# todo

#---------------------------------------------------------------------------------------#
# - Connect User notes to shell tree selection
#---------------------------------------------------------------------------------------#
# - Make oz button to the left of oz input box
#		-Add dialog so you can add different oz contexts
#---------------------------------------------------------------------------------------#
# - Catch no oz's shots in tree selection and fill conected panes will null objectes
#---------------------------------------------------------------------------------------#
# - 
#---------------------------------------------------------------------------------------#
# Kill all urxvt
# kill $(pgrep urxvt)
#---------------------------------------------------------------------------------------#




class UserNotes(QtGui.QWidget):

	def __init__(self, widget_title):

		QtGui.QWidget.__init__(self)

		self.main_layoutV1 = QtGui.QVBoxLayout()
		text_grp_layoutV1 = QtGui.QVBoxLayout()
		self.user_notes = QtGui.QTextEdit()

		self.user_notes_grp = QtGui.QGroupBox('User Notes: ' + widget_title)
		self.user_notes_grp.setLayout(text_grp_layoutV1)
		self.main_layoutV1.addWidget(self.user_notes_grp)
		text_grp_layoutV1.addWidget(self.user_notes)

		self.setLayout(self.main_layoutV1)

	def getText(self):
		return str(self.user_notes.toPlainText())

	def setText(self,setText):
		self.user_notes.setPlainText(setText)
		

class Enote(QtGui.QMainWindow):
	def __init__(self, parent = None):
		super(Enote, self).__init__(parent)
		self.__mainWindow = True
		self.statusBar = QtGui.QStatusBar()
		self.setStatusBar(self.statusBar)
		self.oz_dict = {}

		self.resize(2000, 1200)
		layout = QtGui.QHBoxLayout()
		bar = self.menuBar()
		file = bar.addMenu("File")
		file.addAction("Open     (ctrl+o)", self.openScene)
		# file.addAction("Save      (ctrl+s)")
		file.addAction("Save as  (ctrl+shift+s)", self.save)




	#--# Dock Tree User Notes Bottom	
		self.dock_user_notes = QtGui.QDockWidget("User Notes", self)


		# self.dock_user_notes.setWidget(self.user_notes)222
		self.dock_user_notes.setFloating(False)
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock_user_notes)
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock_user_notes)

	#--# Dock Tree Widget Left
		# main_window_layoutV1 = QtGui.QVBoxLayout()
		self.testButton01 = QtGui.QPushButton(' ')
		self.testButton01.setFixedWidth(40)
		for x in dir(self.testButton01):
			if 'idth' in x:
				print x
		# self. = QtGui.QLineEdit
		
		# self.dock_oz_tree = QtGui.QDockWidget("Oz Shots", self)

		self.oz_user_input = QtGui.QLineEdit('show/seq01/shot01,show/seq01/shot02,show01/seq02/shot03')
		self.oz_tree_wdg = QtGui.QTreeWidget()
		self.oz_tree_wdg.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		self.oz_tree_wdg.setAlternatingRowColors(True)
		# self.setStyleSheet("self.oz_tree_wdg { alternate-background-color: rgb(100, 100, 100); }")
		self.oz_tree_grp = QtGui.QGroupBox()
		self.oz_shelf_grp = QtGui.QGroupBox('Shelf')
		treeL_layoutV1 = QtGui.QVBoxLayout()
		tree_layoutH1 = QtGui.QHBoxLayout()
		shelf_layoutH1 = QtGui.QHBoxLayout()
		self.oz_tree_grp.setLayout(treeL_layoutV1)
		self.oz_shelf_grp.setLayout(shelf_layoutH1)
		treeL_layoutV1.addWidget(self.oz_shelf_grp)
		
		tree_layoutH1.addWidget(self.testButton01)

		treeL_layoutV1.addLayout(tree_layoutH1)

		tree_layoutH1.addWidget(self.oz_user_input)
		treeL_layoutV1.addWidget(self.oz_tree_wdg)
		# self.dock_oz_tree.setWidget(self.oz_tree_grp)
		# self.dock_oz_tree.setFloating(False)
		# self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_oz_tree)
		# self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_oz_tree)
		self.setCentralWidget(self.oz_tree_grp)
		self.setHeader()

		# self.setLayout(layout)
		self.setWindowTitle("Enote1")


	#--# Signals
		self.oz_user_input.returnPressed.connect(lambda: self.ozUserInput())
		self.testButton01.clicked.connect(lambda: self.testPrint())
		self.connect (self.oz_tree_wdg, QtCore.SIGNAL ("itemClicked(QTreeWidgetItem*, int)"), self.onTreeClick)

	#--# Hotkeys
		QtGui.QShortcut(QtGui.QKeySequence("del"), self.oz_tree_wdg, self.confirmDelete)
		QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Shift+s"), self.oz_tree_wdg, self.save)
		QtGui.QShortcut(QtGui.QKeySequence("Ctrl+o"), self.oz_tree_wdg, self.openScene)

	def onTreeClick (self, item, column):

		self.setShotNote(str(item.text(0)))




	def createUserNoteClass(self, widget_title):
		klass = globals()["UserNotes"]
		self.instance = klass(widget_title)
		return self.instance



	def setShotNote(self, arg01):
		user_note_widget = self.oz_dict[str(arg01)]['userNoteWidget']
		self.dock_user_notes.setWidget(user_note_widget)





	def testPrint(self):
		print("Hello World")

		print self.jsonExport()


	def save(self):
		default_directory = ''
		output_file = QtGui.QFileDialog.getSaveFileName(self, 'Save As', default_directory, '*.json')
		if output_file:
			print 'Info:	saving to: ', output_file


		with open(str(output_file), 'w') as fp:
			json.dump(self.jsonExport(), fp, sort_keys=True, indent=4)

	def openScene(self):
		default_directory = ''
		file_to_open = QtGui.QFileDialog.getOpenFileName(self, 'Open', default_directory, '*.json')

		with open(file_to_open, 'r') as fp:
			data = json.load(fp)

		self.propergateTree(data)

	def propergateTree(self, inputDict):


		for key, val in inputDict.iteritems():
			print key, val
			oz_path = inputDict[key]['fullTreePath']
			user_notes = inputDict[key]['userNoteWidget']
			status = inputDict[key]['status']
			scratsh_pad = inputDict[key]['scratchPad']



			self.addTreeItems([oz_path])
			self.oz_dict[key]['userNoteWidget'].setText(user_notes)
			self.oz_dict[key]['status'].setCurrentIndex(status)
			self.oz_dict[key]['scratchPad'].setText(scratsh_pad)




	def confirmDelete(self):

		quit_msg = "Are you sure you want to delete the tree item?"
		reply = QtGui.QMessageBox.question(self, 'Message', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.Yes:
			tree = self.oz_tree_wdg
			root = tree.invisibleRootItem()
			# Kill Process and delete from dictionary
			for item in tree.selectedItems():
				itemText = str(item.text(0))
				if itemText in self.oz_dict:
					tree_shell = self.oz_dict[itemText]['shell']
					tree_shell.killProcess()
					self.oz_dict.pop(itemText)
				self.removeSelectedTreeItem()
		else:
			pass



	def removeSelectedTreeItem(self):
		tree = self.oz_tree_wdg
		root = tree.invisibleRootItem()
		for item in tree.selectedItems():
			(item.parent() or root).removeChild(item)


	def setHeader(self):
		'''Configures header'''
		headerTitles = ['Notes Tree                                       ', 'Tags                   ', '-                                                                                          ']
		self.headerCount = len(headerTitles)
		self.oz_tree_wdg.setColumnCount(self.headerCount)
		self.oz_tree_wdg.setHeaderLabels(headerTitles)
	#--# Set Column Width to match content:
		for column in range( self.oz_tree_wdg.columnCount()):
			self.oz_tree_wdg.resizeColumnToContents(column)
	#--# Dont know what this is doing:
		trickedout = self.oz_tree_wdg.headerItem()
		trickedout.setTextAlignment(1, 0x0004)
		trickedout.setTextAlignment(2, 0x0004)
		#self.resize()


	def getItemCount(self):
		"""Get the count of all items in tree widget
				'itemCount' set to -1 because last iteration is not a tree item
				args=None
				Return = int
		"""
		iterator = QtGui.QTreeWidgetItemIterator(self.oz_tree_wdg)
		item = iterator.value()

		itemCount = -1
		while item:
			item = iterator.value()
			itemCount += 1
			iterator += 1
		return itemCount


	def getOzList(self, input_string):
		if ',' in input_string:
			return  input_string.split(',')
		else:
			return [input_string]

	def ozUserInput(self):
		user_oz_input = self.oz_user_input.text()
		oz_list = self.getOzList(user_oz_input)
		self.addTreeItems(oz_list)

	def sanitizeString(self, input_string):
		# Remove leading double slashes
		while input_string[0] == '/':
			input_string = input_string[1:]
		lead_slash_str = input_string
		# Remove lead/trail white space
		while lead_slash_str[-1] == ' ':
			print 'trail'
			lead_slash_str = lead_slash_str[:-1]
		while lead_slash_str[0] == ' ':
			print 'lead'
			lead_slash_str = lead_slash_str[1:]
		# Add leading slash
		if lead_slash_str[0] != '/':
			lead_slash_str = "/{0}".format(lead_slash_str)
		output_string = lead_slash_str
		print "Sanatized str: ", output_string

		return output_string





	def addTreeItems(self, oz_list):
		"""Add a item to tree widget
				args=None
		"""
		print 'addTreeItems oz_list = ', oz_list
		# Handle list
		for oz_string in oz_list:
			print 'this is the oz string, ', oz_string
			sanitize_oz_string = self.sanitizeString(oz_string)
			print "This is the sanatize string: ", sanitize_oz_string
			chanel_index = sanitize_oz_string.split('/')
			# Remove first empty group due to leading slash(/)
			chanel_index = [x for x in chanel_index if x != '']
			
			iterator = QtGui.QTreeWidgetItemIterator(self.oz_tree_wdg)
			item = iterator.value()
			last_index = True

			# Itterate throug all items in tree
			# If show name dosent already exist in tree
			if chanel_index[0] in self.getRootItems():
				# itterate through the tree item count
				for x in range(self.getItemCount()):
					item = iterator.value()

					# if string exists in 'channel_index' remove from list
					# set removed item to new parent
					if item.text(0) in chanel_index:
						chanel_index.remove(item.text(0))
						new_parent = item

					iterator += 1

				# Add to tree widget with the new parent
				for index, treeItem in enumerate(chanel_index):
					# If this is the last itteration add a status combobox

					new_parent = self.addParent(new_parent, index, treeItem, '%s data' % treeItem, last_index)
					self.appendToOzDict(treeItem, sanitize_oz_string)
			# else this is the first entry into the tree widget
			else:
				# Create FIRST tree item
				for index, treeItem in enumerate(chanel_index):

					if index == 0:
						new_parent = self.addParent(self.oz_tree_wdg, index, treeItem, '%s data' % treeItem, last_index)
					else:
						new_parent = self.addParent(new_parent, index, treeItem, '%s data' % treeItem, last_index)

					self.appendToOzDict(treeItem, sanitize_oz_string)

			self.setShotNote(treeItem)
			# print self.user_notes.toPlainText()


	def appendToOzDict(self, oz_key, launch_command):
		self.oz_dict[oz_key] = {
			'fullTreePath'    :str(launch_command),
			'userNoteWidget':self.createUserNoteClass(oz_key),
			'scratchPad'    :self.scratchPadObject,
			}

	def jsonExport(self):
		'''
		store
			fullTreePath
			userNoteWidget
			status
			scratchPad

		'''
		export_dict = {}
		for key, val in self.oz_dict.iteritems():
			export_dict[key] = {
				'fullTreePath'     : str(self.oz_dict[key]['fullTreePath']),
				'userNoteWidget' : str(self.oz_dict[key]['userNoteWidget'].getText()),
				'status'         : int(self.oz_dict[key]['status'].currentIndex()),
				'scratchPad'     : str(self.oz_dict[key]['scratchPad'].text())}
		return export_dict


	def getRootItems(self):
		"""Will return a list of all the root items
				args=None
				return=list
		"""
		root = self.oz_tree_wdg.invisibleRootItem()
		child_count = root.childCount()
		return_list = []
		for i in range(child_count):
			item = root.child(i)
			itemName = item.text(0) # text at first (0) column
			return_list.append(itemName)

		if return_list == [0]:
			return []
		else:
			return return_list

	def addParent(self, parent, column, title, data, last_index):
		print "Parent-->", parent
		print "column-->", column
		print "title-->", title
		print "date-->", data
		print "last_index-->", last_index


		item =  QtGui.QTreeWidgetItem(parent, [title])
		item.setData(column, QtCore.Qt.UserRole, data)
		item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
		item.setExpanded (True)
		self.scratchPadObject = QtGui.QLineEdit()
		self.oz_tree_wdg.setItemWidget(item, 2, self.scratchPadObject)

		return item



	def closeEvent(self, event):
		self.__mainWindow = False

		# quit_msg = "Are you sure you want to Exit?"
		# reply = QtGui.QMessageBox.question(self, 'Message', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

		# if reply == QtGui.QMessageBox.Yes:
		# 	self.killAllShellEmbedItems()
		# 	event.accept()

		# else:
		# 	event.ignore()


def main():
	app = QtGui.QApplication(sys.argv)
	ex = Enote()
	ex.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()



