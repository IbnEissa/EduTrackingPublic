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
        self.ui.tabMainTab.setCurrentIndex(6)
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
