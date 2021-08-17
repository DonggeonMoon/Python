import sys
import os
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
            self.setWindowTitle("하위 폴더 속 파일 모으기")
            self.setGeometry(300, 300, 470, 110)

            self.label1 = QLabel("파일 경로: ", self)
            self.label1.move(20, 20)

            self.lineEdit1 = QLineEdit("", self)
            self.lineEdit1.move(90, 25)
            self.lineEdit1.resize(250, 20)

            self.label2 = QLabel("복사할 위치: ", self)
            self.label2.move(20, 50)

            self.lineEdit2 = QLineEdit("", self)
            self.lineEdit2.move(90, 50)
            self.lineEdit2.resize(250, 20)

            self.button1 = QPushButton("검색", self)
            self.button1.move(350, 23)
            self.button1.resize(100, 25)

            self.button2 = QPushButton("검색", self)
            self.button2.move(350, 48)
            self.button2.resize(100, 25)

            self.button3 = QPushButton("실행", self)
            self.button3.move(350, 73)
            self.button3.resize(100, 25)

            self.button1.clicked.connect(self.search_path)
            self.button2.clicked.connect(self.search_path2)
            self.button3.clicked.connect(self.execute)

    def search_path(self):
            dirname = QFileDialog.getExistingDirectory(self, 'Open File', '\\')
            self.lineEdit1.setText(dirname)

    def search_path2(self):
            dirname2 = QFileDialog.getExistingDirectory(self, 'Open File', '\\')
            self.lineEdit2.setText(dirname2)
            
    def execute(self):
            directory = self.lineEdit1.text()
            copy_directory = self.lineEdit2.text()

            for (dirpath, dirnames, filenames) in os.walk(directory):
                    for filename in filenames:
                            address = dirpath.strip(' ') + '\\' + filename
                            print(address)
                            shutil.copy(address, copy_directory)
                            # 파일 이름이 같은 경우 가장 마지막으로 복사한 것만.
            reply = QMessageBox.question(self, '완료', '복사를 완료하였습니다.',
                                      QMessageBox.Ok | QMessageBox.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
