from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QHBoxLayout
)

from PyQt5.QtCore import Qt

from app.api.adapters.publishers_data_adapter import PublishersDataAdapter
from app.api.models.publisher import Publisher
from app.gui.components.add_publisher import AddPublisherDialog

class PublishersWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # Search + Add Button
        search_layout = QHBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search publisher...")
        self.search_box.textChanged.connect(self.search_publishers)

        add_btn = QPushButton("+")
        add_btn.setObjectName("addButton")
        

        add_btn.clicked.connect(self.add_publisher)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(add_btn)

        self.layout.addLayout(search_layout)

        # Author list
        self.list_layout = QVBoxLayout()
        self.layout.addLayout(self.list_layout)

        self.all_publishers = PublishersDataAdapter.get_all()

        self.show_publishers(self.all_publishers)


    def clear_list(self):

        while self.list_layout.count():

            item = self.list_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()


    def show_publishers(self, publishers):

        self.clear_list()

        title = QLabel("Publisher List")

        title.setAlignment(
            Qt.AlignCenter
        )

        self.list_layout.addWidget(
            title
        )

        if not publishers:

            label = QLabel("No Publisher found")

            label.setAlignment(
                Qt.AlignCenter
            )

            self.list_layout.addWidget(
                label
            )

            self.list_layout.addStretch()

            return

        for publisher in publishers:

            btn = QPushButton(
                str(publisher.name)
            )

            btn.setObjectName(
                "publisherButton"
            )

            self.list_layout.addWidget(
                btn
            )

        self.list_layout.addStretch()


    def search_publishers(self, text):

        text = text.lower().strip()

        if not text:

            self.show_publishers(
                self.all_publishers
            )

            return

        filtered = [

            publisher

            for publisher in self.all_publishers

            if text in publisher.name.lower()

        ]

        self.show_publishers(
            filtered
        )
    def add_publisher(self):

        dialog = AddPublisherDialog(self)

        if dialog.exec_():

            self.all_publishers = PublishersDataAdapter.get_all()

            self.show_publishers(
                self.all_publishers
            )