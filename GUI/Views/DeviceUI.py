from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QAbstractItemView, QHeaderView, QDialog, QApplication, \
    QVBoxLayout, QWidget, QHBoxLayout
# from PyZkUI.models import ZK
from zk import const

from zk import ZK

from GUI.Dialogs.DeviceDailog import MyDialog
from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonDeviceWidget, DeleteUpdateButtonTeachersWidget


# from GUI.Dialogs.MouseClick import CustomTableWidget


class DeviceUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ips = ''
        self.ports = ''

    def cell_clicked(self):
        current_row = self.ui.tblDevice.currentRrow()
        mydialog = MyDialog()
        mydialog.accept()
        port_number = self.ui.tblDevice.item(current_row, 1).text()
        ip_address = self.ui.tblDevice.item(current_row, 2).text()
        mydialog.txtPortNumber.setText(port_number)
        mydialog.txtIPAddress.setText(ip_address)

    def use_ui_elements(self):
        # self.ui.tblDeviceUsers.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.ui.tblDeviceUsers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.ui.tblDeviceUsers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tblDevice.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblDevice.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblDevice.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnNewDevice.clicked.connect(self.device_connection)
        # self.ui.btnShowDeviceUsers.clicked.connect(self.show_device_users)

    def show_device_users(self):
        print("the show button is clicked")
        zk = ZK('192.168.1.201', port=4370, timeout=5)
        conn = zk.connect()
        if conn:
            conn.enable_device()
            users = conn.get_users()
            for user in users:
                if user.privilege == const.USER_ADMIN:
                    privilege = 'Admin'
                else:
                    privilege = 'User'
                operations_buttons = DeleteUpdateButtonTeachersWidget(table_widget=self.ui.tblDeviceUsers)
                current_row = self.ui.tblDevice.rowCount()
                self.ui.tblDeviceUsers.insertRow(current_row)
                self.ui.tblDeviceUsers.setItem(current_row, 0, QTableWidgetItem(user.user_id))
                self.ui.tblDeviceUsers.setItem(current_row, 1, QTableWidgetItem(user.name))
                self.ui.tblDeviceUsers.setItem(current_row, 2, QTableWidgetItem(user.password))
                self.ui.tblDeviceUsers.setItem(current_row, 3, QTableWidgetItem(str(privilege)))
                self.ui.tblDeviceUsers.setCellWidget(current_row, 4, operations_buttons.get_buttons('Old'))
                self.ui.tblDeviceUsers.setColumnWidth(current_row, 40)
                self.ui.tblDeviceUsers.setRowHeight(current_row, 150)
        else:
            QMessageBox.warning(self.ui, "تحذير", "لا يوجد جهاز بصمة متصل الآن")

    def device_connection(self):
        mydialog = MyDialog()
        if mydialog.exec_() == QDialog.Accepted:
            try:
                ip_address, port_number = mydialog.save_data()  # Call save_data() on mydialog instance
                if ip_address is not None and port_number is not None:
                    result = self.find_devices(ip_address, int(port_number))

                    if result is not None:
                        true, name, device_time, status = result
                        operations_buttons = DeleteUpdateButtonDeviceWidget(table_widget=self.ui.tblDevice)

                        current_row = self.ui.tblDevice.rowCount()
                        self.ui.tblDevice.insertRow(current_row)
                        self.ui.tblDevice.setItem(current_row, 0, QTableWidgetItem(name))
                        self.ui.tblDevice.setItem(current_row, 1, QTableWidgetItem(ip_address))
                        self.ui.tblDevice.setItem(current_row, 2, QTableWidgetItem(port_number))
                        self.ui.tblDevice.setItem(current_row, 3, QTableWidgetItem(str(device_time)))
                        self.ui.tblDevice.setItem(current_row, 4, QTableWidgetItem(status))
                        self.ui.tblDevice.setCellWidget(current_row, 5, operations_buttons)
                        self.ui.tblDevice.setColumnWidth(current_row, 40)
                        self.ui.tblDevice.setRowHeight(current_row, 150)

                    else:
                        QMessageBox.critical(self.ui, "تحذير", "جهاز البصمة غير موجود")
                else:
                    QMessageBox.critical(self.ui, "تحذير", "يجب ادخال عنوان IP و عنوان Port الخاص بجهاز البصمة")

            except Exception as e:
                error_message = "حدث خطأ:\n\n" + str(e)
                QMessageBox.critical(self.ui, "خطأ", error_message)

    def find_devices(self, i, p):
        global status  # Global variable=''
        try:
            zk = ZK(i, port=p, timeout=5)
            conn = zk.connect()

            if conn:
                status = 'متصل الان'
                device_time = conn.get_time()
                print("the time is: ", device_time)
                #
                print("the device is: ", device_time)
                name = conn.get_device_name()

                conn.enable_device()
                # # id = conn.get_device_id()
                # sn = conn.get_serialnumber()
                # # port = conn.get_device_port()
                # time = conn.get_time()
                # users = conn.get_users()
                #
                # # Populate the table with user data
                # self.ui.tblDevice.setRowCount(0)
                # userss = [1]  # Clear existing rows
                # for user in userss:
                #     name = QTableWidgetItem(name)
                #     ipadd = QTableWidgetItem(i)
                #     ports = QTableWidgetItem(str(p))
                #     time = QTableWidgetItem(str(time))
                #
                #     row_count = self.ui.tblDevice.rowCount()
                #     self.ui.tblDevice.insertRow(row_count)
                #     self.ui.tblDevice.setItem(row_count, 0, name)
                #     self.ui.tblDevice.setItem(row_count, 1, ipadd)
                #     self.ui.tblDevice.setItem(row_count, 2, ports)
                #     self.ui.tblDevice.setItem(row_count, 3, time)
                QMessageBox.information(self.ui, "نجح", "نجح الاتصال")
                return True, name, device_time, status
            else:
                status = 'مفقود الان'
                QMessageBox.warning(self.ui, "تحذير", "فشل الاتصال")
                return False, None, None, status
        except Exception as e:
            status = 'مفقود الان'
            QMessageBox.warning(self.ui, "تحذير", "فشل الاتصال")
            print("Connection Error:", str(e))
            return False, None, None, status
