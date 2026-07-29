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

from app.api.adapters.author_data_adapter import AuthorsDataAdapter
from app.api.models.author import Author


class AuthorsWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # Search + Add Button
        search_layout = QHBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search author...")
        self.search_box.textChanged.connect(self.search_authors)

        add_btn = QPushButton("+")
        add_btn.setObjectName("addButton")

        add_btn.clicked.connect(self.add_author)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(add_btn)

        self.layout.addLayout(search_layout)

        # Author list
        self.list_layout = QVBoxLayout()
        self.layout.addLayout(self.list_layout)

        self.all_authors = AuthorsDataAdapter.get_all()

        self.show_authors(self.all_authors)


    def clear_list(self):

        while self.list_layout.count():

            item = self.list_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()


    def show_authors(self, authors):

        self.clear_list()

        title = QLabel("Author List")
        title.setAlignment(Qt.AlignCenter)

        self.list_layout.addWidget(title)

        if not authors:
            self.list_layout.addWidget(QLabel("No Author found"))
            return


        for author in authors:

            full_name = f"{author.name} {author.last_name}"

            btn = QPushButton(full_name)

            self.list_layout.addWidget(btn)


        self.list_layout.addStretch()


    def search_authors(self, text):

        text = text.lower().strip()

        if not text:
            self.show_authors(self.all_authors)
            return


        filtered = [
            author
            for author in self.all_authors
            if (
                author.name.lower().startswith(text)
                or author.last_name.lower().startswith(text)
                or f"{author.name} {author.last_name}".lower().startswith(text)
            )
        ]

        self.show_authors(filtered)


    def add_author(self):

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

            if (
                not national_code.text().strip()
                or not name.text().strip()
                or not last_name.text().strip()
                or not birthday.text().strip()
                or not grade.text().strip()
            ):
                QMessageBox.warning(
                    self,
                    "Error",
                    "All fields are required."
                )
                return

            author = Author(
                national_code.text().strip(),
                name.text().strip(),
                last_name.text().strip(),
                birthday.text().strip(),
                grade.text().strip()
            )

            AuthorsDataAdapter.insert(author)

            QMessageBox.information(
                self,
                "Success",
                "Author added successfully."
            )

            self.all_authors = AuthorsDataAdapter.get_all()

            self.show_authors(
                self.all_authors
            )

            dialog.accept()


        save_btn.clicked.connect(save)


        dialog.exec_()