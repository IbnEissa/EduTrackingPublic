import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from peewee import MySQLDatabase, Model, CharField

# Importing required libraries
import mysql.connector
from playhouse.db_url import connect


class Student(Model):
    name = CharField()
    age = CharField()

    class Meta:
        database = None


class Teacher(Model):
    name = CharField()
    subject = CharField()

    class Meta:
        database = None


class DatabaseCreationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Create Database')
        self.setup_ui()

    def setup_ui(self):
        self.label = QLabel('Database Name:', self)
        self.label.move(20, 20)

        self.text_input = QLineEdit(self)
        self.text_input.move(120, 20)

        self.create_button = QPushButton('Create', self)
        self.create_button.move(120, 50)
        self.create_button.clicked.connect(self.create_database)

    def create_database(self):
        database_name = self.text_input.text()

        # Connect to MySQL server
        dataBase = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=""
        )

        # Create a cursor object
        cursorObject = dataBase.cursor()

        # Create database
        cursorObject.execute(f"CREATE DATABASE {database_name}")

        # Close the cursor and database connection
        cursorObject.close()
        dataBase.close()

        print(f"Database '{database_name}' created successfully!")

        # Connect to the newly created database
        db = MySQLDatabase(database=database_name, user="root", passwd="")
        Student._meta.database = db
        Teacher._meta.database = db

        # Create the Student table
        db.create_tables([Student])
        print("Student table created successfully!")
        # Create the Teacher table
        db.create_tables([Teacher])
        print("Teacher table created successfully!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DatabaseCreationWidget()
    widget.show()
    sys.exit(app.exec_())
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
# from peewee import MySQLDatabase, Model, CharField
#
# # Importing required libraries
# import mysql.connector
# from playhouse.db_url import connect
#
#
# class Student(Model):
#     name = CharField()
#     age = CharField()
#
#     class Meta:
#         database = None
#
#
# class Teacher(Model):
#     name = CharField()
#     subject = CharField()
#
#     class Meta:
#         database = None
#
#
# class DatabaseCreationWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Create Database')
#         self.setup_ui()
#
#     def setup_ui(self):
#         self.label_db_name = QLabel('Database Name:', self)
#         self.label_db_name.move(20, 20)
#
#         self.text_input_db_name = QLineEdit(self)
#         self.text_input_db_name.move(120, 20)
#
#         self.label_username = QLabel('Username:', self)
#         self.label_username.move(20, 50)
#
#         self.text_input_username = QLineEdit(self)
#         self.text_input_username.move(120, 50)
#
#         self.label_password = QLabel('Password:', self)
#         self.label_password.move(20, 80)
#
#         self.text_input_password = QLineEdit(self)
#         self.text_input_password.setEchoMode(QLineEdit.Password)
#         self.text_input_password.move(120, 80)
#
#         self.create_button = QPushButton('Create', self)
#         self.create_button.move(120, 110)
#         self.create_button.clicked.connect(self.create_database)
#
#     def create_database(self):
#         database_name = self.text_input_db_name.text()
#         username = self.text_input_username.text()
#         password = self.text_input_password.text()
#
#         # Connect to MySQL server
#         dataBase = mysql.connector.connect(
#             host="localhost",
#             user=username,
#             passwd=password
#         )
#
#         # Create a cursor object
#         cursorObject = dataBase.cursor()
#
#         # Create database
#         cursorObject.execute(f"CREATE DATABASE {database_name}")
#
#         # Close the cursor and database connection
#         cursorObject.close()
#         dataBase.close()
#
#         print(f"Database '{database_name}' created successfully!")
#
#         # Connect to the newly created database
#         db = MySQLDatabase(database=database_name, user=username, passwd=password)
#         Student._meta.database = db
#         Teacher._meta.database = db
#
#         # Create the Student table
#         db.create_tables([Student])
#
#         print("Student table created successfully!")
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     widget = DatabaseCreationWidget()
#     widget.show()
#     sys.exit(app.exec_())