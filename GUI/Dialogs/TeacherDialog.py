import sys
from datetime import date

import re
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QEvent
from PyQt5.uic import loadUi
from datetime import datetime
import datetime
from PyQt5.QtCore import QDate

from models.Members import Members


class TeacherDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load the dialog form created with Qt Designer
        loadUi("teacherDialog.ui", self)
        self.btnSaveTeacher.clicked.connect(self.save_data)
        self.btnCancelAddingTeacher.clicked.connect(self.reject)
        # تعيين ترتيب التنقل بين العناصر
        self.txtTeacherFName.installEventFilter(self)
        self.txtTeacherLName.installEventFilter(self)
        self.dateTeacherDOB.installEventFilter(self)
        self.txtTeacherPhone.installEventFilter(self)
        self.combShiftsType.installEventFilter(self)
        self.txtTeacherQualification.installEventFilter(self)
        self.dateTeacherDOQualification.installEventFilter(self)
        self.txtTeacherMajor.installEventFilter(self)
        self.ComboTeacherTask.installEventFilter(self)
        self.setTabOrder(self.btnSaveTeacher, self.btnCancelAddingTeacher)

    def eventFilter(self, obj, event):
        if obj == self.txtTeacherFName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtTeacherLName.setFocus()
            return True
        elif obj == self.txtTeacherLName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.dateTeacherDOB.setFocus()
            return True
        elif obj == self.dateTeacherDOB and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtTeacherPhone.setFocus()
            return True
        elif obj == self.txtTeacherPhone and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.combShiftsType.setFocus()
            return True
        elif obj == self.combShiftsType and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtTeacherQualification.setFocus()
            return True
        elif obj == self.txtTeacherQualification and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.dateTeacherDOQualification.setFocus()
            return True
        elif obj == self.dateTeacherDOQualification and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtTeacherMajor.setFocus()
            return True
        elif obj == self.txtTeacherMajor and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.ComboTeacherTask.setFocus()
            return True
        elif obj == self.ComboTeacherTask and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtExceperianceYears.setFocus()
            return True
        elif obj == self.txtExceperianceYears and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnSaveTeacher.setFocus()
            return True
        return super().eventFilter(obj, event)

    def save_data(self):
        print("the button is clicked ")
        try:
            FName = self.txtTeacherFName.toPlainText()
            LName = self.txtTeacherLName.toPlainText()
            DOB = self.dateTeacherDOB.date().toPyDate()
            Phone = self.txtTeacherPhone.toPlainText()
            ShiftsType = self.combShiftsType.currentText()
            Qualification = self.txtTeacherQualification.toPlainText()
            DOQualification = self.dateTeacherDOQualification.date().toPyDate()
            Major = self.txtTeacherMajor.toPlainText()
            Task = self.ComboTeacherTask.currentText()
            state = self.ComboTeacherStatus.currentText()
            ExceperianceYears = self.txtExceperianceYears.text()
            if FName.strip() == "":
                raise ValueError("يجب ادخال الاسم الاول ")
            if Qualification.strip() == "":
                raise ValueError("يجب ادخال المؤهل ")
            if ExceperianceYears.strip() == "":
                raise ValueError("يجب ادخال سنوات الخبرة ")
            if LName.strip() == "":
                raise ValueError("يجب ادخال اللقب ")
            if DOB > datetime.date.today():
                raise ValueError("تحذير", "يرجى إدخال تاريخ ميلاد صحيح للطالب")
            if Phone.strip() == "":
                raise ValueError("تحذير", "يرجى إدخال رقم هاتف ولي الأمر")
            if not re.match(r'^\d{9}$', Phone):
                raise ValueError("تحذير", "يرجى إدخال رقم ولي الأمر هاتف صحيح مؤلف من تسعة أرقام ")
            if Major.strip() == "":
                raise ValueError("يجب ادخال التخصص ")
            if Task.strip() == "":
                raise ValueError("يجب ادخال المهمة ")
                # existing_member = Members.select().where(
                #     (Members.fName == FName) &
                #     (Members.sName == SName) &
                #     (Members.tName == TName) &
                #     (Members.lName == LName)
                # ).first()
                # if existing_member:
                #     raise ValueError("المعلم موجوداً بالفعل ")
                # else:
            self.accept()
            return FName, LName, DOB, Phone, Qualification, DOQualification, ShiftsType, Major, Task, ExceperianceYears, state
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None, None, None, None, None, None, None, None
