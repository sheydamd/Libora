from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QHBoxLayout
)

from PyQt5.QtCore import Qt
from app.gui.components.add_language import AddLanguageDialog
from app.api.adapters.language_data_adapter import LanguagesDataAdapter



class LanguagesWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)


        # Search + Add Button
        search_layout = QHBoxLayout()


        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search language...")
        self.search_box.textChanged.connect(
            self.search_languages
        )


        add_btn = QPushButton("+")
        add_btn.setObjectName("addButton")
        

        add_btn.clicked.connect(
            self.add_language
        )


        search_layout.addWidget(
            self.search_box
        )

        search_layout.addWidget(
            add_btn
        )


        self.layout.addLayout(
            search_layout
        )



        # List
        self.list_layout = QVBoxLayout()

        self.layout.addLayout(
            self.list_layout
        )



        self.all_languages = LanguagesDataAdapter.get_all()


        self.show_languages(
            self.all_languages
        )



    def clear_list(self):

        while self.list_layout.count():

            item = self.list_layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()



    def show_languages(self, languages):

        self.clear_list()


        title = QLabel(
            "Language List"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        self.list_layout.addWidget(
            title
        )



        if not languages:

            self.list_layout.addWidget(
                QLabel("No Language found")
            )

            return



        for language in languages:


            btn = QPushButton(
                language.name
            )


            self.list_layout.addWidget(
                btn
            )


        self.list_layout.addStretch()



    def search_languages(self, text):

        text = text.lower().strip()


        if not text:

            self.show_languages(
                self.all_languages
            )

            return



        filtered = [

            language

            for language in self.all_languages

            if language.name.lower().startswith(text)

        ]


        self.show_languages(
            filtered
        )



    def add_language(self):

        dialog = AddLanguageDialog(self)

        if dialog.exec_():

            self.all_languages = LanguagesDataAdapter.get_all()

            self.show_languages(
                self.all_languages
            )