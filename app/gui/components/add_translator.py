from PyQt5.QtWidgets import (
    QDialog,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QMessageBox
)

from app.api.adapters.translator_data_adapter import TranslatorsDataAdapter
from app.api.models.translator import Translator


class AddTranslatorDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Translator")

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
            "Grade",
            self.grade
        )

        save_btn = QPushButton("Save")

        layout.addWidget(save_btn)

        save_btn.clicked.connect(
            self.save
        )

    def save(self):

        national_code = self.national_code.text().strip()
        name = self.name.text().strip()
        last_name = self.last_name.text().strip()
        grade = self.grade.text().strip()

        if not all([
            national_code,
            name,
            last_name,
            grade
        ]):

            QMessageBox.warning(
                self,
                "Error",
                "All fields are required."
            )

            return

        try:

            translator = Translator(
                national_code,
                name,
                last_name,
                grade
            )

            TranslatorsDataAdapter.insert(
                translator
            )

            QMessageBox.information(
                self,
                "Success",
                "Translator added successfully."
            )

            self.accept()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )