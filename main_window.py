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

# Exit code signal to request sign out in main loop
SIGNOUT_EXIT_CODE = 888


class MainWindow(QMainWindow):
    """Main application window combining feature modules."""

    def __init__(self, db, current_user):
        super().__init__()

        self.current_user = current_user
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

        layout.addSpacing(15)

        # Active User Info
        user_lbl = QLabel(f"👤 {self.current_user['username']}")
        user_lbl.setStyleSheet("color: #ffd86e; font-weight: bold; font-size: 11px;")
        layout.addWidget(user_lbl)

        layout.addSpacing(15)

        self.dashboard_button = self.create_nav_button("⌂   Dashboard")
        self.tasks_button = self.create_nav_button("☷   My Tasks")

        self.dashboard_button.clicked.connect(lambda: self.show_page("dashboard"))
        self.tasks_button.clicked.connect(lambda: self.show_page("tasks"))

        layout.addWidget(self.dashboard_button)
        layout.addWidget(self.tasks_button)

        layout.addSpacing(15)

        # QUICK LINKS Header
        quick_links_hdr = QLabel("QUICK LINKS")
        quick_links_hdr.setStyleSheet("color: #63799e; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
        layout.addWidget(quick_links_hdr)

        self.add_button = self.create_nav_button("＋   Add Task")
        self.add_button.clicked.connect(self.open_add_dialog)
        layout.addWidget(self.add_button)

        # Pushes Sign Out and footer down to the very bottom
        layout.addStretch()

        # Sign Out Button at the bottom
        signout_btn = self.create_nav_button("              Sign Out")
        signout_btn.clicked.connect(self.handle_signout)
        layout.addWidget(signout_btn)

        layout.addSpacing(10)

        footer = QLabel("TASKTIFY\nTask Management System")
        footer.setStyleSheet("color: #63799e; font-size: 9px;")
        layout.addWidget(footer)

        root.addWidget(sidebar)

    def handle_signout(self):
        reply = QMessageBox.question(
            self,
            "Sign Out",
            "Are you sure you want to sign out?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            from PyQt6.QtWidgets import QApplication
            self.close()  # Completely close and hide dashboard window
            QApplication.exit(SIGNOUT_EXIT_CODE)

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
        title = QLabel(" Upcoming Tasks")
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

        # Clear Filters Button
        self.clear_filter_btn = QPushButton("Clear")
        self.clear_filter_btn.setObjectName("secondary")
        self.clear_filter_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_filter_btn.clicked.connect(self.reset_filters)

        controls.addWidget(self.category_filter)
        controls.addWidget(self.priority_filter)
        controls.addWidget(self.status_filter)
        controls.addWidget(self.clear_filter_btn)

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

        widths = [0, 210, 100, 100, 110, 100, 110, 180]
        for index, width in enumerate(widths):
            self.task_table.setColumnWidth(index, width)

        layout.addWidget(self.task_table, 1)

    def reset_filters(self):
        """Resets search input and filter dropdowns back to default states."""
        self.search_edit.clear()
        self.category_filter.setCurrentIndex(0)
        self.priority_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)
        self.refresh_task_table()

    def get_greeting(self):
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning! ☀️"
        elif hour < 18:
            return "Good afternoon! ☀️"
        else:
            return "Good evening! 🌙"

    def refresh_dashboard(self):
        self.greeting.setText(self.get_greeting())
        stats = self.task_service.get_statistics(self.current_user["id"])

        self.stat_total.number_label.setText(str(stats["total"]))
        self.stat_pending.number_label.setText(str(stats["pending"]))
        self.stat_completed.number_label.setText(str(stats["completed"]))
        self.stat_overdue.number_label.setText(str(stats["overdue"]))
        self.stat_due_soon.number_label.setText(str(stats["due_soon"]))

        tasks = [t for t in self.task_service.get_all_tasks(self.current_user["id"]) if t.status != "Completed"]
        self.upcoming_table.setRowCount(0)

        for row_idx, task in enumerate(tasks):
            self.upcoming_table.insertRow(row_idx)
            self.upcoming_table.setItem(row_idx, 0, QTableWidgetItem(task.title))
            self.upcoming_table.setItem(row_idx, 1, QTableWidgetItem(task.category))

            due = datetime.strptime(task.due_date, "%Y-%m-%d").strftime("%b %d, %Y")
            self.upcoming_table.setItem(row_idx, 2, QTableWidgetItem(due))

            state = self.task_service.get_due_state(task)
            state_item = QTableWidgetItem(state)
            state_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if state == "Overdue":
                state_item.setBackground(QColor("#a83246"))
            elif state == "Due Soon":
                state_item.setBackground(QColor("#c78b32"))
            else:
                state_item.setBackground(QColor("#2a6eb0"))

            self.upcoming_table.setItem(row_idx, 3, state_item)

    def refresh_task_table(self):
        search = self.search_edit.text().lower()
        cat = self.category_filter.currentText()
        prio = self.priority_filter.currentText()
        stat = self.status_filter.currentText()

        all_tasks = self.task_service.get_all_tasks(self.current_user["id"])
        filtered = []

        for t in all_tasks:
            match_search = (search in t.title.lower()) or (search in t.description.lower()) or (search in t.category.lower())
            match_cat = (cat == "All Categories") or (t.category == cat)
            match_prio = (prio == "All Priorities") or (t.priority == prio)
            match_stat = (stat == "All Statuses") or (t.status == stat)

            if match_search and match_cat and match_prio and match_stat:
                filtered.append(t)

        self.task_table.setRowCount(0)
        for row_idx, task in enumerate(filtered):
            self.task_table.insertRow(row_idx)

            # Column 0: ID
            self.task_table.setItem(row_idx, 0, QTableWidgetItem(str(task.id)))

            # Column 1: Title
            self.task_table.setItem(row_idx, 1, QTableWidgetItem(task.title))

            # Column 2: Category
            self.task_table.setItem(row_idx, 2, QTableWidgetItem(task.category))

            # Column 3: Priority Badge Color
            prio_item = QTableWidgetItem(task.priority)
            prio_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if task.priority == "High":
                prio_item.setBackground(QColor("#a83246"))
            elif task.priority == "Medium":
                prio_item.setBackground(QColor("#c78b32"))
            elif task.priority == "Low":
                prio_item.setBackground(QColor("#2b7a4b"))
            self.task_table.setItem(row_idx, 3, prio_item)

            # Column 4: Due Date
            due = datetime.strptime(task.due_date, "%Y-%m-%d").strftime("%b %d, %Y")
            self.task_table.setItem(row_idx, 4, QTableWidgetItem(due))

            # Column 5: Status Badge Color
            stat_item = QTableWidgetItem(task.status)
            stat_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if task.status == "Completed":
                stat_item.setBackground(QColor("#2b7a4b"))
            else:
                stat_item.setBackground(QColor("#3d5a80"))
            self.task_table.setItem(row_idx, 5, stat_item)

            # Column 6: Due State Badge Color
            state = self.task_service.get_due_state(task)
            state_item = QTableWidgetItem(state)
            state_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if state == "Overdue":
                state_item.setBackground(QColor("#a83246"))
            elif state == "Due Soon":
                state_item.setBackground(QColor("#c78b32"))
            elif state == "Completed":
                state_item.setBackground(QColor("#2b7a4b"))
            else:
                state_item.setBackground(QColor("#2a6eb0"))
            self.task_table.setItem(row_idx, 6, state_item)

            # Column 7: Actions Buttons
            btn_box = QWidget()
            btn_layout = QHBoxLayout(btn_box)
            btn_layout.setContentsMargins(4, 2, 4, 2)
            btn_layout.setSpacing(6)

            edit_btn = QPushButton("Edit")
            edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #213555;
                    color: #ffffff;
                    border: 1px solid #3e5481;
                    border-radius: 4px;
                    font-size: 11px;
                    font-weight: bold;
                    min-width: 55px;
                    max-height: 26px;
                }
                QPushButton:hover {
                    background-color: #2c4770;
                }
            """)
            edit_btn.clicked.connect(lambda checked=False, tid=task.id: self.open_edit_dialog(tid))

            del_btn = QPushButton("Delete")
            del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            del_btn.setStyleSheet("""
                QPushButton {
                    background-color: #a83246;
                    color: #ffffff;
                    border: none;
                    border-radius: 4px;
                    font-size: 11px;
                    font-weight: bold;
                    min-width: 55px;
                    max-height: 26px;
                }
                QPushButton:hover {
                    background-color: #be3950;
                }
            """)
            del_btn.clicked.connect(lambda checked=False, tid=task.id: self.confirm_delete(tid))

            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(del_btn)

            self.task_table.setRowHeight(row_idx, 44)
            self.task_table.setCellWidget(row_idx, 7, btn_box)

    def refresh_all(self):
        self.refresh_dashboard()
        self.refresh_task_table()

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
                data = dialog.get_data()
                self.task_service.create_task(
                    user_id=self.current_user["id"],
                    **data
                )
                self.refresh_all()
                self.show_page("tasks")
            except ValueError as error:
                QMessageBox.warning(self, "Invalid Task", str(error))
            except Exception as error:
                QMessageBox.critical(self, "Database Error", f"Could not add the task.\n\n{error}")

    def open_edit_dialog(self, task_id):
        task = self.task_service.get_task(task_id, self.current_user["id"])
        if task is None:
            QMessageBox.warning(self, "Task Not Found", "The selected task no longer exists.")
            return

        dialog = TaskDialog(self, task=task)
        if dialog.exec():
            try:
                data = dialog.get_data()
                self.task_service.update_task(
                    task_id=task_id,
                    user_id=self.current_user["id"],
                    **data
                )
                self.refresh_all()
            except ValueError as error:
                QMessageBox.warning(self, "Invalid Task", str(error))
            except Exception as error:
                QMessageBox.critical(self, "Database Error", f"Could not update task.\n\n{error}")

    def confirm_delete(self, task_id):
        reply = QMessageBox.question(
            self,
            "Delete Task",
            "Are you sure you want to delete this task?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.task_service.delete_task(task_id, self.current_user["id"])
            self.refresh_all()

    def show_verse(self):
        if self.verse_dialog is None or not self.verse_dialog.isVisible():
            self.verse_dialog = VerseDialog(self, self.verse_service)
            self.verse_dialog.finished.connect(self.egg.reset)
            self.verse_dialog.show()