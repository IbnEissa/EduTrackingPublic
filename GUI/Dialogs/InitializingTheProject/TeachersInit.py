import peewee
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi

from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonTeachersWidget
from GUI.Dialogs.TeacherDialog import TeacherDialog
from models.Device import Device
from models.Members import Members
from models.School import School
from models.Subjects import Subjects
from models.Teachers import Teachers


class TeachersInit(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("teachersInit.ui", self)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.lastInsertedTeacherId = 0
        self.lastInsertedMemberId = 0
        self.use_ui_elements()

    def use_ui_elements(self):
        self.btnAddNewTeacher.clicked.connect(self.add_teacher_data)
        self.btnDeleteTeacher.clicked.connect(self.delete_from_list)

    def delete_from_list(self):
        self.listTeachers.takeItem(self.listTeachers.currentRow())

    def add_new_teacher_to_list_view(self, teacher):
        teacher_str = ' '.join(teacher)  # Convert the list to a single string
        self.listTeachers.addItem(teacher_str)

    def add_teacher_data(self):
        teacher_dialog = TeacherDialog()
        if teacher_dialog.exec_() == QDialog.Accepted:
            try:
                lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
                FName, SName, TName, LName, Phone, DOB, Major, Task, state = teacher_dialog.save_data()
                Members.insert({
                    Members.school_id: lastInsertedSchoolId,
                    Members.fName: FName,
                    Members.sName: SName,
                    Members.tName: TName,
                    Members.lName: LName,
                    Members.phone: Phone,
                    Members.dateBerth: DOB,
                }).execute()
                self.lastInsertedMemberId = Members.select(peewee.fn.Max(Members.id)).scalar()
                Teachers.insert({
                    Teachers.members_id: self.lastInsertedMemberId,
                    Teachers.major: Major,
                    Teachers.task: Task,
                    Teachers.state: state,
                }).execute()
                has_finger_print_data = 'لا'
                teacher = [FName, SName, TName, LName, Phone, DOB, Major, Task, state, has_finger_print_data]
                self.lastInsertedTeacherId = Teachers.select(peewee.fn.Max(Teachers.id)).scalar()
                fullName = [teacher[0], teacher[1], teacher[3]]
                # result = self.add_users_to_device(self.lastInsertedTeacherId, fullName)
                # if result:
                self.add_new_teacher_to_list_view(fullName)
                QMessageBox.information(self, "نجاح", "تم الحفظ بنجاح")
                # else:
                #     QMessageBox.critical(self, "خطأ", "لم يتم الحفظ بنجاح")

            except ValueError as e:
                QMessageBox.critical(self, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")