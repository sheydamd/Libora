from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QHBoxLayout
)
from PyQt5.QtCore import Qt

from app.api.adapters.genre_data_adapter import GenresDataAdapter


class SelectGenresDialog(QDialog):

    def __init__(self, selected=None, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Select Genres")

        self.selected = selected or []

        layout = QVBoxLayout(self)

        self.list_widget = QListWidget()

        genres = GenresDataAdapter.get_all()

        selected_ids = {
            genre.id
            for genre in self.selected
        }

        for genre in genres:

            item = QListWidgetItem(
                genre.name
            )

            item.setData(
                Qt.UserRole,
                genre
            )

            item.setCheckState(
                Qt.Checked
                if genre.id in selected_ids
                else Qt.Unchecked
            )

            self.list_widget.addItem(item)

        layout.addWidget(self.list_widget)

        buttons = QHBoxLayout()

        cancel_btn = QPushButton("Cancel")
        select_btn = QPushButton("Select")

        buttons.addWidget(cancel_btn)
        buttons.addWidget(select_btn)

        layout.addLayout(buttons)

        cancel_btn.clicked.connect(
            self.reject
        )

        select_btn.clicked.connect(
            self.select
        )

    def select(self):

        self.selected = []

        for i in range(
            self.list_widget.count()
        ):

            item = self.list_widget.item(i)

            if item.checkState() == Qt.Checked:

                self.selected.append(
                    item.data(Qt.UserRole)
                )

        self.accept()