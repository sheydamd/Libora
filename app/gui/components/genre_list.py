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

from app.api.adapters.genre_data_adapter import GenresDataAdapter
from app.api.models.genre import Genre


class GenresWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search genre...")
        self.search_box.textChanged.connect(self.search_genres)


        search_layout.addWidget(self.search_box)


        self.layout.addLayout(search_layout)


        self.list_layout = QVBoxLayout()
        self.layout.addLayout(self.list_layout)


        self.all_genres = GenresDataAdapter.get_all()

        self.show_genres(self.all_genres)



    def clear_list(self):

        while self.list_layout.count():

            item = self.list_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()



    def show_genres(self, genres):

        self.clear_list()

        title = QLabel("Genre List")
        title.setAlignment(Qt.AlignCenter)

        self.list_layout.addWidget(title)


        if not genres:
            self.list_layout.addWidget(
                QLabel("No Genre found")
            )
            return


        for genre in genres:

            btn = QPushButton(
                genre.name
            )

            self.list_layout.addWidget(btn)


        self.list_layout.addStretch()



    def search_genres(self,text):

        text = text.lower().strip()

        if not text:
            self.show_genres(self.all_genres)
            return


        filtered = [
            genre
            for genre in self.all_genres
            if genre.name.lower().startswith(text)
        ]

        self.show_genres(filtered)


