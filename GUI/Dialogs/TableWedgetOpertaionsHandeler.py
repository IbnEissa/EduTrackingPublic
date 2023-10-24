import peewee
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QWidget, QVBoxLayout, QPushButton, QDialog, \
    QTableWidgetItem, QMessageBox, QStyle
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDate
from zk import ZK
from GUI.Views.CommonFunctionality import Common
from GUI.Dialogs.CouncilFathersDialog import CouncilFathersDialog
from GUI.Dialogs.DeviceDailog import MyDialog
from GUI.Dialogs.InitializingTheProject.DeviceInintDialog import DeviceInitDialog
from GUI.Dialogs.InitializingTheProject.SchoolDialog import SchoolDialog
from GUI.Dialogs.InitializingTheProject.classesDialog import ClassesDialog
from GUI.Dialogs.TeacherDialog import TeacherDialog
import logging
import codecs

from GUI.Dialogs.UserDialog import UserDialog
from GUI.Views.uihandler import UIHandler
from models.ClassRoom import ClassRoom
from models.CouncilFathers import CouncilFathers
from models.Device import Device
from models.Members import Members
from GUI.Dialogs.DeviceDailog import MyDialog
from GUI.Dialogs.TeacherDialog import TeacherDialog
from GUI.Dialogs.StudentDialog import StudentDialog
from models.Members import Members
from models.School import School
from models.Students import Students
from models.Users import Users
from models.term_table import TeacherSubjectClassRoomTermTable

lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()


class DeleteUpdateButtonInitClassRoomWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget

        layout = QVBoxLayout()

        self.update_classroom = QPushButton("تفاصيل")

        self.update_classroom.setStyleSheet("color: white; background-color: blue; font: 12pt 'PT Bold Heading';")
        self.update_classroom.setFixedSize(110, 40)
        layout.addSpacing(3)
        layout.addWidget(self.update_classroom)
        layout.addSpacing(3)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        self.update_classroom.clicked.connect(self.on_update_button_classroom_clicked)

    def on_update_button_classroom_clicked(self):

        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()

                # Fetch the school with the selected ID from the database
                classroom_id = self.table_widget.item(row, 0)
                print("the device id is : ", classroom_id.text())
                # Get the data from the selected row in the table_widget
                name = self.table_widget.item(row, 1)

                if classroom_id and name:
                    classroom_dialog = ClassesDialog()
                    classroom_dialog.labAddClassRoom.setVisible(False)
                    classroom_dialog.btnSaveClasses.setVisible(False)
                    classroom_dialog.btnSkipClasses.setVisible(False)
                    # classroom_dialog.btnAddClasses.setVisible(True)
                    # classroom_dialog.btnDeleteClasses.setVisible(True)
                    classroom_dialog.labAddClassRoom.setText(classroom_id.text())
                    classroom_dialog.txtClassName.setPlainText(name.text())
                    classroom_dialog.btnAddClasses.clicked.connect(
                        lambda: self.on_button_clicked(classroom_dialog, row))
                    classroom_dialog.btnDeleteClasses.clicked.connect(lambda: self.close_dialog(classroom_dialog))

                    if classroom_dialog.exec_() == QDialog.Accepted:
                        pass

    def on_button_clicked(self, classroom_dialog, row):

        name = classroom_dialog.txtClassName.toPlainText()
        self.table_widget.setItem(row, 1, QTableWidgetItem(name))
        classroom_id = classroom_dialog.labAddClassRoom.text()
        print(classroom_id)

        classroom = ClassRoom.get(ClassRoom.id == classroom_id)
        classroom.name = name
        classroom.save()

        QMessageBox.information(self, "نجاح", "تم التعديل بنجاح")
        classroom_dialog.close()

    def close_dialog(self, classroom_dialog):
        classroom_dialog.close()


class DeleteUpdateButtonInitDeviceWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget

        layout = QVBoxLayout()

        self.update_device = QPushButton("تفاصيل")
        self.update_device.setStyleSheet("color: white; background-color: blue; font: 12pt 'PT Bold Heading';")
        self.update_device.setFixedSize(110, 40)
        layout.addSpacing(3)
        layout.addWidget(self.update_device)
        layout.addSpacing(3)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        self.update_device.clicked.connect(self.on_update_button_device_clicked)

    def on_update_button_device_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()

                device_id = self.table_widget.item(row, 0)
                print("the device id is: ", device_id.text())

                name = self.table_widget.item(row, 1)
                ip = self.table_widget.item(row, 2)
                port = self.table_widget.item(row, 3)

                if device_id and name and ip and port:
                    device_dialog = DeviceInitDialog()
                    device_dialog.labAddDivece.setVisible(False)
                    device_dialog.btnSkippingDevice.setVisible(False)
                    device_dialog.btnSaveDevice.setVisible(False)
                    device_dialog.btnSaveInitDevice.setVisible(True)
                    device_dialog.btnCancelInitDevice.setVisible(True)

                    device_dialog.labAddDivece.setText(device_id.text())
                    device_dialog.txtDeviceName.setPlainText(name.text())
                    device_dialog.txtIPNumber.setPlainText(ip.text())
                    device_dialog.txtPortNumber.setPlainText(port.text())

                    device_dialog.btnSaveInitDevice.clicked.connect(lambda: self.on_button_clicked(device_dialog, row))
                    device_dialog.btnCancelInitDevice.clicked.connect(lambda: self.close_dialog(device_dialog))

                    if device_dialog.exec_() == QDialog.Accepted:
                        pass

    def on_button_clicked(self, device_dialog, row):

        name = device_dialog.txtDeviceName.toPlainText()
        ip = device_dialog.txtIPNumber.toPlainText()
        port = device_dialog.txtPortNumber.toPlainText()

        self.table_widget.setItem(row, 1, QTableWidgetItem(name))
        self.table_widget.setItem(row, 2, QTableWidgetItem(ip))
        self.table_widget.setItem(row, 3, QTableWidgetItem(port))

        device_id = device_dialog.labAddDivece.text()
        print(device_id)

        device = Device.get(Device.id == device_id)
        device.name = name
        device.ip = ip
        device.port = port

        device.save()

        QMessageBox.information(self, "نجاح", "تم التعديل بنجاح")
        device_dialog.close()

    def close_dialog(self, device_dialog):
        device_dialog.close()


class DeleteUpdateButtonSchoolWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        self.school_dialog = SchoolDialog()
        layout = QVBoxLayout()

        self.update_school = QPushButton("تفاصيل")
        self.update_school.setStyleSheet("color: white; background-color: blue; font: 12pt 'PT Bold Heading';")
        self.update_school.setFixedSize(110, 40)
        layout.addSpacing(3)
        layout.addWidget(self.update_school)
        layout.addSpacing(3)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        self.update_school.clicked.connect(self.on_update_button_school_clicked)

    def on_update_button_school_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()

                school_id = self.table_widget.item(row, 0)
                print("the school id is: ", school_id.text())

                school_name = self.table_widget.item(row, 1)
                city = self.table_widget.item(row, 2)
                directorate = self.table_widget.item(row, 3)
                print("the directorate is : ", directorate)
                print("the directorate is : ", city)
                village = self.table_widget.item(row, 4)
                academic_level = self.table_widget.item(row, 5)
                student_gender_type = self.table_widget.item(row, 6)

                if school_id and school_name and city and village and academic_level and directorate \
                        and student_gender_type:

                    school_dialog = SchoolDialog()
                    school_dialog.labAddSchool.setVisible(False)
                    school_dialog.btnSaveSchool.setVisible(False)
                    school_dialog.btnUpdateSchool.setVisible(True)
                    school_dialog.btnCancelSchool.setVisible(True)
                    school_dialog.labAddSchool.setText(school_id.text())
                    school_dialog.txtSchoolName.setPlainText(school_name.text())
                    school_dialog.comboCity.setCurrentText(city.text())
                    school_dialog.combDirectorates.setCurrentText(directorate.text())
                    school_dialog.comboCity.currentIndexChanged.connect(school_dialog.on_city_select)
                    # school_dialog.combDirectorates.currentIndexChanged.connect(school_dialog.on_city_select)
                    # school_dialog.txtVillage.setPlainText(village.text())
                    school_dialog.comboAcademicLevel.setCurrentText(academic_level.text())
                    school_dialog.comboGenderType.setCurrentText(student_gender_type.text())
                    school_dialog.btnUpdateSchool.clicked.connect(lambda: self.on_button_clicked(school_dialog, row))
                    school_dialog.btnCancelSchool.clicked.connect(lambda: self.close_dialog(school_dialog))

                    if school_dialog.exec_() == QDialog.Accepted:
                        pass

    def on_button_clicked(self, school_dialog, row):

        school_name = school_dialog.txtSchoolName.toPlainText()
        city = school_dialog.comboCity.currentText()
        directorate = school_dialog.combDirectorates.currentText()
        village = school_dialog.txtVillage.toPlainText()
        academic_level = school_dialog.comboAcademicLevel.currentText()
        student_gender_type = school_dialog.comboGenderType.currentText()

        self.table_widget.setItem(row, 1, QTableWidgetItem(school_name))
        self.table_widget.setItem(row, 2, QTableWidgetItem(city))
        self.table_widget.setItem(row, 3, QTableWidgetItem(directorate))
        self.table_widget.setItem(row, 4, QTableWidgetItem(village))
        self.table_widget.setItem(row, 5, QTableWidgetItem(academic_level))
        self.table_widget.setItem(row, 6, QTableWidgetItem(student_gender_type))

        school_id = school_dialog.labAddSchool.text()
        school = School.get(School.id == school_id)
        school.school_name = school_name
        school.city = city
        school.directorate = directorate
        school.village = village
        school.academic_level = academic_level
        school.student_gender_type = student_gender_type

        school.save()

        QMessageBox.information(self, "نجاح", "تم التعديل بنجاح")
        school_dialog.close()

    def close_dialog(self, school_dialog):
        school_dialog.close()


class DeleteUpdateButtonStudentsWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        layout = QVBoxLayout()
        self.delete_ste = QPushButton("حــــذف")
        self.update_stu = QPushButton("تعــديل")
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

        self.delete_ste.clicked.connect(self.on_delete_button_clicked)
        self.update_stu.clicked.connect(self.on_update_button_clicked)

    def on_delete_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_delete_student")
        if result_condition is True:
            print("on_delete_button_clicked")
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    # Fetch the user with the selected ID from the database
                    member_id = self.table_widget.item(row, 0)
                    student_dialog = StudentDialog()
                    student_dialog.labAddStudent.setText(member_id.text())
                    member_id = student_dialog.labAddStudent.text()
                    try:
                        member = Members.get_by_id(member_id)
                        reply = QMessageBox.question(self, "تأكيدالحذف", "هل أنت متأكد أنك تريد حذف هذا الطالب",
                                                     QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            self.table_widget.removeRow(row)
                            member.delete_instance()
                            QMessageBox.information(self, "نجاح", "تم الحذف بنجاح")
                    except Members.DoesNotExist:
                        print("Student does not exist.")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    def on_update_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_update_student")
        if result_condition is True:

            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()

                    # Fetch the user with the selected ID from the database
                    member_id = self.table_widget.item(row, 0)
                    print("the member id is : ", member_id.text())
                    # Get the data from the selected row in the table_widget
                    fname_stu = self.table_widget.item(row, 1)
                    secname_stu = self.table_widget.item(row, 2)
                    thirname_stu = self.table_widget.item(row, 3)
                    lname_stu = self.table_widget.item(row, 4)
                    class_stu = self.table_widget.item(row, 5)
                    birth_stu = self.table_widget.item(row, 6)
                    par_phone = self.table_widget.item(row, 7)

                    if member_id and fname_stu and secname_stu and thirname_stu and lname_stu and class_stu and birth_stu and par_phone:

                        date = QDate.fromString(birth_stu.text(), "yyyy-MM-dd")
                        student_dialog = StudentDialog()
                        student_dialog.labAddStudent.setVisible(False)
                        student_dialog.labAddStudent.setText(member_id.text())
                        student_dialog.txtStudentFName.setPlainText(fname_stu.text())
                        student_dialog.txtStudentSecName.setPlainText(secname_stu.text())
                        student_dialog.txtStudentThirName.setPlainText(thirname_stu.text())
                        student_dialog.txtStudentLName.setPlainText(lname_stu.text())
                        student_dialog.combClasses.setCurrentText(class_stu.text())
                        student_dialog.dateStudentDOB.setDate(date)
                        student_dialog.txtStudentParentPhone.setPlainText(par_phone.text())
                        if student_dialog.exec_() == QDialog.Accepted:
                            FName, SName, TName, LName, ClassId, Birth, Phone, ClassName = student_dialog.save_data()
                            print("the member id is : ", member_id.text())
                            m = Members.get_members_by_id(self, member_id.text())
                            m.school_id = lastInsertedSchoolId
                            m.fName = FName
                            m.sName = SName
                            m.tName = TName
                            m.lName = LName
                            m.phone = Phone
                            m.dateBerth = Birth
                            m.save()

                            student = Students.get(Students.member_id == m.id)
                            student.class_id = ClassId
                            student.save()
                            self.table_widget.setItem(row, 0, QTableWidgetItem(member_id.text()))
                            self.table_widget.setItem(row, 1, QTableWidgetItem(FName))
                            self.table_widget.setItem(row, 2, QTableWidgetItem(SName))
                            self.table_widget.setItem(row, 3, QTableWidgetItem(TName))
                            self.table_widget.setItem(row, 4, QTableWidgetItem(LName))
                            self.table_widget.setItem(row, 5, QTableWidgetItem(ClassName))
                            self.table_widget.setItem(row, 6, QTableWidgetItem(str(Birth)))
                            self.table_widget.setItem(row, 7, QTableWidgetItem(Phone))
                            self.table_widget.setColumnHidden(0, True)
                            QMessageBox.information(self, "نجاح", "تم التعديل بنجاح")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")


class DeleteUpdateButtonUsersWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        layout = QVBoxLayout()
        self.delete_user = QPushButton("حــــذف")
        self.update_user = QPushButton("تعــديل")
        self.delete_user.setFixedSize(110, 40)
        self.update_user.setStyleSheet("color: white; background-color: blue; font: 12pt 'PT Bold Heading';")
        self.delete_user.setStyleSheet("color: white; background-color: red;font:12pt 'PT Bold Heading';")
        self.update_user.setFixedSize(110, 40)
        layout.addSpacing(3)
        layout.addWidget(self.update_user)
        layout.addSpacing(3)
        layout.addWidget(self.delete_user)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        self.delete_user.clicked.connect(self.on_delete_button_user_clicked)
        self.update_user.clicked.connect(self.on_update_button_user_clicked)

    def on_delete_button_user_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_delete_user")
        if result_condition is True:
            print("on_delete_button_clicked")
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    # Fetch the user with the selected ID from the database
                    member_id = self.table_widget.item(row, 0)
                    user_dialog = UserDialog()
                    user_dialog.labAddUsers.setText(member_id.text())
                    member_id = user_dialog.labAddUsers.text()
                    self.table_widget.removeRow(row)

                    try:
                        idUser = Members.get_by_id(member_id)

                        # Show confirmation message box
                        reply = QMessageBox.question(self, "تأكيدالحذف", "هل أنت متأكد أنك تريد حذف هذا الطالب",
                                                     QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            print(idUser)
                            idUser.delete_instance()
                            QMessageBox.information(self, "نجاح", "تم الحذف بنجاح")

                    except Members.DoesNotExist:
                        print("Student does not exist.")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    def on_update_button_user_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_update_user")
        if result_condition is True:
            schoolID = 1
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()

                    # Fetch the user with the selected ID from the database
                    member_id = self.table_widget.item(row, 0)
                    # Get the data from the selected row in the table_widget
                    Name = self.table_widget.item(row, 1)
                    userName = self.table_widget.item(row, 2)
                    userPassword = self.table_widget.item(row, 3)
                    accountType = self.table_widget.item(row, 4)

                    if member_id and Name and userName and userPassword and accountType:

                        user_dialog = UserDialog()
                        user_dialog.labAddUsers.setVisible(False)
                        user_dialog.labAddUsers.setText(member_id.text())
                        user_dialog.txtName.setPlainText(Name.text())
                        user_dialog.txtUserName.setPlainText(userName.text())
                        user_dialog.txtPasswordUser.setPlainText(userPassword.text())
                        user_dialog.combAccountType.setEditText(accountType.text())

                        if user_dialog.exec_() == QDialog.Accepted:
                            Name = user_dialog.txtName.toPlainText()
                            userName = user_dialog.txtUserName.toPlainText()
                            userPassword = user_dialog.txtPasswordUser.toPlainText()
                            accountType = user_dialog.combAccountType.currentText()

                            # Update the row in the table_widget with the new data
                            self.table_widget.setItem(row, 1, QTableWidgetItem(Name))
                            self.table_widget.setItem(row, 2, QTableWidgetItem(userName))
                            self.table_widget.setItem(row, 3, QTableWidgetItem(userPassword))
                            self.table_widget.setItem(row, 4, QTableWidgetItem(accountType))

                            # Fetch the user with the selected ID from the database
                            member_id = user_dialog.labAddUsers.text()
                            print(member_id)
                            # التحقق مما إذا كان العضو موجودًا بالفعل
                            existing_member = Members.select().where(
                                (Members.fName == Name)

                            ).first()
                            if existing_member:
                                # العضو موجود بالفعل، يمكنك التعامل مع حالة التكرار هنا
                                QMessageBox.critical(self, "خطأ", "العضو موجودًا بالفعل: ")
                                print("العضو موجود بالفعل!")
                                return

                                # العضو غير موجود، قم بإجراء الإدخال
                            else:

                                # Update the Members table
                                member = Members.get_by_id(member_id)
                                member.school_id = schoolID
                                member.fName = Name
                                member.accountType = accountType
                                member.save()

                                # Update the Students table
                                user = Users.get(Users.members_id == member_id)
                                user.userName = userName
                                user.userPassword = userPassword
                                user.save()

                                QMessageBox.information(self, "نجاح", "تم التعديل بنجاح")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")


class DeleteUpdateButtonCouncilFathersWidget(QWidget):
    def __init__(self, table_widget=None, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        self.layout = QVBoxLayout()

        self.delete_button = QPushButton("حــــذف")
        self.update_button = QPushButton("تفـاصيل")
        self.delete_button.setFixedSize(110, 40)
        self.update_button.setStyleSheet("color: white; background-color: blue; font: 12pt 'PT Bold Heading';")
        self.delete_button.setStyleSheet("color: white; background-color: red;font:12pt 'PT Bold Heading';")
        self.update_button.setFixedSize(110, 40)
        self.update_button.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton))

        self.layout.addSpacing(3)
        self.layout.addWidget(self.update_button)
        self.layout.addSpacing(3)
        self.layout.addWidget(self.delete_button)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)
        self.delete_button.clicked.connect(self.on_delete_button_clicked)
        self.update_button.clicked.connect(self.on_update_button_clicked)

    def on_delete_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_delete_fathers")
        if result_condition is True:
            print("on_delete")
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    try:
                        member = Members.get_by_id(member_id)
                        reply = QMessageBox.question(self, "تأكيدالحذف", "هل أنت متأكد أنك تريد حذف هذا الطالب",
                                                     QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            self.table_widget.removeRow(row)
                            member.delete_instance()
                            QMessageBox.information(self, "نجاح", "تم الحذف بنجاح")
                    except Members.DoesNotExist:
                        print("Student does not exist.")

                    self.table_widget.removeRow(row)
                    Members.delete()
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    def on_update_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_update_fathers")
        if result_condition is True:
            print("the update button is clicked")
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    member_id = self.table_widget.item(row, 0)
                    council_fathers_fname = self.table_widget.item(row, 1)
                    council_fathers_sname = self.table_widget.item(row, 2)
                    council_fathers_tname = self.table_widget.item(row, 3)
                    council_fathers_lname = self.table_widget.item(row, 4)
                    council_fathers_phone = self.table_widget.item(row, 5)
                    council_fathers__DOB = self.table_widget.item(row, 6)
                    council_fathers__occupation = self.table_widget.item(row, 7)

                    if council_fathers_fname and council_fathers_sname and council_fathers_tname and council_fathers_lname and council_fathers_phone and council_fathers__DOB and council_fathers__occupation:
                        date = QDate.fromString(council_fathers__DOB.text(), "yyyy-MM-dd")
                        council_fathers_dialog = CouncilFathersDialog()
                        council_fathers_dialog.txtCouncilFathersName.setPlainText(council_fathers_fname.text())
                        council_fathers_dialog.txtCouncilSecName.setPlainText(council_fathers_sname.text())
                        council_fathers_dialog.txtCouncilThirName.setPlainText(council_fathers_tname.text())
                        council_fathers_dialog.txtCouncilLName.setPlainText(council_fathers_lname.text())
                        council_fathers_dialog.txtCouncilPhone.setPlainText(council_fathers_phone.text())
                        council_fathers_dialog.dateCouncilDOB.setDate(date)
                        council_fathers_dialog.txtCouncilTask.setPlainText(council_fathers__occupation.text())

                        if council_fathers_dialog.exec_() == QDialog.Accepted:
                            fname = council_fathers_dialog.txtCouncilFathersName.toPlainText()
                            sname = council_fathers_dialog.txtCouncilSecName.toPlainText()
                            tname = council_fathers_dialog.txtCouncilThirName.toPlainText()
                            lname = council_fathers_dialog.txtCouncilLName.toPlainText()
                            phone = council_fathers_dialog.txtCouncilPhone.toPlainText()
                            DOB = council_fathers_dialog.dateCouncilDOB.date().toPyDate()
                            occupation = council_fathers_dialog.txtCouncilTask.toPlainText()

                            # Update the row in the table_widget with the new data
                            self.table_widget.setItem(row, 1, QTableWidgetItem(fname))
                            self.table_widget.setItem(row, 2, QTableWidgetItem(sname))
                            self.table_widget.setItem(row, 3, QTableWidgetItem(tname))
                            self.table_widget.setItem(row, 4, QTableWidgetItem(lname))
                            self.table_widget.setItem(row, 5, QTableWidgetItem(phone))
                            self.table_widget.setItem(row, 6, QTableWidgetItem(str(DOB)))
                            self.table_widget.setItem(row, 7, QTableWidgetItem(occupation))

                            member = Members.get_by_id(member_id)
                            member.school_id = lastInsertedSchoolId
                            member.fName = fname
                            member.sName = sname
                            member.tName = tname
                            member.lName = lname
                            member.phone = phone
                            member.dateBerth = DOB
                            member.save()

                            # Update the Students table
                            Council = CouncilFathers.get(Students.member_id == member_id)
                            Council.CouncilFathersTask = occupation
                            Council.save()
                            QMessageBox.information(self, "تعديل", "تم التعديل  بنجاح.")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")


class DeleteUpdateButtonDeviceWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        # self.submain = submain_instance
        # self.ui = self.submain.ui
        self.table_widget = table_widget
        # self.zk = ZK()
        layout = QVBoxLayout()

        self.delete_button = QPushButton("حــــذف")
        self.update_button = QPushButton("تعــديل")
        self.connect_button = QPushButton("إتصــــال")
        self.connect_button.setStyleSheet("color: white; background-color: green;font: 12pt 'PT Bold Heading';")
        self.delete_button.setFixedSize(110, 40)
        self.connect_button.setFixedSize(110, 40)
        self.update_button.setStyleSheet("color: white; background-color: blue; font: 12pt 'PT Bold Heading';")
        self.delete_button.setStyleSheet("color: white; background-color: red;font:12pt 'PT Bold Heading';")
        self.update_button.setFixedSize(110, 40)

        layout.addSpacing(3)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.update_button)
        layout.addSpacing(3)
        layout.addWidget(self.delete_button)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        self.delete_button.clicked.connect(self.on_delete_button_clicked)
        self.update_button.clicked.connect(self.on_update_button_clicked)

    def on_delete_button_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                self.table_widget.removeRow(row)

    def on_update_button_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                # Get the data from the selected row in the table_widget
                ip_address_item = self.table_widget.item(row, 1)
                port_number_item = self.table_widget.item(row, 2)

                if ip_address_item and port_number_item:
                    ip_address = ip_address_item.text()
                    port_number = port_number_item.text()
                    device_dialog = MyDialog()
                    device_dialog.txtIPAddress.setPlainText(ip_address)
                    device_dialog.txtPortNumber.setPlainText(port_number)

                    if device_dialog.exec_() == QDialog.Accepted:
                        ip_address = device_dialog.txtIPAddress.toPlainText()
                        port_number = device_dialog.txtPortNumber.toPlainText()

                        # Update the row in the table_widget with the new data
                        self.table_widget.setItem(row, 1, QTableWidgetItem(ip_address))
                        self.table_widget.setItem(row, 2, QTableWidgetItem(port_number))


