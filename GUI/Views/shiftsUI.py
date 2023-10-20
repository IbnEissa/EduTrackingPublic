import peewee
from PyQt5.QtCore import QDate, Qt

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout
from GUI.Dialogs.Shifttimes import Shift_timedialog
from PyQt5.QtCore import QTime, Qt
from models.shift_time import Shift_time


class Shift_timeUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui

    def shift_ui_elements(self):
        self.ui.tblshifttime.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblshifttime.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblshifttime.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnAddNewshift_time.clicked.connect(self.add_new_shift_time)
        self.ui.txtShiftSearch.textChanged.connect(self.get_shift_data)

    def add_new_shift_time(self):
        shift_dialog = Shift_timedialog()
        if shift_dialog.exec_() == QDialog.Accepted:
            try:
                # lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
                name, shift_Type, start_time, delay_times, end_time = shift_dialog.save_data_shift()
                Shift_time.insert({
                    Shift_time.name: name,
                    Shift_time.shift_Type: shift_Type,
                    Shift_time.start_time: start_time,
                    Shift_time.end_time: end_time,
                    Shift_time.delay_times: delay_times,
                }).execute()
                self.lastInsertedshifttime = Shift_time.select(peewee.fn.Max(Shift_time.id)).scalar()
                shift = Shift_time.get(Shift_time.id == self.lastInsertedshifttime)
                creation_date = shift.created_at
                update_date = shift.updated_at
                shift = [self.lastInsertedshifttime, name, shift_Type, start_time, delay_times, end_time,
                         creation_date, update_date
                         ]
                self.add_new_shift_time_to_table_widget(shift)

                QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")
            except ValueError as e:
                QMessageBox.critical(self.ui, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")

    def add_new_shift_time_to_table_widget(self, shifts):
        self.ui.tblshifttime.setColumnHidden(0, True)
        self.ui.tblshifttime.setRowCount(0)
        try:

            current_row = self.ui.tblshifttime.rowCount()  # Get the current row index
            self.ui.tblshifttime.insertRow(current_row)  # Insert a new row at the current row index
            self.ui.tblshifttime.setItem(current_row, 0, QTableWidgetItem(shifts[0]))
            self.ui.tblshifttime.setItem(current_row, 1, QTableWidgetItem(shifts[1]))
            self.ui.tblshifttime.setItem(current_row, 2, QTableWidgetItem(shifts[2]))
            self.ui.tblshifttime.setItem(current_row, 3, QTableWidgetItem(str(shifts[3])))
            self.ui.tblshifttime.setItem(current_row, 4, QTableWidgetItem(str(shifts[4])))
            self.ui.tblshifttime.setItem(current_row, 5, QTableWidgetItem(str(shifts[5])))
            self.ui.tblshifttime.setItem(current_row, 6, QTableWidgetItem(str(shifts[6])))
            self.ui.tblshifttime.setItem(current_row, 7, QTableWidgetItem(str(shifts[7])))
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)

    def get_shift_data(self):
        self.ui.tblshifttime.setColumnHidden(0, True)

        try:
            columns = ['id', 'name', 'shift_Type', 'start_time', 'delay_times', 'end_time', 'created_at', 'updated_at',
                       ]
            search_item = self.ui.txtShiftSearch.toPlainText().lower()
            shift_query = Shift_time.select().where(
                peewee.fn.LOWER(Shift_time.name).contains(search_item)).distinct()
            self.ui.tblshifttime.setRowCount(0)  # Clear existing rows in the table
            for row, shift_itmes in enumerate(shift_query):
                table_items = []
                for column_name in columns:
                    try:
                        item_value = getattr(shift_itmes, column_name)
                    except AttributeError:
                        shift_data = Shift_time.get(Shift_time.id)
                        item_value = getattr(shift_data, column_name)

                    table_item = QTableWidgetItem(str(item_value))
                    table_items.append(table_item)

                self.ui.tblshifttime.insertRow(row)
                for col, item in enumerate(table_items):
                    self.ui.tblshifttime.setItem(row, col, item)

                # self.ui.tblshifttime.setColumnWidth(row, 40)
                # self.ui.tblshifttime.setRowHeight(row, 150)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)
