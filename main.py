from PyQt5.QtWidgets import QApplication

from GUI.Dialogs.DeviceDailog import MyDialog
from GUI.Dialogs.InitializingTheProject.DeviceInintDialog import DeviceInitDialog
from GUI.Dialogs.InitializingTheProject.DialogsManager import DialogManager
from GUI.Dialogs.InitializingTheProject.SchoolDialog import SchoolDialog
from GUI.Dialogs.InitializingTheProject.classesDialog import ClassesDialog
# from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonTeachersWidget
from GUI.Views.AttendanceUI import AttendanceUI
from GUI.Views.CommonFunctionality import Common
from GUI.Views.CouncilFathersUI import CouncilFathersUI
from GUI.Views.DeviceUI import DeviceUI
from GUI.Views.StudentsUI import StudentsUI
from GUI.Views.TeachersUI import TeachersUI
from GUI.Views.uihandler import UIHandler
from GUI.Views.PersonBasicDataUI import SubMain


def main():
    state = 1
    app = QApplication([])
    # initial_design = 'SchoolData.ui'
    main_design = 'Design/EduTrac2.ui'
    if state == 0:
        school = SchoolDialog()
        school.use_ui_elements()
        # dialog_manager = DialogManager()
        # dialog_manager.push_dialog(DeviceInitDialog(dialog_manager))
        # dialog_manager.show_current_dialog()
        # device = DeviceInitDialog()
        # device.use_ui_elements()
        school.show()
        app.exec_()
    else:
        ui_handler = UIHandler(main_design)
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
        council_fathers = CouncilFathersUI(window)
        council_fathers.use_ui_elements()
        app.exec_()


if __name__ == '__main__':
    main()
