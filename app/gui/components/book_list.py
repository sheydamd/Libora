from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QHBoxLayout
)

from PyQt5.QtCore import Qt

from app.api.adapters.book_data_adapter import BooksDataAdapter
from app.gui.components.add_book import AddBookDialog


class BooksWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)

        # =========================
        # Search + Add Button
        # =========================

        search_layout = QHBoxLayout()

        self.search_box = QLineEdit()

        self.search_box.setPlaceholderText(
            "Search book..."
        )

        search_layout.addWidget(
            self.search_box
        )

        add_btn = QPushButton("+")

        add_btn.setObjectName(
            "addButton"
        )

        add_btn.setMinimumWidth(40)

        search_layout.addWidget(
            add_btn
        )

        self.main_layout.addLayout(
            search_layout
        )

        # =========================
        # Events
        # =========================

        self.search_box.textChanged.connect(
            self.search_books
        )

        add_btn.clicked.connect(
            self.add_book
        )

        # =========================
        # Book List
        # =========================

        self.list_layout = QVBoxLayout()

        self.main_layout.addLayout(
            self.list_layout
        )

        # =========================
        # Load Books
        # =========================

        self.all_books = BooksDataAdapter.get_all()

        self.show_books(
            self.all_books
        )


    # =============================
    # Clear List
    # =============================

    def clear_list(self):

        while self.list_layout.count():

            item = self.list_layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()


    # =============================
    # Show Books
    # =============================

    def show_books(self, books):

        self.clear_list()

        title = QLabel(
            "Book List"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        self.list_layout.addWidget(
            title
        )

        if not books:

            label = QLabel(
                "No Book found"
            )

            label.setAlignment(
                Qt.AlignCenter
            )

            self.list_layout.addWidget(
                label
            )

            self.list_layout.addStretch()

            return

        for book in books:

            btn = QPushButton(
                str(book.name)
            )
            btn.setObjectName(
            "bookButton"
            )

            self.list_layout.addWidget(
                btn
            )

        self.list_layout.addStretch()


    # =============================
    # Search Books
    # =============================

    def search_books(self, text):

        text = text.lower().strip()

        if not text:

            self.show_books(
                self.all_books
            )

            return

        filtered = [
            book
            for book in self.all_books
            if (
                text in str(book.name).lower()
                or text in str(book.title).lower()
            )
        ]

        self.show_books(
            filtered
        )


    # =============================
    # Add Book
    # =============================

    def add_book(self):

        dialog = AddBookDialog(
            self
        )

        if dialog.exec_():

            self.all_books = BooksDataAdapter.get_all()

            self.show_books(
                self.all_books
            )