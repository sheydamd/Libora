from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QHBoxLayout
)

from PyQt5.QtCore import Qt

from app.api.adapters.esrb_data_adapter import EsrbsDataAdapter
from app.gui.components.add_esrb import AddEsrbDialog


class EsrbsWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)


        # Search + Add Button
        search_layout = QHBoxLayout()


        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search ESRB...")
        self.search_box.textChanged.connect(self.search_esrb)


        add_btn = QPushButton("+")
        add_btn.setObjectName("addButton")
        


        add_btn.clicked.connect(self.add_esrb)


        search_layout.addWidget(self.search_box)
        search_layout.addWidget(add_btn)


        self.layout.addLayout(search_layout)



        # List
        self.list_layout = QVBoxLayout()

        self.layout.addLayout(
            self.list_layout
        )


        self.all_esrb = EsrbsDataAdapter.get_all()

        self.show_esrb(
            self.all_esrb
        )



    def clear_list(self):

        while self.list_layout.count():

            item = self.list_layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()



    def show_esrb(self, esrbs):

        self.clear_list()


        title = QLabel("ESRB List")

        title.setAlignment(
            Qt.AlignCenter
        )

        self.list_layout.addWidget(
            title
        )


        if not esrbs:

            self.list_layout.addWidget(
                QLabel("No ESRB found")
            )

            return



        for esrb in esrbs:


            btn = QPushButton(
                esrb.name
            )


            self.list_layout.addWidget(
                btn
            )


        self.list_layout.addStretch()



    def search_esrb(self, text):

        text = text.lower().strip()


        if not text:

            self.show_esrb(
                self.all_esrb
            )

            return



        filtered = [

            esrb

            for esrb in self.all_esrb

            if esrb.name.lower().startswith(text)

        ]


        self.show_esrb(
            filtered
        )



    def add_esrb(self):

        dialog = AddEsrbDialog(self)

        if dialog.exec_():

            self.all_esrb = EsrbsDataAdapter.get_all()

            self.show_esrb(
                self.all_esrb
            )