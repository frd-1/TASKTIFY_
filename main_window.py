from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from features.easter_egg.service import VerseService
from features.easter_egg.view import EggWidget, VerseDialog
from features.tasks.repository import TaskRepository
from features.tasks.service import TaskService
from features.tasks.view import TaskDialog
from styles import APP_STYLE


class MainWindow(QMainWindow):
    """Main application window combining feature modules."""

    def __init__(self, db):
        super().__init__()

        self.task_service = TaskService(TaskRepository(db))
        self.verse_service = VerseService()

        self.current_page = "dashboard"
        self.verse_dialog = None

        self.setWindowTitle("TASKTIFY • Task Management System")
        self.resize(1280, 780)
        self.setMinimumSize(1080, 680)
        self.setStyleSheet(APP_STYLE)

        self.build_interface()
        self.refresh_all()

    def build_interface(self):
        background = QWidget()
        background.setObjectName("background")
        background.setStyleSheet("""
            QWidget#background {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #162c59, stop: 0.42 #172d62,
                    stop: 0.72 #102a4f, stop: 1 #0a1932
                );
            }
        """)

        self.setCentralWidget(background)
        root = QHBoxLayout(background)
        root.setContentsMargins(9, 9, 9, 9)
        root.setSpacing(0)

        self.build_sidebar(root)

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(25, 20, 25, 20)
        self.content_layout.setSpacing(16)

        root.addWidget(self.content, 1)

        self.build_dashboard()
        self.build_tasks_page()
        self.show_page("dashboard")

    def build_sidebar(self, root):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(215)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(15, 25, 15, 20)
        layout.setSpacing(7)

        logo = QLabel("✓  TASKTIFY")
        logo.setObjectName("logo")
        layout.addWidget(logo)

        tagline = QLabel("Let your tasks testify to\nyour productivity.")
        tagline.setObjectName("tagline")
        layout.addWidget(tagline)

        layout.addSpacing(25)

        self.dashboard_button = self.create_nav_button("⌂   Dashboard")
        self.tasks_button = self.create_nav_button("☷   My Tasks")
        self.add_button = self.create_nav_button("＋   Add Task")

        self.dashboard_button.clicked.connect(lambda: self.show_page("dashboard"))
        self.tasks_button.clicked.connect(lambda: self.show_page("tasks"))
        self.add_button.clicked.connect(self.open_add_dialog)

        layout.addWidget(self.dashboard_button)
        layout.addWidget(self.tasks_button)
        layout.addWidget(self.add_button)

        layout.addStretch()

        root.addWidget(sidebar)

    @staticmethod
    def create_nav_button(text):
        button = QPushButton(text)
        button.setObjectName("navButton")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button

    def set_selected_navigation(self, selected_button):
        for btn in [self.dashboard_button, self.tasks_button, self.add_button]:
            btn.setProperty("selected", btn is selected_button)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def build_dashboard(self):
        self.dashboard_page = QWidget()
        layout = QVBoxLayout(self.dashboard_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        self.greeting = QLabel()
        self.greeting.setObjectName("pageTitle")
        subtitle = QLabel("Small steps today, big results tomorrow.")
        subtitle.setObjectName("subtitle")
        title_box.addWidget(self.greeting)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()
        layout.addLayout(header)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(11)

        self.stat_total = self.create_stat_card("Total Tasks")
        self.stat_pending = self.create_stat_card("Pending")
        self.stat_completed = self.create_stat_card("Completed")
        self.stat_overdue = self.create_stat_card("Overdue")
        self.stat_due_soon = self.create_stat_card("Due Soon")

        for card in [
            self.stat_total,
            self.stat_pending,
            self.stat_completed,
            self.stat_overdue,
            self.stat_due_soon,
        ]:
            stats_layout.addWidget(card, 1)

        layout.addLayout(stats_layout)

        middle = QHBoxLayout()
        middle.setSpacing(14)

        upcoming_card = QFrame()
        upcoming_card.setObjectName("glassCard")
        upcoming_layout = QVBoxLayout(upcoming_card)
        upcoming_layout.setContentsMargins(18, 16, 18, 16)

        top = QHBoxLayout()
        title = QLabel("Upcoming Tasks")
        title.setStyleSheet("font-size: 16px; font-weight: 800;")
        top.addWidget(title)
        top.addStretch()

        view_all = QPushButton("View All →")
        view_all.setObjectName("secondary")
        view_all.clicked.connect(lambda: self.show_page("tasks"))
        top.addWidget(view_all)

        upcoming_layout.addLayout(top)

        self.upcoming_table = QTableWidget(0, 4)
        self.upcoming_table.setHorizontalHeaderLabels(["Task", "Category", "Due Date", "State"])
        self.upcoming_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.upcoming_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.upcoming_table.verticalHeader().setVisible(False)
        self.upcoming_table.horizontalHeader().setStretchLastSection(True)
        self.upcoming_table.setColumnWidth(0, 245)
        self.upcoming_table.setColumnWidth(1, 100)
        self.upcoming_table.setColumnWidth(2, 105)

        upcoming_layout.addWidget(self.upcoming_table, 1)
        middle.addWidget(upcoming_card, 1)

        egg_card = QFrame()
        egg_card.setObjectName("glassCard")
        egg_layout = QVBoxLayout(egg_card)
        egg_layout.setContentsMargins(20, 12, 20, 12)
        egg_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.egg = EggWidget()
        self.egg.verse_ready.connect(self.show_verse)
        egg_layout.addWidget(self.egg, alignment=Qt.AlignmentFlag.AlignCenter)

        hint = QLabel("  Tap the egg\nfor a surprise verse!")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet("QLabel { color: #dbe6fa; font-size: 13px; font-style: italic; }")
        egg_layout.addWidget(hint)

        middle.addWidget(egg_card)
        layout.addLayout(middle, 1)

    @staticmethod
    def create_stat_card(label):
        card = QFrame()
        card.setObjectName("statCard")
        card.setMinimumHeight(78)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)

        number = QLabel("0")
        number.setObjectName("statNumber")
        text = QLabel(label)
        text.setObjectName("statLabel")

        layout.addWidget(number)
        layout.addWidget(text)

        card.number_label = number
        return card

    def build_tasks_page(self):
        self.tasks_page = QWidget()
        layout = QVBoxLayout(self.tasks_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("☷  My Tasks")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Set the goal, take control!")
        subtitle.setObjectName("subtitle")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()

        add = QPushButton("＋ Add Task")
        add.setObjectName("primary")
        add.setCursor(Qt.CursorShape.PointingHandCursor)
        add.clicked.connect(self.open_add_dialog)
        header.addWidget(add)

        layout.addLayout(header)

        controls = QHBoxLayout()
        controls.setSpacing(8)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("🔍  Search by title, description, or category...")
        self.search_edit.textChanged.connect(self.refresh_task_table)
        controls.addWidget(self.search_edit, 2)

        self.category_filter = QComboBox()
        self.category_filter.addItems(["All Categories", "School", "Project", "Personal", "Other"])

        self.priority_filter = QComboBox()
        self.priority_filter.addItems(["All Priorities", "Low", "Medium", "High"])

        self.status_filter = QComboBox()
        self.status_filter.addItems(["All Statuses", "Pending", "Completed"])

        self.category_filter.currentIndexChanged.connect(self.refresh_task_table)
        self.priority_filter.currentIndexChanged.connect(self.refresh_task_table)
        self.status_filter.currentIndexChanged.connect(self.refresh_task_table)

        controls.addWidget(self.category_filter)
        controls.addWidget(self.priority_filter)
        controls.addWidget(self.status_filter)

        layout.addLayout(controls)

        self.task_table = QTableWidget(0, 8)
        self.task_table.setHorizontalHeaderLabels([
            "ID", "Title", "Category", "Priority", "Due Date", "Status", "Due State", "Actions"
        ])
        self.task_table.setColumnHidden(0, True)
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.task_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.horizontalHeader().setStretchLastSection(True)
        self.task_table.verticalHeader().setDefaultSectionSize(40)

        widths = [0, 210, 100, 95, 110, 95, 95, 150]
        for index, width in enumerate(widths):
            self.task_table.setColumnWidth(index, width)

        layout.addWidget(self.task_table, 1)

    def show_page(self, page):
        self.current_page = page
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        if page == "dashboard":
            self.content_layout.addWidget(self.dashboard_page)
            self.set_selected_navigation(self.dashboard_button)
            self.refresh_dashboard()
        else:
            self.content_layout.addWidget(self.tasks_page)
            self.set_selected_navigation(self.tasks_button)
            self.refresh_task_table()

    def open_add_dialog(self):
        dialog = TaskDialog(self)
        if dialog.exec():
            try:
                self.task_service.create_task(**dialog.get_data())
                self.refresh_all()
                self.show_page("tasks")
            except ValueError as error:
                QMessageBox.warning(self, "Invalid Task", str(error))
            except Exception as error:
                QMessageBox.critical(self, "Database Error", f"Could not add the task.\n\n{error}")

    def open_edit_dialog(self, task_id):
        task = self.task_service.get_task(task_id)
        if task is None:
            QMessageBox.warning(self, "Task Not Found", "The selected task no longer exists.")
            return

        dialog = TaskDialog(self, task)
        if dialog.exec():
            try:
                self.task_service.update_task(task_id, **dialog.get_data())
                self.refresh_all()
            except ValueError as error:
                QMessageBox.warning(self, "Invalid Task", str(error))
            except Exception as error:
                QMessageBox.critical(self, "Database Error", f"Could not update the task.\n\n{error}")

    def confirm_delete(self, task_id):
        task = self.task_service.get_task(task_id)
        if task is None:
            return

        answer = QMessageBox.question(
            self,
            "Delete Task",
            f'Are you sure you want to delete\n"{task.title}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer == QMessageBox.StandardButton.Yes:
            try:
                self.task_service.delete_task(task_id)
                self.refresh_all()
            except Exception as error:
                QMessageBox.critical(self, "Database Error", f"Could not delete the task.\n\n{error}")

    def refresh_task_table(self):
        if not hasattr(self, "task_table"):
            return

        tasks = self.task_service.get_all_tasks()
        search = self.search_edit.text().strip().lower()
        selected_category = self.category_filter.currentText()
        selected_priority = self.priority_filter.currentText()
        selected_status = self.status_filter.currentText()

        filtered_tasks = []
        for task in tasks:
            searchable = f"{task.title} {task.description} {task.category}".lower()

            if search and search not in searchable:
                continue
            if selected_category != "All Categories" and task.category != selected_category:
                continue
            if selected_priority != "All Priorities" and task.priority != selected_priority:
                continue
            if selected_status != "All Statuses" and task.status != selected_status:
                continue

            filtered_tasks.append(task)

        self.task_table.setRowCount(0)

        for task in filtered_tasks:
            row = self.task_table.rowCount()
            self.task_table.insertRow(row)

            self.set_center_item(row, 0, str(task.id))
            self.set_left_item(row, 1, task.title)
            self.set_center_item(row, 2, task.category)
            self.set_center_item(row, 3, task.priority)
            self.set_center_item(row, 4, self.format_date(task.due_date))
            self.set_center_item(row, 5, task.status)

            due_state = self.task_service.get_due_state(task)
            self.set_center_item(row, 6, due_state)

            self.add_action_buttons(row, task.id)

            self.apply_badge(self.task_table.item(row, 3), task.priority)
            self.apply_badge(self.task_table.item(row, 5), task.status)
            self.apply_badge(self.task_table.item(row, 6), due_state)

    def set_center_item(self, row, column, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.task_table.setItem(row, column, item)

    def set_left_item(self, row, column, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.task_table.setItem(row, column, item)

    def add_action_buttons(self, row, task_id):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        edit = QPushButton("Edit")
        edit.setToolTip("Edit Task")
        edit.setFixedSize(58, 26)
        edit.setCursor(Qt.CursorShape.PointingHandCursor)
        edit.setStyleSheet("""
            QPushButton {
                background-color: #1d3760;
                color: #ffffff;
                border: 1px solid #3d5986;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 600;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #294977;
            }
        """)
        edit.clicked.connect(lambda checked=False, tid=task_id: self.open_edit_dialog(tid))

        delete = QPushButton("Delete")
        delete.setToolTip("Delete Task")
        delete.setFixedSize(58, 26)
        delete.setCursor(Qt.CursorShape.PointingHandCursor)
        delete.setStyleSheet("""
            QPushButton {
                background-color: #8e3452;
                color: #ffffff;
                border: 1px solid #a83d5d;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 600;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #a83d5d;
            }
        """)
        delete.clicked.connect(lambda checked=False, tid=task_id: self.confirm_delete(tid))

        layout.addWidget(edit)
        layout.addWidget(delete)
        self.task_table.setCellWidget(row, 7, widget)

    @staticmethod
    def apply_badge(item, value):
        if item is None:
            return

        colors = {
            "High": "#8e3452",
            "Medium": "#9a6c29",
            "Low": "#287c69",
            "Overdue": "#8e3452",
            "Due Soon": "#9a6c29",
            "Upcoming": "#2e6eb4",
            "Completed": "#2c7d60",
            "Pending": "#4b6290",
        }

        if value in colors:
            item.setBackground(QColor(colors[value]))
            item.setForeground(QColor("#ffffff"))

    def refresh_dashboard(self):
        self.greeting.setText(self.get_greeting())
        statistics = self.task_service.get_statistics()

        self.stat_total.number_label.setText(str(statistics["total"]))
        self.stat_pending.number_label.setText(str(statistics["pending"]))
        self.stat_completed.number_label.setText(str(statistics["completed"]))
        self.stat_overdue.number_label.setText(str(statistics["overdue"]))
        self.stat_due_soon.number_label.setText(str(statistics["due_soon"]))

        tasks = [
            task for task in self.task_service.get_all_tasks() if task.status != "Completed"
        ]

        self.upcoming_table.setRowCount(0)

        for task in tasks:
            row = self.upcoming_table.rowCount()
            self.upcoming_table.insertRow(row)

            self.upcoming_table.setItem(row, 0, QTableWidgetItem(task.title))
            self.upcoming_table.setItem(row, 1, QTableWidgetItem(task.category))
            self.upcoming_table.setItem(row, 2, QTableWidgetItem(self.format_date(task.due_date)))

            state = self.task_service.get_due_state(task)
            state_item = QTableWidgetItem(state)
            state_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.apply_badge(state_item, state)

            self.upcoming_table.setItem(row, 3, state_item)

    @staticmethod
    def get_greeting():
        hour = datetime.now().hour
        if 5 <=hour < 12:
            return "Good morning! ☀️"
        if 12 <= hour < 18:
            return "Good afternoon! 🌤️"
        return "Good evening! 🌙"


    @staticmethod
    def format_date(date_string):
        try:
            date_value = datetime.strptime(date_string, "%Y-%m-%d")
            return date_value.strftime("%b %d, %Y")
        except ValueError:
            return date_string

    def refresh_all(self):
        self.refresh_dashboard()
        self.refresh_task_table()

    def show_verse(self):
        self.verse_dialog = VerseDialog(self, self.verse_service)
        self.verse_dialog.finished.connect(self.egg.reset)
        self.verse_dialog.exec()
        self.verse_dialog = None