import peewee
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonTermInitWidget
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
        # self.btnSkippingTermSessions.clicked.connect(self.accept)

    def use_ui_elements(self):
        self.btnAddNewSession.clicked.connect(self.add_new_sessions_to_table_widget)
        # self.btnSaveTermSessions.clicked.connect(self.add_members_database)
        self.btnSkippingTermSessions.clicked.connect(self.accept)

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
            return class_name, subject, number_of_sessions, self.lastInsertedTermSession
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None

    def add_new_sessions_to_table_widget(self):
        try:
            class_name, subject, number_of_sessions, id = self.add_sessions_database()
            operations_buttons = DeleteUpdateButtonTermInitWidget(table_widget=self.tblTermSessions)
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
