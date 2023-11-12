import peewee
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidgetItem, QRadioButton, QComboBox, QButtonGroup, QMessageBox

from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonTeacherScheduleWidget
from GUI.Views.CommonFunctionality import Common
from models.ClassRoom import ClassRoom
import os
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import pdfkit
import datetime

from models.Teachers import Teachers
from models.Members import Members
from models.Teachers_Schedule import Teachers_Schedule


class Teacher_class_scheduleUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ui.tblTeacherSchedule.setColumnHidden(0, True)
        self.ui.tblTeacherSchedule.setColumnHidden(6, True)
        self.get_classe()
        self.get_session()
        self.get_subject()
        self.get_days()
        self.get_teacher()

    def use_ui_elements(self):
        self.ui.tblStudentSchedule.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblStudentSchedule.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblStudentSchedule.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnAddNewTeacherSchedule.clicked.connect(self.add_new_teacher_schedule)
        self.ui.btnShowDataTeachers.clicked.connect(self.get_data_schedule_teacher_for_changed)
        self.ui.btnShowScheduleTeachers.clicked.connect(self.get_data_schedule_teacher_for_export)
        self.ui.btnReportAddNewTeacherSchedule.clicked.connect(self.generate_pdf_schedule_teacher_report)
        self.ui.RemveTableTeacher.clicked.connect(self.remove_teacher_schedule)

    def get_classe(self):
        # classes = ClassRoom.select(ClassRoom.name)
        # for classe in classes:
        #     self.ui.combTeacherChosseClass.addItem(classe.name)
        classe = Common.get_classes(self.ui)
        self.ui.combTeacherChosseClass.clear()
        self.ui.combTeacherChosseClass.addItems(classe)

    def get_session(self):
        session = Common.get_sessions(self.ui)
        self.ui.combTeacherChosseSession.clear()
        self.ui.combTeacherChosseSession.addItems(session)

    def get_subject(self):
        subject = Common.get_subjects(self.ui)
        self.ui.combTeacherChosseSubject.clear()
        self.ui.combTeacherChosseSubject.addItems(subject)
        # selected_subject = self.ui.combTeacherChosseSubject.currentText()

    def get_days(self):
        subject = Common.get_days(self.ui)
        self.ui.combTeacherChosseDay.clear()
        self.ui.combTeacherChosseDay.addItems(subject)

    def get_teacher(self):
        members = Members.select().join(Teachers)
        for member in members:
            full_name = member.fName + ' ' + member.lName
            self.ui.combChosseTeacher.addItem(full_name)

    def add_new_teacher_schedule(self):
        self.ui.tblTeacherSchedule.setColumnHidden(6, True)
        selected_class = self.ui.combTeacherChosseClass.currentText()
        selected_session = self.ui.combTeacherChosseSession.currentText()
        selected_subject = self.ui.combTeacherChosseSubject.currentText()
        selected_day = self.ui.combTeacherChosseDay.currentText()
        selected_teacher = self.ui.combChosseTeacher.currentText()

        # Check if the selected teacher has already been assigned the maximum number of sessions
        query_teacher_sessions = Teachers_Schedule.select().where(
            Teachers_Schedule.Teacher_Name == selected_teacher
        )
        if query_teacher_sessions.count() >= 7:
            QMessageBox.information(self.ui, "تحذير", "اكتمل عدد الحصص لهذا المعلم")
        else:
            # Check if the selected teacher already has the selected session assigned in any class
            query_session_teacher = Teachers_Schedule.select().where(
                Teachers_Schedule.Teacher_Name == selected_teacher,
                Teachers_Schedule.session == selected_session,
                Teachers_Schedule.Day == selected_day,
                Teachers_Schedule.Class_Name != selected_class
            )
            if query_session_teacher.exists():
                QMessageBox.information(self.ui, "تحذير", "تم تعيين الحصة لمعلم آخر")
            else:
                # Check if the selected session is already assigned to any teacher in the selected class
                query_session_class = Teachers_Schedule.select().where(
                    Teachers_Schedule.Class_Name == selected_class,
                    Teachers_Schedule.session == selected_session,
                    Teachers_Schedule.Day == selected_day,
                    Teachers_Schedule.Teacher_Name != selected_teacher
                )
                if query_session_class.exists():
                    QMessageBox.information(self.ui, "تحذير", "تم تعيين الحصة لمعلم آخر")
                else:
                    query_duplicate_session = Teachers_Schedule.select().where(
                        Teachers_Schedule.Teacher_Name == selected_teacher,
                        Teachers_Schedule.Class_Name == selected_class,
                        Teachers_Schedule.session == selected_session,
                        Teachers_Schedule.Day == selected_day
                    )
                    if query_duplicate_session.exists():
                        QMessageBox.information(self.ui, "تحذير", "تم تعيين نفس الحصة للمعلم في نفس الفصل في نفس اليوم")
                    else:
                        # Insert the new entry into the Teachers_Schedule table
                        Teachers_Schedule.create(
                            Teacher_Name=selected_teacher,
                            Day=selected_day,
                            Subject=selected_subject,
                            session=selected_session,
                            Class_Name=selected_class
                        )
                        QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")
                        current_row = self.ui.tblTeacherSchedule.rowCount()
                        self.ui.tblTeacherSchedule.insertRow(current_row)
                        self.ui.tblTeacherSchedule.setItem(current_row, 1, QTableWidgetItem(selected_day))
                        self.ui.tblTeacherSchedule.setItem(current_row, 2, QTableWidgetItem(selected_subject))
                        self.ui.tblTeacherSchedule.setItem(current_row, 3, QTableWidgetItem(selected_session))
                        self.ui.tblTeacherSchedule.setItem(current_row, 4, QTableWidgetItem(selected_class))
                        self.ui.tblTeacherSchedule.setItem(current_row, 5, QTableWidgetItem(selected_teacher))
                        self.ui.tblTeacherSchedule.setColumnWidth(current_row, 40)
                        self.ui.tblTeacherSchedule.setRowHeight(current_row, 150)
                        Common.style_table_widget(self.ui, self.ui.tblTeacherSchedule)
                        if selected_session == "السابعة":
                            self.ui.tblTeacherSchedule.setRowCount(0)  # Clear existing rows in the table
                            QMessageBox.information(self.ui, "اشعار",
                                                    f"أختار اليوم التالي لأضافة الحصص للصف {selected_class}")
                if self.ui.tblTeacherSchedule.rowCount() == 42:
                    QMessageBox.information(self.ui, "اشعار", f"تم اضافة الجدول الاسبوعي للصف {selected_class}")

    def remove_teacher_schedule(self):
        self.ui.tblTeacherSchedule.setRowCount(0)

    def get_data_schedule_teacher_for_changed(self):
        # self.ui.tblTeacherSchedule.setColumnHidden(0, True)
        self.ui.tblTeacherSchedule.setColumnHidden(6, False)
        try:
            columns = ['id', 'Day', 'Subject', 'session', 'Class_Name', 'Teacher_Name']
            selected_class = self.ui.combTeacherChosseClass.currentText().lower()
            # selected_session = self.ui.combTeacherChosseSession.currentText().lower()
            # selected_subject = self.ui.combTeacherChosseSubject.currentText().lower()
            # selected_day = self.ui.combTeacherChosseDay.currentText().lower()
            # selected_teacher = self.ui.combChosseTeacher.currentText().lower()
            members_query = Teachers_Schedule.select().where(
                # (peewee.fn.LOWER(Teachers_Schedule.Class_Name).contains(selected_class)) |
                # (peewee.fn.LOWER(Teachers_Schedule.session).contains(selected_session)) |
                # (peewee.fn.LOWER(Teachers_Schedule.Subject).contains(selected_subject)) |
                # (peewee.fn.LOWER(Teachers_Schedule.Day).contains(selected_day)) |
                (peewee.fn.LOWER(Teachers_Schedule.Class_Name).contains(selected_class))
            ).distinct()
            self.ui.tblTeacherSchedule.setRowCount(0)  # Clear existing rows in the table
            for row, member_data in enumerate(members_query):
                table_items = []
                for column_name in columns:
                    try:
                        item_value = getattr(member_data, column_name)
                    except AttributeError:
                        teacher_schedule_data = Teachers_Schedule.get(Teachers_Schedule.id == member_data.id)
                        item_value = getattr(teacher_schedule_data, column_name)

                    table_item = QTableWidgetItem(str(item_value))
                    table_items.append(table_item)

                self.ui.tblTeacherSchedule.insertRow(row)
                for col, item in enumerate(table_items):
                    self.ui.tblTeacherSchedule.setItem(row, col, item)

                self.ui.tblTeacherSchedule.setColumnWidth(row, 40)
                self.ui.tblTeacherSchedule.setRowHeight(row, 150)
                operations_buttons = DeleteUpdateButtonTeacherScheduleWidget(table_widget=self.ui.tblTeacherSchedule)
                self.ui.tblTeacherSchedule.setCellWidget(row, 6, operations_buttons)
                Common.style_table_widget(self.ui, self.ui.tblTeacherSchedule)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def get_data_schedule_teacher_for_export(self):
        # استعلم جدول Teachers_Schedule للحصول على البيانات المطلوبة
        query = Teachers_Schedule.select().execute()

        # Clear the existing contents of the table widget
        table_widget = self.ui.tblShowScheduleTeachers
        table_widget.clearContents()

        # Define column mapping for session and table column index
        column_mapping = {
            ('السبت', 'الاولى'): 1,
            ('السبت', 'الثانية'): 2,
            ('السبت', 'الثالثة'): 3,
            ('السبت', 'الرابعة'): 4,
            ('السبت', 'الخامسة'): 5,
            ('السبت', 'السادسة'): 6,
            ('السبت', 'السابعة'): 7,
            ('الاحد', 'الاولى'): 8,
            ('الاحد', 'الثانية'): 9,
            ('الاحد', 'الثالثة'): 10,
            ('الاحد', 'الرابعة'): 11,
            ('الاحد', 'الخامسة'): 12,
            ('الاحد', 'السادسة'): 13,
            ('الاحد', 'السابعة'): 14,
            ('الاثنين', 'الاولى'): 15,
            ('الاثنين', 'الثانية'): 16,
            ('الاثنين', 'الثالثة'): 17,
            ('الاثنين', 'الرابعة'): 18,
            ('الاثنين', 'الخامسة'): 19,
            ('الاثنين', 'السادسة'): 20,
            ('الاثنين', 'السابعة'): 21,
            ('الثلاثاء', 'الاولى'): 22,
            ('الثلاثاء', 'الثانية'): 23,
            ('الثلاثاء', 'الثالثة'): 24,
            ('الثلاثاء', 'الرابعة'): 25,
            ('الثلاثاء', 'الخامسة'): 26,
            ('الثلاثاء', 'السادسة'): 27,
            ('الثلاثاء', 'السابعة'): 28,
            ('الاربعاء', 'الاولى'): 29,
            ('الاربعاء', 'الثانية'): 30,
            ('الاربعاء', 'الثالثة'): 31,
            ('الاربعاء', 'الرابعة'): 32,
            ('الاربعاء', 'الخامسة'): 33,
            ('الاربعاء', 'السادسة'): 34,
            ('الاربعاء', 'السابعة'): 35,
            ('الخميس', 'الاولى'): 36,
            ('الخميس', 'الثانية'): 37,
            ('الخميس', 'الثالثة'): 38,
            ('الخميس', 'الرابعة'): 39,
            ('الخميس', 'الخامسة'): 40,
            ('الخميس', 'السادسة'): 41,
            ('الخميس', 'السابعة'): 42
        }

        # Create a dictionary to store the row index for each teacher name
        teacher_rows = {}

        # Iterate over the query results and populate the table
        for item in query:
            teacher_name = item.Teacher_Name
            day = item.Day
            session = item.session

            # Find the row index for the teacher name
            if teacher_name in teacher_rows:
                row = teacher_rows[teacher_name]
            else:
                row = table_widget.rowCount()
                table_widget.setRowCount(row + 1)
                teacher_name_item = QTableWidgetItem(teacher_name)
                table_widget.setItem(row, 0, teacher_name_item)
                teacher_rows[teacher_name] = row
            if (day, session) in column_mapping:
                column = column_mapping[(day, session)]
                subject_item = QTableWidgetItem(item.Subject)
                print(subject_item.text())
                table_widget.setItem(row, column, subject_item)

    def generate_pdf_schedule_teacher_report(self):
        # Get the table widget
        table_widget = self.ui.tblTeacherSchedule

        # Get the column names
        column_names = ['الاولى', 'الثانية ', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة',
                        'الاولى', 'الثانية ', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة',
                        'الاولى', 'الثانية ', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة',
                        'الاولى', 'الثانية ', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة',
                        'الاولى', 'الثانية ', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة',
                        'الاولى', 'الثانية ', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة']

        # Create the HTML table
        html_table = """<html>
                             <center>
                             <style>
                                 table {
                                     border-collapse: collapse;
                                     direction: rtl;
                                     width: 50%;
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
        html_table += "<caption><center><font size='5' color='black'<italc>جدول الحصص الاسبوعية للصف</italc> {}</font></center></caption>".format(
            table_widget)
        # Add the header row
        html_table += "<tr>"
        for name in column_names:
            html_table += f"<th>{name}</th>"
        html_table += "</tr>"

        # Add the data rows
        for row in range(table_widget.rowCount()):
            html_table += "<tr>"
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
