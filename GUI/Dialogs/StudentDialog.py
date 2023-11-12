import sys
from datetime import date
import re
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QEvent
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
        loadUi("GUI/UIFiles/studentDialog.ui", self)
        self.btnSaveStudent.clicked.connect(self.save_data)
        self.btnCancelAddingStudent.clicked.connect(self.reject)
        self.get_classes_combo_data()
        self.combClasses.currentIndexChanged.connect(self.comb_classes_changed)
        # تعيين ترتيب التنقل بين العناصر
        self.txtStudentFName.installEventFilter(self)
        self.txtStudentSecName.installEventFilter(self)
        self.txtStudentThirName.installEventFilter(self)
        self.txtStudentLName.installEventFilter(self)
        self.combClasses.installEventFilter(self)
        self.dateStudentDOB.installEventFilter(self)
        self.txtStudentParentPhone.installEventFilter(self)
        self.setTabOrder(self.btnSaveStudent, self.btnCancelAddingStudent)

    def comb_classes_changed(self, index):
        class_name = self.combClasses.currentText()
        class_id = ClassRoom.get_class_id_from_name(self, class_name)
        return class_id

    def get_classes_combo_data(self):
        column_names = 'name'
        classes = Common.get_combo_box_data(self, ClassRoom, column_names)
        self.combClasses.clear()
        self.combClasses.addItems(classes)

    def eventFilter(self, obj, event):
        if obj == self.txtStudentFName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtStudentSecName.setFocus()
            return True
        elif obj == self.txtStudentSecName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtStudentThirName.setFocus()
            return True
        elif obj == self.txtStudentThirName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtStudentLName.setFocus()
            return True
        elif obj == self.txtStudentLName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.dateStudentDOB.setFocus()
            return True
        elif obj == self.dateStudentDOB and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtStudentParentPhone.setFocus()
            return True
        elif obj == self.txtStudentParentPhone and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.combClasses.setFocus()
            return True
        elif obj == self.combClasses and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnSaveStudent.setFocus()
            return True
        # elif obj == self.btnSaveStudent and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
        #     self.btnSaveStudent.setFocus()
        #     return True
        return super().eventFilter(obj, event)

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
            if ClassId is None:
                raise ValueError("تحذير", "يرجى اختيار صف الطالب")
            if ClassName.strip() == "":
                raise ValueError("تحذير", "يرجى اختيار صف الطالب")
            if Birth > datetime.date.today():
                raise ValueError("تحذير", "يرجى إدخال تاريخ ميلاد صحيح للطالب")
            if Phone.strip() == "":
                raise ValueError("تحذير", "يرجى إدخال رقم هاتف ولي الأمر")
            if not re.match(r'^\d{9}$', Phone):
                raise ValueError("تحذير", "يرجى إدخال رقم ولي الأمر هاتف صحيح مؤلف من تسعة أرقام ")
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
