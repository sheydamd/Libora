from PyQt5.QtWidgets import (
    QDialog,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QMessageBox
)

from app.api.adapters.resources_data_adapter import ResourcesDataAdapter
from app.api.models.resource import Resource


class AddResourceDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Resource")

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

            resource = Resource(name)

            ResourcesDataAdapter.insert(
                resource
            )

            QMessageBox.information(
                self,
                "Success",
                "Resource added successfully."
            )

            self.accept()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )