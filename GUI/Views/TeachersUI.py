from datetime import datetime
import datetime
import logging
import peewee
from PyQt5.QtCore import QDate, Qt

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout
from zk import ZK

from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonTeachersWidget
# from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonTeachersWidget
from GUI.Dialogs.TeacherDialog import TeacherDialog
from GUI.Views.CommonFunctionality import Common
from GUI.Views.DeviceUI import DeviceUI
from models.Members import Members
from models.School import School
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
        # self.ui.tblTeachers.setColumnHidden(0, True)

    def use_ui_elements(self):
        self.ui.tblTeachers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblTeachers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblTeachers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnAddNewTeacher.clicked.connect(self.add_members_database)
        self.ui.txtTeachersSearch.textChanged.connect(self.get_members_data)

    def get_members_data(self):
        result_condition = Common.grant_permission_to_clicked_button(self.ui, permission="bt_search_teacher")
        if result_condition is True:
            Common.style_table_widget(self.ui, self.ui.tblTeachers)
            columns = ['id', 'fName', 'dateBerth', 'phone', 'qualification',
                       'date_qualification', 'Shift_type', 'major', 'task', 'exceperiance_years',
                       'state',
                       'fingerPrintData']
            search_item = self.ui.txtTeachersSearch.toPlainText().lower()

            members_query = Members.select().join(Teachers).where(
                peewee.fn.LOWER(Members.fName).contains(search_item)).distinct()

            self.ui.tblTeachers.setRowCount(0)
            for row, member_data in enumerate(members_query):
                table_items = []
                for column_name in columns:
                    teacher_data = Teachers.get(Teachers.members_id == member_data.id)
                    try:
                        item_value = getattr(member_data, column_name)
                        if column_name == 'fName':
                            fName_value = getattr(member_data, column_name)
                            lName_value = getattr(member_data, 'lName')
                            item_value = fName_value + ' ' + lName_value
                            if column_name == 'id':
                                item_value = getattr(teacher_data, 'id')
                    except AttributeError:
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

                self.ui.tblTeachers.setColumnWidth(row, 120)
                self.ui.tblTeachers.setRowHeight(row, 170)
                operations_buttons = DeleteUpdateButtonTeachersWidget(table_widget=self.ui.tblTeachers)
                if self.finger_button_state:
                    new_instance = operations_buttons.get_buttons('New')
                    self.ui.tblTeachers.setCellWidget(row, 12, new_instance)
                    Common.style_table_widget(self.ui, self.ui.tblTeachers)
                else:
                    new_instance = operations_buttons.get_buttons('Old')
                    self.ui.tblTeachers.setCellWidget(row, 12, new_instance)
                    Common.style_table_widget(self.ui, self.ui.tblTeachers)
        else:
            QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")

    def add_members_database(self):
        # self.ui.tblTeachers.setRowCount(0)
        result_condition = Common.grant_permission_to_clicked_button(self.ui, permission="bt_save_teacher")
        if result_condition is True:
            Common.style_table_widget(self.ui, self.ui.tblTeachers)
            teacher_dialog = TeacherDialog()
            if teacher_dialog.exec_() == QDialog.Accepted:

                try:
                    lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
                    FName, LName, DOB, Phone, Qualification, DOQualification, ShiftsType, Major, Task, ExceperianceYears, state = teacher_dialog.save_data()
                    Members.insert({
                        Members.school_id: lastInsertedSchoolId,
                        Members.fName: FName,
                        Members.lName: LName,
                        Members.dateBerth: DOB,
                        Members.phone: Phone,

                    }).execute()
                    self.lastInsertedMemberId = Members.select(peewee.fn.Max(Members.id)).scalar()
                    Teachers.insert({
                        Teachers.members_id: self.lastInsertedMemberId,
                        Teachers.Shift_type: ShiftsType,
                        Teachers.major: Major,
                        Teachers.task: Task,
                        Teachers.exceperiance_years: ExceperianceYears,
                        Teachers.qualification: Qualification,
                        Teachers.date_qualification: DOQualification,
                        Teachers.state: state,
                    }).execute()
                    has_finger_print_data = 'لا'
                    teacher = [FName, LName, DOB, Phone, Qualification, DOQualification, ShiftsType, Major, Task,
                               ExceperianceYears, state, has_finger_print_data]
                    self.lastInsertedTeacherId = Teachers.select(peewee.fn.Max(Teachers.id)).scalar()
                    operations_buttons = DeleteUpdateButtonTeachersWidget(table_widget=self.ui.tblTeachers)
                    operations_buttons.add_users_to_device(self.lastInsertedTeacherId, 'صالح')
                    self.add_new_teacher_to_table_widget(self.lastInsertedTeacherId, teacher)
                    Common.style_table_widget(self.ui, self.ui.tblTeachers)
                    QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")
                except ValueError as e:
                    QMessageBox.critical(self.ui, "خطأ", f"فشلت العملية  : {str(e)}")
        else:
            QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")

    def add_new_teacher_to_table_widget(self, teacher_id, teacher):
        try:
            operations_buttons = DeleteUpdateButtonTeachersWidget(table_widget=self.ui.tblTeachers)
            current_row = self.ui.tblTeachers.rowCount()
            self.ui.tblTeachers.insertRow(current_row)
            self.ui.tblTeachers.setItem(current_row, 0, QTableWidgetItem(str(teacher_id)))
            self.ui.tblTeachers.setItem(current_row, 1, QTableWidgetItem(str(teacher[0] + ' ' + teacher[1])))
            self.ui.tblTeachers.setItem(current_row, 2, QTableWidgetItem(str(teacher[2])))
            self.ui.tblTeachers.setItem(current_row, 3, QTableWidgetItem(str(teacher[3])))
            self.ui.tblTeachers.setItem(current_row, 4, QTableWidgetItem(teacher[4]))
            self.ui.tblTeachers.setItem(current_row, 5, QTableWidgetItem(str(teacher[5])))
            self.ui.tblTeachers.setItem(current_row, 6, QTableWidgetItem(teacher[6]))
            self.ui.tblTeachers.setItem(current_row, 7, QTableWidgetItem(teacher[7]))
            self.ui.tblTeachers.setItem(current_row, 8, QTableWidgetItem(teacher[8]))
            self.ui.tblTeachers.setItem(current_row, 9, QTableWidgetItem(str(teacher[9])))
            self.ui.tblTeachers.setItem(current_row, 10, QTableWidgetItem(teacher[10]))
            self.ui.tblTeachers.setItem(current_row, 11, QTableWidgetItem(teacher[11]))
            self.ui.tblTeachers.setCellWidget(current_row, 12, operations_buttons.get_buttons('Old'))
            self.ui.tblTeachers.setColumnWidth(current_row, 60)
            self.ui.tblTeachers.setRowHeight(current_row, 150)
            Common.style_table_widget(self.ui, self.ui.tblTeachers)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)
