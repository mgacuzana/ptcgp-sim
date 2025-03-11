[1mdiff --git a/__pycache__/ui_main_tabs.cpython-312.pyc b/__pycache__/ui_main_tabs.cpython-312.pyc[m
[1mindex 7ae665b..0a2f658 100644[m
Binary files a/__pycache__/ui_main_tabs.cpython-312.pyc and b/__pycache__/ui_main_tabs.cpython-312.pyc differ
[1mdiff --git a/main.py b/main.py[m
[1mindex efde246..b5c844a 100644[m
[1m--- a/main.py[m
[1m+++ b/main.py[m
[36m@@ -114,13 +114,11 @@[m [mclass MainWindow(QMainWindow):[m
 [m
     def startUIPackSelectionTab(self):[m
 [m
[31m-        #because the Pack selectin tab can only be started from the expansion selection tab, the selected expansion can always be selected at the address below[m
[31m-        selected_exp = self.centralWidget().layout().itemAt(1).itemAt(0).widget().text()[m
[31m-        [m
[31m-        pack_list = None[m
[31m-        for expansion in self.all_expansions:[m
[31m-            if expansion.__str__() == selected_exp:[m
[31m-                pack_list = expansion.packs[m
[32m+[m[32m        #Picking an expansion button on the expansion tab sets one of the expansions to be the selected_exp attribute[m
[32m+[m[32m        #which is called here at the creation of the pack selection tab creation to get a pack_list[m
[32m+[m[32m        selected_exp = self.uiExpansionsTab.selected_exp[m
[32m+[m[32m        pack_list = selected_exp.packs[m
[32m+[m
         if pack_list is None:[m
             #!!HIGH PROIRITY TO IMPLEMENT[m
             print("They didn't select an expansion in the list. Tell them off about it in a Dialog box.")[m
[1mdiff --git a/settings/settings.json b/settings/settings.json[m
[1mindex aa0796d..7803c3e 100644[m
[1m--- a/settings/settings.json[m
[1m+++ b/settings/settings.json[m
[36m@@ -1,4 +1,4 @@[m
 {[m
 	"Show packs": "Yes",[m
 	"Save to collection": "No",[m
[31m-	"Current Collection": "None"}[m
\ No newline at end of file[m
[32m+[m	[32m"Current Collection": "New Collection.json"}[m
\ No newline at end of file[m
[1mdiff --git a/ui_main_tabs.py b/ui_main_tabs.py[m
[1mindex daa6df2..c9a8141 100644[m
[1m--- a/ui_main_tabs.py[m
[1m+++ b/ui_main_tabs.py[m
[36m@@ -20,7 +20,8 @@[m [mclass UIExpansionsTab(object):[m
         self.centralwidget = QWidget(MainWindow)[m
 [m
         #Set the window size to fit all of the buttons that will be created[m
[31m-        num_buttons = len(all_expansions)[m
[32m+[m[32m        self.all_expansions = all_expansions[m
[32m+[m[32m        num_buttons = len(self.all_expansions)[m
         width = 600*num_buttons[m
         MainWindow.setGeometry(50, 50, width, 900)[m
 [m
[36m@@ -29,24 +30,23 @@[m [mclass UIExpansionsTab(object):[m
         #Generate expansion selection buttons and place them next to eachother in an HBox[m
         self.buttons_hbox = QHBoxLayout()[m
         buttons = [][m
[31m-        for i, expansion in enumerate(all_expansions):[m
[32m+[m[32m        for i, expansion in enumerate(self.all_expansions):[m
             buttons.append( QPushButton(expansion.__str__(), self.centralwidget))[m
 [m
             #Connect each button to a lambda function calling pack selection with its own expansion[m
             #I do no know why the 'ch' argument is required, but I'm guessing it relates to the self argument[m
[31m-            buttons[i].clicked.connect(lambda ch, i= expansion: self.expansionSelection(i))[m
[32m+[m[32m            buttons[i].clicked.connect(lambda ch, i = i, exp = expansion: self.expansionSelection(i, exp))[m
 [m
             self.buttons_hbox.addWidget(buttons[i])[m
             buttons[i].setFixedHeight(900)[m
 [m
         #Create a bottom row of buttons to return to the main navigation page or proceed to selection[m
[31m-        self.SelectedExp = QLineEdit("Pick an expansion")[m
[32m+[m[32m        #self.SelectedExp = QLineEdit("Pick an expansion")[m
         self.PacksBTN = QPushButton("Select")[m
         self.BackBTN = QPushButton("Back", self.centralwidget)[m
         #self.BackBTN.move(100, 350)[m
 [m
         bottom_row = QHBoxLayout()[m
[31m-        bottom_row.addWidget(self.SelectedExp)[m
         bottom_row.addWidget(self.PacksBTN)[m
         bottom_row.addWidget(self.BackBTN)[m
 [m
[36m@@ -59,9 +59,14 @@[m [mclass UIExpansionsTab(object):[m
         self.centralwidget.setLayout(main_layout)[m
         MainWindow.setCentralWidget(self.centralwidget)[m
 [m
[31m-    def expansionSelection(self, selected_exp):[m
[31m-        #this text can be accessed when setting up the uiPackSelectionTab by indexing into the centralwidget(which will be this tab)[m
[31m-        self.SelectedExp.setText(selected_exp.__str__())[m
[32m+[m[32m    def expansionSelection(self, expansion_id, selected_exp):[m
[32m+[m[32m        #this attribute is tied to the expansion tab itself which can be accessed by the mainwindow object during startUIPackSelectionTab(self):[m
[32m+[m[32m        self.selected_exp = selected_exp[m
[32m+[m
[32m+[m
[32m+[m[32m        for i in range(self.buttons_hbox.count()):[m
[32m+[m[32m            self.buttons_hbox.itemAt(i).widget().setStyleSheet("background-color:#ffffff;")[m
[32m+[m[32m        self.buttons_hbox.itemAt(expansion_id).widget().setStyleSheet("background-color:#c0c8cf;")[m
 [m
 [m
 [m
[36m@@ -187,8 +192,8 @@[m [mclass UIPackSelectionTab(object):[m
         self.selected_pack = pack_type[m
 [m
         for i in range(self.buttons_hbox.count()):[m
[31m-            self.buttons_hbox.itemAt(i).widget().setStyleSheet("background-color:#ffffff;");[m
[31m-        self.buttons_hbox.itemAt(pack_type_id).widget().setStyleSheet("background-color:#c0c8cf;");[m
[32m+[m[32m            self.buttons_hbox.itemAt(i).widget().setStyleSheet("background-color:#ffffff;")[m
[32m+[m[32m        self.buttons_hbox.itemAt(pack_type_id).widget().setStyleSheet("background-color:#c0c8cf;")[m
 [m
 [m
     def openPacks(self):[m
