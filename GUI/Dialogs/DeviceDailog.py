import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Load the dialog form created with Qt Designer
        loadUi("DeviceDialog.ui", self)
        self.btnSaveDevice.clicked.connect(self.save_data)
        self.btnCancelAddingDevice.clicked.connect(self.reject)

    def save_data(self):
        try:
            ip_address = self.txtIPAddress.toPlainText()
            port_number = self.txtPortNumber.toPlainText()
            if port_number.strip() == "":
                raise ValueError("يجب ادخال عنوان Port الخاص بجهاز البصمة")
            if ip_address.strip() == "":
                raise ValueError("يجب ادخال عنوان IP الخاص بجهاز البصمة")
            self.accept()

            # Return the values as a tuple
            return ip_address, port_number

        except Exception as e:
            # Display error message in a message box
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None
