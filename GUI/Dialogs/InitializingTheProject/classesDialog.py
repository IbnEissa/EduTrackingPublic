import peewee
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QListWidgetItem
from PyQt5.uic import loadUi

from GUI.Dialogs.InitializingTheProject.DialogsManager import DialogManager
from GUI.Dialogs.InitializingTheProject.SubjectsDialog import SubjectsDialog
from GUI.Dialogs.InitializingTheProject.TermSessionsInit import TermSessionsInit
from models.ClassRoom import ClassRoom
from models.School import School


class ClassesDialog(QDialog):
    def __init__(self):
        super().__init__()
        # self.dialog_manager = dialog_manager
        loadUi("ChaptersDataDialog.ui", self)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.lastInsertedSchoolId = 0
        # self.btnSkipClasses.clicked.connect(self.accept)

    # def accept(self):
    #     self.dialog_manager.push_dialog(SubjectsDialog(DialogManager))

    def use_ui_elements(self):
        self.btnSaveClasses.clicked.connect(self.add_classes_data)
        self.btnAddClasses.clicked.connect(self.add_to_list)
        self.btnDeleteClasses.clicked.connect(self.delete_from_list)
        self.btnSkipClasses.clicked.connect(self.skipping_classes)

    def skipping_classes(self):
        # subjects = SubjectsDialog()
        # subjects.use_ui_elements()
        # self.reject()
        # subjects.exec_()
        term = TermSessionsInit()
        term.use_ui_elements()
        self.reject()
        term.exec_()

    def add_to_list(self):
        name = self.txtClassName.toPlainText()
        self.listClasses.addItem(name)

    def delete_from_list(self):
        self.listClasses.takeItem(self.listClasses.currentRow())

    def add_classes_data(self):
        classes_added = False  # Flag to track if any classes were added

        for row in range(self.listClasses.count()):
            item = self.listClasses.item(row)
            name = item.text()
            self.lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
            classRoom = ClassRoom.add(self.lastInsertedSchoolId, [name])

            if classRoom:
                classes_added = True  # Set the flag to True
            else:
                QMessageBox.warning(self, "Error", "Class not added")

        if classes_added:
            self.accept()
            # subjects = SubjectsDialog()
            # subjects.use_ui_elements()
            # subjects.exec_()
            term = TermSessionsInit()
            term.use_ui_elements()
            term.exec_()
