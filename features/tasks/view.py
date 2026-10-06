from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)
from styles import DIALOG_STYLE


class TaskDialog(QDialog):
    """Dialog UI for creating and editing tasks."""

    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.task = task

        is_edit = task is not None
        self.setWindowTitle(
            f"TASKTIFY • {'Edit Task' if is_edit else 'Add Task'}"
        )
        self.setFixedSize(500, 580)
        self.setModal(True)
        self.setStyleSheet(DIALOG_STYLE)

        self.build_interface()

        if is_edit:
            self.populate_fields()

    def build_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(12)

        title = QLabel("Edit Task" if self.task else "+ Add Task")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        layout.addWidget(self.create_label("Task Title"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter task title")
        layout.addWidget(self.title_input)

        layout.addWidget(self.create_label("Description"))
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Enter a description (optional)")
        self.desc_input.setFixedHeight(45)
        layout.addWidget(self.desc_input)

        layout.addWidget(self.create_label("Category"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(["School", "Project", "Personal", "Other"])
        layout.addWidget(self.category_combo)

        layout.addWidget(self.create_label("Priority"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        layout.addWidget(self.priority_combo)

        layout.addWidget(self.create_label("Due Date"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("MMM dd, yyyy")
        layout.addWidget(self.date_input)

        layout.addWidget(self.create_label("Status"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Pending", "Completed"])
        layout.addWidget(self.status_combo)

        layout.addSpacing(10)

        button_box = QHBoxLayout()
        button_box.addStretch()

        save_btn = QPushButton("Save Task" if self.task else "Add Task")
        save_btn.setObjectName("primary")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)

        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addLayout(button_box)

    @staticmethod
    def create_label(text):
        lbl = QLabel(text)
        lbl.setObjectName("fieldLabel")
        return lbl

    def populate_fields(self):
        self.title_input.setText(self.task.title)
        self.desc_input.setPlainText(self.task.description)
        self.category_combo.setCurrentText(self.task.category)
        self.priority_combo.setCurrentText(self.task.priority)

        date = QDate.fromString(self.task.due_date, "yyyy-MM-dd")
        if date.isValid():
            self.date_input.setDate(date)

        self.status_combo.setCurrentText(self.task.status)

    def get_data(self):
        return {
            "title": self.title_input.text(),
            "description": self.desc_input.toPlainText(),
            "category": self.category_combo.currentText(),
            "priority": self.priority_combo.currentText(),
            "due_date": self.date_input.date().toString("yyyy-MM-dd"),
            "status": self.status_combo.currentText(),
        }