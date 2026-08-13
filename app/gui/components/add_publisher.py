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

        # Fields
        self.name = QLineEdit()
        self.address = QLineEdit()
        self.phone_number = QLineEdit()
        self.fax_number = QLineEdit()
        self.email = QLineEdit()
        self.establish_date = QLineEdit()

        layout.addRow(
            "Name",
            self.name
        )

        layout.addRow(
            "Address",
            self.address
        )

        layout.addRow(
            "Phone Number",
            self.phone_number
        )

        layout.addRow(
            "Fax Number",
            self.fax_number
        )

        layout.addRow(
            "Email",
            self.email
        )

        layout.addRow(
            "Establish Date",
            self.establish_date
        )

        # Save button
        save_btn = QPushButton("Save")

        layout.addWidget(
            save_btn
        )

        save_btn.clicked.connect(
            self.save
        )


    def save(self):

        name = self.name.text().strip()
        address = self.address.text().strip()
        phone_number = self.phone_number.text().strip()
        fax_number = self.fax_number.text().strip()
        email = self.email.text().strip()
        establish_date = self.establish_date.text().strip()

        # Validation
        if (
            not name
            or not address
            or not phone_number
            or not fax_number
            or not email
            or not establish_date
        ):

            QMessageBox.warning(
                self,
                "Error",
                "All fields are required."
            )

            return

        try:

            publisher = Publisher(
                name,
                address,
                phone_number,
                fax_number,
                email,
                establish_date
            )

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