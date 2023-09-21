# import PyZkUI
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QWidget, QVBoxLayout, QPushButton, QDialog, \
#     QTableWidgetItem, QMessageBox
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import Qt, QDate
# # from zk import ZK
#
# from GUI.Dialogs.DeviceDailog import MyDialog
# from GUI.Dialogs.TeacherDialog import TeacherDialog
# import logging
# import codecs
#
# from GUI.Views.uihandler import UIHandler
# from models.Members import Members
#
#
# class DeleteUpdateButtonDeviceWidget(QWidget):
#     def __init__(self, table_widget, parent=None):
#         super().__init__(parent)
#         # self.submain = submain_instance
#         # self.ui = self.submain.ui
#         self.table_widget = table_widget
#         # self.zk = ZK()
#         layout = QVBoxLayout()
#
#         self.delete_button = QPushButton("حــــذف")
#         self.update_button = QPushButton("تعــديل")
#         self.connect_button = QPushButton("إتصــــال")
#         self.connect_button.setStyleSheet("color: white; background-color: green;font: 12pt 'PT Bold Heading';")
#         self.delete_button.setFixedSize(110, 40)
#         self.connect_button.setFixedSize(110, 40)
#         self.update_button.setStyleSheet("color: white; background-color: blue; font: 12pt 'PT Bold Heading';")
#         self.delete_button.setStyleSheet("color: white; background-color: red;font:12pt 'PT Bold Heading';")
#         self.update_button.setFixedSize(110, 40)
#
#         layout.addSpacing(3)
#         layout.addWidget(self.connect_button)
#         layout.addWidget(self.update_button)
#         layout.addSpacing(3)
#         layout.addWidget(self.delete_button)
#
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setAlignment(Qt.AlignCenter)
#         self.setLayout(layout)
#
#         self.delete_button.clicked.connect(self.on_delete_button_clicked)
#         self.update_button.clicked.connect(self.on_update_button_clicked)
#
#     def on_delete_button_clicked(self):
#         clicked_button = self.sender()
#         if clicked_button:
#             cell_widget = clicked_button.parentWidget()
#             if cell_widget and self.table_widget:
#                 row = self.table_widget.indexAt(cell_widget.pos()).row()
#                 self.table_widget.removeRow(row)
#
#     def on_update_button_clicked(self):
#         clicked_button = self.sender()
#         if clicked_button:
#             cell_widget = clicked_button.parentWidget()
#             if cell_widget and self.table_widget:
#                 row = self.table_widget.indexAt(cell_widget.pos()).row()
#                 # Get the data from the selected row in the table_widget
#                 ip_address_item = self.table_widget.item(row, 1)
#                 port_number_item = self.table_widget.item(row, 2)
#
#                 if ip_address_item and port_number_item:
#                     ip_address = ip_address_item.text()
#                     port_number = port_number_item.text()
#                     device_dialog = MyDialog()
#                     device_dialog.txtIPAddress.setPlainText(ip_address)
#                     device_dialog.txtPortNumber.setPlainText(port_number)
#
#                     if device_dialog.exec_() == QDialog.Accepted:
#                         ip_address = device_dialog.txtIPAddress.toPlainText()
#                         port_number = device_dialog.txtPortNumber.toPlainText()
#
#                         # Update the row in the table_widget with the new data
#                         self.table_widget.setItem(row, 1, QTableWidgetItem(ip_address))
#                         self.table_widget.setItem(row, 2, QTableWidgetItem(port_number))
#
#
# class DeleteUpdateButtonTeachersWidget(QWidget):
#     def __init__(self, table_widget=None, parent=None):
#         super().__init__(parent)
#         self.table_widget = table_widget
#         self.layout1 = QVBoxLayout()
#         self.layout2 = QVBoxLayout()
#
#         self.delete_button = QPushButton("حــــذف")
#         self.update_button = QPushButton("تعــديل")
#         self.fingerprint_button = QPushButton("إضافة للجهاز")
#         self.delete_button.setFixedSize(110, 40)
#         self.fingerprint_button.setFixedSize(110, 40)
#         self.update_button.setStyleSheet("color: white; background-color: blue; font: 12pt 'PT Bold Heading';")
#         self.fingerprint_button.setStyleSheet("color: white; background-color: green; font: 12pt 'PT Bold Heading';")
#         self.delete_button.setStyleSheet("color: white; background-color: red;font:12pt 'PT Bold Heading';")
#         self.update_button.setFixedSize(110, 40)
#
#         self.layout2.addSpacing(3)
#         self.layout2.addWidget(self.update_button)
#         self.layout2.addSpacing(3)
#         self.layout2.addWidget(self.delete_button)
#         self.layout2.setAlignment(Qt.AlignCenter)
#
#         self.layout1.addSpacing(3)
#         self.layout1.addWidget(self.fingerprint_button)
#         self.layout1.addWidget(self.update_button)
#         self.layout1.addSpacing(3)
#         self.layout1.addWidget(self.delete_button)
#         # self.layout.setContentsMargins(0, 0, 0, 0)
#         self.layout1.setAlignment(Qt.AlignCenter)
#
#         self.delete_button.clicked.connect(self.on_delete_button_clicked)
#         self.update_button.clicked.connect(self.on_update_button_clicked)
#         self.fingerprint_button.clicked.connect(self.add_users_to_device)
#
#     def on_delete_button_clicked(self):
#         print("on_delete_button_clicked")
#         clicked_button = self.sender()
#         if clicked_button:
#             cell_widget = clicked_button.parentWidget()
#             if cell_widget and self.table_widget:
#                 row = self.table_widget.indexAt(cell_widget.pos()).row()
#                 self.table_widget.removeRow(row)
#                 Members.delete()
#
#     def get_buttons(self, operation):
#         if operation == 'New':
#             self.setLayout(self.layout1)
#         elif operation == 'Old':
#             self.setLayout(self.layout2)
#
#         return self
#
#     def on_update_button_clicked(self):
#         clicked_button = self.sender()
#         if clicked_button:
#             cell_widget = clicked_button.parentWidget()
#             if cell_widget and self.table_widget:
#                 row = self.table_widget.indexAt(cell_widget.pos()).row()
#                 # Get the data from the selected row in the table_widget
#                 teacher_name = self.table_widget.item(row, 1)
#                 teacher_phone = self.table_widget.item(row, 2)
#                 teacher_DOB = self.table_widget.item(row, 3)
#                 teacher_major = self.table_widget.item(row, 4)
#                 teacher_occupation = self.table_widget.item(row, 5)
#                 teacher_state = self.table_widget.item(row, 6)
#
#                 if teacher_name and teacher_phone and teacher_DOB and teacher_major and teacher_occupation and teacher_state:
#                     date = QDate.fromString(teacher_DOB.text(), "yyyy-MM-dd")
#                     teacher_dialog = TeacherDialog()
#                     teacher_dialog.txtTeacherFName.setPlainText(teacher_name.text())
#                     teacher_dialog.txtTeacherPhone.setPlainText(teacher_phone.text())
#                     teacher_dialog.dateTeacherDOB.setDate(date)
#                     teacher_dialog.txtTeacherMajor.setPlainText(teacher_major.text())
#                     teacher_dialog.txtTeacherTask.setPlainText(teacher_occupation.text())
#
#                     if teacher_dialog.exec_() == QDialog.Accepted:
#                         name = teacher_dialog.txtTeacherFName.toPlainText()
#                         phone = teacher_dialog.txtTeacherPhone.toPlainText()
#                         DOB = teacher_dialog.dateTeacherDOB.date().toPyDate()
#                         major = teacher_dialog.txtTeacherMajor.toPlainText()
#                         occupation = teacher_dialog.txtTeacherTask.toPlainText()
#
#                         # Update the row in the table_widget with the new data
#                         self.table_widget.setItem(row, 1, QTableWidgetItem(name))
#                         self.table_widget.setItem(row, 2, QTableWidgetItem(phone))
#                         self.table_widget.setItem(row, 3, QTableWidgetItem(str(DOB)))
#                         self.table_widget.setItem(row, 4, QTableWidgetItem(major))
#                         self.table_widget.setItem(row, 5, QTableWidgetItem(occupation))
#                         QMessageBox.information(UIHandler.get_ui(self), "تعديل", "تم التعديل  بنجاح.")
#
#     def add_users_to_device(self):
#         print("the finger button is clicked")
#         try:
#             zk = ZK('192.168.1.201', port=4370, timeout=5)
#             conn = zk.connect()
#             if conn:
#                 conn.enable_device()
#                 # Retrieve the selected teacher's ID and name
#                 clicked_button = self.sender()
#                 if clicked_button:
#                     cell_widget = clicked_button.parentWidget()
#                     if cell_widget and self.table_widget:
#                         row = self.table_widget.indexAt(cell_widget.pos()).row()
#                         teacher_id_item = self.table_widget.item(row, 0)
#                         teacher_name_item = self.table_widget.item(row, 1)
#
#                         if teacher_id_item and teacher_name_item:
#                             teacher_id = teacher_id_item.text()
#                             teacher_name = teacher_name_item.text()
#                             # codecs.encode(teacher_name, 'hex').decode('ascii')
#                             # Enroll the user to the fingerprint device with the padded name
#                             users = conn.get_users()
#                             users_names = []
#                             for user in users:
#                                 users_names.append(user.name)
#                             if teacher_name in users_names:
#                                 QMessageBox.warning(self, "لم تتم الاضافة", "المستخدم موجود مسبقاً")
#                             else:
#                                 conn.set_user(uid=int(teacher_id), name=teacher_name, privilege=0)
#                                 QMessageBox.information(self, "تمت الإضافة", "تمت إضافة المستخدم بنجاح.")
#
#                         else:
#                             logging.error("فشل تحميل الاسم أو رقم المعرف")
#             else:
#                 QMessageBox.warning(self, "تحذير", "لا يوجد جهاز بصمة متصل الآن")
#                 logging.error("الجهاز غير متصل الآن")
#         except Exception as e:
#             QMessageBox.warning(self, "تحذير", "لم تتم الإضافة ".format(teacher_name=e))
#             logging.error("لم تتم الإضافة", exc_info=True)
#
#     def start_enroll_face(sIp="192.168.1.201", iPort=4370, iMachineNumber=1, userid="", fingureindex=0):
#         zk = ZK('192.168.1.201', port=4370, timeout=5)
#         conn = None
#         try:
#             conn = zk.connect()
#
#             if conn:
#                 conn.disable_device()
#
#                 user_id = str(userid)
#                 finger_index = int(fingureindex)
#
#                 # Clear the existing face template for the user
#                 conn.delete_user_face(iMachineNumber, user_id, finger_index)
#
#                 # Start the face enrollment process
#                 if conn.start_enroll_ex(user_id, finger_index, 1):  # 1 represents the face biometric type
#                     logging.info(f"Start to enroll a new user, UserID={user_id}, Face ID={finger_index}, Flag=1")
#                     conn.start_identify()  # Let the device enter 1:N verification condition after enrolling templates
#                     conn.refresh_data(1)  # Refresh the data in the device
#                     start_enroll_result = True
#                 else:
#                     logging.error("Failed to start enrollment.")
#                     start_enroll_result = False
#
#                 conn.enable_device()
#                 return start_enroll_result
#             else:
#                 logging.error("Failed to establish connection to the device.")
#                 return False
#         except Exception as e:
#             logging.error("An error occurred during face enrollment.", exc_info=True)
#             return False
#         finally:
#             if conn:
#                 conn.disconnect()
