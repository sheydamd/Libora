from PyQt5.QtWidgets import (
    QDialog,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QMessageBox
)

from app.api.adapters.language_data_adapter import LanguagesDataAdapter
from app.api.models.language import Language


class AddLanguageDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Language")

        layout = QFormLayout(self)

        self.name = QLineEdit()

        layout.addRow(
            "Name",
            self.name
        )

        save_btn = QPushButton("Save")

        layout.addWidget(save_btn)

        save_btn.clicked.connect(
            self.save
        )

    def save(self):

        name = self.name.text().strip()

        if not name:

            QMessageBox.warning(
                self,
                "Error",
                "Name is required."
            )

            return

        try:

            language = Language(name)

            LanguagesDataAdapter.insert(
                language
            )

            QMessageBox.information(
                self,
                "Success",
                "Language added successfully."
            )

            self.accept()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )