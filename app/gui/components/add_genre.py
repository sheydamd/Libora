from PyQt5.QtWidgets import (
    QDialog,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QMessageBox
)

from app.api.adapters.genre_data_adapter import GenresDataAdapter
from app.api.models.genre import Genre


class AddGenreDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Genre")

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

            genre = Genre(name)

            GenresDataAdapter.insert(
                genre
            )

            QMessageBox.information(
                self,
                "Success",
                "Genre added successfully."
            )

            self.accept()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )