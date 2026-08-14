from PyQt5.QtWidgets import (
    QDialog,
    QLineEdit,
    QTextEdit,
    QFormLayout,
    QPushButton,
    QMessageBox,
    QComboBox
)

from app.api.adapters.book_data_adapter import BooksDataAdapter
from app.api.adapters.author_data_adapter import AuthorsDataAdapter
from app.api.adapters.translator_data_adapter import TranslatorsDataAdapter
from app.api.adapters.genre_data_adapter import GenresDataAdapter
from app.api.adapters.language_data_adapter import LanguagesDataAdapter
from app.api.adapters.resources_data_adapter import ResourcesDataAdapter
from app.api.adapters.esrb_data_adapter import EsrbsDataAdapter
from app.api.adapters.publishers_data_adapter import PublishersDataAdapter

from app.api.models.book import Book

from app.gui.components.multi_select import (
    MultiSelectWidget
)


class AddBookDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle(
            "Add Book"
        )

        self.resize(
            500,
            650
        )

        layout = QFormLayout(self)

        # ==================================
        # Basic Information
        # ==================================

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

        # ==================================
        # ESRB
        # ==================================

        self.esrbs = (
            EsrbsDataAdapter.get_all()
        )

        self.esrb_combo = QComboBox()

        self.esrb_combo.addItem(
            "Select ESRB",
            None
        )

        for esrb in self.esrbs:

            self.esrb_combo.addItem(
                str(esrb.name),
                esrb
            )

        layout.addRow(
            "ESRB",
            self.esrb_combo
        )

        # ==================================
        # Publisher
        # ==================================

        self.publishers = (
            PublishersDataAdapter.get_all()
        )

        self.publisher_combo = QComboBox()

        self.publisher_combo.addItem(
            "Select Publisher",
            None
        )

        for publisher in self.publishers:

            self.publisher_combo.addItem(
                str(publisher.name),
                publisher
            )

        layout.addRow(
            "Publisher",
            self.publisher_combo
        )

        # ==================================
        # Authors
        # ==================================

        self.authors = (
            AuthorsDataAdapter.get_all()
        )

        self.author_select = MultiSelectWidget(
            self.authors,
            "Authors",
            self
        )

        layout.addRow(
            "Authors",
            self.author_select
        )

        # ==================================
        # Translators
        # ==================================

        self.translators = (
            TranslatorsDataAdapter.get_all()
        )

        self.translator_select = MultiSelectWidget(
            self.translators,
            "Translators",
            self
        )

        layout.addRow(
            "Translators",
            self.translator_select
        )

        # ==================================
        # Genres
        # ==================================

        self.genres = (
            GenresDataAdapter.get_all()
        )

        self.genre_select = MultiSelectWidget(
            self.genres,
            "Genres",
            self
        )

        layout.addRow(
            "Genres",
            self.genre_select
        )

        # ==================================
        # Languages
        # ==================================

        self.languages = (
            LanguagesDataAdapter.get_all()
        )

        self.language_select = MultiSelectWidget(
            self.languages,
            "Languages",
            self
        )

        layout.addRow(
            "Languages",
            self.language_select
        )

        # ==================================
        # Resources
        # ==================================

        self.resources = (
            ResourcesDataAdapter.get_all()
        )

        self.resource_select = MultiSelectWidget(
            self.resources,
            "Resources",
            self
        )

        layout.addRow(
            "Resources",
            self.resource_select
        )

        # ==================================
        # Save
        # ==================================

        save_btn = QPushButton(
            "Save"
        )

        save_btn.setObjectName(
            "saveButton"
        )

        save_btn.clicked.connect(
            self.save
        )

        layout.addRow(
            save_btn
        )


    # ======================================
    # Save
    # ======================================

    def save(self):

        name = self.name.text().strip()

        title = self.title.text().strip()

        description = (
            self.description
            .toPlainText()
            .strip()
        )

        esrb = (
            self.esrb_combo
            .currentData()
        )

        publisher = (
            self.publisher_combo
            .currentData()
        )

        authors = (
            self.author_select
            .get_selected_items()
        )

        translators = (
            self.translator_select
            .get_selected_items()
        )

        genres = (
            self.genre_select
            .get_selected_items()
        )

        languages = (
            self.language_select
            .get_selected_items()
        )

        resources = (
            self.resource_select
            .get_selected_items()
        )

        # ==================================
        # Validation
        # ==================================

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
                "Please select ESRB."
            )

            return

        if not publisher:

            QMessageBox.warning(
                self,
                "Error",
                "Please select Publisher."
            )

            return

        # ==================================
        # Create Book
        # ==================================

        book = Book(
            name,
            title,
            description,
            esrb,
            publisher,
            resources,
            authors,
            translators,
            genres,
            languages
        )

        # ==================================
        # Insert
        # ==================================

        try:

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