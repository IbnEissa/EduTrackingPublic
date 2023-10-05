import peewee
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi
from zk import ZK

from GUI.Dialogs.InitializingTheProject.DeviceInintDialog import DeviceInitDialog
from GUI.Dialogs.InitializingTheProject.classesDialog import ClassesDialog
from GUI.Views.CommonFunctionality import Common
from models.City import Cities
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
        # self.comboCity.currentIndexChanged.connect(self.get_directories)
        self.comboCity.currentIndexChanged.connect(self.on_city_select)

    # def retrieve_attendance_data(self):
    #     zk = ZK('192.168.1.201', port=4370, timeout=5)
    #     conn = zk.connect()
    #     if conn:
    #         attendance_data = conn.get_attendance()
    #         conn.disconnect()
    #         for a in attendance_data:
    #             print("the attendance is : " , a)
    #     else:
    #         print('Failed to connect to the device')
    #         return []

    # def get_directories(self, index):
    #     self.combDirectorates.clear()
    #     if index is not None:
    #         column_names = 'name'
    #         where_clause = Directories.city_id == index + 1
    #         directories = Common.get_combo_box_data(self, Directories, column_names, where_clause)
    #         self.combDirectorates.clear()
    #         self.combDirectorates.addItems(directories)

    def get_cities_combo_data(self):
        cities = Common.get_cities(self)
        self.comboCity.clear()
        self.comboCity.addItems(cities)

    def on_city_select(self, index):
        selected_city = self.comboCity.currentText()
        cities = Common.get_cities(self)
        directorates = cities[selected_city]
        self.combDirectorates.clear()
        self.combDirectorates.addItems(directorates)

    def add_school_data(self):
        # self.retrieve_attendance_data()
        name = self.txtSchoolName.toPlainText()
        city = self.comboCity.currentText()
        directorate = self.combDirectorates.currentText()
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
