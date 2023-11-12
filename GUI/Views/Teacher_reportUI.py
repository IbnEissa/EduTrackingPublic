from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout
from GUI.Views.CommonFunctionality import Common
from models.ClassRoom import ClassRoom
# from GUI.Views.DeviceUI import DeviceUI
from models.Members import Members
from models.School import School
from models.Teachers import Teachers
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import peewee
import os
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore
import pdfkit
import base64
import datetime

from models.Weekly_class_schedule import WeeklyClassSchedule


class Teacher_reportUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ips = ''
        self.ports = ''
        self.lastInsertedMemberId = 0
        self.lastInsertedTeacherId = 0
        self.ui.tabTeachersReport.setColumnHidden(0, True)

    def use_ui_elements(self):

        self.ui.tabTeachersReport.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tabTeachersReport.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabTeachersReport.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.txtNameTeacher.textChanged.connect(self.get_report_teacher_data)
        self.ui.btnReportTeacher.clicked.connect(self.generate_pdf_teacher_report)
        self.ui.combReportClass.currentTextChanged.connect(self.get_report_class_data)

    def get_report_teacher_data(self):
        try:
            Common.style_table_widget(self.ui, self.ui.tabTeachersReport)
            column = ['id', 'fName', 'sName', 'tName', 'lName', 'phone', 'major', 'task']
            search_item = self.ui.txtNameTeacher.text().lower()
            members_query = Members.select().join(Teachers).where(
                (peewee.fn.LOWER(Members.fName).contains(search_item)) |
                (peewee.fn.LOWER(Members.lName).contains(search_item)) |
                (peewee.fn.LOWER(Teachers.major).contains(search_item)) |
                (peewee.fn.LOWER(Teachers.task).contains(search_item))
            ).distinct()

            self.ui.tabTeachersReport.setRowCount(0)  # Clear existing rows in the table

            for row, member_data in enumerate(members_query):
                table_items = []
                for column_name in column:
                    try:
                        item_value = getattr(member_data, column_name)

                    except AttributeError:
                        report_data = Teachers.get(Teachers.members_id == member_data.id)
                        item_value = getattr(report_data, column_name)

                    table_item = QTableWidgetItem(str(item_value))
                    table_items.append(table_item)

                self.ui.tabTeachersReport.insertRow(row)
                for col, item in enumerate(table_items):
                    self.ui.tabTeachersReport.setItem(row, col, item)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)

    def get_report_class_data(self):
        try:
            search_item = self.ui.combReportClass.currentText().lower()
            column = ['id', 'fName', 'sName', 'tName', 'lName', 'phone', 'major', 'task']

            members_query = (
                    Teachers
                    .select(Teachers, Members)
                    .join(WeeklyClassSchedule)
                    .join(Members, on=(Members.id == WeeklyClassSchedule.teacher_id))
                    .where(
                        WeeklyClassSchedule.class_room_id == ClassRoom.id) & (ClassRoom.name == search_item))

            self.ui.tabTeachersReport.setRowCount(0)  # Clear existing rows in the table

            for row, member_data in enumerate(members_query):
                table_items = []
                for column_name in column:
                    try:
                        item_value = getattr(member_data, column_name)

                    except AttributeError:
                        report_data = Teachers.get(Teachers.members_id == member_data.id)
                        item_value = getattr(report_data, column_name)

                    table_item = QTableWidgetItem(str(item_value))
                    table_items.append(table_item)

                self.ui.tabTeachersReport.insertRow(row)
                for col, item in enumerate(table_items):
                    self.ui.tabTeachersReport.setItem(row, col, item)

        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)
        print('osama')

    def generate_pdf_teacher_report(self):
        # Get the table widget
        table_widget = self.ui.tabTeachersReport

        # Get the column names
        column_names = ['الرقم', 'الاسم ', 'التلفون', 'المؤهل', 'التخصص']

        # Create the HTML table
        html_table = """<html>
                        <center>
                        <style>
                            table {
                                border-collapse: collapse;
                                direction: rtl;
                                width: 90%;
                            }
                            th, td {
                                border: 1px solid black;
                                padding: 8px;
                                direction: rtl;
                                text-align: center;
                            }
                            .p1 {
                                 text-align: right;
                            }
                            .date {
                                text-align: left;
                            }
                        </style>
                        <body><br>
                        <h2> بسم الله الرحمن الرحيم</h2>
                        <p class="p1"> الجمهورية  اليمنية</p>
                        <p class="p1">وزارة التربية والتعليم</p><p class="date">التاريخ : <span id="current-date"></span></p>                        
                        <hr>
                        <br><br><br><br><br><br><br>
                        <table>"""

        # Add the header row
        html_table += "<tr>"
        for name in column_names:
            html_table += f"<th>{name}</th>"
        html_table += "</tr>"

        # Add the data rows
        for row in range(table_widget.rowCount()):
            html_table += "<tr>"
            for col in range(table_widget.columnCount()):
                if col == 0:  # Add values from the sixth column onwards
                    item = table_widget.item(row, col)
                    if item is not None:
                        value = item.text()
                    else:
                        value = ""
                    html_table += f"<td>{value}</td>"
                elif col == 1:  # Combine values from second, third, fourth, and fifth columns
                    combined_value = ""
                    for sub_col in range(1, 5):  # Combine values from columns 1, 2, 3, and 4 (0-indexed)
                        item = table_widget.item(row, sub_col)
                        if item is not None:
                            value = item.text()
                            combined_value += value + " "
                    html_table += f"<td>{combined_value.strip()}</td>"
                elif col >= 5:  # Add values from the sixth column onwards
                    item = table_widget.item(row, col)
                    if item is not None:
                        value = item.text()
                    else:
                        value = ""
                    html_table += f"<td>{value}</td>"
            html_table += "</tr>"

        html_table += "</table></body></center></html>"

        # Get the current date
        current_date = datetime.date.today().strftime("%d-%m-%Y")

        # Insert the current date into the HTML code
        html_table = html_table.replace('<span id="current-date"></span>', current_date)

        # Define the input and output file paths
        input_file = 'temp.html'
        output_file = 'temp.pdf'

        # Write the HTML table to a temporary file with the correct encoding
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(html_table)

        # Configure the path to wkhtmltopdf
        config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

        # Set the options for PDF generation
        options = {
            'page-size': 'A4',
            'margin-top': '0mm',
            'margin-right': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
            'encoding': 'UTF-8',  # Specify the encoding
            'no-outline': None,  # Show table borders
        }

        # Generate the PDF
        pdfkit.from_file(input_file, output_file, configuration=config, options=options)

        # Open a file dialog to select the output PDF file path
        filename, _ = QFileDialog.getSaveFileName(None, 'Save PDF Report', '', 'PDF Files (*.pdf)')
        if filename:
            # Move the temporary PDF file to the desired output location
            os.rename(output_file, filename)

            # Show a success message
            QMessageBox.information(self.ui, "Success", "PDF report saved successfully!")

        # Delete the temporary HTML and PDF files
        os.remove(input_file)

        print('PDF generated successfully.')