class DeleteUpdateButtonTeachersWidget(QWidget):
    def __init__(self, table_widget=None, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()

        self.delete_button = QPushButton("حــــذف")
        self.update_button = QPushButton("تفـاصيل")
        self.fingerprint_button = QPushButton("إضافة للجهاز")
        self.delete_button.setFixedSize(110, 40)
        self.fingerprint_button.setFixedSize(110, 40)
        self.update_button.setStyleSheet("color: white; background-color: blue; font: 12pt 'PT Bold Heading';")
        self.fingerprint_button.setStyleSheet("color: white; background-color: green; font: 12pt 'PT Bold Heading';")
        self.delete_button.setStyleSheet("color: white; background-color: red;font:12pt 'PT Bold Heading';")
        self.update_button.setFixedSize(110, 40)
        self.update_button.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton))

        self.layout2.addSpacing(3)
        self.layout2.addWidget(self.update_button)
        self.layout2.addSpacing(3)
        self.layout2.addWidget(self.delete_button)
        self.layout2.setAlignment(Qt.AlignCenter)

        self.layout1.addSpacing(3)
        self.layout1.addWidget(self.fingerprint_button)
        self.layout1.addWidget(self.update_button)
        self.layout1.addSpacing(3)
        self.layout1.addWidget(self.delete_button)
        # self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout1.setAlignment(Qt.AlignCenter)

        self.delete_button.clicked.connect(self.on_delete_button_clicked)
        self.update_button.clicked.connect(self.on_update_button_clicked)
        # self.fingerprint_button.clicked.connect(self.add_users_to_device)

    def on_delete_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_delete_teacher")
        if result_condition is True:
            print("on_delete_button_clicked")
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    self.table_widget.removeRow(row)
                    Members.delete()
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    def get_buttons(self, operation):
        if operation == 'New':
            self.setLayout(self.layout1)
        elif operation == 'Old':
            self.setLayout(self.layout2)

        return self

    def on_update_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_update_teacher")
        if result_condition is True:
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    # Get the data from the selected row in the table_widget
                    fname = self.table_widget.item(row, 1)
                    sname = self.table_widget.item(row, 2)
                    tname = self.table_widget.item(row, 3)
                    lname = self.table_widget.item(row, 4)
                    teacher_phone = self.table_widget.item(row, 5)
                    teacher_DOB = self.table_widget.item(row, 6)
                    teacher_major = self.table_widget.item(row, 7)
                    teacher_occupation = self.table_widget.item(row, 8)
                    teacher_state = self.table_widget.item(row, 9)

                    if fname and sname and tname and lname and teacher_phone and teacher_DOB and teacher_major and teacher_occupation and teacher_state:
                        date = QDate.fromString(teacher_DOB.text(), "yyyy-MM-dd")
                        teacher_dialog = TeacherDialog()
                        teacher_dialog.txtTeacherFName.setPlainText(fname.text())
                        teacher_dialog.txtTeacherSecName.setPlainText(sname.text())
                        teacher_dialog.txtTeacherThirName.setPlainText(tname.text())
                        teacher_dialog.txtTeacherLName.setPlainText(lname.text())
                        teacher_dialog.txtTeacherPhone.setPlainText(teacher_phone.text())
                        teacher_dialog.dateTeacherDOB.setDate(date)
                        teacher_dialog.txtTeacherMajor.setPlainText(teacher_major.text())
                        teacher_dialog.txtTeacherTask.setPlainText(teacher_occupation.text())

                        if teacher_dialog.exec_() == QDialog.Accepted:
                            fname = teacher_dialog.txtTeacherFName.toPlainText()
                            sname = teacher_dialog.txtTeacherSecName.toPlainText()
                            tname = teacher_dialog.txtTeacherThirName.toPlainText()
                            lname = teacher_dialog.txtTeacherLName.toPlainText()
                            phone = teacher_dialog.txtTeacherPhone.toPlainText()
                            DOB = teacher_dialog.dateTeacherDOB.date().toPyDate()
                            major = teacher_dialog.txtTeacherMajor.toPlainText()
                            occupation = teacher_dialog.txtTeacherTask.toPlainText()

                            # Update the row in the table_widget with the new data
                            self.table_widget.setItem(row, 1, QTableWidgetItem(fname))
                            self.table_widget.setItem(row, 2, QTableWidgetItem(sname))
                            self.table_widget.setItem(row, 3, QTableWidgetItem(tname))
                            self.table_widget.setItem(row, 4, QTableWidgetItem(lname))
                            self.table_widget.setItem(row, 5, QTableWidgetItem(phone))
                            self.table_widget.setItem(row, 6, QTableWidgetItem(str(DOB)))
                            self.table_widget.setItem(row, 7, QTableWidgetItem(major))
                            self.table_widget.setItem(row, 8, QTableWidgetItem(occupation))
                            QMessageBox.information(self, "تعديل", "تم التعديل  بنجاح.")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    def add_users_to_device(self, teacher_id):
        try:
            self.last_inserted_device = Device.select(peewee.fn.Max(Device.id)).scalar()
            device = Device.get(Device.id == self.last_inserted_device)
            zk = ZK(device.ip, port=device.port, timeout=5)
            # uid = []
            # users_id = []
            conn = zk.connect()
            conn.set_user(uid=int(teacher_id), user_id=str(teacher_id), privilege=0)
            # users = conn.get_users()
            # for user in users:
            #     uid.append(user.uid)
            # for user in users:
            #     users_id.append(user.user_id)
            # return users_id, uid
        except Exception as e:
            QMessageBox.warning(self, "تحذير", "لا يوجد جهاز بصمة متصل الآن")

    def start_enroll_face(sIp="192.168.1.201", iPort=4370, iMachineNumber=1, userid="", fingureindex=0):
        zk = ZK('192.168.1.201', port=4370, timeout=5)
        conn = None
        try:
            conn = zk.connect()
            if conn:
                conn.disable_device()
                user_id = str(userid)
                finger_index = int(fingureindex)

                # Clear the existing face template for the user
                conn.delete_user_face(iMachineNumber, user_id, finger_index)

                # Start the face enrollment process
                if conn.start_enroll_ex(user_id, finger_index, 1):  # 1 represents the face biometric type
                    logging.info(f"Start to enroll a new user, UserID={user_id}, Face ID={finger_index}, Flag=1")
                    conn.start_identify()  # Let the device enter 1:N verification condition after enrolling templates
                    conn.refresh_data(1)  # Refresh the data in the device
                    start_enroll_result = True
                else:
                    logging.error("Failed to start enrollment.")
                    start_enroll_result = False

                conn.enable_device()
                return start_enroll_result
            else:
                logging.error("Failed to establish connection to the device.")
                return False
        except Exception as e:
            logging.error("An error occurred during face enrollment.", exc_info=True)
            return False
        finally:
            if conn:
                conn.disconnect()
