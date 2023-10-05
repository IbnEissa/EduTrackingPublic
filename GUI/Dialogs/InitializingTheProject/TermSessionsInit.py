import peewee
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem, QWidget, QVBoxLayout, QPushButton
from PyQt5.uic import loadUi
from GUI.Views.CommonFunctionality import Common
from models.ClassRoom import ClassRoom
from models.term_table import TeacherSubjectClassRoomTermTable


class TermSessionsInit(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("TermSessionsInit.ui", self)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.lastInsertedTermSession = 0
        self.get_subject()
        self.get_classes()
        self.operation = ""

    def use_ui_elements(self):
        self.btnAddNewSession.clicked.connect(self.add_sessions_database)
        self.btnMoveTermSessions.clicked.connect(self.accept)
        self.btnSkippingTermSessions.clicked.connect(self.reject)

    def change_to_update_operation(self):
        print("the method is called")
        self.btnAddNewSession.setText("حفظ")
        self.btnAddNewSession.setStyleSheet("background-color: red;")

    def change_to_add_operation(self):
        self.btnAddNewSession.setText("إضافة")

    def get_subject(self):
        subjects = Common.get_subjects(self)
        self.comboSubjects.clear()
        self.comboSubjects.addItems(subjects)

    def get_classes(self):
        self.comboClasses.clear()
        column_names = 'name'
        classes = Common.get_combo_box_data(self, ClassRoom, column_names)
        self.comboClasses.clear()
        self.comboClasses.addItems(classes)

    # def skipping_term_sessions(self):
    #     self.accept()
    # if self.exec_() == QDialog.Accepted:
    #     state_value = 1
    #     main = Main(state_value)
    #     main.method_1()
    def add_sessions_database(self):
        self.operation = "Add"
        try:
            class_name = self.comboClasses.currentText()
            class_id = ClassRoom.get_class_id_from_name(self, class_name)
            # teacher_id = Members.get_member_id_from_name(self, class_name)
            subject = self.comboSubjects.currentText()
            number_of_sessions = self.txtNumberOfSessions.toPlainText()
            TeacherSubjectClassRoomTermTable.insert({
                TeacherSubjectClassRoomTermTable.subject_id: subject,
                TeacherSubjectClassRoomTermTable.class_room_id: class_id,
                TeacherSubjectClassRoomTermTable.number_of_lessons: number_of_sessions,
            }).execute()
            self.lastInsertedTermSession = TeacherSubjectClassRoomTermTable.select(
                peewee.fn.Max(TeacherSubjectClassRoomTermTable.id)).scalar()
            if number_of_sessions.strip() == "":
                raise ValueError("يجب ادخال عدد الحصص ")
            self.add_new_sessions_to_table_widget(self.operation, class_name, subject, number_of_sessions,
                                                  self.lastInsertedTermSession)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None

    def add_new_sessions_to_table_widget(self, operation, class_name, subject, number_of_sessions, id, row_number=None):
        if operation == "Add":
            try:
                operations_buttons = DeleteUpdateButtonTermInitWidget(table_widget=self.tblTermSessions)
                # class_name, subject, number_of_sessions, id = self.add_sessions_database()
                current_row = self.tblTermSessions.rowCount()
                self.tblTermSessions.insertRow(current_row)
                self.tblTermSessions.setItem(current_row, 0, QTableWidgetItem(str(id)))
                self.tblTermSessions.setItem(current_row, 1, QTableWidgetItem(class_name))
                self.tblTermSessions.setItem(current_row, 2, QTableWidgetItem(subject))
                self.tblTermSessions.setItem(current_row, 3, QTableWidgetItem(str(number_of_sessions)))
                self.tblTermSessions.setCellWidget(current_row, 4, operations_buttons)
                self.tblTermSessions.setColumnWidth(current_row, 40)
                self.tblTermSessions.setRowHeight(current_row, 150)
                Common.style_table_widget(self, self.tblTermSessions)
                QMessageBox.information(self, "نجاح", "تم الحفظ بنجاح")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")
        # elif operation == "Update":
        #     try:
        #         operations_buttons = DeleteUpdateButtonTermInitWidget(table_widget=self.tblTermSessions)
        #         current_row = int(row_number)
        #         # self.tblTermSessions.updateRow(int(row_number))
        #         self.tblTermSessions.setItem(current_row, 0, QTableWidgetItem(str(id)))
        #         self.tblTermSessions.setItem(current_row, 1, QTableWidgetItem(class_name))
        #         self.tblTermSessions.setItem(current_row, 2, QTableWidgetItem(subject))
        #         self.tblTermSessions.setItem(current_row, 3, QTableWidgetItem(str(number_of_sessions)))
        #         self.tblTermSessions.setCellWidget(current_row, 4, operations_buttons)
        #         self.tblTermSessions.setColumnWidth(current_row, 40)
        #         self.tblTermSessions.setRowHeight(current_row, 150)
        #         Common.style_table_widget(self, self.tblTermSessions)
        #         QMessageBox.information(self, "نجاح", "تم الحفظ بنجاح")
        #     except Exception as e:
        #         QMessageBox.critical(self, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")


class DeleteUpdateButtonTermInitWidget(QWidget):
    def __init__(self, table_widget=None, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        layout = QVBoxLayout()
        self.delete_ste = QPushButton("حــــذف")
        self.update_stu = QPushButton("تفاصيل")
        self.delete_ste.setFixedSize(110, 40)
        self.update_stu.setStyleSheet("color: white; background-color: blue; font: 12pt 'PT Bold Heading';")
        self.delete_ste.setStyleSheet("color: white; background-color: red;font:12pt 'PT Bold Heading';")
        self.update_stu.setFixedSize(110, 40)
        layout.addSpacing(3)
        layout.addWidget(self.update_stu)
        layout.addSpacing(3)
        layout.addWidget(self.delete_ste)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        self.state = False
        self.delete_ste.clicked.connect(self.on_delete_button_clicked)
        self.update_stu.clicked.connect(self.on_update_button_clicked)

    def on_delete_button_clicked(self):
        print("on_delete_button_clicked")
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                # Fetch the user with the selected ID from the database
                term_id = self.table_widget.item(row, 0)
                try:
                    term = TeacherSubjectClassRoomTermTable.get_by_id(int(term_id.text()))
                    reply = QMessageBox.question(self, "تأكيدالحذف", "هل أنت متأكد أنك تريد حذف هذا الطالب",
                                                 QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.table_widget.removeRow(row)
                        term.delete_instance()
                        QMessageBox.information(self, "نجاح", "تم الحذف بنجاح")
                        self.delete_ste.setStyleSheet(
                            "color: white; background-color: green;font:12pt 'PT Bold Heading';")

                except TeacherSubjectClassRoomTermTable.DoesNotExist:
                    print("Student does not exist.")

    def on_update_button_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                term_id = self.table_widget.item(row, 0)
                print("the member id is : ", term_id.text())
                class_name = self.table_widget.item(row, 1)
                subject_name = self.table_widget.item(row, 2)
                number_of_sessions = self.table_widget.item(row, 3)
                if term_id and class_name and subject_name and number_of_sessions:
                    term_update = TermSessionsInitUpdate()
                    term_update.comboClasses.setCurrentText(class_name.text())
                    term_update.comboSubjects.setCurrentText(subject_name.text())
                    term_update.txtNumberOfSessions.setPlainText(number_of_sessions.text())
                    term_update.lblTermId.setText(str(term_id.text()))
                    if term_update.exec_() == QDialog.Accepted:
                        class_name = term_update.comboClasses.currentText()
                        subject_name = term_update.comboSubjects.currentText()
                        number_of_sessions = term_update.txtNumberOfSessions.toPlainText()
                        term_id = term_update.lblTermId.text()
                        class_id = ClassRoom.get_class_id_from_name(self, class_name)
                        term = TeacherSubjectClassRoomTermTable.get_by_id(term_id)
                        term.class_room_id = class_id
                        term.subject_id = subject_name
                        term.number_of_lessons = number_of_sessions
                        term.save()
                        self.table_widget.setItem(row, 0, QTableWidgetItem(term_id))
                        self.table_widget.setItem(row, 1, QTableWidgetItem(class_name))
                        self.table_widget.setItem(row, 2, QTableWidgetItem(subject_name))
                        self.table_widget.setItem(row, 3, QTableWidgetItem(number_of_sessions))
                        Common.style_table_widget(self, self.table_widget)
                        # self.table_widget.setColumnHidden(0, True)
                        QMessageBox.information(self, "نجاح", "تم التعديل بنجاح")
                    # term_update = TermSessionsInitUpdate()
                    # term_update.use_ui_elements()

                    # term_update.exec_()
                else:
                    QMessageBox.critical(self, "خطأ", " يجب تحديد البيانات المطلوبة")


class TermSessionsInitUpdate(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("TermSessionsInitUpdate.ui", self)
        self.get_classes()
        self.get_subject()
        self.updated_term_id = 0
        self.btnSaveTermSessionsUpdate.clicked.connect(self.save_data)
        self.btnCancelUpdateSession.clicked.connect(self.reject)


    def save_data(self):
        class_name = self.comboClasses.currentText()
        subject_name = self.comboSubjects.currentText()
        number_of_sessions = self.txtNumberOfSessions.toPlainText()
        row_number = self.lblRowNumber.text()
        term_id = self.lblTermId.text()
        self.accept()
        return row_number, term_id, class_name, subject_name, number_of_sessions

    # def update_table_widget(self):
    #     save_data = self.save_data()
    #     if save_data:
    #         row_number = save_data[0]
    #         term_id = save_data[1]
    #         class_name = save_data[2]
    #         subject_name = save_data[3]
    #         number_of_sessions = save_data[4]
    #         term = TermSessionsInit()
    #         term.add_new_sessions_to_table_widget("Update", class_name, subject_name, number_of_sessions, term_id,
    #                                               row_number)
    #         # current_row = self.tblTermSessions.rowCount()
    #         # self.tblTermSessions.updateRow(current_row)
    #         # self.tblTermSessions.setItem(row_number, 0, QTableWidgetItem(str(term_id)))
    #         # self.tblTermSessions.setItem(row_number, 1, QTableWidgetItem(class_name))
    #         # self.tblTermSessions.setItem(row_number, 2, QTableWidgetItem(subject_name))
    #         # self.tblTermSessions.setItem(row_number, 3, QTableWidgetItem(str(number_of_sessions)))
    #         # self.tblTermSessions.setCellWidget(row_number, 4, operations_buttons)
    #         # self.tblTermSessions.setColumnWidth(row_number, 40)
    #         # self.tblTermSessions.setRowHeight(row_number, 150)
    #         # Common.style_table_widget(self, self.tblTermSessions)

    # def get_data_from_table_widget(self, row, term_id, class_name, subject_name, number_of_sessions):
    #     self.comboClasses.setCurrentText(class_name)
    #     self.comboSubjects.setCurrentText(subject_name)
    #     self.txtNumberOfSessions.setPlainText(number_of_sessions)
    #     self.lblTermId.setText(str(term_id))
    #     self.lblRowNumber.setText(str(row))

    def get_classes(self):
        self.comboClasses.clear()
        column_names = 'name'
        classes = Common.get_combo_box_data(self, ClassRoom, column_names)
        self.comboClasses.clear()
        self.comboClasses.addItems(classes)

    def get_subject(self):
        subjects = Common.get_subjects(self)
        self.comboSubjects.clear()
        self.comboSubjects.addItems(subjects)
