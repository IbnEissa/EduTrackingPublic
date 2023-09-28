import sys
from datetime import date

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from datetime import datetime
import datetime
from PyQt5.QtCore import QDate

from GUI.Views.CommonFunctionality import Common
from models.ClassRoom import ClassRoom


class StudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load the dialog form created with Qt Designer
        loadUi("studentDialog.ui", self)
        self.btnSaveStudent.clicked.connect(self.save_data)
        self.btnCancelAddingStudent.clicked.connect(self.reject)
        self.get_classes_combo_data()
        self.combClasses.currentIndexChanged.connect(self.comb_classes_changed)

    def comb_classes_changed(self, index):
        class_name = self.combClasses.currentText()
        class_id = ClassRoom.get_class_id_from_name(self, class_name)
        return class_id

    def get_classes_combo_data(self):
        column_names = 'name'
        classes = Common.get_combo_box_data(self, ClassRoom, column_names)
        self.combClasses.clear()
        self.combClasses.addItems(classes)

    def save_data(self):
        try:
            FName = self.txtStudentFName.toPlainText()
            SName = self.txtStudentSecName.toPlainText()
            TName = self.txtStudentThirName.toPlainText()
            LName = self.txtStudentLName.toPlainText()
            ClassId = self.comb_classes_changed(self.combClasses.currentIndex())
            ClassName = self.combClasses.currentText()
            Birth = self.dateStudentDOB.date().toPyDate()
            Phone = self.txtStudentParentPhone.toPlainText()

            if FName.strip() == "":
                raise ValueError("يجب ادخال الاسم الاول ")
            if SName.strip() == "":
                raise ValueError("يجب ادخال إسم الأب ")
            if TName.strip() == "":
                raise ValueError("يجب ادخال الاسم الجد ")
            if LName.strip() == "":
                raise ValueError("يجب ادخال إسم اللقب ")
            # if ClassName.strip() == "":
            #     raise ValueError("يجب ادخال الاسم الفصل ")

            if Phone.strip() == "":
                raise ValueError("يجب ادخال رقم الهاتف ")
            self.accept()
            # print(FName)
            # Return the values as a tuple
            return FName, SName, TName, LName, ClassId, Birth, Phone, ClassName

        except Exception as e:
            # Display error message in a message box
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None, None, None, None, None, None



