from datetime import datetime

import peewee
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QMessageBox
from zk import ZK

from GUI.Views.CommonFunctionality import Common
from models.Attendance import AttendanceModel
from models.Device import Device


class Attendance(object):
    def __init__(self, user_id, timestamp, status, punch):
        self.user_id = user_id
        self.timestamp = timestamp
        self.status = status
        self.punch = punch
        self.last_inserted_device = 0


class AttendanceRetriever(object):
    def __init__(self, device_ip, device_port=4370):
        self.device_ip = device_ip
        self.device_port = device_port

    def retrieve_attendance_data(self):
        zk = ZK(self.device_ip, port=self.device_port)
        conn = zk.connect()
        if conn:
            attendance_data = conn.get_attendance()
            conn.disconnect()
            return attendance_data
        else:
            print('Failed to connect to the device')
            return []


class AttendanceUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.search_thread = None
        self.attendance_time = ''
        self.previous_stylesheet = self.ui.comboAddendenceTime.styleSheet()
        self.ui.checkFilterWithDays.clicked.connect(self.on_checkbox_state_changed)
        self.ui.comboAddendenceTime.stateChanged.connect()

    def use_ui_elements(self):
        self.ui.tblLoadAttendence.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblLoadAttendence.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblLoadAttendence.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tblLoadAttendence.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblLoadAttendence.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblLoadAttendence.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnLoadAttendence.clicked.connect(self.filter_methods)
        self.ui.btnSaveAttendenceData.clicked.connect(self.add_attendance_to_database)
        Common.style_table_widget(self.ui, self.ui.tblLoadAttendence)

    def get_user_name(self, user_id):
        zk = ZK('192.168.1.201', port=4370, timeout=5)
        conn = zk.connect()
        if conn:
            conn.enable_device()
            users = conn.get_users()
            for user in users:
                if user.user_id == user_id:
                    return user.name

        return 'Unknown'

    def show_searching_widget(self):
        self.ui.layout.addWidget(self.ui.searching_widget)  # Show the searching widget

    def on_checkbox_state_changed(self, state):
        print("state of the checkbox is ", state)
        if state:
            self.execute_method_when_checked()
        else:
            self.execute_method_when_unchecked()
        # print("state of the checkbox is ", state)
        # if state == 2:
        #     self.ui.comboAddendenceTime.setEnabled(True)
        # elif state == 0:
        #     self.ui.comboAddendenceTime.setEnabled(False)

    def execute_method_when_checked(self):
        self.ui.comboAddendenceTime.setEnabled(True)
        self.ui.comboAddendenceTime.setStyleSheet(self.previous_stylesheet)

    def execute_method_when_unchecked(self):
        self.ui.comboAddendenceTime.setEnabled(False)
        self.ui.comboAddendenceTime.setStyleSheet("QComboBox { background-color: #333333; color: #ffffff; }")

    def hide_searching_widget(self):
        self.ui.layout.removeWidget(self.ui.searching_widget)
        self.ui.searching_widget.hide()  # Hide the searching widget

    # def control_filter_check_boxes(self):
    #     if self.ui.checkFilterWithDays.isChecked():
    #         self.ui.btnLoadAttendence.setEnabled(True)
    #     else:
    #         self.ui.btnLoadAttendence.setEnabled(False)
    #     if self.ui.checkFilterWithTime.isChecked():
    #         self.ui.btnLoadAttendence.setEnabled(True)
    #     else:
    #         self.ui.btnLoadAttendence.setEnabled(False)
    def add_attendance_to_database(self):
        self.last_inserted_device = Device.select(peewee.fn.Max(Device.id)).scalar()
        try:
            if self.last_inserted_device != 0:
                for row in range(self.ui.tblLoadAttendence.rowCount()):
                    uid = self.ui.tblLoadAttendence.item(row, 0).text()
                    timestamp = self.ui.tblLoadAttendence.item(row, 2).text()
                    status = self.ui.tblLoadAttendence.item(row, 3).text()
                    punch = self.ui.tblLoadAttendence.item(row, 4).text()
                    print("the type of the users: ", type(uid))
                    AttendanceModel.insert({
                        AttendanceModel.teacher_id: str(uid),
                        AttendanceModel.device_number: self.last_inserted_device,
                        AttendanceModel.out_time: timestamp,
                        AttendanceModel.input_time: timestamp,
                        AttendanceModel.status: status,
                        AttendanceModel.punch: punch,
                    }).execute()
                QMessageBox.information(self.ui, 'نجاح', 'تمت إضافة البيانات')
            else:
                QMessageBox.warning(self.ui, 'تحذير', 'قم بإضافة جهاز بصمة')
        except Exception as e:
            error_message = "حدث خطأ\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)

    def start_attendance_retrieval(self):
        if not self.search_thread or not self.search_thread.isRunning():
            self.search_thread = AttendanceSearchThread(self.display_attendance_data)
            self.search_thread.start()

    def display_attendance_data(self, attendance_data):
        self.ui.tblLoadAttendence.clearContents()
        self.ui.tblLoadAttendence.setRowCount(0)
        if attendance_data:
            for index, attendance in enumerate(attendance_data):
                user_id = attendance.user_id
                status = attendance.status
                punch = str(attendance.punch)
                user_name = self.get_user_name(user_id)
                timestamp = attendance.timestamp.strftime('%Y-%m-%d')
                current_row = self.ui.tblLoadAttendence.rowCount()
                self.ui.tblLoadAttendence.insertRow(current_row)
                self.ui.tblLoadAttendence.setItem(current_row, 0, QTableWidgetItem(str(user_id)))
                self.ui.tblLoadAttendence.setItem(current_row, 1, QTableWidgetItem(user_name))
                self.ui.tblLoadAttendence.setItem(current_row, 2, QTableWidgetItem(timestamp))
                self.ui.tblLoadAttendence.setItem(current_row, 3, QTableWidgetItem(status))
                self.ui.tblLoadAttendence.setItem(current_row, 4, QTableWidgetItem(punch))

    def filter_methods(self):
        # if self.ui.checkFilterWithDays.isNotChecked():
        attendance_time = self.ui.comboAddendenceTime.currentText()
        if attendance_time == 'اليوم':
            self.display_today_attendance()
        elif attendance_time == 'الكل':
            self.start_attendance_retrieval()
        elif attendance_time == 'هذا الشهر':
            self.show_month_attendance_data()
        # elif self.ui.checkFilterWithDate.isChecked():

    def display_today_attendance(self):
        self.ui.tblLoadAttendence.clearContents()
        self.ui.tblLoadAttendence.setRowCount(0)
        attendance_time = self.ui.comboAddendenceTime.currentText()
        attendance_retriever = AttendanceRetriever('192.168.1.201')
        attendance_data = attendance_retriever.retrieve_attendance_data()

        for attendance in attendance_data:
            user_id = attendance.user_id
            status = attendance.status
            punch = str(attendance.punch)
            user_name = self.get_user_name(user_id)
            timestamp = attendance.timestamp.strftime('%Y-%m-%d')
            today = datetime.today().strftime('%Y-%m-%d')
            # today = datetime.today().strftime('%Y-%m-%d')
            if attendance_time == 'اليوم' and timestamp == today:
                time = timestamp
                current_row = self.ui.tblLoadAttendence.rowCount()
                self.ui.tblLoadAttendence.insertRow(current_row)
                self.ui.tblLoadAttendence.setItem(current_row, 0, QTableWidgetItem(str(user_id)))
                self.ui.tblLoadAttendence.setItem(current_row, 1, QTableWidgetItem(user_name))
                self.ui.tblLoadAttendence.setItem(current_row, 2, QTableWidgetItem(time))
                self.ui.tblLoadAttendence.setItem(current_row, 3, QTableWidgetItem(status))
                self.ui.tblLoadAttendence.setItem(current_row, 4, QTableWidgetItem(punch))
            # return attendance_data

    def show_month_attendance_data(self):
        self.ui.tblLoadAttendence.clearContents()
        self.ui.tblLoadAttendence.setRowCount(0)
        attendance_time = self.ui.comboAddendenceTime.currentText()
        attendance_retriever = AttendanceRetriever('192.168.1.201')
        attendance_data = attendance_retriever.retrieve_attendance_data()

        for attendance in attendance_data:
            user_id = attendance.user_id
            status = attendance.status
            punch = str(attendance.punch)
            user_name = self.get_user_name(user_id)
            timestamp = attendance.timestamp.strftime('%m')
            full_timestamp = attendance.timestamp.strftime('%Y-%m-%d')
            # today = datetime.monthname(datetime.today().month).today().strftime('%Y-%m-%d')
            today = str(datetime.today().month)
            # today = datetime.today().month
            if attendance_time == 'هذا الشهر' and timestamp == today:
                # time = timestamp
                current_row = self.ui.tblLoadAttendence.rowCount()
                self.ui.tblLoadAttendence.insertRow(current_row)
                self.ui.tblLoadAttendence.setItem(current_row, 0, QTableWidgetItem(str(user_id)))
                self.ui.tblLoadAttendence.setItem(current_row, 1, QTableWidgetItem(user_name))
                self.ui.tblLoadAttendence.setItem(current_row, 2, QTableWidgetItem(full_timestamp))
                self.ui.tblLoadAttendence.setItem(current_row, 3, QTableWidgetItem(status))
                self.ui.tblLoadAttendence.setItem(current_row, 4, QTableWidgetItem(punch))


class AttendanceSearchThread(QThread):
    def __init__(self, callback, parent=None):
        super().__init__(parent)
        self.callback = callback

    def run(self):
        attendance_retriever = AttendanceRetriever('192.168.1.201')
        attendance_data = attendance_retriever.retrieve_attendance_data()
        self.callback(attendance_data)
