import sys
from datetime import date

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from datetime import datetime
import datetime
from PyQt5.QtCore import QDate


class TeacherDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load the dialog form created with Qt Designer
        loadUi("teacherDialog.ui", self)
        self.btnSaveTeacher.clicked.connect(self.save_data)
        self.btnCancelAddingTeacher.clicked.connect(self.reject)

    def save_data(self):
        try:
            FName = self.txtTeacherFName.toPlainText()
            SName = self.txtTeacherSecName.toPlainText()
            TName = self.txtTeacherThirName.toPlainText()
            LName = self.txtTeacherLName.toPlainText()
            Phone = self.txtTeacherPhone.toPlainText()
            DOB = self.dateTeacherDOB.date().toPyDate()
            Major = self.txtTeacherMajor.toPlainText()
            Task = self.txtTeacherTask.toPlainText()
            state = 'مفعل'
            if FName.strip() == "":
                raise ValueError("يجب ادخال الاسم الاول ")
            if SName.strip() == "":
                raise ValueError("يجب ادخال الاسم الثاني ")
            if TName.strip() == "":
                raise ValueError("يجب ادخال الاسم الثالث ")
            if LName.strip() == "":
                raise ValueError("يجب ادخال اللقب ")
            if Phone.strip() == "":
                raise ValueError("يجب ادخال رقم الهاتف ")
            if Major.strip() == "":
                raise ValueError("يجب ادخال التخصص ")
            if Task.strip() == "":
                raise ValueError("يجب ادخال المهمة ")
            self.accept()

            # Return the values as a tuple
            return FName, SName, TName, LName, Phone, DOB, Major, Task, state

        except Exception as e:
            # Display error message in a message box
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None, None, None, None, None, None, None, None
