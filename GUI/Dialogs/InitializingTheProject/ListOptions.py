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


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QApplication, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QPoint

from GUI.Dialogs.UserLogoutDialog import UserLogoutDialog
from GUI.Views.CommonFunctionality import Common
from GUI.Views.LoginState import LoginState


class OptionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignLeft)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.list_widget = QListWidget()
        self.list_widget.setLayoutDirection(Qt.LeftToRight)  # Set right-to-left layout direction
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable vertical scrollbar
        self.list_widget.setStyleSheet(
            "QListWidget { background-color: white; border: 0px solid white; }")
        self.layout.addWidget(self.list_widget)

        self.list_widget.itemClicked.connect(self.accept)

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
        # self.dialog.setOptions([])

    def use_ui_elements(self):
        self.ui.btnEntery.clicked.connect(self.show_options_entery)
        self.ui.btnSettings.clicked.connect(self.show_options_settings)
        self.ui.btnUserDetails.clicked.connect(self.show_options_user_details)
        self.ui.btnReports.clicked.connect(self.show_options_reports)

    def show_options(self, options, QPushButton):
        if QPushButton == self.ui.btnEntery:
            self.dialog.setOptions(options)
            button_rect = QPushButton.rect()
            button_bottom_left = QPushButton.mapToGlobal(button_rect.bottomLeft())
            dialog_width = self.dialog.width()
            dialog_height = self.dialog.height()
            self.dialog.move(button_bottom_left - QPoint(dialog_width, dialog_height))
            if self.dialog.exec_() == QDialog.Accepted:
                selected_option = self.dialog.selectedOption()
                self.show_entry_tab(selected_option)
        if QPushButton == self.ui.btnSettings:
            self.dialog.setOptions(options)
            button_rect = QPushButton.rect()
            button_bottom_left = QPushButton.mapToGlobal(button_rect.bottomLeft())
            dialog_width = self.dialog.width()
            dialog_height = self.dialog.height()
            self.dialog.move(button_bottom_left - QPoint(dialog_width, dialog_height))
            if self.dialog.exec_() == QDialog.Accepted:
                selected_option = self.dialog.selectedOption()
                self.show_settings_tab(selected_option)
        if QPushButton == self.ui.btnUserDetails:
            self.dialog.setOptions(options)
            button_rect = QPushButton.rect()
            button_bottom_left = QPushButton.mapToGlobal(button_rect.bottomLeft())
            dialog_width = self.dialog.width()
            dialog_height = self.dialog.height()
            self.dialog.move(button_bottom_left + QPoint(dialog_width, dialog_height))
            if self.dialog.exec_() == QDialog.Accepted:
                selected_option = self.dialog.selectedOption()
                self.show_user_details_tab(selected_option)
        if QPushButton == self.ui.btnReports:
            self.dialog.setOptions(options)
            button_rect = QPushButton.rect()
            button_bottom_left = QPushButton.mapToGlobal(button_rect.bottomLeft())
            dialog_width = self.dialog.width()
            dialog_height = self.dialog.height()
            self.dialog.move(button_bottom_left - QPoint(dialog_width, dialog_height))
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
        if selected_option == 'جدول حصص الطلاب':
            self.ui.tabMainTab.setCurrentIndex(1)
            self.ui.tabDataManagement.setCurrentIndex(3)
        if selected_option == 'جدول حصص المعلمين':
            self.ui.tabMainTab.setCurrentIndex(1)
            self.ui.tabDataManagement.setCurrentIndex(2)
        if selected_option == 'عرض حسب الورديات':
            self.ui.tabMainTab.setCurrentIndex(2)
            self.ui.tabEmpsMovement.setCurrentIndex(2)
        if selected_option == 'طالــب جديد':
            self.ui.tabMainTab.setCurrentIndex(1)
            self.ui.tabDataManagement.setCurrentIndex(1)
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
            # self.ui.tabDataManagement.setCurrentIndex(3)
            QMessageBox.information(self.ui, 'تحذير', 'لم يتم اضافة الواجهه بعد')

    def show_settings_tab(self, selected_option):
        if selected_option == 'المستخدمين':
            self.ui.tabMainTab.setCurrentIndex(4)
            self.ui.tabSettings.setCurrentIndex(0)
        if selected_option == 'الصلاحيات':
            self.ui.tabMainTab.setCurrentIndex(4)
            self.ui.tabSettings.setCurrentIndex(1)
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

    def show_user_details_tab(self, selected_option):

        if selected_option == 'تسجيل الخروج':
             user_logout = UserLogoutDialog()
             user_logout.exec_()

            # Main(1, False)
        if selected_option == 'الحساب':
            QMessageBox.information(self.ui, 'تحذير', 'لم يتم اضافة الواجهه بعد')

    def show_reports_tab(self, selected_option):
        if selected_option == 'الموضفين':
            print('the selected option is : ', selected_option)
            # self.ui.tabMainTab.setCurrentIndex(3)
            self.ui.tabTeachersReports.setCurrentIndex(0)
            # QMessageBox.information(self.ui, 'تحذير', 'لم يتم اضافة الواجهه بعد')
        elif selected_option == 'الطلاب':
            print('the selected option is : ', selected_option)
            self.ui.tabMainTab.setCurrentIndex(3)
            self.ui.tabTeachersReports.setCurrentIndex(1)

    def show_options_entery(self):
        options = [
            ("طالــب جديد", "icons/add1.png"),
            ("موضفيـــن", "icons/تنزيل (3).jpg"),
            ("مجلس الاباء", "icons/تنزيل (3).jpg"),
            ("سجــــلات الحضور", "icons/add1.png"),
            ("جدول حصص المعلمين", "icons/add1.png"),
            ("جدول حصص الطلاب", "icons/add1.png"),
            ("عرض الحضور والانصراف", "icons/add1.png"),
            ("عرض حسب الورديات", "icons/add1.png"),
            ("جهاز البصمة", "icons/images.jpg"),
            ("غياب بعذر", "icons/add1.png"),
            ("الحسابـــات", "icons/تنزيل (2).jpg"),
        ]

        self.show_options(options, self.ui.btnEntery)

    def show_options_settings(self):
        options = [
            ("تهيئةالمدرسة", "icons/users_Details.svg"),
            ("تهيئة حصص الترم", "icons/users_Details.svg"),
            ("تهيئةالورديات", "icons/users_Details.svg"),
            ("المستخدمين", "icons/users_accounts.jpg"),
            ("الصلاحيات", "icons/permission.png"),
        ]
        self.show_options(options, self.ui.btnSettings)

    def show_options_user_details(self):
        options = [
            ("تسجيل الخروج", "icons/log-out.svg"),
            ("الحساب", "icons/users.png"),
        ]
        self.show_options(options, self.ui.btnUserDetails)

    def show_options_reports(self):
        options = [
            ("الموضفين", "icons/newData.png"),
            ("الطلاب", "icons/remarks-24.svg"),
        ]
        self.show_options(options, self.ui.btnReports)
