import sys

import peewee
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton

from GUI.Dialogs.InitializingTheProject.ListOptions import OptionUI
from GUI.Dialogs.InitializingTheProject.SchoolDialog import SchoolDialog
from GUI.Dialogs.InitializingTheProject.TermSessionsInit import TermSessionsInit
from GUI.Dialogs.UserLoginDialog import UserLoginDialog
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
        self.window = None
    # def __init__(self):
    #     self.logged_in = False
    #     # self.login_state = login_state
    #     # self.window = None
    #     self.app = None

    # def start_application(self):
    #     if self.app is None:
    #         # Start the application if it's not running
    #         self.app = QApplication([])
    #         self.login()
    #         sys.exit(self.app.exec_())
    #     else:
    #         # Close the application if it's already running
    #         self.app.quit()
    #         self.app = None
    #         self.login()

    # def login(self):
    #     user_login = UserLoginDialog()
    #     user_login.use_ui_elements()
    #     user_login.exec_()
    #     result = user_login.login()
    #     if result is True:
    #         self.logged_in = True
    #         self.show_main_ui()
    #     else:
    #         print("Login canceled or failed")

    # def logout(self):
    #     user_logout = UserLogoutDialog()
    #     if user_logout.exec_() == QDialog.Accepted:
    #         self.logged_in = False
    #         print("Logout successful")
    #         self.login()
    #     else:
    #         print("Logout canceled")
    #
    # print("Logout canceled")

    # def show_main_ui(self):
    #     if self.logged_in:
    #         main_design = 'Design/EduTracMain.ui'
    #         ui_handler = UIHandler(main_design)
    #         window = SubMain(ui_handler)
    #         Device = DeviceUI(window)
    #         Device.use_ui_elements()
    #         Teacher = TeachersUI(window)
    #         Teacher.use_ui_elements()
    #         options = OptionUI(window)
    #         options.use_ui_elements()
    #         attendance = AttendanceUI(window)
    #         attendance.use_ui_elements()
    #         shift = Shift_timeUI(window)
    #         shift.shift_ui_elements()
    #         common = Common(window)
    #         common.use_ui_elements()
    #         students = StudentsUI(window)
    #         students.use_ui_elements()
    #         permission = PermissionUI(window)
    #         permission.permission_ui_elements()
    #         council_fathers = CouncilFathersUI(window)
    #         council_fathers.use_ui_elements()
    #         user = UsersUI(window)
    #         user.use_ui_elements()
    #         window.ui.showMaximized()
    #         app = QApplication([])
    #         sys.exit(app.exec_())

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

    def method_1(self):
        user_login = UserLoginDialog()
        user_login.use_ui_elements()
        user_login.exec_()
        result = user_login.login()
        if result is True:
            # QMessageBox.information(self.window, "تسجيل الدخول", "تم تسجيل الدخول بنجاح")
            # print("hello main")
            main_design = 'Design/EduTracMain.ui'
            ui_handler = UIHandler(main_design)
            window = SubMain(ui_handler)
            Device = DeviceUI(window)
            Device.use_ui_elements()
            Teacher = TeachersUI(window)
            Teacher.use_ui_elements()
            options = OptionUI(window)
            options.use_ui_elements()
            attendance = AttendanceUI(window)
            attendance.use_ui_elements()
            shift = Shift_timeUI(window)
            shift.shift_ui_elements()
            common = Common(window)
            common.use_ui_elements()
            students = StudentsUI(window)
            students.use_ui_elements()
            permission = PermissionUI(window)
            permission.permission_ui_elements()
            council_fathers = CouncilFathersUI(window)
            council_fathers.use_ui_elements()
            user = UsersUI(window)
            user.use_ui_elements()
            window.ui.showMaximized()
            app = QApplication([])
            sys.exit(app.exec_())


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
