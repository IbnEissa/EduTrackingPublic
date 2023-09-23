import sys
from datetime import date

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from datetime import datetime
import datetime
from PyQt5.QtCore import QDate

from models.Members import Members


class CouncilFathersDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load the dialog form created with Qt Designer
        loadUi("CouncilFathersDialog.ui", self)
        self.btnSaveCouncil.clicked.connect(self.save_data)
        self.btnCancelAddingCouncil.clicked.connect(self.reject)

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
            if CouncilPhone.strip() == "":
                raise ValueError("يجب ادخال الهاتف ")
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
