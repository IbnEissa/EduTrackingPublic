# from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QDialog, QListWidget, \
#     QListWidgetItem, QMessageBox
# from PyQt5.QtCore import Qt, QPoint, QEvent
# from PyQt5.QtGui import QIcon, QFont, QColor
#
#
# class OptionUI:
#     def __init__(self, submain_instance):
#         self.submain = submain_instance
#         self.ui = self.submain.ui
#
#     def use_ui_elements(self):
#         self.ui.btnEntery.clicked.connect(self.show_options('btnEntery'))
#         self.ui.btnSettings.clicked.connect(self.show_options('btnSettings'))
#
#     def show_options(self, btn_name):
#         if btn_name == 'btnEntery':
#             dialog = OptionDialog(self.ui.btnEntery)
#             button_rect = self.ui.btnEntery.rect()
#             button_bottom_left = self.ui.btnEntery.mapToGlobal(button_rect.bottomLeft())
#             dialog_width = dialog.width()
#             dialog_height = dialog.height()
#             dialog.move(button_bottom_left - QPoint(dialog_width, dialog_height))
#             if dialog.exec_() == QDialog.Accepted:
#                 selected_option = dialog.selectedOption()
#                 self.show_tab(selected_option)
#
#         elif btn_name == 'btnSettings':
#             dialog = OptionDialog(self.ui.btnSettings)
#             button_rect = self.ui.btnSettings.rect()
#             button_bottom_left = self.ui.btnSettings.mapToGlobal(button_rect.bottomLeft())
#             dialog_width = dialog.width()
#             dialog_height = dialog.height()
#             dialog.move(button_bottom_left - QPoint(dialog_width, dialog_height))
#             if dialog.exec_() == QDialog.Accepted:
#                 selected_option = dialog.selectedOption()
#                 self.show_tab(selected_option)
#
#     def show_tab(self, selected_option):
#         if selected_option == 'سجــــلات الحضور':
#             self.ui.tabMainTab.setCurrentIndex(2)
#             self.ui.tabEmpsMovement.setCurrentIndex(0)
#         elif selected_option == 'طالــب جديد':
#             self.ui.tabMainTab.setCurrentIndex(1)
#             self.ui.tabDataManagement.setCurrentIndex(1)
#         elif selected_option == 'موضفيـــن':
#             self.ui.tabMainTab.setCurrentIndex(1)
#             self.ui.tabDataManagement.setCurrentIndex(0)
#         elif selected_option == 'جهاز البصمة':
#             self.ui.tabMainTab.setCurrentIndex(4)
#             self.ui.tabSettings.setCurrentIndex(0)
#             self.ui.tabDevice.setCurrentIndex(0)
#         elif selected_option == 'غياب بعذر':
#             QMessageBox.information(self.ui, 'تحذير', 'لم يتم اضافة الواجهه بعد')
#         elif selected_option == 'الحسابـــات':
#             # self.ui.tabDataManagement.setCurrentIndex(3)
#             QMessageBox.information(self.ui, 'تحذير', 'لم يتم اضافة الواجهه بعد')
#         elif selected_option == 'تسجيل الخروج':
#             QMessageBox.information(self.ui, 'تحذير', 'لم يتم اضافة الواجهه بعد')
#
#
# class OptionDialog(QDialog):
#     def __init__(self, parent=None, btn_name=None):
#         super().__init__(parent)
#         self.btn_name = btn_name
#         self.layout = QVBoxLayout(self)
#         self.layout.setAlignment(Qt.AlignLeft)
#         self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.main_list_widget = QListWidget()
#         self.main_list_widget.setLayoutDirection(Qt.LeftToRight)  # Set right-to-left layout direction
#         self.main_list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable vertical scrollbar
#         self.main_list_widget.setStyleSheet(
#             "QListWidget { background-color: white; border: 0px solid white; }")
#         if self.btn_name == 'btnSettings':
#             main_items = [
#                 ("طالــب جديد", "icons/add1.png"),
#                 ("موضفيـــن", "icons/تنزيل (3).jpg"),
#                 ("سجــــلات الحضور", "icons/add1.png"),
#                 ("جهاز البصمة", "icons/fingerPrint.jpg"),
#                 ("غياب بعذر", "icons/add1.png"),
#                 ("الحسابـــات", "icons/تنزيل (2).jpg"),
#                 ("تسجيل الخروج", "icons/add1.png")
#             ]
#             for item_text, icon_path in main_items:
#                 item = QListWidgetItem(QIcon(icon_path), item_text)
#                 font = QFont()
#                 font.setPointSize(12)
#                 item.setFont(font)
#                 item.setForeground(QColor("black"))  # Set the text color to black
#                 item.setTextAlignment(Qt.AlignCenter | Qt.AlignRight)  # Align the item's text to the right
#                 item.setBackground(QColor("white"))  # Set the background color of each item to white
#                 self.main_list_widget.addItem(item)
#
#             self.layout.addWidget(self.main_list_widget)
#
#             self.main_list_widget.itemClicked.connect(self.accept)
#
#             self.adjustSize()
#         elif self.btn_name == 'btnEntery':
#             main_items = [
#                 ("سجــــلات الحضور", "icons/add1.png"),
#                 ("جهاز البصمة", "icons/fingerPrint.jpg"),
#                 ("غياب بعذر", "icons/add1.png"),
#                 ("الحسابـــات", "icons/تنزيل (2).jpg"),
#                 ("تسجيل الخروج", "icons/add1.png")
#             ]
#             for item_text, icon_path in main_items:
#                 item = QListWidgetItem(QIcon(icon_path), item_text)
#                 font = QFont()
#                 font.setPointSize(12)
#                 item.setFont(font)
#                 item.setForeground(QColor("black"))  # Set the text color to black
#                 item.setTextAlignment(Qt.AlignCenter | Qt.AlignRight)  # Align the item's text to the right
#                 item.setBackground(QColor("white"))  # Set the background color of each item to white
#                 self.main_list_widget.addItem(item)
#         # self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
#         # self.setWindowFlags(Qt.WindowTitleHint | Qt.CustomizeWindowHint)
#
#     def selectedOption(self):
#         selected_item = self.main_list_widget.currentItem()
#         if selected_item:
#             return selected_item.text()
#         return ""
from PyQt5.QtGui import QIcon, QColor, QFont
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QIcon
# from PyQt5.QtWidgets import QDialog, QListWidget, QListWidgetItem, QApplication, QVBoxLayout
#
#
# class OptionDialog(QDialog):
#     def __init__(self, parent=None, btn_name=None):
#         super().__init__(parent)
#         self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.layout = QVBoxLayout(self)
#         self.layout.setAlignment(Qt.AlignLeft)
#         self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.main_list_widget = QListWidget()
#         self.main_list_widget.setLayoutDirection(Qt.LeftToRight)  # Set right-to-left layout direction
#         self.main_list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable vertical scrollbar
#         self.main_list_widget.setStyleSheet(
#             "QListWidget { background-color: white; border: 0px solid white; }")
#         # self.main_list_widget = QListWidget()
#         # self.main_list_widget.setStyleSheet("QListWidget { background-color: white; border: 0px solid white; }")
#
#         main_items = [
#             ("سجــــلات الحضور", "icons/add1.png"),
#             ("جهاز البصمة", "icons/fingerPrint.jpg"),
#             ("غياب بعذر", "icons/add1.png"),
#             ("الحسابـــات", "icons/تنزيل (2).jpg"),
#             ("تسجيل الخروج", "icons/add1.png")
#             # Add more options and corresponding icons
#         ]
#
#         for item_text, icon_path in main_items:
#             item = QListWidgetItem(QIcon(icon_path), item_text)
#             self.main_list_widget.addItem(item)
#
#         self.main_list_widget.itemClicked.connect(self.accept)
#
#         layout = QVBoxLayout(self)
#         layout.addWidget(self.main_list_widget)
#         self.adjustSize()
#
#     def selectedOption(self):
#         if self.main_list_widget.currentItem():
#             return self.main_list_widget.currentItem().text()
#         return None
#
#
# class OptionUI:
#     def __init__(self, submain_instance):
#         self.submain = submain_instance
#         self.ui = self.submain.ui
#
#     def use_ui_elements(self):
#         self.ui.btnEntery.clicked.connect(lambda: self.show_options('btnEntery'))
#         self.ui.btnSettings.clicked.connect(lambda: self.show_options('btnSettings'))
#
#     def show_options(self, btn_name):
#         dialog = OptionDialog(self.ui, btn_name)
#         if dialog.exec_() == QDialog.Accepted:
#             selected_option = dialog.selectedOption()
#             self.show_tab(selected_option)
#
#     def show_tab(self, selected_option):
#         if selected_option == 'Option 1':
#             # Show tab for Option 1
#             pass
#         elif selected_option == 'Option 2':
#             # Show tab for Option 2
#             pass
#         elif selected_option == 'Option 3':
#             # Show tab for Option 3
#             pass
#         # Add more conditions for other options
#
# #
# # app = QApplication([])  # Create the application instance
# # option_ui = OptionUI(submain_instance)  # Initialize the OptionUI class
# # app.exec_()  # Start the application event loop


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QApplication, QPushButton, QMessageBox, \
    QMainWindow, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QEvent

