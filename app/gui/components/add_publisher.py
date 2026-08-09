from PyQt5.QtWidgets import (
    QDialog,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QMessageBox
)

from app.api.adapters.publishers_data_adapter import PublishersDataAdapter
from app.api.models.publisher import Publisher


class AddPublisherDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Publisher")

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

            publisher = Publisher(name)

            PublishersDataAdapter.insert(
                publisher
            )

            QMessageBox.information(
                self,
                "Success",
                "Publisher added successfully."
            )

            self.accept()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )