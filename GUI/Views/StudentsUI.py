import peewee
from PyQt5.QtCore import QDate, Qt

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout

from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonStudentsWidget
from GUI.Dialogs.StudentDialog import StudentDialog
from GUI.Views.CommonFunctionality import Common
from models.ClassRoom import ClassRoom
from models.Members import Members
from models.School import School
from models.Students import Students


class StudentsUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ips = ''
        self.ports = ''
        self.lastInsertedMemberId = 0
        self.lastInsertedStudentId = 0
        self.id = 0
        self.ui.tblStudents.setColumnHidden(0, True)

    def use_ui_elements(self):
        self.ui.tblStudents.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblStudents.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblStudents.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnAddNewStudent.clicked.connect(self.add_members_database)
        self.ui.txtStudentsSearch.textChanged.connect(self.get_member_data)

    def add_members_database(self):
        result_condition = Common.grant_permission_to_clicked_button(self.ui, permission="bt_save_student")
        if result_condition is True:
            student_dialog = StudentDialog()
            if student_dialog.exec_() == QDialog.Accepted:
                try:
                    lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
                    FName, SName, TName, LName, ClassId, Birth, Phone, ClassName = student_dialog.save_data()
                    Members.insert({
                        Members.school_id: lastInsertedSchoolId,
                        Members.fName: FName,
                        Members.sName: SName,
                        Members.tName: TName,
                        Members.lName: LName,
                        Members.phone: Phone,
                        Members.dateBerth: Birth,
                    }).execute()
                    self.lastInsertedMemberId = Members.select(peewee.fn.Max(Members.id)).scalar()
                    Students.insert({
                        Students.member_id: self.lastInsertedMemberId,
                        Students.class_id: ClassId,
                    }).execute()
                    self.lastInsertedStudentId = Students.select(peewee.fn.Max(Students.id)).scalar()
                    student = [FName, SName, TName, LName, ClassId, Birth, Phone, ClassName]
                    for s in student:
                        print(s)
                    self.add_new_student_to_table_widget(self.lastInsertedStudentId, student)
                    QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")
                except ValueError as e:
                    QMessageBox.critical(self.ui, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")
        else:
            QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")

    def add_new_student_to_table_widget(self, student_id, student):
        # self.ui.tblStudents.setColumnHidden(8, True)
        self.ui.tblStudents.setColumnHidden(0, True)
        self.ui.tblStudents.setRowCount(0)
        try:
            operationsButtons = DeleteUpdateButtonStudentsWidget(table_widget=self.ui.tblStudents)
            current_row = self.ui.tblTeachers.rowCount()  # Get the current row index
            self.ui.tblStudents.insertRow(current_row)  # Insert a new row at the current row index
            self.ui.tblStudents.setItem(current_row, 0, QTableWidgetItem(student_id))
            self.ui.tblStudents.setItem(current_row, 1, QTableWidgetItem(student[0]))
            self.ui.tblStudents.setItem(current_row, 2, QTableWidgetItem(student[1]))
            self.ui.tblStudents.setItem(current_row, 3, QTableWidgetItem(student[2]))
            self.ui.tblStudents.setItem(current_row, 4, QTableWidgetItem(student[3]))
            self.ui.tblStudents.setItem(current_row, 5, QTableWidgetItem(student[7]))
            self.ui.tblStudents.setItem(current_row, 6, QTableWidgetItem(str(student[5])))
            self.ui.tblStudents.setItem(current_row, 7, QTableWidgetItem(str(student[6])))
            self.ui.tblStudents.setCellWidget(current_row, 8, operationsButtons)
            self.ui.tblStudents.setColumnWidth(current_row, 40)
            self.ui.tblStudents.setRowHeight(current_row, 150)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)

    def get_member_data(self):
        result_condition = Common.grant_permission_to_clicked_button(self.ui, permission="bt_search_student")
        if result_condition is True:
            self.ui.tblStudents.setColumnHidden(8, False)
            try:
                columns = ['id', 'fName', 'sName', 'tName', 'lName', 'class_id', 'dateBerth', 'phone']
                search_item = self.ui.txtStudentsSearch.toPlainText().lower()
                members_query = Members.select().join(Students).join(ClassRoom, on=(Students.class_id == ClassRoom.id),
                                                                     join_type=peewee.JOIN.LEFT_OUTER).where(
                    peewee.fn.LOWER(Members.fName).contains(search_item)).distinct()

                self.ui.tblStudents.setRowCount(0)  # Clear existing rows in the table

                for row, member_data in enumerate(members_query):
                    table_items = []

                    for column_name in columns:
                        try:
                            item_value = getattr(member_data, column_name)
                        except AttributeError:
                            student_data = Students.get(Students.member_id == member_data.id)
                            item_value = getattr(student_data, column_name)
                            if column_name == 'class_id':
                                self.id = getattr(student_data, column_name)

                        table_item = QTableWidgetItem(str(item_value))
                        table_items.append(table_item)

                    self.ui.tblStudents.insertRow(row)

                    for col, item in enumerate(table_items):
                        self.ui.tblStudents.setItem(row, col, item)

                    self.ui.tblStudents.setColumnWidth(row, 40)
                    self.ui.tblStudents.setRowHeight(row, 150)

                    operations_buttons = DeleteUpdateButtonStudentsWidget(table_widget=self.ui.tblStudents)
                    self.ui.tblStudents.setCellWidget(row, 8, operations_buttons)
                    class_name = ClassRoom.get_class_name_from_id(self.ui, self.id)
                    print(class_name)
                    self.ui.tblStudents.setItem(row, 5, QTableWidgetItem(class_name))
                    Common.style_table_widget(self.ui, self.ui.tblStudents)
            except Exception as e:
                error_message = "حدث خطأ:\n\n" + str(e)
                QMessageBox.critical(self.ui, "خطأ", error_message)
        else:
            QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")
