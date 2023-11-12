from datetime import datetime
import datetime
import logging
import peewee
from PyQt5.QtCore import QDate, Qt
from models.ClassRoom import ClassRoom

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout
from GUI.Views.CommonFunctionality import Common
from GUI.Views.DeviceUI import DeviceUI
from models.Members import Members
from models.Students import Students
import os
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import pdfkit
import datetime


class Student_reportUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ips = ''
        self.ports = ''
        self.lastInsertedMemberId = 0
        self.lastInsertedTeacherId = 0
        self.finger_button_state = True
        self.ui.tabStudentsReport.setColumnHidden(0, True)
        self.set_data_in_comboSearch()

    def use_ui_elements(self):
        self.ui.combStudentReport.currentTextChanged.connect(self.get_report_student_data)
        self.ui.btnReportStudent.clicked.connect(self.generate_pdf_student_report)

    def set_data_in_comboSearch(self):
        self.ui.combStudentReport.clear()
        data = ClassRoom.select(ClassRoom.id, ClassRoom.name)

        for d in data:
            self.ui.combStudentReport.addItem(d.name, userData=d.id)
            # self.ui.comboStudReport.setItemData(d.id, d.id)

    def get_report_student_data(self):
        current_text = self.ui.combStudentReport.currentText()
        class_room_id = ClassRoom.select().where(ClassRoom.name == current_text).get().id

        if class_room_id:

            members_query = Members.select().join(Students).where(Students.class_id == class_room_id)

            print(members_query.count())

            self.ui.tabStudentsReport.setColumnHidden(8, False)
            self.ui.tabStudentsReport.setRowCount(0)
            try:
                columns = ['id', 'fName', 'sName', 'tName', 'lName', 'class_id', 'dateBerth', 'phone']

                for row, member_data in enumerate(members_query):
                    table_items = []

                    for column_name in columns:
                        try:
                            item_value = getattr(member_data, column_name)
                        except AttributeError:
                            student_data = Students.get(Students.member_id == member_data.id)
                            item_value = getattr(student_data, column_name)
                            if column_name == 'class_id':
                                self.ui.id = getattr(student_data, column_name)

                        table_item = QTableWidgetItem(str(item_value))
                        table_items.append(table_item)

                    self.ui.tabStudentsReport.insertRow(row)

                    for col, item in enumerate(table_items):
                        self.ui.tabStudentsReport.setItem(row, col, item)

                    self.ui.tabStudentsReport.setItem(row, 5, QTableWidgetItem(current_text))
                    Common.style_table_widget(self.ui, self.ui.tabStudentsReport)
            except Exception as e:
                error_message = "حدث خطأ:\n\n" + str(e)
                QMessageBox.critical(self.ui, "خطأ", error_message)

        else:
            QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")

    def generate_pdf_student_report(self):
        # Get the table widget
        table_widget = self.ui.tabStudentsReport

        # Get the column names
        column_names = ['الرقم', 'الاسم ', 'الصف', 'تاريخ الميلاد', 'رقم التلفون']

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
