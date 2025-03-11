from modules.collection import Collection
#from modules.expansion import Expansion
from modules.pack import Pack

from utils.fileio import load_collection, save_collection, get_settings
from ui_dialogs import InputErrorDialog, OpenPackDialog

from PyQt5.QtWidgets import QPushButton , QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator




class UIExpansionsTab(object):
    def setupUI(self, MainWindow, all_expansions):

        ##Create a new UI where the user can select one of the given expansions
        MainWindow.setWindowTitle("Pick an Expansion!")
        self.centralwidget = QWidget(MainWindow)

        #Set the window size to fit all of the buttons that will be created
        self.all_expansions = all_expansions
        num_buttons = len(self.all_expansions)
        width = 600*num_buttons
        MainWindow.setGeometry(50, 50, width, 900)


        
        #Generate expansion selection buttons and place them next to eachother in an HBox
        self.buttons_hbox = QHBoxLayout()
        buttons = []
        for i, expansion in enumerate(self.all_expansions):
            buttons.append( QPushButton(expansion.__str__(), self.centralwidget))

            #Connect each button to a lambda function calling pack selection with its own expansion
            #I do no know why the 'ch' argument is required, but I'm guessing it relates to the self argument
            buttons[i].clicked.connect(lambda ch, i = i, exp = expansion: self.expansionSelection(i, exp))

            self.buttons_hbox.addWidget(buttons[i])
            buttons[i].setFixedHeight(900)

        #Create a bottom row of buttons to return to the main navigation page or proceed to selection
        #self.SelectedExp = QLineEdit("Pick an expansion")
        self.PacksBTN = QPushButton("Select")
        self.BackBTN = QPushButton("Back", self.centralwidget)
        #self.BackBTN.move(100, 350)

        bottom_row = QHBoxLayout()
        bottom_row.addWidget(self.PacksBTN)
        bottom_row.addWidget(self.BackBTN)

        #Place the expansion selection buttons and back button into the main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.buttons_hbox)
        main_layout.addLayout(bottom_row)

        #Honestly not exactly sure what this does (pushes new layout to the main window?)
        self.centralwidget.setLayout(main_layout)
        MainWindow.setCentralWidget(self.centralwidget)

    def expansionSelection(self, expansion_id, selected_exp):
        #this attribute is tied to the expansion tab itself which can be accessed by the mainwindow object during startUIPackSelectionTab(self):
        self.selected_exp = selected_exp


        for i in range(self.buttons_hbox.count()):
            self.buttons_hbox.itemAt(i).widget().setStyleSheet("background-color:#ffffff;")
        self.buttons_hbox.itemAt(expansion_id).widget().setStyleSheet("background-color:#c0c8cf;")



