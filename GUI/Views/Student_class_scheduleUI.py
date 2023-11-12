from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidgetItem, QRadioButton, QComboBox, QButtonGroup, QMessageBox
from GUI.Views.CommonFunctionality import Common
from models.ClassRoom import ClassRoom
import os
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import pdfkit
import datetime

from models.Teachers_Schedule import Teachers_Schedule


class Student_class_scheduleUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.get_classes()
        self.get_session()
        self.get_subject()
        self.get_days()

    def use_ui_elements(self):
        self.ui.tblStudentSchedule.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblStudentSchedule.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblStudentSchedule.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.ui.btnAddNewStudentSchedule.clicked.connect(self.add_new_student_schedule)
        self.ui.btnShowScheduleStudents.clicked.connect(self.get_data_schedule_students)
        self.ui.btnReportAddNewStudentSchedule.clicked.connect(self.generate_pdf_schedule_student_report)

    def get_classes(self):
        classes = ClassRoom.select(ClassRoom.name)
        for classe in classes:
            self.ui.combChosseClass.addItem(classe.name)

    def get_session(self):
        session = Common.get_sessions(self.ui)
        self.ui.combChosseSession.clear()
        self.ui.combChosseSession.addItems(session)

    def get_subject(self):
        subject = Common.get_subjects(self.ui)
        self.ui.combChosseSubject.clear()
        self.ui.combChosseSubject.addItems(subject)

    def get_days(self):
        subject = Common.get_days(self.ui)
        self.ui.combChosseDay.clear()
        self.ui.combChosseDay.addItems(subject)

    # def add_new_student_schedule(self):
    #     selected_class = self.ui.combChosseClass.currentText()
    #     selected_session = self.ui.combChosseSession.currentText()
    #     selected_subject = self.ui.combChosseSubject.currentText()
    #     selected_day = self.ui.combChosseDay.currentText()
    #     current_row = self.ui.tblStudentSchedule.rowCount()
    #     self.ui.tblStudentSchedule.insertRow(current_row)
    #     self.ui.tblStudentSchedule.setItem(current_row, 0, QTableWidgetItem(selected_class))
    #     self.ui.tblStudentSchedule.setItem(current_row, 1, QTableWidgetItem(selected_session))
    #     self.ui.tblStudentSchedule.setItem(current_row, 2, QTableWidgetItem(selected_subject))
    #     self.ui.tblStudentSchedule.setItem(current_row, 3, QTableWidgetItem(selected_day))

    def get_data_schedule_students(self):
        selected_name_class = self.ui.combClassStudentSelected.currentText()
        if selected_name_class == "الاول" or selected_name_class == "الثاني" or selected_name_class == "الثالث" \
                or selected_name_class == "الرابع" or selected_name_class == "الخامس" or selected_name_class == "السادس" or selected_name_class == "السابع" \
                or selected_name_class == "الثامن":
            query = Teachers_Schedule.select().where(
                Teachers_Schedule.Class_Name == selected_name_class
            ).order_by(
                Teachers_Schedule.Day,
                Teachers_Schedule.session
            )

            # Create a mapping of session values to column indices
            session_mapping = {
                'الاولى': 0,
                'الثانية': 1,
                'الثالثة': 2,
                'الرابعة': 3,
                'الخامسة': 4,
                'السادسة': 5,
                'السابعة': 6,
            }

            # Create a mapping of day values to row indices
            day_mapping = {
                'السبت': 0,
                'الاحد': 1,
                'الاثنين': 2,
                'الثلاثاء': 3,
                'الاربعاء': 4,
                'الخميس': 5,
            }

            table_widget = self.ui.tblStudentSchedule  # Replace "tblShowScheduleStudents" with the actual name of your QTableWidget

            # Clear the table widget
            table_widget.clearContents()

            # Iterate over the query results and populate the table widget
            for schedule in query:
                day_index = day_mapping.get(schedule.Day)
                if day_index is None:
                    continue  # Skip rows with invalid 'Day' values

                # Determine the column index based on the value of 'session'
                session_index = session_mapping.get(schedule.session)
                if session_index is None:
                    continue  # Skip columns with invalid 'session' values

                item_subject = QTableWidgetItem(schedule.Subject)
                table_widget.setItem(day_index, session_index, item_subject)

        else:
            table_widget = self.ui.tblStudentSchedule  # Replace "tblShowScheduleStudents" with the actual name of your QTableWidget
            table_widget.clearContents()

    ##############################################################################
    # this code to show subject with name teacher

    # selected_name_class = self.ui.combClassStudentSelected.currentText()
    # if selected_name_class == "الثالث" or selected_name_class == "الرابع":
    #     query = Teachers_Schedule.select().where(
    #         Teachers_Schedule.Class_Name == selected_name_class
    #     ).order_by(
    #         Teachers_Schedule.Day,
    #         Teachers_Schedule.session
    #     )
    #
    #     # Create a mapping of session values to column indices
    #     session_mapping = {
    #         'الاولى': 0,
    #         'الثانية': 1,
    #         'الثالثة': 2,
    #         'الرابعة': 3,
    #         'الخامسة': 4,
    #         'السادسة': 5,
    #         'السابعة': 6,
    #     }
    #
    #     # Create a mapping of day values to row indices
    #     day_mapping = {
    #         'السبت': 0,
    #         'الاحد': 1,
    #         'الاثنين': 2,
    #         'الثلاثاء': 3,
    #         'الاربعاء': 4,
    #         'الخميس': 5,
    #     }
    #
    #     table_widget = self.ui.tblShowScheduleStudents  # Replace "tblShowScheduleStudents" with the actual name of your QTableWidget
    #
    #     # Clear the table widget
    #     table_widget.clearContents()
    #
    #     # Iterate over the query results and populate the table widget
    #     for schedule in query:
    #         day_index = day_mapping.get(schedule.Day)
    #         if day_index is None:
    #             continue  # Skip rows with invalid 'Day' values
    #
    #         # Determine the column index based on the value of 'session'
    #         session_index = session_mapping.get(schedule.session)
    #         if session_index is None:
    #             continue  # Skip columns with invalid 'session' values
    #
    #         subject_teacher = f"{schedule.Subject} - {schedule.Teacher_Name}"
    #         item_subject = QTableWidgetItem(subject_teacher)
    #         table_widget.setItem(day_index, session_index, item_subject)
    #
    # else:
    #     table_widget = self.ui.tblShowScheduleStudents  # Replace "tblShowScheduleStudents" with the actual name of your QTableWidget
    #     table_widget.clearContents()

    def generate_pdf_schedule_student_report(self):
        table_widget = self.ui.tblStudentSchedule

        # Get the column names
        column_names = ['الاولى', 'الثانية ', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة']

        # Additional column names for days of the week
        days_week = ['السبت', 'الاحد', 'الاثنين', 'الثلاثاء', 'الاربعاء', 'الخميس']

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
                         <p class="p1">وزارة التربية والتعليم</p>
                         <p class="date">التاريخ : <span id="current-date"></span></p>
                         <hr>
                         <br><br><br><br><br><br><br>
                         <table>"""
        name_class = self.ui.combClassStudentSelected.currentText()
        html_table += "<caption><center><font size='5' color='black'<italc>جدول الحصص الاسبوعية للصف</italc> {}</font></center></caption>".format(
            name_class)
        # Add the header row
        html_table += "<tr>"
        html_table += "<th>اليوم</th>"  # Header for the first column
        for name in column_names:
            html_table += f"<th>{name}</th>"
        html_table += "</tr>"

        # Add the data rows
        for row in range(table_widget.rowCount()):
            html_table += "<tr>"
            html_table += f"<td><b>{days_week[row]}</b></td>"  # Day of the week column
            for col in range(table_widget.columnCount()):
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
