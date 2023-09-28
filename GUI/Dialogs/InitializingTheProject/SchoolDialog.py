import peewee
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi

from GUI.Dialogs.InitializingTheProject.DeviceInintDialog import DeviceInitDialog
from GUI.Dialogs.InitializingTheProject.classesDialog import ClassesDialog
from GUI.Views.CommonFunctionality import Common
from models.City import Cities
from models.Directorate import Directories
from models.School import School


class SchoolDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("SchoolData.ui", self)
        self.get_cities_combo_data()
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

    # this is the method that makes the design of the dialog very good

    def use_ui_elements(self):
        self.btnSaveSchool.clicked.connect(self.add_school_data)
        # self.btnSkipSchool.clicked.connect(self.skipping_dialog)
        self.comboCity.currentIndexChanged.connect(self.get_directories)

    def get_directories(self, index):
        self.combDirectorates.clear()
        if index is not None:
            column_names = 'name'
            where_clause = Directories.city_id == index + 1
            directories = Common.get_combo_box_data(self, Directories, column_names, where_clause)
            self.combDirectorates.clear()
            self.combDirectorates.addItems(directories)

    def get_cities_combo_data(self):
        column_names = 'name'
        cities = Common.get_combo_box_data(self, Cities, column_names)
        self.comboCity.clear()
        self.comboCity.addItems(cities)

    def add_school_data(self):
        name = self.txtSchoolName.toPlainText()
        city = self.comboCity.currentIndex() + 1
        directorate = 1
        village = self.txtVillage.toPlainText()
        academic_level = self.comboAcademicLevel.currentText()
        student_gender_type = self.comboGenderType.currentText()
        school = School.add(name, city, directorate, village, academic_level, student_gender_type)
        if school:
            self.accept()
            device = DeviceInitDialog()
            device.use_ui_elements()
            device.exec_()
        else:
            QMessageBox.warning(self, "Error", "School not added")

    def skipping_dialog(self):
        device = DeviceInitDialog()
        device.use_ui_elements()
        device.exec_()
        self.hide()
