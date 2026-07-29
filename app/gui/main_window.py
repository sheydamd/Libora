import sys
import os

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QStackedWidget,
    QToolButton,
    QAction
)
from app.gui.components.author_list import AuthorsWidget
from app.gui.components.publisher_list import PublishersWidget
from app.gui.components.translator_list import TranslatorsWidget
from app.gui.components.esrb_list import EsrbsWidget
from app.gui.components.genre_list import GenresWidget
from app.gui.components.resource_list import ResourcesWidget
from app.gui.components.language_list import LanguagesWidget
from app.gui.components.book_list import BooksWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library System")
        self.resize(1000, 600)

        # ================= MENU =================
        menubar = self.menuBar()

        books_menu = menubar.addMenu("Books")
        data_menu = menubar.addMenu("Data")
        rent_menu = menubar.addMenu("Rent")
        setting_menu = menubar.addMenu("Settings")
        help_menu = menubar.addMenu("Help")

        books_menu.addActions([
            QAction("Add Book", self),
            QAction("Edit Book", self),
            QAction("Delete Book", self),
            QAction("Search Book", self),
            QAction("View All Books", self)
        ])

        data_menu.addActions([
            QAction("Author", self),
            QAction("Translator", self),
            QAction("Publisher", self),
            QAction("Genre", self),
            QAction("Language", self),
            QAction("Resource", self),
            QAction("ESRB", self)
        ])

        rent_menu.addActions([
            QAction("Rent Book", self),
            QAction("Issue", self),
            QAction("Return Book", self),
            QAction("Renew Rent", self)
        ])

        setting_menu.addActions([
            QAction("Appearance", self)
        ])

        help_menu.addActions([
            QAction("Help", self),
            QAction("About", self)
        ])

        # ================= CENTRAL =================
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.create_ui(main_layout)

    def create_ui(self, parent_layout):
        main_grid = QGridLayout()
        parent_layout.addLayout(main_grid)

        # ============ ICON BAR ============
        self.icon_bar = QWidget()
        self.icon_bar.setObjectName("IconBar")
        self.icon_bar.setFixedWidth(75)

        icons_layout = QVBoxLayout(self.icon_bar)

        def icon_button(file, text):
            btn = QToolButton()
            path = os.path.join(BASE_DIR, "resources", "icons", file)
            btn.setIcon(QIcon(path))
            btn.setIconSize(QSize(28, 28))
            btn.setToolTip(text)
            return btn

        self.icon_books = icon_button("books.svg", "Books")
        self.icon_author = icon_button("pencil.svg", "Authors")
        self.icon_translate = icon_button("g_translate_24dp_000000_FILL0_wght400_GRAD0_opsz24.svg", "Translator")
        self.icon_language = icon_button("language_24dp_000000_FILL0_wght400_GRAD0_opsz24.svg", "Language")
        self.icon_publish = icon_button("publish_24dp_000000_FILL0_wght400_GRAD0_opsz24.svg", "Publish")
        self.icon_resource = icon_button("database_24dp_000000_FILL0_wght400_GRAD0_opsz24.svg", "Resources")
        self.icon_esrb = icon_button("grading_24dp_000000_FILL0_wght400_GRAD0_opsz24.svg", "ESRB")
        self.icon_genre = icon_button("auto_stories_24dp_000000_FILL0_wght400_GRAD0_opsz24.svg", "Genres")

        icons_layout.addWidget(self.icon_books)
        icons_layout.addWidget(self.icon_author)
        icons_layout.addWidget(self.icon_translate)
        icons_layout.addWidget(self.icon_language)
        icons_layout.addWidget(self.icon_publish)
        icons_layout.addWidget(self.icon_resource)
        icons_layout.addWidget(self.icon_esrb)
        icons_layout.addWidget(self.icon_genre)
        icons_layout.addStretch()
        self.icon_author.clicked.connect(self.open_authors)
        self.icon_publish.clicked.connect(self.open_publishers)
        self.icon_translate.clicked.connect(self.open_translators)
        self.icon_esrb.clicked.connect(self.open_esrbs)
        self.icon_genre.clicked.connect(self.open_genres)
        self.icon_language.clicked.connect(self.open_languages)
        self.icon_resource.clicked.connect(self.open_resources)
        self.icon_books.clicked.connect(self.open_books)
    

        # ============ LEFT MENU ============
        self.left_panel = QWidget()
        self.left_panel.setObjectName("LeftPanel")
        self.left_panel.setFixedWidth(220)

        left = QVBoxLayout(self.left_panel)
        left.addStretch()

        # ============ RIGHT ============
        self.right_panel = QWidget()
        self.right_panel.setObjectName("RightPanel")

        right = QVBoxLayout(self.right_panel)
        self.stack = QStackedWidget()
        right.addWidget(self.stack)

        main_grid.addWidget(self.icon_bar, 0, 0)
        main_grid.addWidget(self.left_panel, 0, 1)
        main_grid.addWidget(self.right_panel, 0, 2)

    
    def open_authors(self):

        # پاک کردن پنل وسط
        layout = self.left_panel.layout()


        while layout.count():

            item = layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()



        # ساخت کامپوننت
        authors_widget = AuthorsWidget()


        layout.addWidget(
            authors_widget
        )
    
    def open_publishers(self):

        # پاک کردن پنل وسط
        layout = self.left_panel.layout()


        while layout.count():

            item = layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()



        # ساخت کامپوننت
        publishers_widget = PublishersWidget()


        layout.addWidget(
            publishers_widget
        )
    

    def open_translators(self):

        # پاک کردن پنل وسط
        layout = self.left_panel.layout()


        while layout.count():

            item = layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()



        # ساخت کامپوننت
        translators_widget = TranslatorsWidget()


        layout.addWidget(
            translators_widget
        )

    def open_esrbs(self):
        layout = self.left_panel.layout()


        while layout.count():

            item = layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()



        esrb_widget = EsrbsWidget()


        layout.addWidget(
            esrb_widget
        )

    def open_genres(self):
        layout = self.left_panel.layout()


        while layout.count():

            item = layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()



        resource_widget = GenresWidget()


        layout.addWidget(
            resource_widget
        )

    def open_resources(self):
        layout = self.left_panel.layout()


        while layout.count():

            item = layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()



        resource_widget = ResourcesWidget()


        layout.addWidget(
            resource_widget
        )

    def open_languages(self):
        layout = self.left_panel.layout()


        while layout.count():

            item = layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()



        language_widget = LanguagesWidget()


        layout.addWidget(
            language_widget
        )

    def open_books(self):

        layout = self.left_panel.layout()


        while layout.count():

            item = layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()



        book_widget = BooksWidget()


        layout.addWidget(
            book_widget
        )

    def setup_books(self):
        page = self.make_form([
            ("Title:", QLineEdit()),
            ("Publisher:", QLineEdit())
        ])
        self.stack.addWidget(page)

    def setup_authors(self):
        page = self.make_form([
            ("Name:", QLineEdit()),
            ("Family:", QLineEdit()),
            ("Active:", QCheckBox())
        ])
        self.stack.addWidget(page)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open(os.path.join(BASE_DIR, "theme.qss"), "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())