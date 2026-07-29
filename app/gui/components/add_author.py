from PyQt5.QtWidgets import (
    QDialog,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QMessageBox
)

from app.api.adapters.author_data_adapter import AuthorsDataAdapter
from app.api.models.author import Author


class AddAuthorDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Author")

        layout = QFormLayout(self)

        self.national_code = QLineEdit()
        self.name = QLineEdit()
        self.last_name = QLineEdit()
        self.birthday = QLineEdit()
        self.grade = QLineEdit()

        layout.addRow(
            "National Code",
            self.national_code
        )

        layout.addRow(
            "Name",
            self.name
        )

        layout.addRow(
            "Last Name",
            self.last_name
        )

        layout.addRow(
            "Birthday",
            self.birthday
        )

        layout.addRow(
            "Grade",
            self.grade
        )

        save_btn = QPushButton("Save")

        layout.addWidget(
            save_btn
        )

        save_btn.clicked.connect(
            self.save
        )
        save_btn.setObjectName("addButton")


    def save(self):

        national_code = self.national_code.text().strip()
        name = self.name.text().strip()
        last_name = self.last_name.text().strip()
        birthday = self.birthday.text().strip()
        grade = self.grade.text().strip()

        if not national_code or not name or not last_name or not birthday or not grade:

            QMessageBox.warning(
                self,
                "Error",
                "All fields are required."
            )

            return

        try:

            author = Author(
                national_code,
                name,
                last_name,
                birthday,
                grade
            )

            AuthorsDataAdapter.insert(
                author
            )

            QMessageBox.information(
                self,
                "Success",
                "Author added successfully."
            )

            self.accept()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )