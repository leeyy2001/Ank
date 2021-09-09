import sys

import openpyxl
from PyQt5.QtSql import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

workbook = openpyxl.load_workbook(r"D:\yylee\Transfer yy\Moving files\Programming projects\Anki\translations_testing.xlsx")

sh = workbook.active

english = sh['A']
malay = sh['B']

eng_list = []
mly_list = []

for x in range(len(english)):
    proto_el = str(english[x].value)
    proto_el = proto_el.replace("\xa0", " ")
    eng_list.append(proto_el)

for y in range(len(malay)):
    proto_mly = str(malay[y].value)
    proto_mly = proto_mly.replace("\xa0", " ")
    mly_list.append(proto_mly)

translations = list(zip(eng_list, mly_list))

class counter:
   def __iter__(self):
      self.a = 0
      return self

   def __next__(self):
      x = self.a
      self.a += 1
      return x

counter = counter()
iterate = iter(counter)

class anki(QWidget):
   def __init__(self, parent=None):
      super().__init__(parent)

      self.x = next(iterate)
      
      self.setWindowTitle("Proto Anki")
      self.resize(400, 200)

      self.textEdit = QTextEdit()
      self.textEdit.setPlainText(translations[self.x][0])        
      self.translation_btn = QPushButton("Check translation?")
      self.next_btn = QPushButton("Next?")
      self.wordbank_btn = QPushButton("Edit or check the word bank.")

      #Setting the layout for the GUI by adding and ordering the buttons.
      layout = QVBoxLayout()
      layout.addWidget(self.textEdit)
      layout.addWidget(self.translation_btn)
      #added functions that will resume development once databases can be incorporated.
      layout.addWidget(self.next_btn)
      layout.addWidget(self.wordbank_btn)
      #sets the vertical layout on the current widget which is a window.
      self.setLayout(layout)

      #Connecting the buttons to a function when they are clicked by the user.
      self.translation_btn.clicked.connect(self.translation_btn_clicked)
      self.next_btn.clicked.connect(self.next_btn_clicked)
      self.wordbank_btn.clicked.connect(self.wordbank_btn_clicked)

   def translation_btn_clicked(self):
      self.textEdit.setPlainText(translations[self.x][1])

   #when the button next is pressed the value of self.x increases by 1. This change is affected throughout the code.
   #Thus when you click the change will apply.
   def next_btn_clicked(self): 
      self.x = next(iterate)
      self.textEdit.setPlainText(translations[self.x][0])

   def wordbank_btn_clicked(self):
      #Since I want to open the widget in another window, I cannot assign it a parent, so I need to store a reference to it somewhere 
      #Thus storing it in the Anki clas. Now, the other window will stay open for as long as anki class stays open
      self.wordbank_win = wordbank()
      self.wordbank_win.show()
   
class wordbank(QWidget):
   def __init__(self):
      super().__init__()

      self.title = "Wordbank"
      self.top = 100
      self.left = 100
      self.width = 500
      self.height = 400

      self.InitWindow()

   def InitWindow(self):
      self.setWindowTitle(self.title)
      self.setGeometry(self.top, self.left, self.width, self.height)
      
      self.CreateWindows()

      self.show()

   def CreateWindows(self):
      self.tableWidget = QTableWidget()
      self.tableWidget.setRowCount(len(translations) + 1)
      self.tableWidget.setColumnCount(2)
      self.tableWidget.setColumnWidth(1, 300)

      self.tableWidget.setItem(0,0, QTableWidgetItem("English"))
      self.tableWidget.setItem(0,1, QTableWidgetItem("Malay"))

      #Loops through the list of words and present them in table form.
      #i is the y-coordinates of the table. Since y-coordinate = 0 is used as a header, the y-coordinates for the values start at 1.
      #Since there are only 2 columns, the x-coordinate is between 0 and 1, thus there is no need for a loop, only 2 values 0 and 1 
      #are needed. Then since the index for translations start at 0, we need to take i-1 to get the corresponding value. So the first
      #will occupy y-coordinate 1, but the index would be from 0 onwards. Thus i-1. The other index is just for the index within the
      #list containing the pairs of english and malay words. 
      for i in range(1, len(translations) + 1):
         self.tableWidget.setItem(i, 0, QTableWidgetItem(translations[i-1][0]))
         self.tableWidget.setItem(i, 1, QTableWidgetItem(translations[i-1][1]))

      self.add_words = QPushButton("Add Words")
      self.vBoxLayout = QVBoxLayout()
      self.vBoxLayout.addWidget(self.tableWidget)
      self.setLayout(self.vBoxLayout)

if __name__ == "__main__":
   app = QApplication(sys.argv)
   win = anki()
   win.show()
   sys.exit(app.exec_())
