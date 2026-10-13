from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout
from styles import DIALOG_STYLE


class AuthDialog(QDialog):
    """Dialog interface for Login and Registration."""

    def __init__(self, auth_service, parent=None):
        super().__init__(parent)
        self.auth_service = auth_service
        self.logged_in_user = None

        self.setWindowTitle("TASKTIFY • Authentication")
        self.setFixedSize(380, 320)
        self.setModal(True)
        self.setStyleSheet(DIALOG_STYLE)

        self.build_interface()

    def build_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(12)

        title = QLabel("Welcome to TASKTIFY")
        title.setObjectName("dialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Please sign in or register to continue")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #b9c9e6; font-size: 12px;")
        layout.addWidget(subtitle)

        layout.addSpacing(10)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        layout.addSpacing(10)

        button_box = QHBoxLayout()
        button_box.setSpacing(10)

        login_btn = QPushButton("Login")
        login_btn.setObjectName("primary")
        login_btn.setFixedHeight(38)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.clicked.connect(self.handle_login)

        register_btn = QPushButton("Register")
        register_btn.setObjectName("secondary")
        register_btn.setFixedHeight(38)
        register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        register_btn.clicked.connect(self.handle_register)

        button_box.addWidget(login_btn)
        button_box.addWidget(register_btn)
        layout.addLayout(button_box)

    def clear_inputs(self):
        """Clears authentication input fields."""
        self.username_input.clear()
        self.password_input.clear()

    def handle_login(self):
        user = self.username_input.text()
        pwd = self.password_input.text()

        success, msg, user_data = self.auth_service.login(user, pwd)
        if success:
            self.logged_in_user = user_data
            self.clear_inputs()
            self.accept()
        else:
            QMessageBox.warning(self, "Login Error", msg)
            self.password_input.clear()

    def handle_register(self):
        user = self.username_input.text()
        pwd = self.password_input.text()

        success, msg = self.auth_service.register(user, pwd)
        if success:
            QMessageBox.information(self, "Success", msg)
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Registration Error", msg)