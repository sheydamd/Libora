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

from app.api.adapters.resources_data_adapter import ResourcesDataAdapter
from app.api.models.resource import Resource


class ResourcesWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)


        # Search + Add Button
        search_layout = QHBoxLayout()


        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search resource...")
        self.search_box.textChanged.connect(
            self.search_resources
        )


        add_btn = QPushButton("+")
        add_btn.setObjectName("addButton")
        


        add_btn.clicked.connect(
            self.add_resource
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


        self.all_resources = ResourcesDataAdapter.get_all()


        self.show_resources(
            self.all_resources
        )



    def clear_list(self):

        while self.list_layout.count():

            item = self.list_layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()



    def show_resources(self, resources):

        self.clear_list()


        title = QLabel(
            "Resource List"
        )

        title.setAlignment(
            Qt.AlignCenter
        )


        self.list_layout.addWidget(
            title
        )



        if not resources:

            self.list_layout.addWidget(
                QLabel("No Resource found")
            )

            return



        for resource in resources:


            text = f"{resource.title} - {resource.type}"


            btn = QPushButton(
                text
            )


            self.list_layout.addWidget(
                btn
            )


        self.list_layout.addStretch()



    def search_resources(self, text):

        text = text.lower().strip()


        if not text:

            self.show_resources(
                self.all_resources
            )

            return



        filtered = [

            resource

            for resource in self.all_resources

            if (
                resource.title.lower().startswith(text)
                or resource.type.lower().startswith(text)
            )

        ]


        self.show_resources(
            filtered
        )



    def add_resource(self):

        dialog = QDialog(self)

        dialog.setWindowTitle(
            "Add Resource"
        )


        layout = QFormLayout(dialog)



        title = QLineEdit()

        type_ = QLineEdit()

        establish_date = QLineEdit()



        layout.addRow(
            "Title",
            title
        )

        layout.addRow(
            "Type",
            type_
        )

        layout.addRow(
            "Establish Date",
            establish_date
        )



        save_btn = QPushButton(
            "Save"
        )


        layout.addWidget(
            save_btn
        )



        def save():


            if not title.text():

                QMessageBox.warning(
                    self,
                    "Error",
                    "Title is required."
                )

                return



            resource = Resource(
                title.text(),
                type_.text(),establish_date.text()
            )



            ResourcesDataAdapter.insert(
                resource
            )



            QMessageBox.information(
                self,
                "Success",
                "Resource added successfully."
            )



            self.all_resources = ResourcesDataAdapter.get_all()


            self.show_resources(
                self.all_resources
            )


            dialog.accept()



        save_btn.clicked.connect(
            save
        )


        dialog.exec_()