import sys
from PyQt5.QtWidgets import QApplication, QDialog
from GUI.Dialogs.InitializingTheProject.SchoolDialog import SchoolDialog
from GUI.Dialogs.InitializingTheProject.TermSessionsInit import TermSessionsInit
from GUI.Dialogs.ProgressBarDialog import AttendanceUI
from GUI.Views.CommonFunctionality import Common
from GUI.Views.CouncilFathersUI import CouncilFathersUI
from GUI.Views.DeviceUI import DeviceUI
from GUI.Views.StudentsUI import StudentsUI
from GUI.Views.TeachersUI import TeachersUI
from GUI.Views.UsersUI import UsersUI
from GUI.Views.uihandler import UIHandler
from GUI.Views.PersonBasicDataUI import SubMain


class Main:
    def __init__(self, state):
        self.state = state
        self.window = None

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
        main_design = 'Design/EduTrac2.ui'
        ui_handler = UIHandler(main_design)
        window = SubMain(ui_handler)
        window.ui.showMaximized()
        Device = DeviceUI(window)
        Device.use_ui_elements()
        Teacher = TeachersUI(window)
        Teacher.use_ui_elements()
        # attendance = AttendanceUI(window)
        # attendance.use_ui_elements()
        common = Common(window)
        common.use_ui_elements()
        students = StudentsUI(window)
        students.use_ui_elements()
        council_fathers = CouncilFathersUI(window)
        council_fathers.use_ui_elements()
        user = UsersUI(window)
        user.use_ui_elements()
        sys.exit(app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    state_value = 0
    main = Main(state_value)
    main.main()
    sys.exit(app.exec_())
