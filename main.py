import sys
from functools import partial

import peewee
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton

from GUI.Dialogs.InitializingTheProject.ListOptions import OptionUI, OptionDialog
from GUI.Dialogs.InitializingTheProject.SchoolDialog import SchoolDialog
from GUI.Dialogs.InitializingTheProject.TermSessionsInit import TermSessionsInit
from GUI.Dialogs.UserLoginDialog import UserLoginDialog
from GUI.Dialogs.UserLogoutDialog import UserLogoutDialog
from GUI.Views.AttendanceUI import AttendanceUI
from GUI.Views.CommonFunctionality import Common
from GUI.Views.CouncilFathersUI import CouncilFathersUI
from GUI.Views.DeviceUI import DeviceUI
from GUI.Views.PermissionUI import PermissionUI
from GUI.Views.StudentsUI import StudentsUI
from GUI.Views.TeachersUI import TeachersUI
from GUI.Views.UsersUI import UsersUI
from GUI.Views.shiftsUI import Shift_timeUI
from GUI.Views.uihandler import UIHandler
from GUI.Views.PersonBasicDataUI import SubMain
from models.School import School
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox


class Main:
    def __init__(self, state, login_state):
        self.state = state
        self.login_state = login_state
        # self.window = None
        self.dialog = OptionDialog()

        self.main_design = 'Design/EduTracMain.ui'
        self.ui_handler = UIHandler(self.main_design)
        self.window = SubMain(self.ui_handler)
        self.app = QApplication([])
        self.window.ui.btnSchoolName.clicked.connect(self.close_dialog)

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
            button_rect = self.window.ui.btnUserDetails.rect()
            # button_bottom_left = self.window.ui.btnUserDetails.mapToGlobal(button_rect.bottomLeft())
            # dialog_width = self.dialog.width()
            # dialog_height = self.dialog.height()
            # self.dialog.move(button_bottom_left + QPoint(dialog_width, dialog_height))
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

    main = Main(state_value, login)
    main.main()
    # sys.exit(app.exec_())

    # main_app = Main()
    # main_app.start_application()
