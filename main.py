import getopt
import sys

#from modules.collection import Collection
#from modules.expansion import Expansion
#from modules.pack import Pack
from utils.fileio import load_expansions, load_collection
from utils.ui_fileio import UICollectionSelectionTab, UISettingsTab

from ui_main_tabs import UIExpansionsTab, UIPackSelectionTab

from PyQt5.QtWidgets import QApplication , QMainWindow , QPushButton , QWidget, QHBoxLayout, QVBoxLayout



##Global Functions
#its possible this function is not required. may need to be removed later.
def handle_opts():
    in_batch_mode = False
    existing_collection_filename = None

    arguments = sys.argv[1:]
    short_opts = "bI:"
    long_opts = ["batch-mode", "use-collection="]
    selected_opts, _ = getopt.getopt(arguments, short_opts, long_opts)
    for opt, val in selected_opts:
        if opt in ("-b", "--batch-mode"):
            in_batch_mode = True
        elif opt in ("-I", "--use-collection"):
            if val.endswith(".json"):
                existing_collection_filename = val
            else:
                existing_collection_filename = f"{val}.json"
    # flags = [key for key, val in selected_opts if val == '']
    # in_batch_mode = "--batch-mode" in flags or "-b" in flags
    return in_batch_mode, existing_collection_filename





class UIWindow(object):
    def setupUI(self, MainWindow):
        
        MainWindow.setWindowTitle("PTCGP SIM App")
        self.centralwidget = QWidget(MainWindow)
        ##!!THE MENU DOES NOT RESIZE PROPERLY WHEN RELOADING FROM THE EXPANSION SELECTION TAB. BUG REASON UNKNOWN
        MainWindow.setGeometry(100, 100, 1200, 400)

        hbox = QHBoxLayout()

        #The left side of the start menu has button to change collection or settings
        #Neither button is implemented yet
        menu_buttons = QVBoxLayout()
        self.settings_button = QPushButton("Settings", self.centralwidget)
        self.collection_button = QPushButton("Select Collection", self.centralwidget)

        menu_buttons.addWidget(self.settings_button)
        menu_buttons.addWidget(self.collection_button)
        menu_buttons.setSpacing(0)

        #The left side of the menu is one big button to select
        self.ToolsBTN = QPushButton('Expansion Tab', self.centralwidget)

        hbox.addLayout(menu_buttons)
        hbox.addWidget(self.ToolsBTN)
        self.settings_button.setFixedHeight(188)
        self.collection_button.setFixedHeight(188)
        self.ToolsBTN.setFixedHeight(375)

        self.centralwidget.setLayout(hbox)

        MainWindow.setCentralWidget(self.centralwidget)



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        #Handle arguments and make all_expansions list
        in_batch_mode, existing_collection_filename = handle_opts()
        if existing_collection_filename:
            try:
                existing_collection = load_collection(existing_collection_filename)
                sys.stdout.write(f"Adding to existing collection:\n{str(existing_collection)}\n\n")
            except FileNotFoundError as e:
                sys.stderr.write(f"File not found: {str(e)}")
                sys.exit(1)
        self.all_expansions = load_expansions("genetic-apex.json", "mythical-island.json")


        self.uiWindow = UIWindow()
        self.uiCollectionSelection = UICollectionSelectionTab()
        self.uiExpansionsTab = UIExpansionsTab()
        self.uiPackSelectionTab = UIPackSelectionTab()
        self.uiSettingsTab = UISettingsTab()
        self.startUIWindow()


    def startUICollectionSelectionTab(self):

        self.uiCollectionSelection.setupUI(self)
        self.uiCollectionSelection.BackBTN.clicked.connect(self.startUIWindow)
        self.show()

    def startUIExpansionsTab(self):

        
        self.uiExpansionsTab.setupUI(self, self.all_expansions)
        self.uiExpansionsTab.BackBTN.clicked.connect(self.startUIWindow)
        self.uiExpansionsTab.PacksBTN.clicked.connect(self.startUIPackSelectionTab)
        self.show()

    def startUIPackSelectionTab(self):

        #Picking an expansion button on the expansion tab sets one of the expansions to be the selected_exp attribute
        #which is called here at the creation of the pack selection tab creation to get a pack_list
        selected_exp = self.uiExpansionsTab.selected_exp
        pack_list = selected_exp.packs

        if pack_list is None:
            #!!HIGH PROIRITY TO IMPLEMENT
            print("They didn't select an expansion in the list. Tell them off about it in a Dialog box.")

        self.uiPackSelectionTab.setupUI(self, pack_list)

        self.uiPackSelectionTab.BackBTN.clicked.connect(self.startUIExpansionsTab)


    def startUISettingsTab(self):
        self.uiSettingsTab.setupUI(self)
        self.uiSettingsTab.BackBTN.clicked.connect(self.startUIWindow)
        self.show()

    def startUIWindow(self):
        self.uiWindow.setupUI(self)
        self.uiWindow.collection_button.clicked.connect(self.startUICollectionSelectionTab)
        self.uiWindow.settings_button.clicked.connect(self.startUISettingsTab)
        self.uiWindow.ToolsBTN.clicked.connect(self.startUIExpansionsTab)
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())