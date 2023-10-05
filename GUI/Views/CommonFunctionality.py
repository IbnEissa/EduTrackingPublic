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

    def get_subjects(self):
        subjects = ["الرياضيات",
                    "العلوم",
                    "اللغة العربية",
                    "اللغة الإنجليزية",
                    "التاريخ",
                    "الجغرافيا",
                    "الفيزياء",
                    "الكيمياء",
                    "الأحياء",
                    "القران الكريم",
                    "التربية الوطنية",
                    "التربية الاسلامية",
                    "الاجتماعيات"
                    ]
        return subjects

    def get_days(self):
        days = ["السبت",
                "الاحد",
                "الاثنين",
                "الثلاثاء",
                "الاربعاء",
                "الخميس",
                ]
        return days

    def get_sessions(self):
        sessions = ["الاولى",
                    "الثانية",
                    "الثالثة",
                    "الرابعة",
                    "الخامسة",
                    "السادسة",
                    "السابعة",
                    "الثامنة",
                    ]
        return sessions

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

    def get_cities(self):
        cities = {
            "صنعاء": [
                "أمانة العاصمة",
                "أرحب",
                "الطيال",
                "بني ضبيان",
                "صعفان",
                "الحصن",
                "بلاد الروس",
                "جحانة",
                "مناخة",
                "الحيمة الخارجية",
                "بني حشيش",
                "خولان",
                "نهم",
                "الحيمة الداخلية",
                "بني مطر",
                "سنحان وبني بهلول",
                "همدان"
            ],
            "عدن": [
                "خور مكسر",
                "صيرة",
                "المعلا",
                "التواهي",
                "البريقة",
                "المنصورة",
                "الشيخ عثمان",
                "دارس سعد"
            ],
            "المحويت": [
                "شبام كوكبان",
                "الطويلة",
                "الرجم",
                "الخبت",
                "ملحان",
                "حفاش",
                "بني سعد",
                "مدينة المحويت",
                "المحويت"
            ],
            "ذمار": [
                "الحداء",
                "جهران",
                "جبل الشرق",
                "مغرب عنس",
                "عتمة",
                "وصاب العالي",
                "وصاب السافل",
                "مدينة ذمار",
                "ميفعة عنس",
                "عنس",
                "ضوران أنس",
                "المنار"
            ],
            "الجوف": [
                "الخب والشعف",
                "الحميدات",
                "المطه",
                "الزاهر",
                "الحزم",
                "المتون",
                "المصلوب",
                "الغيل",
                "الخلق",
                "برط العنان",
                "رجوزه",
                "خراب المراشي"
            ], "عمران": [
                "السود",
                "السودة",
                "العشة",
                "المدان",
                "بني صريم",
                "ثلاء",
                "جبل عيال يزيد",
                "حرف سفيان",
                "حوث",
                "خارف",
                "ذيبين",
                "ريدة",
                "شهارة",
                "صوير",
                "ظليمة حبور",
                "عمران",
                "عيال سريح",
                "قفلة عذر",
                "مسور"
            ],
            "البيضاء": [
                "البيضاء",
                "الرياشيه",
                "الزاهر",
                "السواديه",
                "الشرية",
                "الصومعه",
                "الطفة",
                "العرش",
                "القريشيه",
                "الملاجم",
                "ذي ناعم",
                "رداع",
                "ردمان",
                "صباح",
                "البيضاء",
                "مسورة",
                "مكيراس",
                "ناطع",
                "نعمان",
                "ولد ربيع"
            ],
            "حضرموت": [
                "الديس",
                "الريدة وقصيعر",
                "السوم",
                "الشحر",
                "الضليعه",
                "العبر",
                "القطن",
                "القف",
                "المكلا",
                "بروم ميفع",
                "تريم",
                "ثمود",
                "حجر",
                "حجر الصيعر",
                "حديبو",
                "حريضة",
                "دوعن",
                "رخيه",
                "رماه",
                "زمنخ ومنوخ",
                "ساه",
                "سيئون",
                "شبام",
                "عمد",
                "غيل با وزير",
                "غيل بن يمين",
                "قلنسية وعبد الكوري",
                "المكلا",
                "وادي العين",
                "يبعث"
            ],
            "صعدة": [
                "باقم",
                "قطابر",
                "منبه",
                "غمر",
                "رازح",
                "شداء",
                "الظاهر",
                "حيدان",
                "ساقين",
                "مجز",
                "سحار",
                "الصفراء",
                "الحشوه",
                "كتاف والبقع",
                "صعده"
            ],
            "شبوة": [
                "دهر",
                "الطلح",
                "جردان",
                "عرماء",
                "عسيلان",
                "عين",
                "بيحان",
                "مرخه العليا",
                "مرخه السلفى",
                "نصاب",
                "حطيب",
                "الصعيد",
                "عتق",
                "حبان",
                "الروضه",
                "ميفعه",
                "رضوم"
            ],
            "لحج": [
                "الحد",
                "الحوطة",
                "القبيطة",
                "المسيمير",
                "المضاربة والعارة",
                "المفلحي",
                "المقاطرة",
                "الملاح",
                "تبن",
                "حالمين",
                "جبيل جبر",
                "ردفان",
                "طور الباحة",
                "يافع",
                "يهر"
            ],
            "أرخبيل سقطرى": [
                "حديبو",
                "قلنسية وعبد الكوري"
            ],
            "المهرة": [
                "شحن",
                "حات",
                "حوف",
                "الغيظة",
                "منعر",
                "المسيلة",
                "سيحوت",
                "قشن",
                "حصوين"
            ],
            "الضالع": [
                "الأزرق",
                "الحشاء",
                "الحصين",
                "الشعيب",
                "الضالع",
                "جبن",
                "جحاف",
                "دمت",
                "قعطبة"
            ],
            "أبين": [
                "زنجبار",
                "المحفد",
                "مودية",
                "جيشان",
                "لودر",
                "سباح",
                "رصد",
                "سرار",
                "أحور",
                "خنفر",
                "الوضيع"
            ],
            "ريمة": [
                "بلاد الطعام",
                "السلفية",
                "الجبين",
                "مزهر",
                "كسمة",
                "الجعفرية"
            ],
            "مأرب": [
                "الجوبة",
                "العبدية",
                "بدبدة",
                "جبل مراد",
                "حريب",
                "حريب القرامش",
                "رحبة",
                "رغوان",
                "صرواح",
                "مأرب",
                "ماهلية",
                "مجزر",
                "مدغل الجدعان"
            ],
            "إب": [
                "إب",
                "الرضمة",
                "السبرة",
                "السدة",
                "السياني",
                "الشعر",
                "الظهار",
                "العدين",
                "القفر",
                "المخادر",
                "المشنة",
                "النادرة",
                "بعدان",
                "جبلة",
                "حبيش",
                "حزم العدين",
                "ذي السفال",
                "فرع العدين",
                "مذيخرة",
                "يريم"
            ],
            "حجة": [
                "أسلم",
                "أفلح الشام",
                "أفلح اليمن",
                "الجميمة",
                "الشاهل",
                "الشغادرة",
                "المحابشة",
                "المغربة",
                "المفتاح",
                "بكيل المير",
                "بني العوام",
                "بني قيس الطور",
                "حجة",
                "حرض",
                "حيران",
                "خيران المحرق",
                "شرس",
                "عبس",
                "قارة",
                "قفل شمر",
                "كحلان الشرف",
                "وضرة",
                "كحلان عفار",
                "كشر",
                "كعيدنة",
                "مبين",
                "مدينة حجة",
                "مستباء",
                "ميدي",
                "نجرة",
                "وشحة"
            ],
            "تعز": [
                "التعزية",
                "جبل حبشي",
                "حيفان",
                "خدير",
                "ذباب",
                "سامع",
                "شرعب الرونة",
                "شرعب السلام",
                "الشمايتين",
                "صالة",
                "صبر الموادم",
                "الصلو",
                "القاهرة",
                "ماوية",
                "المخاء",
                "المسراخ",
                "مشرعة وحدنان",
                "المظفر",
                "المعافر",
                "مقبنة",
                "المواسط",
                "موزع",
                "الوازعية"
            ],
            "الحديدة": [
                "الزهرة",
                "اللحية",
                "كمران",
                "الصلي",
                "المنيرة",
                "القناوص",
                "الزيدية",
                "المغلا",
                "الضحى",
                "باجل",
                "الحجيلة",
                "برع",
                "المراوعة",
                "الدريهمي",
                "السخنة",
                "المنصورية",
                "بيت الفقيه",
                "جبل راس",
                "حيس",
                "الخوخة",
                "الحوك",
                "الميناء",
                "الحالي",
                "زبيد",
                "الجراحي",
                "التحيتا"
            ]
        }
        return cities

    def style_table_widget(self, table_widget):
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for row in range(table_widget.rowCount()):
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                if item is not None:
                    item.setTextAlignment(Qt.AlignCenter)
