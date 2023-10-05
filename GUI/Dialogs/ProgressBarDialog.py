from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem
from zk import ZK


class Attendance(object):
    def __init__(self, user_id, timestamp, status, punch=0):
        self.user_id = user_id
        self.timestamp = timestamp
        self.status = status
        self.punch = punch


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
        self.search_thread = None  # Initialize search thread as None

    def use_ui_elements(self):
        self.ui.tblAttendence.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblAttendence.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblAttendence.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tblAttendence.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblAttendence.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblAttendence.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.ui.btnShowAttendance.clicked.connect(self.start_attendance_retrieval)

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

    def hide_searching_widget(self):
        self.ui.layout.removeWidget(self.ui.searching_widget)
        self.ui.searching_widget.hide()  # Hide the searching widget

    def start_attendance_retrieval(self):
        if not self.search_thread or not self.search_thread.isRunning():
            self.search_thread = AttendanceSearchThread(self.display_attendance_data)
            self.search_thread.start()

    def display_attendance_data(self, attendance_data):
        # Clear the table before populating new data
        self.ui.tblAttendence.clearContents()
        self.ui.tblAttendence.setRowCount(0)

        if attendance_data:
            for index, attendance in enumerate(attendance_data):
                user_id = attendance.user_id
                timestamp = attendance.timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Convert to string
                status = attendance.status
                punch = str(attendance.punch)  # Convert to string
                user_name = self.get_user_name(user_id)  # Retrieve user name from device
                current_row = self.ui.tblAttendence.rowCount()
                self.ui.tblAttendence.insertRow(current_row)
                self.ui.tblAttendence.setItem(current_row, 0, QTableWidgetItem(str(user_id)))
                self.ui.tblAttendence.setItem(current_row, 1, QTableWidgetItem(user_name))  # Set user name
                self.ui.tblAttendence.setItem(current_row, 2, QTableWidgetItem(timestamp))
                self.ui.tblAttendence.setItem(current_row, 3, QTableWidgetItem(status))
                self.ui.tblAttendence.setItem(current_row, 4, QTableWidgetItem(punch))
        else:
            print('No attendance data available.')


class AttendanceSearchThread(QThread):
    def __init__(self, callback, parent=None):
        super().__init__(parent)
        self.callback = callback

    def run(self):
        attendance_retriever = AttendanceRetriever('192.168.1.201')
        attendance_data = attendance_retriever.retrieve_attendance_data()
        self.callback(attendance_data)

