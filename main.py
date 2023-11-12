import sys
from datetime import datetime
from functools import partial

import peewee
from PyQt5.QtCore import QPoint, QTimer, QDateTime
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from zk import ZK

from GUI.Dialogs.InitializingTheProject.ListOptions import OptionUI, OptionDialog
from GUI.Dialogs.InitializingTheProject.SchoolDialog import SchoolDialog
from GUI.Dialogs.InitializingTheProject.TermSessionsInit import TermSessionsInit
from GUI.Dialogs.InitializingTheProject.showInitializeData import ShowInitialData
from GUI.Dialogs.UserLoginDialog import UserLoginDialog
from GUI.Dialogs.UserLogoutDialog import UserLogoutDialog
from GUI.Views.AttendanceUI import AttendanceUI
from GUI.Views.CommonFunctionality import Common
from GUI.Views.CouncilFathersUI import CouncilFathersUI
from GUI.Views.DeviceUI import DeviceUI
from GUI.Views.PermissionUI import PermissionUI
from GUI.Views.Student_class_scheduleUI import Student_class_scheduleUI
from GUI.Views.Student_reportUI import Student_reportUI
from GUI.Views.StudentsUI import StudentsUI
from GUI.Views.Teacher_class_scheduleUI import Teacher_class_scheduleUI
from GUI.Views.Teacher_reportUI import Teacher_reportUI
from GUI.Views.TeachersUI import TeachersUI
from GUI.Views.UsersUI import UsersUI
from GUI.Views.backupUI import Backup_UI
from GUI.Views.shiftsUI import Shift_timeUI
from GUI.Views.uihandler import UIHandler
from GUI.Views.PersonBasicDataUI import SubMain
from models.Device import Device
from models.School import School
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from models.Users import Users


