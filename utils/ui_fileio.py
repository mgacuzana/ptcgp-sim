import os
import sys
import time
import datetime

from consts import Rarity#, parse_rarity_str
#from modules.expansion import Expansion
#from modules.pack import Pack
#from modules.card import Card
from modules.collection import Collection
from utils.fileio import load_collection, save_collection, get_script_folder, get_settings, set_settings

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox
from PyQt5.QtCore import Qt


class UICollectionSelectionTab(object):
	def __init__(self):
		self.selected_collection = None
		self.base_path = get_script_folder() / "collections"
		self.LABELS = (
			'Collection Name',
			'# of Cards',
			'# of Rares',
			'Edit Date'
			)

	def setupUI(self, MainWindow):

		#Setup new window box
		MainWindow.setWindowTitle('Would you like to save your cards to a collection?')
		self.centralwidget = QWidget(MainWindow)
		MainWindow.setGeometry(100, 100, 1300, 800)


		#Show current collections on the left side
		self.option_display = QVBoxLayout()
		options_label = QLabel('Here are the collections in your current directory')
		options_label.setAlignment(Qt.AlignCenter)

		confirm_option_row = QHBoxLayout()
		self.option_chosen = QLineEdit('')
		option_confirm = QPushButton('Select')
		option_confirm.clicked.connect(self.confirm_selection)

		
		self.make_table()

		confirm_option_row.addWidget(self.option_chosen)
		confirm_option_row.addWidget(option_confirm)



		self.option_display.addWidget(options_label)
		self.option_display.addWidget(self.collection_display)
		self.option_display.addLayout(confirm_option_row)


		#Show current selection on the left side
		selected_display = QVBoxLayout()
		settings = get_settings()
		current_collection, ext = os.path.splitext(settings['Current Collection'])
		self.selected_header = QLabel('')
		if not current_collection == 'None':
			self.selected_header.setText("You've selected {}.".format(current_collection))
		else:
			self.selected_header.setText("You've not selected a collection, yet.")
		self.selected_header.setAlignment(Qt.AlignCenter)
		self.BackBTN = QPushButton("Back", self.centralwidget)


		selected_display.addWidget(self.selected_header)
		selected_display.addWidget(self.BackBTN)

		#Create main layout and add sub_layouts
		main_layout = QHBoxLayout()
		main_layout.addLayout(self.option_display)
		main_layout.addLayout(selected_display)

		self.centralwidget.setLayout(main_layout)
		MainWindow.setCentralWidget(self.centralwidget)

	def on_row_selected(self):
		row_num = self.collection_display.currentRow()
		selection = self.collection_display.item(row_num, 0)
		if selection is not None:
			self.option_chosen.setText(selection.text())

	def confirm_selection(self):
		#Get current selected file and its path
		selection = self.option_chosen.text()
		file_path = os.path.join(self.base_path, selection + ".json")
		
		#If the file exists, then add it to seleted
		if os.path.isfile(file_path):
			self.selected_header.setText("You've selected {}.".format(selection))
			filename = selection + ".json"
			set_settings(collection = filename)

			self.selected_collection = file_path
		#otherwise, confirm if the user intended to make a new collection.
		else:
			question = 'There is no collection such collection as "{}". Would you like to make a new collection with that name?'.format(selection)
			answer = self.confirmation_dialog(question)
			if answer:
				#Make a new, empty collection and set it to the selected collection
				save_collection("{}.json".format(selection), Collection())
				self.selected_header.setText("You've selected {}.".format(selection))
				filename = selection + ".json"
				set_settings(collection = filename)
				self.selected_collection = file_path

				#Remove the old collection display screen and replace it with the new table list
				self.option_display.removeWidget(self.collection_display)
				self.make_table()
				self.option_display.insertWidget(1, self.collection_display)



	def confirmation_dialog(self, confirmation):
		reply = QMessageBox.question(self.centralwidget, 'Confirmation',
			confirmation, QMessageBox.Yes |
			QMessageBox.No, QMessageBox.No)

		if reply == QMessageBox.Yes:
			return True
		else:
			return False

	def make_table(self):
		self.collection_display = QTableWidget(10,4, 
								selectionBehavior=QAbstractItemView.SelectRows,
            					selectionMode=QAbstractItemView.SingleSelection
            					)
		self.collection_display.setHorizontalHeaderLabels(self.LABELS)
		self.collection_display.itemSelectionChanged.connect(self.on_row_selected)
		collection_data = collection_table_data()

		#add scroll buttons to allow for more rows later
		if len(collection_data) >= 10:
			collection_data = collection_data[0:9]

		for i, collection in enumerate(collection_data):
			collection_name = QTableWidgetItem(collection['Name'])
			print(collection['Name'])
			collection_cards = QTableWidgetItem(str(collection['# of Cards']))
			collection_rares = QTableWidgetItem(str(collection['# of Rares']))
			collection_date = QTableWidgetItem(collection['Edit Date'])

			self.collection_display.setItem(i, 0, collection_name)
			self.collection_display.setItem(i, 1, collection_cards)
			self.collection_display.setItem(i, 2, collection_rares)
			self.collection_display.setItem(i, 3, collection_date)


