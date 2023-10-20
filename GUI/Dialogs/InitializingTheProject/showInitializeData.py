from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonSchoolWidget, DeleteUpdateButtonDeviceWidget, \
    DeleteUpdateButtonInitDeviceWidget, DeleteUpdateButtonInitClassRoomWidget
from models.School import School
from models.ClassRoom import ClassRoom
from models.Device import Device
from GUI.Views.CommonFunctionality import Common
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout
from GUI.Views.CommonFunctionality import Common


class ShowInitialData:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ui.tblSchoolData.setColumnHidden(0, True)
        self.ui.tblDiveceData.setColumnHidden(0, True)
        self.ui.tblClassRoomData.setColumnHidden(0, True)
        self.get_school_data()
        self.get_device_data()
        self.get_classroom_data()
        # self.get_subjects_data()

    def get_school_data(self):
        columns = ['id', 'school_name', 'city', 'directorate', 'village', 'academic_level', 'student_gender_type',
                   'created_at', 'updated_at']

        school_query = School.select()

        self.ui.tblSchoolData.setRowCount(0)  # Clear existing rows in the table
        for row, school_data in enumerate(school_query):
            table_items = []
            for column_name in columns:
                item_value = getattr(school_data, column_name)
                table_item = QTableWidgetItem(str(item_value))
                table_items.append(table_item)

            self.ui.tblSchoolData.insertRow(row)
            for col, item in enumerate(table_items):
                self.ui.tblSchoolData.setItem(row, col, item)

            self.ui.tblSchoolData.setColumnWidth(row, 40)
            self.ui.tblSchoolData.setRowHeight(row, 150)
            operations_buttons = DeleteUpdateButtonSchoolWidget(table_widget=self.ui.tblSchoolData)
            self.ui.tblSchoolData.setCellWidget(row, 9, operations_buttons)
            Common.style_table_widget(self.ui, self.ui.tblSchoolData)

    def get_device_data(self):
        columns = ['id', 'name', 'ip', 'port', 'status']

        device_query = Device.select()

        self.ui.tblDiveceData.setRowCount(0)  # Clear existing rows in the table
        for row, device_data in enumerate(device_query):
            table_items = []
            for column_name in columns:
                item_value = getattr(device_data, column_name)
                table_item = QTableWidgetItem(str(item_value))
                table_items.append(table_item)

            self.ui.tblDiveceData.insertRow(row)
            for col, item in enumerate(table_items):
                self.ui.tblDiveceData.setItem(row, col, item)

            self.ui.tblDiveceData.setColumnWidth(row, 40)
            self.ui.tblDiveceData.setRowHeight(row, 150)
            operations_buttons = DeleteUpdateButtonInitDeviceWidget(table_widget=self.ui.tblDiveceData)
            self.ui.tblDiveceData.setCellWidget(row, 5, operations_buttons)
            Common.style_table_widget(self.ui, self.ui.tblDiveceData)

    def get_classroom_data(self):
        columns = ['id', 'name']

        classroom_query = ClassRoom.select()

        self.ui.tblClassRoomData.setRowCount(0)  # Clear existing rows in the table
        for row, classroom_data in enumerate(classroom_query):
            table_items = []
            for column_name in columns:
                item_value = getattr(classroom_data, column_name)
                table_item = QTableWidgetItem(str(item_value))
                table_items.append(table_item)

            self.ui.tblClassRoomData.insertRow(row)
            for col, item in enumerate(table_items):
                self.ui.tblClassRoomData.setItem(row, col, item)

            self.ui.tblClassRoomData.setColumnWidth(row, 40)
            self.ui.tblClassRoomData.setRowHeight(row, 150)
            operations_buttons = DeleteUpdateButtonInitClassRoomWidget(table_widget=self.ui.tblClassRoomData)
            self.ui.tblClassRoomData.setCellWidget(row, 2, operations_buttons)
            Common.style_table_widget(self.ui, self.ui.tblClassRoomData)

    # def get_subjects_data(self):
    #     subjects = Common.get_subjects(self.ui)
    #     self.ui.tblsubjectData.setRowCount(len(subjects))
    #     # self.ui.tblsubjectData.setColumnCount(1)
    #     for row, subject in enumerate(subjects):
    #         item = QTableWidgetItem(subject)
    #         self.ui.tblsubjectData.setItem(row, 0, item)
    #         operations_buttons = DeleteUpdateButtonInitSubjectWidget(table_widget=self.ui.tblsubjectData)
    #         self.ui.tblsubjectData.setCellWidget(row, 1, operations_buttons)
    #         Common.style_table_widget(self.ui, self.ui.tblsubjectData)
