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

        self.title = QLineEdit()
        self.type = QLineEdit()
        self.establish_date = QLineEdit()

        layout.addRow(
            "Title",
            self.title
        )

        layout.addRow(
            "Type",
            self.type
        )

        layout.addRow(
            "Establish Date",
            self.establish_date
        )

        save_btn = QPushButton("Save")

        layout.addWidget(save_btn)

        save_btn.clicked.connect(
            self.save
        )


    def save(self):

        title = self.title.text().strip()
        resource_type = self.type.text().strip()
        establish_date = self.establish_date.text().strip()

        if not title or not resource_type or not establish_date:

            QMessageBox.warning(
                self,
                "Error",
                "All fields are required."
            )

            return

        try:

            resource = Resource(
                title,
                resource_type,
                establish_date
            )

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