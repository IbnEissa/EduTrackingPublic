import peewee
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonTeachersWidget
from GUI.Dialogs.TeacherDialog import TeacherDialog
from GUI.Views.CommonFunctionality import Common
# from NewMain import Main
from models.Members import Members
from models.School import School
from models.Teachers import Teachers


class TermSessionsInit(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("TermSessionsInit.ui", self)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.lastInsertedTeacherId = 0
        self.lastInsertedMemberId = 0
        self.use_ui_elements()

    def use_ui_elements(self):
        self.btnAddNewSession.clicked.connect(self.add_members_database)
        self.btnSaveTermSessions.clicked.connect(self.add_members_database)
        self.btnSkippingTermSessions.clicked.connect(self.accept)

    # def skipping_term_sessions(self):
    #     self.accept()
        # if self.exec_() == QDialog.Accepted:
        #     state_value = 1
        #     main = Main(state_value)
        #     main.method_1()

    def add_members_database(self):
        Common.style_table_widget(self, self.listTeachers)
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
                teacher = [self.lastInsertedTeacherId, FName, SName, TName, LName, state, has_finger_print_data]
                self.lastInsertedTeacherId = Teachers.select(peewee.fn.Max(Teachers.id)).scalar()
                # self.get_members_data()
                fullName = [teacher[0], teacher[1], teacher[3]]
                print(fullName)
                operations_buttons = DeleteUpdateButtonTeachersWidget(table_widget=self.listTeachers)
                result = operations_buttons.add_users_to_device(self.lastInsertedTeacherId, fullName)
                print(result)
                if result:
                    self.add_new_teacher_to_table_widget(teacher)
                    Common.style_table_widget(self, self.listTeachers)
                    QMessageBox.information(self, "نجاح", "تم الحفظ بنجاح")
                else:
                    QMessageBox.critical(self, "خطأ", "لم يتم الحفظ بنجاح")

            except ValueError as e:
                QMessageBox.critical(self, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")

    def add_new_teacher_to_table_widget(self, teacher):
        try:
            operations_buttons = DeleteUpdateButtonTeachersWidget(table_widget=self.listTeachers)
            current_row = self.listTeachers.rowCount()
            self.listTeachers.insertRow(current_row)
            self.listTeachers.setItem(current_row, 0, QTableWidgetItem(str(teacher[0])))
            self.listTeachers.setItem(current_row, 1, QTableWidgetItem(teacher[1]))
            self.listTeachers.setItem(current_row, 2, QTableWidgetItem(teacher[2]))
            self.listTeachers.setItem(current_row, 3, QTableWidgetItem(teacher[3]))
            self.listTeachers.setItem(current_row, 4, QTableWidgetItem(teacher[4]))
            self.listTeachers.setItem(current_row, 5, QTableWidgetItem(str(teacher[5])))
            self.listTeachers.setCellWidget(current_row, 6, operations_buttons.get_buttons('Old'))
            self.listTeachers.setColumnWidth(current_row, 40)
            self.listTeachers.setRowHeight(current_row, 150)
            Common.style_table_widget(self, self.listTeachers)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
