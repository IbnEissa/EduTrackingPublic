import sys
from datetime import date

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from datetime import datetime
import datetime
from PyQt5.QtCore import QDate


class Shift_timedialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load the dialog form created with Qt Designer
        loadUi("shiftDialog.ui", self)
        self.btnSaveshift.clicked.connect(self.save_data_shift)
        self.btnCancelAddingshift.clicked.connect(self.reject)

    def save_data_shift(self):
        try:
            name = self.txtshift_name.toPlainText()
            shift_Type = self.txtshift_Type.toPlainText()
            start_time = self.timeEdit.time().toPyTime()
            delay_times = self.txtdelay_time.toPlainText()
            end_time = self.timeEdit_2.time().toPyTime()

            if name == "":
                raise ValueError("يجب ادخال الاسم ")
            if shift_Type == "":
                raise ValueError("يجب ادخال نوع الوردية  ")
            if start_time == "":
                raise ValueError("يجب ادخال  وقت البدء ")
            if delay_times == "":
                raise ValueError("يجب ادخال   الوقت التاخير ")
            if end_time == "":
                raise ValueError("يجب ادخال  وقت النهاية ")
            self.accept()
            return name, shift_Type, start_time, delay_times, end_time

        except Exception as e:
            # Display error message in a message box
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None