class UISettingsTab(object):
    def setupUI(self, MainWindow):
        ##Create a new UI where the user can select one of the given expansions
        #Set the window size, title, and central widgets
        MainWindow.setWindowTitle("Settings")
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setGeometry(50, 50, 900, 900)


        settings_menu = QGridLayout()

        current_settings = get_settings()

        #First settings item
        settings_menu.addWidget(QLabel('Show Pack Contents?'), 0, 0)
        self.show_pack_contents_btn = QPushButton('     ')
        self.show_pack_contents_btn.setCheckable(True)
        if current_settings['Show packs'] == 'Yes':
            self.show_pack_contents_btn.setChecked(True)
        self.show_pack_contents_btn.clicked.connect(self.updateButtonStates)
        settings_menu.addWidget(self.show_pack_contents_btn, 0, 1)

        #Second settings item
        self.save_cards_btn = QPushButton('     ')
        self.save_cards_btn.setCheckable(True)
        if current_settings['Save to collection'] == 'Yes':
            self.save_cards_btn.setChecked(True)
        self.save_cards_btn.clicked.connect(self.updateButtonStates)
        settings_menu.addWidget(QLabel('Save cards to a collection?'), 1, 0)
        settings_menu.addWidget(self.save_cards_btn, 1, 1)

        #Set Button States
        self.updateButtonStates()



        button_row = QHBoxLayout()
        SaveBTN = QPushButton('Save Changes')
        SaveBTN.clicked.connect(self.save_changes)
        self.BackBTN = QPushButton('Back')

        button_row.addWidget(SaveBTN)
        button_row.addWidget(self.BackBTN)
        

        main_layout = QVBoxLayout()
        main_layout.addLayout(settings_menu)
        main_layout.addLayout(button_row)

        #send layout to main window
        self.centralwidget.setLayout(main_layout)
        MainWindow.setCentralWidget(self.centralwidget)

    def save_changes(self):
    	show_packs = self.show_pack_contents_btn.isChecked()
    	save_collection = self.save_cards_btn.isChecked()
    	set_settings(show_packs = show_packs, save_collection = save_collection)

    def updateButtonStates(self):

 
        # if button is checked
        if self.show_pack_contents_btn.isChecked():
            #self.show_pack_contents_btn.setStyleSheet("background-color : lightblue")
            self.show_pack_contents_btn.setText('Show Packs')
        # if it is unchecked
        else:
            #self.show_pack_contents_btn.setStyleSheet("background-color : lightgrey")
            self.show_pack_contents_btn.setText("Don't Show Packs")

        if self.save_cards_btn.isChecked():
        	self.save_cards_btn.setText('Save Cards')
        else:
        	self.save_cards_btn.setText("Don't Save Cards")

def collection_table_data():
	base_path = get_script_folder() / "collections"
	if not os.path.exists(base_path):
		os.makedirs(base_path)
	
	collection_info = []
	for file in os.listdir(base_path):
		name, ext = os.path.splitext(file)

		#get edit date
		read_edit_date = time.ctime(os.path.getmtime(base_path / file))
		edit_datetime = datetime.datetime.strptime(str(read_edit_date), "%a %b %d %H:%M:%S %Y")
		formatted_date = edit_datetime.strftime("%Y-%m-%d")
		if ext == '.json':

			temp_collection = load_collection(file)

			#Count cards !!ONLY COUNTS UNIQUE CARD TYPES NOT TOTAL NUMBER OF CARDS!!
			num_cards = 0
			num_rares = 0
			for card in temp_collection.items():
				if not card[0].rarity < Rarity.STAR_1:
					num_rares += card[1]
				num_cards += card[1]

			#summarize info
			collection_info.append({"Name": name, "# of Cards": num_cards, "# of Rares": num_rares, "Edit Date": formatted_date})

	return collection_info


