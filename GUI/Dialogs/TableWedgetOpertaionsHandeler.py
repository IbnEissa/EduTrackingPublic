
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QWidget, QVBoxLayout, QPushButton, QDialog, \
    QTableWidgetItem, QMessageBox, QStyle
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDate
from zk import ZK

from GUI.Dialogs.DeviceDailog import MyDialog
from GUI.Dialogs.TeacherDialog import TeacherDialog
import logging
import codecs

from GUI.Dialogs.UserDialog import UserDialog
from GUI.Views.uihandler import UIHandler
from models.Members import Members
from GUI.Dialogs.DeviceDailog import MyDialog
from GUI.Dialogs.TeacherDialog import TeacherDialog
from GUI.Dialogs.StudentDialog import StudentDialog
from models.Members import Members
from models.Students import Students
from models.Users import Users


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
                print(member_id)

                try:
                    member = Members.get_by_id(member_id)

                    # Show confirmation message box
                    reply = QMessageBox.question(self, "تأكيدالحذف", "هل أنت متأكد أنك تريد حذف هذا الطالب",
                                                 QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.table_widget.removeRow(row)
                        member.delete_instance()
                        QMessageBox.information(self, "نجاح", "تم الحذف بنجاح")
                except Members.DoesNotExist:
                    print("Student does not exist.")

    def on_update_button_clicked(self):
        self.table_widget.setColumnHidden(0, True)
        schoolID = 1
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()

                # Fetch the user with the selected ID from the database
                member_id = self.table_widget.item(row, 0)
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
                        fname = student_dialog.txtStudentFName.toPlainText()
                        sname = student_dialog.txtStudentSecName.toPlainText()
                        thirname = student_dialog.txtStudentThirName.toPlainText()
                        lname = student_dialog.txtStudentLName.toPlainText()
                        stuClass = student_dialog.combClasses.currentText()
                        birth = student_dialog.dateStudentDOB.date().toPyDate()
                        phoneStu = student_dialog.txtStudentParentPhone.toPlainText()

                        # Update the row in the table_widget with the new data
                        self.table_widget.setItem(row, 1, QTableWidgetItem(fname))
                        self.table_widget.setItem(row, 2, QTableWidgetItem(sname))
                        self.table_widget.setItem(row, 3, QTableWidgetItem(thirname))
                        self.table_widget.setItem(row, 4, QTableWidgetItem(lname))
                        self.table_widget.setItem(row, 5, QTableWidgetItem(stuClass))
                        self.table_widget.setItem(row, 6, QTableWidgetItem(str(birth)))
                        self.table_widget.setItem(row, 7, QTableWidgetItem(phoneStu))

                        # Fetch the user with the selected ID from the database
                        member_id = student_dialog.labAddStudent.text()
                        print(member_id)
                        # التحقق مما إذا كان العضو موجودًا بالفعل
                        existing_member = Members.select().where(
                            (Members.fName == fname) &
                            (Members.sName == sname) &
                            (Members.tName == thirname) &
                            (Members.lName == lname)
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
                            member.fName = fname
                            member.sName = sname
                            member.tName = thirname
                            member.lName = lname
                            member.phone = phoneStu
                            member.dateBerth = birth
                            member.save()

                            # Update the Students table
                            student = Students.get(Students.member_id == member_id)
                            student.className = stuClass
                            student.Phone = phoneStu
                            student.save()

                            QMessageBox.information(self, "نجاح", "تم التعديل بنجاح")


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

    def on_update_button_user_clicked(self):
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
        print("on_delete_button_clicked")
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                self.table_widget.removeRow(row)
                Members.delete()

    def get_buttons(self, operation):
        if operation == 'New':
            self.setLayout(self.layout1)
        elif operation == 'Old':
            self.setLayout(self.layout2)

        return self

    def on_update_button_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                # Get the data from the selected row in the table_widget
                fname = self.table_widget.item(row, 1)
                sname = self.table_widget.item(row, 2)
                tname = self.table_widget.item(row,3)
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
                        QMessageBox.information(UIHandler.get_ui(self), "تعديل", "تم التعديل  بنجاح.")

    def add_users_to_device(self, teacher_id, teacher_name):
        try:
            zk = ZK('192.168.1.201', port=4370, timeout=5)
            conn = zk.connect()
            if conn:
                conn.enable_device()
                users = conn.get_users()
                users_names = []

                teacherName = f"{teacher_name[0]} { teacher_name[1]} { teacher_name[2]}"
                print (teacherName)
                for user in users:
                    users_names.append(user.name)
                if teacherName in users_names:
                    QMessageBox.warning(self, "لم تتم الاضافة", "المستخدم موجود مسبقاً")
                    return False
                else:
                    conn.set_user(uid=int(teacher_id), name=teacherName, privilege=0)
                    return True
            else:
                QMessageBox.warning(self, "فشل", "لا يوجد جهاز بصمة متصل الآن ")
                return False
            #
            # try:
            #     conn.enable_device()
            #     # Retrieve the selected teacher's ID and name
            #     # clicked_button = self.sender()
            #     # if clicked_button:
            #     #     cell_widget = clicked_button.parentWidget()
            #     #     if cell_widget and self.table_widget:
            #     #         row = self.table_widget.indexAt(cell_widget.pos()).row()
            #     #         teacher_id_item = self.table_widget.item(row, 0)
            #     #         teacher_name_item = self.table_widget.item(row, 1)
            #     #
            #     #         if teacher_id_item and teacher_name_item:
            #     #             teacher_id = teacher_id_item.text()
            #     #             teacher_name = teacher_name_item.text()
            #     # codecs.encode(teacher_name, 'hex').decode('ascii')
            #     # Enroll the user to the fingerprint device with the padded name
            #     users = conn.get_users()
            #     users_names = []
            #     for user in users:
            #         users_names.append(user.name)
            #     if teacher_name in users_names:
            #         QMessageBox.warning(self, "لم تتم الاضافة", "المستخدم موجود مسبقاً")
            #     else:
            #         conn.set_user(uid=int(teacher_id), name=teacher_name, privilege=0)
            #         return True
            # except Exception as e:
            #     QMessageBox.warning(self, "تحذير", "لم تتم الإضافة ".format(teacher_name=e))
            #     logging.error("لم تتم الإضافة", exc_info=True)

        except Exception as e:
            QMessageBox.warning(self, "تحذير", "لا يوجد جهاز بصمة متصل الآن".format(teacher_name=e))
            logging.error("الجهاز غير متصل الآن")

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