class Main:
    def __init__(self, state):
        self.state = state
        # self.login_state = login_state
        # self.window = None
        self.dialog = OptionDialog()
        self.last_inserted_device = Device.select(peewee.fn.Max(Device.id)).scalar()
        device = Device.get(Device.id == self.last_inserted_device)
        self.zk = ZK(device.ip, port=device.port, timeout=5)
        self.main_design = 'EduTracMain.ui'
        self.ui_handler = UIHandler(self.main_design)
        self.window = SubMain(self.ui_handler)
        self.app = QApplication([])
        self.system_date_timer = QTimer()
        self.device_timer = QTimer()
        # self.device_timer.timeout.connect(self.find_the_device_connected)
        self.system_date_timer.timeout.connect(self.update_system_date_label)
        self.system_date_timer.start(1000)
        self.device_timer.start(10000)
        self.window.ui.btnExit.clicked.connect(self.close_application)
        self.window.ui.btnRefresh.clicked.connect(self.find_the_device_connected)
        self.window.ui.btnConnectDivice.clicked.connect(self.connect_device)

    def close_application(self):
        Users.update_all_states_to_false()
        reply = QMessageBox.question(self.window.ui, "معلومة", "هل حقاً تريد الخروج؟", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.app.quit()
        else:
            pass

    def connect_device(self):
        if self.window.ui.btnConnectDivice.text() == "الجهاز متصل":
            QMessageBox.information(self.window.ui, "معلومه", "الجهاز متصل حالياً")
        else:
            self.find_the_device_connected()

    def find_the_device_connected(self):
        # self.last_inserted_device = Device.select(peewee.fn.Max(Device.id)).scalar()
        # device = Device.get(Device.id == self.last_inserted_device)
        # zk = ZK(device.ip, port=device.port, timeout=5)
        try:
            conn = self.zk.connect()
            if conn:
                self.device_timer.stop()
                self.window.ui.btnConnectDivice.setText("الجهاز متصل")
                self.window.ui.btnConnectDivice.setStyleSheet("color: green;background-color: white;")
        except Exception as e:
            self.device_timer.start(10000)
            self.device_timer.stop()
            QMessageBox.warning(self.window.ui, 'خطأ', "لا يوجد جهاز بصمة متصل")
            self.window.ui.btnConnectDivice.setText("توصيل الجهاز")
            self.window.ui.btnConnectDivice.setStyleSheet("color: red;background-color: white;")

    def update_system_date_label(self):
        current_datetime = QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString("dd/MM/yyyy")
        formatted_time = current_datetime.toString("hh:mm:ss")
        self.window.ui.lblCurrentSystemDateAndTime.setText("التاريخ :  " + formatted_datetime + "   الساعة :   " + formatted_time)
        # self.window.ui.lblCurrentSystemDateAndTime.setStyleSheet("font-family:Shorooq_N1.ttf;")

    def close_dialog(self):
        print("the school is clicked ")
        if self.dialog.exec_() == QDialog.Accepted:
            self.dialog.reject()

    def main(self):
        if self.state == 0:
            self.method_0()
        elif self.state == 1:
            self.method_1()
        else:
            print("Invalid state value")

    def method_0(self):
        school = SchoolDialog()
        school.use_ui_elements()
        school.exec_()

        if school.result() == QDialog.Accepted:
            term_dialog = TermSessionsInit()
            term_dialog.accept()
            term_dialog.use_ui_elements()

            if term_dialog.result() == QDialog.Accepted:
                self.method_1()

    def show_options_user_details(self, btn_name):
        options = [
            ("الحساب", "icons/users.png"),
            ("تبديل المستخدم", "icons/log-out.svg"),
            ("خروج نهائي", "icons/log-out.svg"),
        ]
        self.show_options(options, btn_name)

    def show_options(self, options, btn_name):
        if btn_name == 'btnUserDetails':
            self.dialog.setOptions(options)
            self.dialog.move(50, 100)
            if self.dialog.exec_() == QDialog.Accepted:
                selected_option = self.dialog.selectedOption()
                self.show_user_details_tab(selected_option)

    def show_user_details_tab(self, selected_option):

        if selected_option == 'تبديل المستخدم':
            # self.app.quit()
            user_logout = UserLogoutDialog()
            user_logout.exec_()
        if selected_option == 'خروج نهائي':
            self.app.quit()

        if selected_option == 'الحساب':
            QMessageBox.information(self.window.ui, 'تحذير', 'لم يتم اضافة الواجهه بعد')

    def method_1(self):
        user_login = UserLoginDialog()
        user_login.use_ui_elements()
        user_login.exec_()
        result = user_login.login()
        if result is True:
            self.window.ui.comboAddendenceTime.setEnabled(False)
            self.window.ui.comboAddendenceTime.setStyleSheet("QComboBox { background-color: #333333; color: #333333; }")
            self.window.ui.checkFilterWithDate.setChecked(True)
            ShowInitialData(self.window)
            Device = DeviceUI(self.window)
            Device.use_ui_elements()
            Teacher = TeachersUI(self.window)
            Teacher.use_ui_elements()
            options = OptionUI(self.window)
            options.use_ui_elements()
            self.window.ui.btnUserDetails.clicked.connect(lambda: self.show_options_user_details('btnUserDetails'))
            attendance = AttendanceUI(self.window)
            attendance.use_ui_elements()
            shift = Shift_timeUI(self.window)
            shift.shift_ui_elements()
            common = Common(self.window)
            common.use_ui_elements()
            students = StudentsUI(self.window)
            students.use_ui_elements()
            permission = PermissionUI(self.window)
            permission.permission_ui_elements()
            council_fathers = CouncilFathersUI(self.window)
            council_fathers.use_ui_elements()
            user = UsersUI(self.window)
            user.use_ui_elements()
            student_reports = Student_reportUI(self.window)
            student_reports.use_ui_elements()
            teacher_reports = Teacher_reportUI(self.window)
            teacher_reports.use_ui_elements()
            student_class_schedule = Student_class_scheduleUI(self.window)
            student_class_schedule.use_ui_elements()
            teacher_class_schedule = Teacher_class_scheduleUI(self.window)
            teacher_class_schedule.use_ui_elements()
            backup = Backup_UI(self.window)
            backup.use_ui_elements()
            self.window.ui.showMaximized()
            sys.exit(self.app.exec_())


# class UserLogoutDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("User Logout")
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)
#
#         self.logout_label = QLabel("Are you sure you want to logout?")
#         self.logout_button = QPushButton("Logout")
#
#         self.layout.addWidget(self.logout_label)
#         self.layout.addWidget(self.logout_button)
#
#         self.logout_button.clicked.connect(self.logout)
#
#     def logout(self):
#         # Perform logout logic here
#         # You can clear user session, reset variables, or perform any necessary operations
#         self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    school_data = School.select(peewee.fn.Max(School.id)).scalar()
    login = False
    print("the log in state is ", login)
    if school_data:
        state_value = 1
    else:
        state_value = 0

    main = Main(state_value)
    main.main()
    # sys.exit(app.exec_())

    # main_app = Main()
    # main_app.start_application()
