from datetime import datetime
import datetime
import logging
import peewee
from PyQt5.QtCore import QDate, Qt

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout
from zk import ZK

from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonTeachersWidget
from GUI.Dialogs.TeacherDialog import TeacherDialog
from GUI.Views.DeviceUI import DeviceUI
from models.Members import Members
from models.Teachers import Teachers


class TeachersUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ips = ''
        self.ports = ''
        self.lastInsertedMemberId = 0
        self.lastInsertedTeacherId = 0
        self.finger_button_state = True

    def use_ui_elements(self):
        self.ui.tblTeachers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblTeachers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblTeachers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnAddNewTeacher.clicked.connect(self.add_members_database)
        self.ui.txtTeachersSearch.textChanged.connect(self.get_members_data)

    def get_members_data(self):
        columns = ['id', 'fName', 'phone', 'dateBerth', 'major', 'task', 'state', 'fingerPrintData']
        search_item = self.ui.txtTeachersSearch.toPlainText().lower()

        members_query = Members.select().join(Teachers).where(
            peewee.fn.LOWER(Members.fName).contains(search_item)).distinct()

        self.ui.tblTeachers.setRowCount(0)  # Clear existing rows in the table
        for row, member_data in enumerate(members_query):
            table_items = []
            for column_name in columns:
                try:
                    item_value = getattr(member_data, column_name)

                except AttributeError:
                    teacher_data = Teachers.get(Teachers.id == member_data.id)
                    item_value = getattr(teacher_data, column_name)
                    if column_name == 'fingerPrintData':
                        item_value = getattr(teacher_data, column_name)
                        if item_value:
                            item_value = 'نعم'
                            self.finger_button_state = False
                        else:
                            item_value = 'لا'
                            self.finger_button_state = True

                table_item = QTableWidgetItem(str(item_value))
                table_items.append(table_item)

            self.ui.tblTeachers.insertRow(row)
            for col, item in enumerate(table_items):
                self.ui.tblTeachers.setItem(row, col, item)

            # Create a new instance of the widget for each row
            self.ui.tblTeachers.setColumnWidth(row, 40)
            self.ui.tblTeachers.setRowHeight(row, 150)
            operations_buttons = DeleteUpdateButtonTeachersWidget(table_widget=self.ui.tblTeachers)
            if self.finger_button_state:
                new_instance = operations_buttons.get_buttons('New')
                self.ui.tblTeachers.setCellWidget(row, 8, new_instance)
            else:
                new_instance = operations_buttons.get_buttons('Old')
                self.ui.tblTeachers.setCellWidget(row, 8, new_instance)

    def add_members_database(self):
        teacher_dialog = TeacherDialog()
        if teacher_dialog.exec_() == QDialog.Accepted:
            try:
                schoolID = 1
                FName, SName, TName, LName, Phone, DOB, Major, Task, state = teacher_dialog.save_data()
                Members.insert({
                    Members.school_id: schoolID,
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
                    # Teachers.fingerPrintData: fingerPrintData,
                }).execute()
                has_finger_print_data = 'لا'
                teacher = [FName, SName, TName, LName, Phone, DOB, Major, Task, state, has_finger_print_data]
                self.lastInsertedTeacherId = Teachers.select(peewee.fn.Max(Teachers.id)).scalar()
                # self.get_members_data()
                fullName = [teacher[0], teacher[1], teacher[3]]
                print (fullName)
                operations_buttons = DeleteUpdateButtonTeachersWidget(table_widget=self.ui.tblTeachers)
                result = operations_buttons.add_users_to_device(self.lastInsertedTeacherId, fullName)
                print(result)
                if result:
                    self.add_new_teacher_to_table_widget(self.lastInsertedTeacherId, teacher)
                    QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")
                else:
                    QMessageBox.critical(self.ui, "خطأ", "لم يتم الحفظ بنجاح")

            except ValueError as e:
                QMessageBox.critical(self.ui, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")

    def add_new_teacher_to_table_widget(self, teacher_id, teacher):
        try:
            operations_buttons = DeleteUpdateButtonTeachersWidget(table_widget=self.ui.tblTeachers)
            current_row = self.ui.tblTeachers.rowCount()
            self.ui.tblTeachers.insertRow(current_row)
            self.ui.tblTeachers.setItem(current_row, 0, QTableWidgetItem(str(teacher_id)))
            self.ui.tblTeachers.setItem(current_row, 1, QTableWidgetItem(teacher[0]))
            self.ui.tblTeachers.setItem(current_row, 2, QTableWidgetItem(teacher[1]))
            self.ui.tblTeachers.setItem(current_row, 3, QTableWidgetItem(teacher[2]))
            self.ui.tblTeachers.setItem(current_row, 4, QTableWidgetItem(teacher[3]))
            self.ui.tblTeachers.setItem(current_row, 5, QTableWidgetItem(str(teacher[4])))
            self.ui.tblTeachers.setItem(current_row, 6, QTableWidgetItem(str(teacher[5])))
            self.ui.tblTeachers.setItem(current_row, 7, QTableWidgetItem(teacher[6]))
            self.ui.tblTeachers.setItem(current_row, 8, QTableWidgetItem(teacher[7]))
            self.ui.tblTeachers.setItem(current_row, 9, QTableWidgetItem(teacher[8]))
            self.ui.tblTeachers.setItem(current_row, 10, QTableWidgetItem(teacher[9]))
            self.ui.tblTeachers.setCellWidget(current_row, 11, operations_buttons.get_buttons('Old'))
            self.ui.tblTeachers.setColumnWidth(current_row, 40)
            self.ui.tblTeachers.setRowHeight(current_row, 150)
            # self.add_to_members_to_device(str(teacher_id),teacher[0])
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)
