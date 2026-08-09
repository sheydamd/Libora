from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QComboBox,
    QHBoxLayout,
    QWidget,
    QMessageBox
)

from app.api.models.book import Book

from app.api.adapters.book_data_adapter import BooksDataAdapter
from app.api.adapters.esrb_data_adapter import EsrbsDataAdapter
from app.api.adapters.publishers_data_adapter import PublishersDataAdapter



class AddBookDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Add Book")

        self.authors = []
        self.translators = []
        self.genres = []
        self.languages = []
        self.resources = []

        layout = QFormLayout(self)

        self.name = QLineEdit()
        self.title = QLineEdit()
        self.description = QTextEdit()

        layout.addRow(
            "Name",
            self.name
        )

        layout.addRow(
            "Title",
            self.title
        )

        layout.addRow(
            "Description",
            self.description
        )

        # ESRB

        self.esrb = QComboBox()

        self.esrbs = EsrbsDataAdapter.get_all()

        self.esrb.addItem(
            "Select ESRB",
            None
        )

        for esrb in self.esrbs:

            self.esrb.addItem(
                str(esrb.name),
                esrb
            )

        layout.addRow(
            "ESRB",
            self.esrb
        )

        # Publisher

        self.publisher = QComboBox()

        self.publishers = PublishersDataAdapter.get_all()

        self.publisher.addItem(
            "Select Publisher",
            None
        )

        for publisher in self.publishers:

            self.publisher.addItem(
                str(publisher.name),
                publisher
            )

        layout.addRow(
            "Publisher",
            self.publisher
        )

        # Authors

        self.author_btn = QPushButton(
            "Select Authors"
        )

        self.author_btn.clicked.connect(
            self.select_authors
        )

        layout.addRow(
            "Authors",
            self.author_btn
        )

        # Translators

        self.translator_btn = QPushButton(
            "Select Translators"
        )

        self.translator_btn.clicked.connect(
            self.select_translators
        )

        layout.addRow(
            "Translators",
            self.translator_btn
        )

        # Genres

        self.genre_btn = QPushButton(
            "Select Genres"
        )

        self.genre_btn.clicked.connect(
            self.select_genres
        )

        layout.addRow(
            "Genres",
            self.genre_btn
        )

        # Languages

        self.language_btn = QPushButton(
            "Select Languages"
        )

        self.language_btn.clicked.connect(
            self.select_languages
        )

        layout.addRow(
            "Languages",
            self.language_btn
        )

        # Resources

        self.resource_btn = QPushButton(
            "Select Resources"
        )

        self.resource_btn.clicked.connect(
            self.select_resources
        )

        layout.addRow(
            "Resources",
            self.resource_btn
        )

        # Save

        save_btn = QPushButton(
            "Save"
        )

        layout.addWidget(
            save_btn
        )

        save_btn.clicked.connect(
            self.save
        )


    def select_authors(self):

        dialog = SelectAuthorsDialog(
            self.authors,
            self
        )

        if dialog.exec_():

            self.authors = dialog.selected

            self.author_btn.setText(f"{len(self.authors)} selected"
            )


    def select_translators(self):

        dialog = SelectTranslatorsDialog(
            self.translators,
            self
        )

        if dialog.exec_():

            self.translators = dialog.selected

            self.translator_btn.setText(
                f"{len(self.translators)} selected"
            )


    def select_genres(self):

        dialog = SelectGenresDialog(
            self.genres,
            self
        )

        if dialog.exec_():

            self.genres = dialog.selected

            self.genre_btn.setText(
                f"{len(self.genres)} selected"
            )


    def select_languages(self):

        dialog = SelectLanguagesDialog(
            self.languages,
            self
        )

        if dialog.exec_():

            self.languages = dialog.selected

            self.language_btn.setText(
                f"{len(self.languages)} selected"
            )


    def select_resources(self):

        dialog = SelectResourcesDialog(
            self.resources,
            self
        )

        if dialog.exec_():

            self.resources = dialog.selected

            self.resource_btn.setText(
                f"{len(self.resources)} selected"
            )


    def save(self):

        name = self.name.text().strip()
        title = self.title.text().strip()
        description = self.description.toPlainText().strip()

        esrb = self.esrb.currentData()
        publisher = self.publisher.currentData()

        if not name:

            QMessageBox.warning(
                self,
                "Error",
                "Book name is required."
            )

            return

        if not title:

            QMessageBox.warning(
                self,
                "Error",
                "Book title is required."
            )

            return

        if not esrb:

            QMessageBox.warning(
                self,
                "Error",
                "Please select an ESRB."
            )

            return

        if not publisher:

            QMessageBox.warning(
                self,
                "Error",
                "Please select a publisher."
            )

            return

        try:

            book = Book(
                name,
                title,
                description,
                esrb,
                publisher,
                self.resources,
                self.authors,
                self.translators,
                self.genres,
                self.languages
            )

            BooksDataAdapter.insert(
                book
            )

            QMessageBox.information(
                self,
                "Success",
                "Book added successfully."
            )

            self.accept()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )