from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFormLayout,
    QDialog,
    QMessageBox,
    QHBoxLayout
)

from PyQt5.QtCore import Qt

from app.api.adapters.publishers_data_adapter import PublishersDataAdapter
from app.api.models.publisher import Publisher


class PublishersWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # Search + Add Button
        search_layout = QHBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search publisher...")
        self.search_box.textChanged.connect(self.search_publishers)

        add_btn = QPushButton("+")
        add_btn.setObjectName("addButton")
        

        add_btn.clicked.connect(self.add_publisher)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(add_btn)

        self.layout.addLayout(search_layout)

        # Author list
        self.list_layout = QVBoxLayout()
        self.layout.addLayout(self.list_layout)

        self.all_publisher = PublishersDataAdapter.get_all()

        self.show_publishers(self.all_publisher)


    def clear_list(self):

        while self.list_layout.count():

            item = self.list_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()


    def show_publishers(self,publishers):

        self.clear_list()

        title = QLabel("Publisher List")
        title.setAlignment(Qt.AlignCenter)

        self.list_layout.addWidget(title)

        if not publishers:
            self.list_layout.addWidget(QLabel("No Publisher found"))
            return


        for publisher in publishers:

            full_name = f"{publisher.name}"

            btn = QPushButton(full_name)

            self.list_layout.addWidget(btn)


        self.list_layout.addStretch()


    def search_publishers(self, text):

        text = text.lower().strip()

        if not text:
            self.publishers(self.all_publishers)
            return


        filtered = [
            Publisher
            for publisher in self.all_publisher
            if (
                publisher.name.lower().startswith(text)
                or f"{publisher.name}".lower().startswith(text)
            )
        ]

        self.show_publishers(filtered)


    def add_publisher(self):

        dialog = QDialog(self)
        dialog.setWindowTitle("+")

        layout = QFormLayout(dialog)


        national_code = QLineEdit()
        name = QLineEdit()
        last_name = QLineEdit()
        birthday = QLineEdit()
        grade = QLineEdit()


        layout.addRow("National Code", national_code)
        layout.addRow("Name", name)
        layout.addRow("Last Name", last_name)
        layout.addRow("Birthday", birthday)
        layout.addRow("Grade", grade)


        save_btn = QPushButton("Save")

        layout.addWidget(save_btn)


        def save():

            if not name.text() or not last_name.text():

                QMessageBox.warning(
                    self,
                    "Error",
                    "Name and Last Name are required."
                )
                return


            publisher = Publisher(
                national_code.text(),
                name.text(),
                last_name.text(),
                birthday.text(),
                grade.text()
            )


            PublishersDataAdapter.insert(publisher)


            QMessageBox.information(
                self,
                "Success",
                "Publisher added successfully."
            )


            # Refresh list
            self.all_publishers =PublishersDataAdapter.get_all()
            self.show_publishers(self.all_publisher)


            dialog.accept()


        save_btn.clicked.connect(save)


        dialog.exec_()