import peewee
from PyQt5.QtCore import QDate, Qt

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout

from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonUsersWidget
from GUI.Dialogs.UserDialog import UserDialog
from models.Members import Members
from models.Users import Users





class UsersUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ips = ''
        self.ports = ''
        self.lastInsertedMemberId = 0
        self.lastInsertedUserId = 0
        self.ui.tblUsers.setColumnHidden(0, True)
        self.ui.tblUsers.setColumnHidden(5, True)


    def use_ui_elements(self):
        self.ui.tblUsers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblUsers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblUsers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnAddNewUser.clicked.connect(self.add_new_user)
        self.ui.txtUsersSearch.textChanged.connect(self.get_member_data)
    def addMembersDataBase(self):
        if self.ui.tblUsers.rowCount() > 0:
            schoolID = 1  # قم بتعديل هذا السطر إذا كان لديك معرف مدرسة محدد
            last_row_index = self.ui.tblUsers.rowCount() - 1
            Name = self.ui.tblUsers.item(last_row_index, 1).text()
            userName = self.ui.tblUsers.item(last_row_index, 2).text()
            userPassword = self.ui.tblUsers.item(last_row_index, 3).text()
            accountType = self.ui.tblUsers.item(last_row_index, 4).text()
            try:

                # التحقق مما إذا كان العضو موجودًا بالفعل
                existing_member = Members.select().where(
                    (Members.fName == Name)
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
                            Members.fName: Name,
                            Members.accountType: accountType,
                        }).execute()
                        self.lastInsertedMemberId = Members.select(peewee.fn.Max(Members.id)).scalar()
                        Users.insert({
                            Users.members_id: self.lastInsertedMemberId,
                            Users.userName: userName,
                            Users.userPassword: userPassword,

                        }).execute()
                        self.lastInsertedUserId = Users.select(peewee.fn.Max(Users.id)).scalar()

                        print("the id inserted m is : ", self.lastInsertedMemberId)
                        print("the id inserted S is : ", self.lastInsertedUserId)
                        QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")
                    except ValueError as e:
                        QMessageBox.critical(self.ui, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")



            except Exception as e:

                error_message = "حدث خطأ:\n\n" + str(e)
                QMessageBox.critical(self.ui, "خطأ", error_message)

    def add_new_user(self):

        self.ui.tblUsers.setRowCount(0)
        user_dialog = UserDialog()
        if user_dialog.exec_() == QDialog.Accepted:

            try:

                operationsButtons = DeleteUpdateButtonUsersWidget(table_widget=self.ui.tblUsers)
                accountType, Name, userName, userPassword = user_dialog.save_data()  # Call save_data() on mydialog instance
                current_row = self.ui.tblTeachers.rowCount()  # Get the current row index
                self.ui.tblUsers.insertRow(current_row)  # Insert a new row at the current row index
                self.ui.tblUsers.setItem(current_row, 1, QTableWidgetItem(Name))
                self.ui.tblUsers.setItem(current_row, 2, QTableWidgetItem(userName))
                self.ui.tblUsers.setItem(current_row, 3, QTableWidgetItem(userPassword))
                self.ui.tblUsers.setItem(current_row, 4, QTableWidgetItem(accountType))
                self.ui.tblUsers.setCellWidget(current_row, 5, operationsButtons)

                self.ui.tblUsers.setColumnWidth(current_row, 40)
                self.ui.tblUsers.setRowHeight(current_row, 150)

                # self.addMembersDataBase()

            except Exception as e:

                error_message = "حدث خطأ:\n\n" + str(e)
                QMessageBox.critical(self.ui, "خطأ", error_message)


    def get_member_data(self):

        self.ui.tblUsers.setColumnHidden(5, False)

        try:
            columns = ['id', 'fName', 'userName', 'userPassword', 'accountType']
            # search_item = self.ui.txtTeachersSearch.lower()
            search_item = self.ui.txtUsersSearch.toPlainText().lower()
            members_query = Members.select().join(Users).where(
                peewee.fn.LOWER(Members.fName).contains(search_item)).distinct()

            self.ui.tblUsers.setRowCount(0)  # Clear existing rows in the table
            for row, member_data in enumerate(members_query):
                table_items = []
                for column_name in columns:
                    try:
                        item_value = getattr(member_data, column_name)
                    except AttributeError:
                        User_data = Users.get(Users.members_id == member_data.id)
                        item_value = getattr(User_data, column_name)

                    table_item = QTableWidgetItem(str(item_value))
                    table_items.append(table_item)

                self.ui.tblUsers.insertRow(row)
                for col, item in enumerate(table_items):
                    self.ui.tblUsers.setItem(row, col, item)

                self.ui.tblUsers.setColumnWidth(row, 40)
                self.ui.tblUsers.setRowHeight(row, 150)

                operations_buttons = DeleteUpdateButtonUsersWidget(table_widget=self.ui.tblUsers)
                self.ui.tblUsers.setCellWidget(row, 5, operations_buttons)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)





