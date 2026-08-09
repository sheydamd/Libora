from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QHBoxLayout
)
from PyQt5.QtCore import Qt

from app.api.adapters.author_data_adapter import AuthorsDataAdapter


class SelectAuthorsDialog(QDialog):

    def __init__(self, selected=None, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Select Authors")

        self.selected = selected or []

        layout = QVBoxLayout(self)

        self.list_widget = QListWidget()

        authors = AuthorsDataAdapter.get_all()

        selected_ids = {
            author.id
            for author in self.selected
        }

        for author in authors:

            item = QListWidgetItem(
                f"{author.name} {author.last_name}"
            )

            item.setData(
                Qt.UserRole,
                author
            )

            item.setCheckState(
                Qt.Checked
                if author.id in selected_ids
                else Qt.Unchecked
            )

            self.list_widget.addItem(item)

        layout.addWidget(self.list_widget)

        buttons = QHBoxLayout()

        cancel_btn = QPushButton("Cancel")
        select_btn = QPushButton("Select")

        buttons.addWidget(cancel_btn)
        buttons.addWidget(select_btn)

        layout.addLayout(buttons)

        cancel_btn.clicked.connect(
            self.reject
        )

        select_btn.clicked.connect(
            self.select
        )

    def select(self):

        self.selected = []

        for i in range(
            self.list_widget.count()
        ):

            item = self.list_widget.item(i)

            if item.checkState() == Qt.Checked:

                self.selected.append(
                    item.data(Qt.UserRole)
                )

        self.accept()