from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QDialog,
    QVBoxLayout,
    QCheckBox,
    QScrollArea,
    QLabel,
    QDialogButtonBox
)

from PyQt5.QtCore import Qt


class MultiSelectDialog(QDialog):

    def __init__(
        self,
        items,
        selected_items=None,
        title="Select",
        parent=None
    ):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setMinimumSize(400, 500)

        self.items = items

        # قبلی‌ها
        self.selected_ids = set()

        if selected_items:

            for item in selected_items:

                if item.id is not None:
                    self.selected_ids.add(item.id)

        # =========================
        # Main Layout
        # =========================

        main_layout = QVBoxLayout(self)

        # =========================
        # Search
        # =========================

        self.search_box = QLineEdit()

        self.search_box.setPlaceholderText(
            "Search..."
        )

        self.search_box.textChanged.connect(
            self.filter_items
        )

        main_layout.addWidget(
            self.search_box
        )

        # =========================
        # Selected Count
        # =========================

        self.selected_label = QLabel()

        main_layout.addWidget(
            self.selected_label
        )

        # =========================
        # Scroll Area
        # =========================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.container = QWidget()

        self.items_layout = QVBoxLayout(
            self.container
        )

        self.scroll.setWidget(
            self.container
        )

        main_layout.addWidget(
            self.scroll
        )

        # =========================
        # Buttons
        # =========================

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(
            self.accept
        )

        buttons.rejected.connect(
            self.reject
        )

        main_layout.addWidget(
            buttons
        )

        # =========================
        # Initial Load
        # =========================

        self.checkboxes = []

        self.build_items(
            self.items
        )

        self.update_selected_label()


    # =============================
    # Build Items
    # =============================

    def build_items(self, items):

        while self.items_layout.count():

            child = self.items_layout.takeAt(0)

            if child.widget():

                child.widget().deleteLater()

        self.checkboxes = []

        for item in items:

            checkbox = QCheckBox(
                self.get_item_name(item)
            )

            checkbox.setProperty(
                "item_id",
                item.id
            )

            if item.id in self.selected_ids:

                checkbox.setChecked(True)

            checkbox.stateChanged.connect(
                lambda state, obj=item:
                self.checkbox_changed(
                    state,
                    obj
                )
            )

            self.items_layout.addWidget(
                checkbox
            )

            self.checkboxes.append(
                checkbox
            )

        self.items_layout.addStretch()


    # =============================
    # Item Name
    # =============================

    def get_item_name(self, item):

        if hasattr(item, "name"):

            if hasattr(item, "last_name"):

                return f"{item.name} {item.last_name}"

            return str(item.name)

        if hasattr(item, "title"):

            return str(item.title)

        return str(item)


    # =============================
    # Checkbox Changed
    # =============================

    def checkbox_changed(
        self,state,
        item
    ):

        if state == Qt.Checked:

            self.selected_ids.add(
                item.id
            )

        else:

            self.selected_ids.discard(
                item.id
            )

        self.update_selected_label()


    # =============================
    # Search
    # =============================

    def filter_items(self, text):

        text = text.lower().strip()

        if not text:

            self.build_items(
                self.items
            )

            self.update_selected_label()

            return

        filtered = [

            item

            for item in self.items

            if text in self.get_item_name(
                item
            ).lower()

        ]

        self.build_items(
            filtered
        )

        self.update_selected_label()


    # =============================
    # Selected Count
    # =============================

    def update_selected_label(self):

        count = len(
            self.selected_ids
        )

        self.selected_label.setText(
            f"Selected: {count}"
        )


    # =============================
    # Get Selected
    # =============================

    def get_selected_items(self):

        return [

            item

            for item in self.items

            if item.id in self.selected_ids

        ]


    def accept(self):

        # آخرین وضعیت checkboxها را ذخیره کن
        for checkbox in self.checkboxes:

            item_id = checkbox.property(
                "item_id"
            )

            if checkbox.isChecked():

                self.selected_ids.add(
                    item_id
                )

            else:

                self.selected_ids.discard(
                    item_id
                )

        super().accept()


# =========================================================
# Multi Select Widget
# =========================================================

class MultiSelectWidget(QWidget):

    def __init__(
        self,
        items,
        title="Select",
        parent=None
    ):
        super().__init__(parent)

        self.items = items

        self.title = title

        self.selected_items = []

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # =========================
        # Selected Text
        # =========================

        self.display = QLineEdit()

        self.display.setReadOnly(True)

        self.display.setPlaceholderText(
            f"Select {title}..."
        )

        # =========================
        # Three Dot Button
        # =========================

        self.select_btn = QPushButton(
            "..."
        )

        self.select_btn.setFixedWidth(
            45
        )

        self.select_btn.setObjectName(
            "selectButton"
        )

        self.select_btn.clicked.connect(
            self.open_dialog
        )

        layout.addWidget(
            self.display
        )

        layout.addWidget(
            self.select_btn
        )


    # =============================
    # Open Dialog
    # =============================

    def open_dialog(self):

        dialog = MultiSelectDialog(
            self.items,
            self.selected_items,
            self.title,
            self
        )

        if dialog.exec_():

            self.selected_items = (
                dialog.get_selected_items()
            )

            self.update_display()


    # =============================
    # Display Selected
    # =============================

    def update_display(self):

        if not self.selected_items:

            self.display.clear()

            self.display.setPlaceholderText(
                f"Select {self.title}..."
            )

            return

        names = [

            self.get_item_name(item)

            for item in self.selected_items

        ]

        self.display.setText(
            ", ".join(names)
        )


    # =============================
    # Item Name
    # =============================

    def get_item_name(self, item):

        if hasattr(item, "name"):

            if hasattr(item, "last_name"):

                return (
                    f"{item.name} "
                    f"{item.last_name}"
                )

            return str(item.name)

        if hasattr(item, "title"):

            return str(item.title)

        return str(item)


    # =============================
    # Get Selected
    # =============================

    def get_selected_items(self):

        return self.selected_items

    # =============================
    # Set Selected
    # =============================

    def set_selected_items(
        self,
        items
    ):

        self.selected_items = items

        self.update_display()