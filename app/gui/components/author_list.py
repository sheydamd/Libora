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
        

        add_btn = QPushButton("+")



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

