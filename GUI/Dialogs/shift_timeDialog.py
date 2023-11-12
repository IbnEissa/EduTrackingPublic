import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QEvent, QTime
from PyQt5.QtGui import QKeyEvent
from PyQt5.uic import loadUi


class Shift_timedialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("shiftDialog.ui", self)
        self.btnSaveshift.clicked.connect(self.save_data_shift)
        self.btnCancelAddingshift.clicked.connect(self.reject)

        self.txtshift_name.installEventFilter(self)
        self.txtshift_Type.installEventFilter(self)
        self.timeStartEnter.installEventFilter(self)
        self.timeEndEnter.installEventFilter(self)

        self.timeDelay.installEventFilter(self)
        self.timeStartOut.installEventFilter(self)
        self.timeEndOut.installEventFilter(self)
        self.txtPayPerShift.installEventFilter(self)

        self.setTabOrder(self.btnSaveshift, self.btnCancelAddingshift)

    def eventFilter(self, obj, event):
        if obj == self.txtshift_name and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtshift_Type.setFocus()
            return True
        elif obj == self.txtshift_Type and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.timeStartEnter.setFocus()
            return True
        elif obj == self.timeStartEnter and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.timeEndEnter.setFocus()
            return True
        elif obj == self.timeEndEnter and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.timeDelay.setFocus()
            return True
        elif obj == self.timeDelay and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.timeStartOut.setFocus()
            return True
        elif obj == self.timeStartOut and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.timeEndOut.setFocus()
            return True
        elif obj == self.timeEndOut and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtPayPerShift.setFocus()
            return True
        elif obj == self.txtPayPerShift and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnSaveshift.setFocus()
            return True

        return super().eventFilter(obj, event)

    def save_data_shift(self):
        try:
            name = self.txtshift_name.toPlainText()
            shift_Type = self.txtshift_Type.toPlainText()
            entry_start_time = self.timeStartEnter.time().toPyTime()
            entry_end_time = self.timeEndEnter.time().toPyTime()
            delay_times = self.timeDelay.toPlainText()
            checkout_start_time = self.timeStartOut.time().toPyTime()
            checkout_end_time = self.timeEndOut.time().toPyTime()
            pay_per_shift = self.txtPayPerShift.toPlainText()

            entry_start_time_str = entry_start_time.strftime('%H:%M')
            entry_end_time_str = entry_end_time.strftime('%H:%M')
            checkout_start_time_str = checkout_start_time.strftime('%H:%M')
            checkout_end_time_str = checkout_end_time.strftime('%H:%M')

            if name == "":
                raise ValueError("يجب ادخال الاسم ")
            if shift_Type == "":
                raise ValueError("يجب ادخال نوع الوردية  ")
            if entry_start_time == "":
                raise ValueError("يجب ادخال  وقت بداية الدخول ")
            if entry_end_time == "":
                raise ValueError("يجب ادخال  وقت نهاية الدخول ")
            if delay_times == "":
                raise ValueError("يجب ادخال   الوقت التاخير ")
            if checkout_start_time == "":
                raise ValueError("يجب ادخال  وقت بداية الخروج ")
            if checkout_end_time == "":
                raise ValueError("يجب ادخال  وقت نهاية الخروج ")
            if pay_per_shift == "":
                raise ValueError("يجب ادخال الاجر ")
            self.accept()
            return name, shift_Type, entry_start_time_str, entry_end_time_str, delay_times, checkout_start_time_str, checkout_end_time_str, pay_per_shift

        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None, None, None, None, None
