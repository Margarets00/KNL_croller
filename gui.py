import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget, QPushButton,QGridLayout, QLabel, QLineEdit, QTextEdit

class MyApp(QMainWindow):
    def __init__(self):# 생성자?
        super().__init__()
        self.setupUI()

    def setupUI(self): 
        wid = QWidget(self)
        self.setCentralWidget(wid)
        grid = QGridLayout()
        wid.setLayout(grid)

        startButton= QPushButton("시작")
        year = QLineEdit()
        month = QLineEdit()
        grid.addWidget(startButton,0,2,-1,2)
        grid.addWidget(QLabel('년도 :'), 0, 0)
        grid.addWidget(QLabel('월 :'), 1, 0)
        grid.addWidget(year, 0, 1)
        grid.addWidget(month, 1, 1)
        self.setWindowTitle('국립 중앙 도서관 제어번호 수집 프로그램')
        self.statusBar().showMessage('준비..')
        startButton.clicked.connect(self.button_click())
        self.setGeometry(300, 300, 300, 200)
       
    def button_click(self):
        a = year.text()
        b = month.text()
        print (a)

if __name__ == '__main__':#__main__ -> 파일 이름 / 파일이 실행될 경우 객체 생성
   app = QApplication(sys.argv)
   window = MyApp()
   window.show()
   sys.exit(app.exec_())