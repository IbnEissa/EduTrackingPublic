import sys
from datetime import date
import re
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi
from datetime import datetime
import datetime
from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt, QEvent
from models.Members import Members
from PyQt5.QtCore import Qt, QEvent


class CouncilFathersDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load the dialog form created with Qt Designer
        loadUi("CouncilFathersDialog.ui", self)
        self.btnSaveCouncil.clicked.connect(self.save_data)
        self.btnCancelAddingCouncil.clicked.connect(self.reject)
        self.txtCouncilFathersName.installEventFilter(self)
        self.txtCouncilSecName.installEventFilter(self)
        self.txtCouncilThirName.installEventFilter(self)
        self.txtCouncilLName.installEventFilter(self)
        self.txtCouncilPhone.installEventFilter(self)
        self.dateCouncilDOB.installEventFilter(self)
        self.txtCouncilTask.installEventFilter(self)
        self.setTabOrder(self.btnSaveCouncil, self.btnCancelAddingCouncil)

    def eventFilter(self, obj, event):
        if obj == self.txtCouncilFathersName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtCouncilSecName.setFocus()
            return True
        elif obj == self.txtCouncilSecName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtCouncilThirName.setFocus()
            return True
        elif obj == self.txtCouncilThirName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtCouncilLName.setFocus()
            return True
        elif obj == self.txtCouncilLName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtCouncilPhone.setFocus()
            return True
        elif obj == self.txtCouncilPhone and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.dateCouncilDOB.setFocus()
            return True
        elif obj == self.dateCouncilDOB and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtCouncilTask.setFocus()
            return True
        elif obj == self.txtCouncilTask and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnSaveCouncil.setFocus()
            return True
        return super().eventFilter(obj, event)

    def save_data(self):
        try:
            CouncilFathersName = self.txtCouncilFathersName.toPlainText()
            CouncilSecName = self.txtCouncilSecName.toPlainText()
            CouncilThirName = self.txtCouncilThirName.toPlainText()
            CouncilLName = self.txtCouncilLName.toPlainText()
            CouncilPhone = self.txtCouncilPhone.toPlainText()
            CouncilDOB = self.dateCouncilDOB.date().toPyDate()
            CouncilTask = self.txtCouncilTask.toPlainText()

            if CouncilFathersName.strip() == "":
                raise ValueError("يجب ادخال الاسم  ")
            if CouncilSecName.strip() == "":
                raise ValueError("يجب ادخال الاسم الثاني ")
            if CouncilThirName.strip() == "":
                raise ValueError("يجب ادخال الاسم الثالث ")
            if CouncilLName.strip() == "":
                raise ValueError("يجب ادخال اللقب ")
            if CouncilDOB > datetime.date.today():
                raise ValueError("تحذير", "يرجى إدخال تاريخ ميلاد صحيح للطالب")
            if CouncilPhone.strip() == "":
                raise ValueError("تحذير", "يرجى إدخال رقم هاتف ولي الأمر")
            if not re.match(r'^\d{9}$', CouncilPhone):
                raise ValueError("تحذير", "يرجى إدخال رقم ولي الأمر هاتف صحيح مؤلف من تسعة أرقام ")
            if CouncilTask.strip() == "":
                raise ValueError("يجب ادخال المهمة ")
            existing_member = Members.select().where(
                (Members.fName == CouncilFathersName) &
                (Members.sName == CouncilSecName) &
                (Members.tName == CouncilThirName) &
                (Members.lName == CouncilLName)
            ).first()
            if existing_member:
                raise ValueError("العضو موجوداً بالفعل ")
            else:
                self.accept()
                return CouncilFathersName, CouncilSecName, CouncilThirName, CouncilLName, CouncilPhone, CouncilDOB, CouncilTask
        except Exception as e:
            # Display error message in a message box
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None, None, None, None
