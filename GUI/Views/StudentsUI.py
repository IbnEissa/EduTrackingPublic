import peewee
from PyQt5.QtCore import QDate, Qt

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout

from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonStudentsWidget
from GUI.Dialogs.StudentDialog import StudentDialog
from models.Members import Members
from models.Students import Students


class StudentsUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ips = ''
        self.ports = ''
        self.lastInsertedMemberId = 0
        self.lastInsertedStudentId = 0
        # self.ui.tblStudents.setColumnHidden(0, True)
        # self.ui.tblStudents.setColumnHidden(8, True)

    def use_ui_elements(self):
        self.ui.tblStudents.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblStudents.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblStudents.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnAddNewStudent.clicked.connect(self.add_new_student)
        self.ui.txtStudentsSearch.textChanged.connect(self.get_member_data)

    def addMembersDataBase(self):
        if self.ui.tblStudents.rowCount() > 0:
            schoolID = 1  # قم بتعديل هذا السطر إذا كان لديك معرف مدرسة محدد
            last_row_index = self.ui.tblStudents.rowCount() - 1
            fname = self.ui.tblStudents.item(last_row_index, 1).text()
            sname = self.ui.tblStudents.item(last_row_index, 2).text()
            tname = self.ui.tblStudents.item(last_row_index, 3).text()
            lname = self.ui.tblStudents.item(last_row_index, 4).text()
            classname = self.ui.tblStudents.item(last_row_index, 5).text()
            dateBerth = self.ui.tblStudents.item(last_row_index, 6).text()
            parentPhone = self.ui.tblStudents.item(last_row_index, 7).text()

            # التحقق مما إذا كان العضو موجودًا بالفعل
            existing_member = Members.select().where(
                (Members.fName == fname) &
                (Members.sName == sname) &
                (Members.tName == tname) &
                (Members.lName == lname)
            ).first()
            if existing_member:
                # العضو موجود بالفعل، يمكنك التعامل مع حالة التكرار هنا
                QMessageBox.critical(self.ui, "خطأ", "العضو موجودًا بالفعل: ")
                print("العضو موجود بالفعل!")
                return

                # العضو غير موجود، قم بإجراء الإدخال
            else:
                try:
                    Members.insert({
                        Members.school_id: schoolID,
                        Members.fName: fname,
                        Members.sName: sname,
                        Members.tName: tname,
                        Members.lName: lname,
                        Members.phone: parentPhone,
                        Members.dateBerth: dateBerth,
                    }).execute()
                    self.lastInsertedMemberId = Members.select(peewee.fn.Max(Members.id)).scalar()
                    Students.insert({
                        Students.member_id: self.lastInsertedMemberId,
                        Students.class_id: classname,
                    }).execute()
                    self.lastInsertedStudentId = Students.select(peewee.fn.Max(Students.id)).scalar()

                    print("the id inserted m is : ", self.lastInsertedMemberId)
                    print("the id inserted S is : ", self.lastInsertedStudentId)
                    QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")
                except ValueError as e:
                    QMessageBox.critical(self.ui, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")

    def add_new_student(self):
        print("the add clicked")
        self.ui.tblStudents.setColumnHidden(8, True)
        self.ui.tblStudents.setColumnHidden(0, True)
        self.ui.tblStudents.setRowCount(0)
        student_dialog = StudentDialog()
        if student_dialog.exec_() == QDialog.Accepted:
            try:
                operationsButtons = DeleteUpdateButtonStudentsWidget(table_widget=self.ui.tblStudents)
                FName, SName, TName, LName, Classname, Birth, Phone = student_dialog.save_data()  # Call save_data() on mydialog instance
                current_row = self.ui.tblTeachers.rowCount()  # Get the current row index
                self.ui.tblStudents.insertRow(current_row)  # Insert a new row at the current row index
                self.ui.tblStudents.setItem(current_row, 1, QTableWidgetItem(FName))
                self.ui.tblStudents.setItem(current_row, 2, QTableWidgetItem(SName))
                self.ui.tblStudents.setItem(current_row, 3, QTableWidgetItem(TName))
                self.ui.tblStudents.setItem(current_row, 4, QTableWidgetItem(LName))
                self.ui.tblStudents.setItem(current_row, 5, QTableWidgetItem(str(Classname)))
                self.ui.tblStudents.setItem(current_row, 6, QTableWidgetItem(str(Birth)))
                self.ui.tblStudents.setItem(current_row, 7, QTableWidgetItem(Phone))
                self.ui.tblStudents.setCellWidget(current_row, 8, operationsButtons)

                self.ui.tblStudents.setColumnWidth(current_row, 40)
                self.ui.tblStudents.setRowHeight(current_row, 150)

                self.addMembersDataBase()

            except Exception as e:
                error_message = "حدث خطأ:\n\n" + str(e)
                QMessageBox.critical(self.ui, "خطأ", error_message)

    def get_member_data(self):
        self.ui.tblStudents.setColumnHidden(8, False)

        try:
            columns = ['id', 'fName', 'sName', 'tName', 'lName', 'class_id', 'dateBerth', 'phone']
            # search_item = self.ui.txtTeachersSearch.lower()
            search_item = self.ui.txtStudentsSearch.toPlainText().lower()
            members_query = Members.select().join(Students).where(
                peewee.fn.LOWER(Members.fName).contains(search_item)).distinct()

            self.ui.tblStudents.setRowCount(0)  # Clear existing rows in the table
            for row, member_data in enumerate(members_query):
                table_items = []
                for column_name in columns:
                    try:
                        item_value = getattr(member_data, column_name)
                    except AttributeError:
                        Student_data = Students.get(Students.member_id == member_data.id)
                        item_value = getattr(Student_data, column_name)

                    table_item = QTableWidgetItem(str(item_value))
                    table_items.append(table_item)

                self.ui.tblStudents.insertRow(row)
                for col, item in enumerate(table_items):
                    self.ui.tblStudents.setItem(row, col, item)

                self.ui.tblStudents.setColumnWidth(row, 40)
                self.ui.tblStudents.setRowHeight(row, 150)

                operations_buttons = DeleteUpdateButtonStudentsWidget(table_widget=self.ui.tblStudents)
                self.ui.tblStudents.setCellWidget(row, 8, operations_buttons)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)