class UIPackSelectionTab(object):
    def setupUI(self, MainWindow, pack_list):
        ##Create a new UI where the user can select one of the given expansions
        MainWindow.setWindowTitle("What Pack would you like to open?")
        self.centralwidget = QWidget(MainWindow)

        #Set the window size to fit all of the buttons that will be created
        num_buttons = len(pack_list)
        width = 600*num_buttons
        MainWindow.setGeometry(50, 50, width, 900)


        
        #Generate expansion selection buttons and place them next to eachother in an HBox
        self.buttons_hbox = QHBoxLayout()
        buttons = []
        self.pack_list = pack_list
        self.selected_pack = None
        for i, pack in enumerate(pack_list):
            buttons.append( QPushButton(pack.__str__(), self.centralwidget))

            #Connect each button to a lambda function calling pack selection with its own expansion
            #I do no know why the 'ch' argument is required, but I'm guessing it relates to the self argument
            buttons[i].clicked.connect(lambda ch, i= i: self.packSelection(i))

            self.buttons_hbox.addWidget(buttons[i])
            buttons[i].setFixedHeight(900)

        


        ##Create a bottom row of buttons to return to the main navigation page or proceed to selection

        #Create left section of the row where a user can select a number of packs
        numPacksPrompt = QVBoxLayout()
        self.NumPrompt = QLabel("How many packs?")

        numSelect = QHBoxLayout()
        self.DecrementBTN = QPushButton("-")
        self.DecrementBTN.clicked.connect(self.numPacksDown)
        self.NumPacks = QLineEdit("1")
        self.IncrementBTN = QPushButton("+")
        self.IncrementBTN.clicked.connect(self.numPacksUp)

        numSelect.addWidget(self.DecrementBTN)
        numSelect.addWidget(self.NumPacks)
        numSelect.addWidget(self.IncrementBTN)
        numSelect.setSpacing(0)
        

        numPacksPrompt.addWidget(self.NumPrompt)
        numPacksPrompt.addLayout(numSelect)

        #Format numpacks ui features to look like one connected widget
        self.DecrementBTN.setFixedWidth(50)
        self.DecrementBTN.setFixedHeight(50)
        self.NumPacks.setFixedWidth(125)
        self.NumPacks.setFixedHeight(50)
        self.IncrementBTN.setFixedWidth(50)
        self.IncrementBTN.setFixedHeight(50)
        self.NumPacks.setAlignment(Qt.AlignCenter)
        self.NumPacks.setValidator(QIntValidator(1,999))
        numPacksPrompt.setAlignment(self.NumPrompt, Qt.AlignCenter)

        #Add open packs and back button
        self.OpenPacksBTN = QPushButton("Open!")
        self.OpenPacksBTN.clicked.connect(self.openPacks)
        self.BackBTN = QPushButton("Back", self.centralwidget)

        bottom_row = QHBoxLayout()
        bottom_row.addLayout(numPacksPrompt)
        bottom_row.addWidget(self.OpenPacksBTN)
        bottom_row.addWidget(self.BackBTN)

        #Place the expansion selection buttons and back button into the main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.buttons_hbox)
        main_layout.addLayout(bottom_row)

        #Load the built layout into the main window so it is shown instead of the previous tab
        self.centralwidget.setLayout(main_layout)
        MainWindow.setCentralWidget(self.centralwidget)

    def numPacksDown(self):
        one_down = int(self.NumPacks.text()) - 1
        #The user should only be able to open positive integers of packs
        if one_down < 1:
            error_message = "Error: Cannot open less than one (1) pack."
            error_dialog = InputErrorDialog(error_message)
            error_dialog.exec_()
        #this error catch may not be necessary since this button should decrement the counter, but I've left it just in case.
        elif one_down > 999:
            error_message = "Error: You could open more than 999 packs, but I won't let you :P"
            error_dialog = InputErrorDialog(error_message)
            error_dialog.exec_()
        else:
            self.NumPacks.setText(str(one_down))

    def numPacksUp(self):
        #Increment number of packs by 1 but ensure the total number is in bounds
        one_more = int(self.NumPacks.text()) + 1
        #this error catch may not be necessary since this button should increment the counter, but I've left it just in case.
        if one_more < 1:
            error_message = "Error: Cannot open less than one (1) pack."
            error_dialog = InputErrorDialog(error_message)
            error_dialog.exec_()
        #keep number in UI bounds and keep program running smoothly by limiting number of packs
        #this limit should possibly be lowered to 99 to prevent tediously clicking through hundreds of packs when show_packs is on.
        #(or maybe add skip rest of packs feature)
        elif one_more > 999:
            error_message = "Error: You could open more than 999 packs, but I won't let you :P"
            error_dialog = InputErrorDialog(error_message)
            error_dialog.exec_()
        else:
            self.NumPacks.setText(str(one_more))


    def packSelection(self, pack_type_id):
        pack_type = self.pack_list[pack_type_id]
        self.selected_pack = pack_type

        for i in range(self.buttons_hbox.count()):
            self.buttons_hbox.itemAt(i).widget().setStyleSheet("background-color:#ffffff;")
        self.buttons_hbox.itemAt(pack_type_id).widget().setStyleSheet("background-color:#c0c8cf;")


    def openPacks(self):

        #read settings and selections to determine pack opening functions
        settings = get_settings()
        #need to add a feature that handles if a pack_type has not yet been selected by user
        pack_type = self.selected_pack
        num_packs = int(self.NumPacks.text())
        temp_collection = Collection()

        for i in range(num_packs):
            pack = Pack(pack_type.name, pack_type.available, pack_type.pull_rates, pack_type.rare_pack_rate)
            received = pack.open(instantaneous = True)

            for card in pack.cards:
                temp_collection.add(card)

            if pack.is_rare:
                alert = "Rare Pack Opend!!"
                alert_dialog = InputErrorDialog(alert)
                alert_dialog.exec()

            if settings['Show packs'] == 'Yes':
                pack_dialog = OpenPackDialog(received)
                pack_dialog.exec_()

        if settings['Save to collection'] == "Yes":
	        answer = self.confirmation_dialog("You opened {} unique cards! Would you like to add them to your collection?".format(len(temp_collection.items())))

	        if answer:
	            collection_name = get_settings()['Current Collection']
	            working_collection = load_collection(collection_name)
	            working_collection += temp_collection
	            save_collection(collection_name, working_collection, overwrite = True)
        

    def confirmation_dialog(self, confirmation):
        reply = QMessageBox.question(self.centralwidget, 'Confirmation',
            confirmation, QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            return True
        else:
            return False