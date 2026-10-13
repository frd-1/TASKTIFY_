import sys
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from database.database import Database
from features.authentication.repository import AuthRepository
from features.authentication.service import AuthService
from features.authentication.view import AuthDialog
from main_window import SIGNOUT_EXIT_CODE, MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("TASKTIFY")
    app.setApplicationDisplayName("TASKTIFY")
    app.setFont(QFont("Roboto", 10))

    database = Database("tasktify.db")
    auth_repo = AuthRepository(database)
    auth_service = AuthService(auth_repo)

    while True:
        auth_dialog = AuthDialog(auth_service)
        if auth_dialog.exec() == AuthDialog.DialogCode.Accepted:
            current_user = auth_dialog.logged_in_user
            window = MainWindow(database, current_user=current_user)
            window.show()

            exit_code = app.exec()

            # If user logged out, delete window instance and loop back to AuthDialog
            if exit_code == SIGNOUT_EXIT_CODE:
                del window
                continue
            else:
                database.close()
                sys.exit(exit_code)
        else:
            database.close()
            sys.exit(0)


if __name__ == "__main__":
    main()