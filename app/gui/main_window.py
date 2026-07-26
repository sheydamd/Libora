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
