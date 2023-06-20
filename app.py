from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys

class MainWindow(QMainWindow):

# display functions
    def dark_light(self):
        if self.bg_color == "#12252c":
            self.bg_color, self.text_color = "#ffffa1", "#000000" 
        else:
            self.bg_color, self.text_color = "#12252c", "#ffffa1"
        self.text_area.setStyleSheet(f"color:{self.text_color}; font-size:14px")
        self.setStyleSheet(f'background-color:{self.bg_color}')

    def translucent_opaque(self):
        if self.opacity != 1:
            self.opacity = 1
        else:
            self.opacity = 0.5
        self.setWindowOpacity(self.opacity)


# save & open file functions
    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.critical)
        dlg.show()

    def new_f(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "")
        if not path:
            return
        self.save_to_path(path)
        self.path = path

    def open_f(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "")
        if path:
            try:
                with open(path, 'r') as f:
                    text = f.read()
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.text_area.setPlainText(text)
                self.path = path

    def save_f(self):
        if self.path is None:
            return self.save_as_f()
        else:
            self.save_to_path(self.path)

    def save_as_f(self, doc):
        text = doc.text()
        if text == ".txt":
            extension = "Text Files (*.txt)"
        elif text == ".doc":
            extension = "Word Document (*.doc)"

        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", f"{extension}")
        if not path:
            return
        self.save_to_path(path)

    def save_to_path(self, path):
        text = self.text_area.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(f"{text}\n")
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path


# clear functions
    def clear(self):
        self.clear_text()
        self.clear_p4th()

    def clear_text(self):
        self.text_area.clear()
        self.path = None

    def clear_p4th(self):
        self.path = None


# actions (calling the functions above)
    def createActions(self):
        self.dark_light_mode = QAction(QIcon("icons/dark-light.png"),'dark/light', self)
        self.dark_light_mode.triggered.connect(self.dark_light)

        self.translucent_opaque_mode = QAction(QIcon("icons/transparent.png"), 'translucent/opaque', self)
        self.translucent_opaque_mode.triggered.connect(self.translucent_opaque)

        self.new = QAction('New File', self)
        self.new.triggered.connect(self.new_f)

        self.open = QAction('Open File', self)
        self.open.triggered.connect(self.open_f)

        self.save = QAction('Save', self)
        self.save.triggered.connect(self.save_f)

        self.save_as_txt = QAction('.txt', self)
        self.save_as_txt.triggered.connect(lambda: self.save_as_f(self.save_as_txt))

        self.save_as_docx = QAction('.doc', self)
        self.save_as_docx.triggered.connect(lambda: self.save_as_f(self.save_as_docx))

        self.clear_content = QAction("Clear content", self)
        self.clear_content.triggered.connect(self.clear_text)

        self.clear_path = QAction("Clear path", self)
        self.clear_path.triggered.connect(self.clear_p4th)

        self.clear_both = QAction("Clear both", self)
        self.clear_both.triggered.connect(self.clear)
        

# init UI/widgets
    def init_UI(self):
        menubar = QMenuBar()
        menubar.setStyleSheet("color:grey")
        self.setMenuBar(menubar)

        fileMenu = QMenu("File", self)
        fileMenu.setStyleSheet('background-color:lightgrey')
        fileMenu.addAction(self.new)
        fileMenu.addAction(self.open)

        saveMenu = QMenu("Save", self)
        saveMenu.setStyleSheet('background-color:lightgrey')
        saveMenu.addAction(self.save)

        saveSubMenu = saveMenu.addMenu("Save as...")
        saveSubMenu.addAction(self.save_as_txt)
        saveSubMenu.addAction(self.save_as_docx)

        clearMenu = QMenu("Clear", self)
        clearMenu.setStyleSheet('background-color:lightgrey')
        clearMenu.addAction(self.clear_content)
        clearMenu.addAction(self.clear_path)
        clearMenu.addSeparator()
        clearMenu.addAction(self.clear_both)
        
        menubar.addMenu(fileMenu)
        menubar.addMenu(saveMenu)
        menubar.addMenu(clearMenu)
        menubar.addAction(self.dark_light_mode)
        menubar.addAction(self.translucent_opaque_mode)
        

        self.text_area = QPlainTextEdit(self)
        self.text_area.setPlaceholderText("Hello World !")
        self.text_area.setStyleSheet(f"color:{self.text_color}; font-size:14px; ")


        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(self.text_area)
        self.setCentralWidget(central_widget)


# init
    def __init__(self):
        super().__init__()

        self.opacity = 0.5
        self.bg_color = "#12252c"
        self.text_color = "#ffffa1"
        self.setWindowTitle("Translucent Text Editor")
        self.setWindowIcon(QIcon("./icons/paper.png"))
        self.setStyleSheet(f'background-color:{self.bg_color}')
        self.setWindowOpacity(self.opacity)
        self.setGeometry(160, 85, 1200, 700)

        self.createActions()
        self.init_UI()


# launch
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())