from GUI.Dialogs.UserLogoutDialog import UserLogoutDialog
from GUI.Views.CommonFunctionality import Common
from GUI.Views.LoginState import LoginState
from GUI.Views.PermissionUI import PermissionUI
from models.Permissions import Permissions
from models.Users import Users


class OptionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window | Qt.FramelessWindowHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignLeft)

        self.list_widget = QListWidget()
        self.list_widget.setLayoutDirection(Qt.LeftToRight)
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_widget.setStyleSheet(
            "QListWidget { background-color: white; border: 0px solid white; font-family:Motken K Sina;color: black; font-size: 16px;}")
        self.layout.addWidget(self.list_widget)

        self.close_button = QPushButton("إغــــــــــــلاق")
        self.close_button.setStyleSheet(
            "QPushButton { background-color: red; font-family:Motken K Sina;color: white; font-size: 16px;}")
        self.close_button.clicked.connect(self.close_dialog)
        self.layout.addWidget(self.close_button)

        self.list_widget.itemClicked.connect(self.accept)

    def close_dialog(self):
        self.close()

    def setOptions(self, options):
        self.list_widget.clear()

        for item_text, icon_path in options:
            item = QListWidgetItem(QIcon(icon_path), item_text)

            font = QFont()
            font.setPointSize(12)
            item.setFont(font)
            item.setForeground(QColor("black"))  # Set the text color to black
            item.setTextAlignment(Qt.AlignCenter | Qt.AlignRight)  # Align the item's text to the right
            item.setBackground(QColor("white"))
            self.list_widget.addItem(item)

    def selectedOption(self):
        if self.list_widget.currentItem():
            return self.list_widget.currentItem().text()
        return None


class OptionUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.dialog = OptionDialog()
        self.dialog.close_button.clicked.connect(self.close_dialog)
        # self.dialog.setOptions([])
        # self.installEventFilter(self.dialog)

    def close_dialog(self):
        self.ui.btnEmps.setStyleSheet(
            "QPushButton { background-color: qlineargradient(spread:pad, x1:0.964478, y1:0.193, x2:1, y2:0, stop:0 rgba(191, 194, 181, 255), stop:1 rgba(255, 255, 255, 255));color:black}")
        self.ui.btnSettings.setStyleSheet(
            "QPushButton { background-color: qlineargradient(spread:pad, x1:0.964478, y1:0.193, x2:1, y2:0, stop:0 rgba(191, 194, 181, 255), stop:1 rgba(255, 255, 255, 255));color:black}")
        self.ui.btnStudents.setStyleSheet(
            "QPushButton { background-color: qlineargradient(spread:pad, x1:0.964478, y1:0.193, x2:1, y2:0, stop:0 rgba(191, 194, 181, 255), stop:1 rgba(255, 255, 255, 255));color:black}")
        self.ui.btnReports.setStyleSheet(
            "QPushButton { background-color: qlineargradient(spread:pad, x1:0.964478, y1:0.193, x2:1, y2:0, stop:0 rgba(191, 194, 181, 255), stop:1 rgba(255, 255, 255, 255));color:black}")
        self.ui.btnHome.setStyleSheet(
            "QPushButton { background-color: qlineargradient(spread:pad, x1:0.964478, y1:0.193, x2:1, y2:0, stop:0 rgba(191, 194, 181, 255), stop:1 rgba(255, 255, 255, 255));color:black}")

    # def mousePressEvent(self, event):
    #     option_dialog = self.findChild(OptionDialog)
    #     if option_dialog is not None:
    #         option_dialog.close()
    #     super().mousePressEvent(event)

    def use_ui_elements(self):
        self.ui.btnEmps.clicked.connect(lambda: self.show_options_entery("btnEmps"))
        # self.ui.btnEmps.clicked.connect(self.show_options_entery)
        self.ui.btnSettings.clicked.connect(lambda: self.show_options_settings('btnSettings'))
        self.ui.btnStudents.clicked.connect(lambda: self.show_options_students('btnStudents'))
        self.ui.btnReports.clicked.connect(lambda: self.show_options_reports('btnReports'))

    def show_options(self, options, button_name):

        print("the button clicked is 2: ", button_name)
        if button_name == 'btnEmps':
            self.dialog.setOptions(options)
            self.dialog.move(1350, 500)
            if self.dialog.exec_() == QDialog.Accepted:
                selected_option = self.dialog.selectedOption()
                self.show_entry_tab(selected_option)
        if button_name == 'btnStudents':
            self.dialog.setOptions(options)
            self.dialog.move(1350, 620)
            if self.dialog.exec_() == QDialog.Accepted:
                selected_option = self.dialog.selectedOption()
                self.show_students_tab(selected_option)
        if button_name == 'btnSettings':
            self.dialog.setOptions(options)
            self.dialog.move(1350, 770)
            if self.dialog.exec_() == QDialog.Accepted:
                selected_option = self.dialog.selectedOption()
                self.show_settings_tab(selected_option)
        if button_name == 'btnReports':
            self.dialog.setOptions(options)
            self.dialog.move(1350, 740)
            if self.dialog.exec_() == QDialog.Accepted:
                selected_option = self.dialog.selectedOption()
                self.show_reports_tab(selected_option)

    def show_entry_tab(self, selected_option):
        if selected_option == 'سجــــلات الحضور':
            self.ui.tabMainTab.setCurrentIndex(2)
            self.ui.tabEmpsMovement.setCurrentIndex(0)
        if selected_option == 'عرض الحضور والانصراف':
            self.ui.tabMainTab.setCurrentIndex(2)
            self.ui.tabEmpsMovement.setCurrentIndex(1)
        if selected_option == 'مجلس الاباء':

            self.ui.tabMainTab.setCurrentIndex(1)
            self.ui.tabDataManagement.setCurrentIndex(4)

        if selected_option == 'جدول حصص المعلمين':
            self.ui.tabMainTab.setCurrentIndex(1)
            self.ui.tabDataManagement.setCurrentIndex(2)
        if selected_option == 'عرض حسب الورديات':
            self.ui.tabMainTab.setCurrentIndex(2)
            self.ui.tabEmpsMovement.setCurrentIndex(2)

        if selected_option == 'موضفيـــن':
            self.ui.tabMainTab.setCurrentIndex(1)
            self.ui.tabDataManagement.setCurrentIndex(0)
        if selected_option == 'جهاز البصمة':
            self.ui.tabMainTab.setCurrentIndex(4)
            self.ui.tabSettings.setCurrentIndex(2)
        if selected_option == 'جدول حصص المعلمين':
            self.ui.tabMainTab.setCurrentIndex(1)
            self.ui.tabDataManagement.setCurrentIndex(2)
        if selected_option == 'غياب بعذر':
            QMessageBox.information(self.ui, 'تحذير', 'لم يتم اضافة الواجهه بعد')
        if selected_option == 'الحسابـــات':
            QMessageBox.information(self.ui, 'تحذير', 'لم يتم اضافة الواجهه بعد')

    def show_students_tab(self, selected_option):
        if selected_option == 'جدول حصص الطلاب':
            self.ui.tabMainTab.setCurrentIndex(1)
            self.ui.tabDataManagement.setCurrentIndex(3)
        if selected_option == 'طالــب جديد':
            self.ui.tabMainTab.setCurrentIndex(1)
            self.ui.tabDataManagement.setCurrentIndex(1)
        if selected_option == 'الحسابـــات':
            # self.ui.tabDataManagement.setCurrentIndex(3)
            QMessageBox.information(self.ui, 'تحذير', 'لم يتم اضافة الواجهه بعد')

    def show_settings_tab(self, selected_option):
        if selected_option == 'المستخدمين':
            result_condition = self.grant_permission_tab_to_user(permission="bt_show_attendance")
            if result_condition is True:
                self.ui.tabMainTab.setCurrentIndex(4)
                self.ui.tabSettings.setCurrentIndex(0)
            else:
                QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")

        if selected_option == 'الصلاحيات':
            result_condition = self.grant_permission_tab_to_user(permission="bt_export_attendance")
            if result_condition is True:
                self.ui.tabMainTab.setCurrentIndex(4)
                self.ui.tabSettings.setCurrentIndex(1)
            else:
                QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")
        if selected_option == 'جهاز البصمة':
            self.ui.tabMainTab.setCurrentIndex(4)
            self.ui.tabSettings.setCurrentIndex(2)
        if selected_option == 'تهيئةالمدرسة':
            self.ui.tabMainTab.setCurrentIndex(4)
            self.ui.tabSettings.setCurrentIndex(3)
        if selected_option == 'تهيئة حصص الترم':
            self.ui.tabMainTab.setCurrentIndex(4)
            self.ui.tabSettings.setCurrentIndex(4)
        if selected_option == 'تهيئةالورديات':
            self.ui.tabMainTab.setCurrentIndex(4)
            self.ui.tabSettings.setCurrentIndex(5)
        if selected_option == 'نسخة احتياطية':
            self.ui.tabMainTab.setCurrentIndex(4)
            self.ui.tabSettings.setCurrentIndex(6)

    def grant_permission_tab_to_user(self, permission):
        name = Users.get_name_with_true_state()
        print("grant permission button to ", name)
        # selected_user = "moh"  # Replace with your logic to get the selected user
        user = Users.get(Users.Name == name)
        permissions = (
            Permissions.select()
            .join(Users, on=(Permissions.users_id == Users.id))
            .where(Users.id == user.id)
            .get()
        )
        print(permission)
        if getattr(permissions, permission) == True:
            return True
        else:
            return False

    def show_user_details_tab(self, selected_option):

        if selected_option == 'تبديل المستخدم':
            user_logout = UserLogoutDialog()
            user_logout.exec_()
        if selected_option == 'خروج نهائي':
            QMessageBox.information(self.ui, 'تحذير', 'لم يتم اضافة الواجهه بعد')

        if selected_option == 'الحساب':
            QMessageBox.information(self.ui, 'تحذير', 'لم يتم اضافة الواجهه بعد')

    def show_reports_tab(self, selected_option):
        if selected_option == 'الموضفين':
            print('the selected option is : ', selected_option)
            self.ui.tabMainTab.setCurrentIndex(3)
            self.ui.tabTeachersReports.setCurrentIndex(1)
            # QMessageBox.information(self.ui, 'تحذير', 'لم يتم اضافة الواجهه بعد')
        if selected_option == 'الطلاب':
            print('the selected option is : ', selected_option)
            self.ui.tabMainTab.setCurrentIndex(3)
            self.ui.tabTeachersReports.setCurrentIndex(0)

    def show_options_entery(self, button_name):
        self.ui.btnEmps.setStyleSheet("QPushButton { background-color: red;}")
        options = [
            ("موضفيـــن", "icons/تنزيل (3).jpg"),
            ("مجلس الاباء", "icons/تنزيل (3).jpg"),
            ("سجــــلات الحضور", "icons/add1.png"),
            ("جدول حصص المعلمين", "icons/add1.png"),
            ("عرض الحضور والانصراف", "icons/add1.png"),
            ("عرض حسب الورديات", "icons/add1.png"),
            ("جهاز البصمة", "icons/images.jpg"),
            ("غياب بعذر", "icons/add1.png"),
            ("الحسابـــات", "icons/تنزيل (2).jpg"),
        ]

        self.show_options(options, button_name)

    def show_options_students(self, button_name):
        self.ui.btnStudents.setStyleSheet("QPushButton { background-color: red;}")

        # self.ui.btnStudents.setStyleSheet( "QPushButton { background-color: red;}")
        # self.ui.btnStudents.setStyleSheet( "QPushButton { background-color: red;}")
        # self.ui.btnStudents.setStyleSheet( "QPushButton { background-color: red;}")
        # self.ui.btnStudents.setStyleSheet( "QPushButton { background-color: red;}")
        options = [
            ("طالــب جديد", "icons/add1.png"),
            ("جدول حصص الطلاب", "icons/add1.png"),
            ("الحسابـــات", "icons/تنزيل (2).jpg"),
        ]
        self.show_options(options, button_name)

    def show_options_settings(self, button_name):
        self.ui.btnSettings.setStyleSheet("QPushButton { background-color: red;}")
        options = [
            ("تهيئةالمدرسة", "icons/users_Details.svg"),
            ("تهيئة حصص الترم", "icons/users_Details.svg"),
            ("تهيئةالورديات", "icons/users_Details.svg"),
            ("المستخدمين", "icons/users_accounts.jpg"),
            ("الصلاحيات", "icons/permission.png"),
            ("نسخة احتياطية", "icons/permission.png"),
        ]
        self.show_options(options, button_name)

    def show_options_user_details(self, button_name):
        print("the selected option is : ", button_name)
        options = [
            ("الحساب", "icons/users.png"),
            ("تبديل المستخدم", "icons/log-out.svg"),
            ("خروج نهائي", "icons/log-out.svg"),

        ]
        self.show_options(options, button_name)

    def show_options_reports(self, button_name):
        self.ui.btnReports.setStyleSheet("QPushButton { background-color: red;}")
        options = [
            ("الموضفين", "icons/newData.png"),
            ("الطلاب", "icons/remarks-24.svg"),
        ]
        self.show_options(options, button_name)
