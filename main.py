from PyQt5.QtWidgets import QApplication

from GUI.Dialogs.DeviceDailog import MyDialog
# from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonTeachersWidget
from GUI.Views.AttendanceUI import AttendanceUI
from GUI.Views.CommonFunctionality import Common
from GUI.Views.DeviceUI import  DeviceUI
from GUI.Views.StudentsUI import StudentsUI
from GUI.Views.TeachersUI import TeachersUI
from GUI.Views.uihandler import UIHandler
from GUI.Views.PersonBasicDataUI import SubMain


def main():
    app = QApplication([])
    ui_handler = UIHandler('Design/EduTrac2.ui')
    window = SubMain(ui_handler)
    # window.ui.show()
    window.ui.showMaximized()
    Device = DeviceUI(window)
    Device.use_ui_elements()
    Teacher = TeachersUI(window)
    Teacher.use_ui_elements()
    attendance = AttendanceUI(window)
    attendance.use_ui_elements()
    common = Common(window)
    common.use_ui_elements()
    students = StudentsUI(window)
    students.use_ui_elements()
    app.exec_()


if __name__ == '__main__':
    main()
