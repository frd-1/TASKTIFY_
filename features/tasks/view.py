# Used for dates and alignment
from PyQt6.QtCore import QDate, Qt

# PyQt widgets used to build the task form
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

# Style used for the dialog
from styles import DIALOG_STYLE


# Dialog window for adding and editing tasks
class TaskDialog(QDialog):
    """Dialog UI for creating and editing tasks."""

    def __init__(self, parent=None, task=None):
        # Initialize the parent QDialog
        super().__init__(parent)

        # Store the task being edited
        self.task = task

        # Check if the dialog is being used to edit a task
        is_edit = task is not None

        # Set the title depending on add or edit mode
        self.setWindowTitle(
            f"TASKTIFY • {'Edit Task' if is_edit else 'Add Task'}"
        )

        # Set the size of the dialog
        self.setFixedSize(500, 580)

        # Keep the dialog active until the user closes it
        self.setModal(True)

        # Apply the dialog style
        self.setStyleSheet(DIALOG_STYLE)

        # Build the form interface
        self.build_interface()

        # If editing, show the existing task information
        if is_edit:
            self.populate_fields()

    # Creates the task form
    def build_interface(self):

        # Create the main vertical layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(12)

        # Add the form title
        title = QLabel(
            "Edit Task" if self.task else "+ Add Task"
        )
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        # Task title field
        layout.addWidget(self.create_label("Task Title"))

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(
            "Enter task title"
        )
        layout.addWidget(self.title_input)

        # Description field
        layout.addWidget(self.create_label("Description"))

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText(
            "Enter a description (optional)"
        )
        self.desc_input.setFixedHeight(45)
        layout.addWidget(self.desc_input)

        # Category dropdown
        layout.addWidget(self.create_label("Category"))

        self.category_combo = QComboBox()
        self.category_combo.addItems(
            ["School", "Project", "Personal", "Other"]
        )
        layout.addWidget(self.category_combo)

        # Priority dropdown
        layout.addWidget(self.create_label("Priority"))

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(
            ["Low", "Medium", "High"]
        )
        layout.addWidget(self.priority_combo)

        # Due date field
        layout.addWidget(self.create_label("Due Date"))

        self.date_input = QDateEdit()

        # Allow the user to open a calendar
        self.date_input.setCalendarPopup(True)

        # Set today's date as the default
        self.date_input.setDate(
            QDate.currentDate()
        )

        # Set the date display format
        self.date_input.setDisplayFormat(
            "MMM dd, yyyy"
        )

        layout.addWidget(self.date_input)

        # Status dropdown
        layout.addWidget(self.create_label("Status"))

        self.status_combo = QComboBox()
        self.status_combo.addItems(
            ["Pending", "Completed"]
        )
        layout.addWidget(self.status_combo)

        # Add some space before the buttons
        layout.addSpacing(10)

        # Create a horizontal layout for the buttons
        button_box = QHBoxLayout()
        button_box.addStretch()

        # Create the Save/Add button
        save_btn = QPushButton(
            "Save Task" if self.task else "Add Task"
        )
        save_btn.setObjectName("primary")

        # Change the mouse cursor when hovering
        save_btn.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        # Close the dialog successfully when clicked
        save_btn.clicked.connect(self.accept)

        # Create the Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")

        # Change the mouse cursor when hovering
        cancel_btn.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        # Close the dialog without saving
        cancel_btn.clicked.connect(self.reject)

        # Add the buttons to the button layout
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)

        # Add the button layout to the main layout
        layout.addLayout(button_box)

    # Creates a label for a form field
    @staticmethod
    def create_label(text):

        # Create the label
        lbl = QLabel(text)

        # Give the label a style name
        lbl.setObjectName("fieldLabel")

        # Return the label
        return lbl

    # Loads existing task information into the form
    def populate_fields(self):

        # Put the existing title into the title field
        self.title_input.setText(
            self.task.title
        )

        # Put the existing description into the description field
        self.desc_input.setPlainText(
            self.task.description
        )

        # Select the existing category
        self.category_combo.setCurrentText(
            self.task.category
        )

        # Select the existing priority
        self.priority_combo.setCurrentText(
            self.task.priority
        )

        # Convert the saved date into a QDate
        date = QDate.fromString(
            self.task.due_date,
            "yyyy-MM-dd"
        )

        # Only set the date if it is valid
        if date.isValid():
            self.date_input.setDate(date)

        # Select the existing status
        self.status_combo.setCurrentText(
            self.task.status
        )

    # Gets all the information entered in the form
    def get_data(self):

        # Return the form data as a dictionary
        return {
            "title": self.title_input.text(),
            "description": self.desc_input.toPlainText(),
            "category": self.category_combo.currentText(),
            "priority": self.priority_combo.currentText(),
            "due_date": self.date_input.date().toString(
                "yyyy-MM-dd"
            ),
            "status": self.status_combo.currentText(),
        }

