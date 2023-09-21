import sys
from datetime import date

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from datetime import datetime
import datetime
from PyQt5.QtCore import QDate


class UserDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load the dialog form created with Qt Designer
        loadUi("newUser.ui", self)
        self.btnSaveUser.clicked.connect(self.save_data)
        self.btnCancelAddingUser.clicked.connect(self.reject)

    def save_data(self):
        try:
            accountType = self.combAccountType.currentText()
            Name = self.txtName.toPlainText()
            userName = self.txtUserName.toPlainText()
            userPassword = self.txtPasswordUser.toPlainText()



            if accountType.strip() == "":
                raise ValueError("يجب ادخال الاسم الاول ")
            if Name.strip() == "":
                raise ValueError("يجب ادخال إسم الأب ")
            if userName.strip() == "":
                raise ValueError("يجب ادخال الاسم الجد ")
            if userPassword.strip() == "":
                raise ValueError("يجب ادخال إسم اللقب ")

            self.accept()
            # print(FName)
            # Return the values as a tuple
            return accountType, Name, userName, userPassword

        except Exception as e:
            # Display error message in a message box
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None, None, None, None, None


