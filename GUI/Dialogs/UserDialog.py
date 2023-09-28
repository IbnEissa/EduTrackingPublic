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
            account_type = self.comboAccountType.currentText()
            name = self.txtname.toPlainText()
            user_name = self.txtUserName.toPlainText()
            password = self.txtPassword.toPlainText()

            if name.strip() == "":
                raise ValueError("يجب ادخال الاسم ")
            if user_name.strip() == "":
                raise ValueError("يجب ادخال إسم المستخدم ")
            if password.strip() == "":
                raise ValueError("يجب ادخال كلمة المرور ")
            self.accept()
            return account_type, name, user_name, password

        except Exception as e:
            # Display error message in a message box
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None
