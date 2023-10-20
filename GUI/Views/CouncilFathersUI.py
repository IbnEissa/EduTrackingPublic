from datetime import datetime
import datetime
import logging
import peewee
from PyQt5.QtCore import QDate, Qt

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout
# from zk import ZK

# from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonCouncilFathersWidget
from GUI.Dialogs.CouncilFathersDialog import CouncilFathersDialog
from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonCouncilFathersWidget
from GUI.Views.CommonFunctionality import Common
from GUI.Views.DeviceUI import DeviceUI
from models.Members import Members
from models.CouncilFathers import CouncilFathers
from models.School import School


class CouncilFathersUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ips = ''
        self.ports = ''
        self.lastInsertedMemberId = 0
        self.lastInsertedCouncilFathersId = 0
        self.lastInsertedSchoolId = 0

    def use_ui_elements(self):
        self.ui.tblCouncilFathers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblCouncilFathers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblCouncilFathers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnAddNewCouncilFathers.clicked.connect(self.add_council_fathers_database)
        self.ui.txtCouncilFathersSearch.textChanged.connect(self.get_council_fathers_data)

    def get_council_fathers_data(self):
        result_condition = Common.grant_permission_to_clicked_button(self.ui, permission="bt_search_fathers")
        if result_condition is True:
            columns = ['id', 'fName', 'sName', 'tName', 'lName', 'phone', 'dateBerth', 'CouncilFathersTask']

            search_item = self.ui.txtCouncilFathersSearch.toPlainText().lower()

            members_query = Members.select().join(CouncilFathers).where(
                peewee.fn.LOWER(Members.fName).contains(search_item)).distinct()

            self.ui.tblCouncilFathers.setRowCount(0)  # Clear existing rows in the table
            for row, member_data in enumerate(members_query):
                table_items = []
                for column_name in columns:
                    try:
                        item_value = getattr(member_data, column_name)
                    except AttributeError:
                        CouncilFathers_data = CouncilFathers.get(CouncilFathers.members_id == member_data.id)
                        item_value = getattr(CouncilFathers_data, column_name)
                    table_item = QTableWidgetItem(str(item_value))
                    table_items.append(table_item)

                self.ui.tblCouncilFathers.insertRow(row)
                for col, item in enumerate(table_items):
                    self.ui.tblCouncilFathers.setItem(row, col, item)

                self.ui.tblCouncilFathers.setColumnWidth(row, 40)
                self.ui.tblCouncilFathers.setRowHeight(row, 150)
                operations_buttons = DeleteUpdateButtonCouncilFathersWidget(table_widget=self.ui.tblCouncilFathers)
                self.ui.tblCouncilFathers.setCellWidget(row, 8, operations_buttons)
                Common.style_table_widget(self.ui, self.ui.tblCouncilFathers)
        else:
            QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")

    def add_council_fathers_database(self):
        result_condition = Common.grant_permission_to_clicked_button(self.ui, permission="bt_save_fathers")
        if result_condition is True:
            CouncilFathers_dialog = CouncilFathersDialog()
            if CouncilFathers_dialog.exec_() == QDialog.Accepted:
                try:
                    lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
                    CouncilFathersName, CouncilSecName, CouncilThirdName, CouncilLName, CouncilPhone, CouncilDOB, CouncilTask = CouncilFathers_dialog.save_data()
                    Members.insert({
                        Members.school_id: lastInsertedSchoolId,
                        Members.fName: CouncilFathersName,
                        Members.sName: CouncilSecName,
                        Members.tName: CouncilThirdName,
                        Members.lName: CouncilLName,
                        Members.phone: CouncilPhone,
                        Members.dateBerth: CouncilDOB,

                    }).execute()
                    self.lastInsertedMemberId = Members.select(peewee.fn.Max(Members.id)).scalar()
                    CouncilFathers.insert({
                        CouncilFathers.members_id: self.lastInsertedMemberId,
                        CouncilFathers.CouncilFathersTask: CouncilTask,
                    }).execute()

                    councilFathers = [CouncilFathersName, CouncilSecName, CouncilThirdName, CouncilLName, CouncilPhone,
                                      CouncilDOB, CouncilTask]
                    self.lastInsertedCouncilFathersId = CouncilFathers.select(peewee.fn.Max(CouncilFathers.id)).scalar()
                    self.add_new_council_fathers_to_table_widget(self.lastInsertedCouncilFathersId, councilFathers)
                    QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")
                except ValueError as e:
                    QMessageBox.critical(self.ui, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")
        else:
            QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")

    def add_new_council_fathers_to_table_widget(self, council_fathers_id, council_fathers):
        try:
            operations_buttons = DeleteUpdateButtonCouncilFathersWidget(table_widget=self.ui.tblCouncilFathers)
            current_row = self.ui.tblCouncilFathers.rowCount()
            self.ui.tblCouncilFathers.insertRow(current_row)
            self.ui.tblCouncilFathers.setItem(current_row, 0, QTableWidgetItem(str(council_fathers_id)))
            self.ui.tblCouncilFathers.setItem(current_row, 1, QTableWidgetItem(council_fathers[0]))
            self.ui.tblCouncilFathers.setItem(current_row, 2, QTableWidgetItem(council_fathers[1]))
            self.ui.tblCouncilFathers.setItem(current_row, 3, QTableWidgetItem(council_fathers[2]))
            self.ui.tblCouncilFathers.setItem(current_row, 4, QTableWidgetItem(council_fathers[3]))
            self.ui.tblCouncilFathers.setItem(current_row, 5, QTableWidgetItem(str(council_fathers[4])))
            self.ui.tblCouncilFathers.setItem(current_row, 6, QTableWidgetItem(str(council_fathers[5])))
            self.ui.tblCouncilFathers.setItem(current_row, 7, QTableWidgetItem(council_fathers[6]))
            self.ui.tblCouncilFathers.setCellWidget(current_row, 8, operations_buttons)
            self.ui.tblCouncilFathers.setColumnWidth(current_row, 40)
            self.ui.tblCouncilFathers.setRowHeight(current_row, 150)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)
