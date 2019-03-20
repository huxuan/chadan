#coding=utf-8


from selenium import webdriver
from chadan import chadan_cls
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import sys
from chadanui import Ui_Dialog

class mywindow(QtWidgets.QWidget,Ui_Dialog):
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)

        self.startButton.clicked.connect(self.startChadan)
        self.stopButton.clicked.connect(self.stopChadan)
        self.Button_get_cash.clicked.connect(self.get_cash)

    def keyPressEvent(self, e):
        print('e.key() ={}'.format(e.key()))
        print('Qt.Key_Enter = {}'.format(Qt.Key_Enter))
        if (e.key() == Qt.Key_Return) | (e.key() == Qt.Key_Enter):
            # print('test')
            self.startChadan()

    def chadanLogin(self):
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()
        self.chadan_obj = chadan_cls(self.browser)
        # username = '15359190337'
        # psw = self.psw_lineEdit.text()
        self.chadan_obj.login(self, '15359190337', 'abcd190337')
        # print("helloWorld")
        self.status.setText('在线')
        self.raise_()

    def startChadan(self):
        self.chadan_obj.startdan()

    def stopChadan(self):
        self.chadan_obj.stopdan()
        self.dan_statu.setText('未启动')
        self.dan_info_phone.setText('null')
        # self.dan_info_deadtime.setText('')

    def get_cash(self):
        if self.chadan_obj.withdrawApply():
            QMessageBox.information(self, "消息", "提现成功", QMessageBox.Yes)
        else:
            QMessageBox.information(self, "消息", "提现失败", QMessageBox.Yes)

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    myshow=mywindow()
    myshow.chadanLogin()
    myshow.show()
    sys.exit(app.exec_())
    # threading.Thread(target=self.getdan_task, args=(arg), name='GetDan')
#
# if  __name__=="__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     widget = QtWidgets.QMainWindow()
#     ui= Ui_Dialog()
#     ui.setupUi(widget)
#     widget.show()
#     sys.exit(app.exec_())
