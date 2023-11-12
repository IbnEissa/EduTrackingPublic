import sys
from datetime import date

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QEvent
from PyQt5.uic import loadUi
from datetime import datetime
import datetime
from PyQt5.QtCore import QDate

from models.Users import Users


class UserLoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load the dialog form created with Qt Designer
        loadUi("GUI/UIFiles/loginDialog.ui", self)
        # self.ui.Users.update_state_to_false()

    def use_ui_elements(self):
        self.btnLoginUser.clicked.connect(self.login)

    def login(self):
        print("the login is pressed ")
        username = self.txtUserNameLogin.text()
        password = self.txtPasswordUserLogin.text()

        try:
            Users.get(Users.userName == username, Users.userPassword == password)

            print("successful")
            # Update the state field to 'True'
            Users.update(state='True').where(Users.userName == username).execute()
            # self.accept()
            self.close()
            return True
            # Main.method_2(self)
        except Users.DoesNotExist:
            # Login failed
            QMessageBox.warning(self, "حاول مرة أخرى", "خطأ في اسم المستخدم أو كلمة مرور!")

    # def get_name_with_false_state(self):
    #     Users.update(state='False').where(Users.userName == username).execute()
    def eventFilter(self, obj, event):
        if obj == self.txtUserNameLogin and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtPasswordUserLogin.setFocus()
            return True
        elif obj == self.txtPasswordUserLogin and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnLoginUser.setFocus()
            return True
        return super().eventFilter(obj, event)