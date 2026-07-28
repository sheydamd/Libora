from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)

from PyQt5.QtCore import Qt

from app.api.adapters.book_data_adapter import BooksDataAdapter



class BooksWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.load_books()



    def load_books(self):

        title = QLabel("Books List")

        title.setAlignment(
            Qt.AlignCenter
        )

        self.layout.addWidget(title)



        books = BooksDataAdapter.get_all()



        if not books:

            self.layout.addWidget(
                QLabel("No books found")
            )

            return



        for book in books:

            btn = QPushButton(
                book.name
            )

            btn.setMinimumHeight(50)


            btn.clicked.connect(
                lambda checked, b=book:
                self.show_book(b)
            )


            self.layout.addWidget(btn)



        self.layout.addStretch()



    def show_book(self, book):

        print(
            "Selected book:",
            book.name
        )