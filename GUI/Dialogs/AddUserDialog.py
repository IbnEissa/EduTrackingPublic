import sys
from datetime import date

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from datetime import datetime
import datetime
from PyQt5.QtCore import QDate


class AddUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load the dialog form created with Qt Designer
        loadUi("AddUserDialog.ui", self)
        self.btnAddUser.clicked.connect(self.save_data)

    def save_data(self):
        try:
            typeAccount = self.cobAccountType.toPlainText()
            userName = self.txtUserName.toPlainText()
            passWord = self.txtPassWord.toPlainText()

            if typeAccount.strip() == "":
                raise ValueError("يجب ادخال الاسم الاول ")
            if userName.strip() == "":
                raise ValueError("يجب ادخال رقم الهاتف ")
            if passWord.strip() == "":
                raise ValueError("يجب ادخال رقم الهاتف ")




        except Exception as e:
            # Display error message in a message box
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None, None, None, None, None
