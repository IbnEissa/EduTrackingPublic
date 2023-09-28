from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView


class Common:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui

    def use_ui_elements(self):
        self.ui.btnHome.clicked.connect(self.home_button_clicked)
        self.ui.btnManagement.clicked.connect(self.btn_management_clicked)
        self.ui.btnEmpsMovement.clicked.connect(self.btn_emp_movement)
        self.ui.btnReports.clicked.connect(self.reports_button_clicked)
        self.ui.btnArchive.clicked.connect(self.archive_button_clicked)
        self.ui.btnSettings.clicked.connect(self.settings_button_clicked)
        self.ui.tabMainTab.tabBar().setVisible(False)
        self.ui.tabMainTab.setCurrentIndex(0)

    def home_button_clicked(self):
        self.ui.tabMainTab.setCurrentIndex(0)

    def settings_button_clicked(self):
        self.ui.tabMainTab.setCurrentIndex(5)
        self.ui.tabSettings.setCurrentIndex(0)

    def btn_management_clicked(self):
        self.ui.tabMainTab.setCurrentIndex(1)
        self.ui.tabDataManagement.setCurrentIndex(0)

    def btn_emp_movement(self):
        self.ui.tabMainTab.setCurrentIndex(2)
        self.ui.tabEmpsMovement.setCurrentIndex(0)

    def reports_button_clicked(self):
        self.ui.tabMainTab.setCurrentIndex(4)
        self.ui.tabTeachersReports.setCurrentIndex(0)

    def archive_button_clicked(self):
        self.ui.tabMainTab.setCurrentIndex(4)

    def get_combo_box_data(self, table_model, column_name, where_clause=None):
        query = table_model.select(getattr(table_model, column_name)).distinct()
        print(f"The where clause is: {where_clause}")
        if where_clause is not None:
            query = query.where(where_clause)
        items = []
        for data in query:
            item_value = getattr(data, column_name)
            items.append(str(item_value))
        return items

    def style_table_widget(self, table_widget):
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for row in range(table_widget.rowCount()):
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                if item is not None:
                    item.setTextAlignment(Qt.AlignCenter)
