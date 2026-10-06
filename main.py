import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from database.database import Database
from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("TASKTIFY")
    app.setApplicationDisplayName("TASKTIFY")
    app.setFont(QFont("Roboto", 10))

    database = Database("tasktify.db")

    window = MainWindow(database)
    window.show()

    exit_code = app.exec()
    database.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()