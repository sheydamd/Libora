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

from app.api.adapters.translator_data_adapter import TranslatorsDataAdapter
from app.api.models.translator import Translator


class TranslatorsWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)


        # Search 
        search_layout = QHBoxLayout()


        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search translator...")
        self.search_box.textChanged.connect(
            self.search_translators
        )




        search_layout.addWidget(
            self.search_box
        )



        self.layout.addLayout(
            search_layout
        )



        # List
        self.list_layout = QVBoxLayout()

        self.layout.addLayout(
            self.list_layout
        )


        self.all_translators = TranslatorsDataAdapter.get_all()


        self.show_translators(
            self.all_translators
        )



    def clear_list(self):

        while self.list_layout.count():

            item = self.list_layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()



    def show_translators(self, translators):

        self.clear_list()


        title = QLabel(
            "Translator List"
        )

        title.setAlignment(
            Qt.AlignCenter
        )


        self.list_layout.addWidget(
            title
        )



        if not translators:

            self.list_layout.addWidget(
                QLabel("No Translator found")
            )

            return



        for translator in translators:


            full_name = (
                f"{translator.name} "
                f"{translator.last_name}"
            )


            btn = QPushButton(
                full_name
            )


            self.list_layout.addWidget(
                btn
            )


        self.list_layout.addStretch()



    def search_translators(self, text):

        text = text.lower().strip()


        if not text:

            self.show_translators(
                self.all_translators
            )

            return



        filtered = [

            translator

            for translator in self.all_translators

            if (
                translator.name.lower().startswith(text)
                or translator.last_name.lower().startswith(text)
                or
                f"{translator.name} {translator.last_name}"
                .lower()
                .startswith(text)
            )

        ]


        self.show_translators(
            filtered
        )
