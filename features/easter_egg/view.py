from PyQt6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QDialog, QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from features.easter_egg.service import VerseService
from styles import DIALOG_STYLE


class VerseDialog(QDialog):
    """Dialog displaying the easter egg Bible verse."""

    def __init__(self, parent=None, verse_service=None):
        super().__init__(parent)
        self.verse_service = verse_service or VerseService()

        self.setWindowTitle("TASKTIFY • Bible Verse")
        self.setFixedSize(550, 400)
        self.setModal(True)
        self.setStyleSheet(DIALOG_STYLE)

        verse_obj = self.verse_service.get_random_verse()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 28, 35, 25)
        layout.setSpacing(14)

        icon = QLabel("✦")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("QLabel { color: #ffd86e; font-size: 32px; }")
        layout.addWidget(icon)

        title = QLabel("A Little Reminder for You")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        card = QFrame()
        card.setObjectName("verseCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 25, 30, 25)
        card_layout.setSpacing(18)

        verse_label = QLabel(f"“{verse_obj.text}”")
        verse_label.setWordWrap(True)
        verse_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        verse_label.setStyleSheet("QLabel { color: #fff6d8; font-size: 17px; font-weight: 500; }")
        card_layout.addWidget(verse_label)

        reference_label = QLabel(f"— {verse_obj.reference}")
        reference_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        reference_label.setStyleSheet("QLabel { color: #b9c9e6; font-size: 12px; font-weight: 700; }")
        card_layout.addWidget(reference_label)

        layout.addWidget(card, 1)

        amen_button = QPushButton("Amen 🙏")
        amen_button.setObjectName("primary")
        amen_button.setFixedSize(160, 44)
        amen_button.clicked.connect(self.accept)
        layout.addWidget(amen_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setWindowOpacity(0.0)
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(450)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def showEvent(self, event):
        super().showEvent(event)
        self.fade_animation.start()


class EggWidget(QFrame):
    """Interactive animated egg widget."""

    verse_ready = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(230, 245)
        self.stage = 0
        self.busy = False
        self.shake_animation = None

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Tap the egg for a surprise!")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.busy:
            self.start_cracking()

    def start_cracking(self):
        self.busy = True
        self.stage = 1
        self.update()

        original_position = self.pos()
        self.shake_animation = QPropertyAnimation(self, b"pos")
        self.shake_animation.setDuration(850)
        self.shake_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.shake_animation.setStartValue(original_position)

        self.shake_animation.setKeyValueAt(0.10, original_position + QPoint(-8, 0))
        self.shake_animation.setKeyValueAt(0.20, original_position + QPoint(8, 0))
        self.shake_animation.setKeyValueAt(0.30, original_position + QPoint(-9, 0))
        self.shake_animation.setKeyValueAt(0.40, original_position + QPoint(9, 0))
        self.shake_animation.setKeyValueAt(0.50, original_position + QPoint(-7, 0))
        self.shake_animation.setKeyValueAt(0.60, original_position + QPoint(7, 0))
        self.shake_animation.setKeyValueAt(0.70, original_position + QPoint(-4, 0))
        self.shake_animation.setEndValue(original_position)

        self.shake_animation.finished.connect(self.show_crack)
        self.shake_animation.start()

    def show_crack(self):
        self.stage = 2
        self.update()
        QTimer.singleShot(750, self.reveal_verse)

    def reveal_verse(self):
        if not self.busy:
            return
        self.stage = 3
        self.update()
        self.verse_ready.emit()

    def reset(self):
        self.stage = 0
        self.busy = False
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center_x = self.width() // 2
        base_y = 150

        if self.stage in (1, 2, 3):
            for radius in range(92, 45, -8):
                alpha = max(4, 48 - (radius - 45))
                painter.setBrush(QColor(255, 213, 100, alpha))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(center_x - radius, base_y - radius, radius * 2, radius * 2)

        painter.setBrush(QColor(3, 10, 25, 190))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - 70, base_y + 35, 140, 23)

        painter.setBrush(QColor("#3c765a"))
        leaves = [
            (32, 165, 42, 15), (50, 179, 34, 13),
            (130, 174, 43, 14), (151, 160, 35, 13), (76, 177, 35, 12)
        ]
        for x, y, width, height in leaves:
            painter.drawEllipse(x, y, width, height)

        flowers = [(47, 180), (155, 176), (78, 187)]
        for x, y in flowers:
            painter.setBrush(QColor("#f6d8ed"))
            painter.drawEllipse(x, y, 10, 10)
            painter.drawEllipse(x + 7, y, 10, 10)
            painter.drawEllipse(x + 3, y - 7, 10, 10)
            painter.setBrush(QColor("#f4c85b"))
            painter.drawEllipse(x + 5, y + 3, 8, 8)

        egg_points = [
            QPoint(center_x, 40), QPoint(center_x - 36, 51),
            QPoint(center_x - 54, 92), QPoint(center_x - 51, 140),
            QPoint(center_x - 31, 167), QPoint(center_x, 176),
            QPoint(center_x + 31, 167), QPoint(center_x + 51, 140),
            QPoint(center_x + 54, 92), QPoint(center_x + 36, 51)
        ]
        painter.setBrush(QColor("#fff0ba"))
        painter.setPen(QPen(QColor("#dfbd67"), 2))
        painter.drawPolygon(egg_points)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#e8bb5b"))
        spots = [
            (center_x - 26, 73, 12, 16), (center_x + 16, 68, 12, 14),
            (center_x - 31, 115, 11, 14), (center_x + 21, 109, 14, 17),
            (center_x - 5, 145, 14, 11)
        ]
        for x, y, width, height in spots:
            painter.drawEllipse(x, y, width, height)

        if self.stage >= 2:
            painter.setPen(QPen(QColor("#c78b32"), 3))
            crack_points = [
                QPoint(center_x - 52, 110), QPoint(center_x - 29, 104),
                QPoint(center_x - 9, 116), QPoint(center_x + 9, 103),
                QPoint(center_x + 29, 113), QPoint(center_x + 52, 105)
            ]
            painter.drawPolyline(crack_points)

        if self.stage == 3:
            painter.setPen(QPen(QColor("#ffe79a"), 3))
            sparks = [
                (center_x - 67, 74, center_x - 82, 59),
                (center_x + 67, 74, center_x + 82, 59),
                (center_x - 70, 135, center_x - 86, 145),
                (center_x + 70, 135, center_x + 86, 145),
                (center_x - 5, 29, center_x - 5, 10),
                (center_x + 20, 36, center_x + 29, 20)
            ]
            for x1, y1, x2, y2 in sparks:
                painter.drawLine(x1, y1, x2, y2)

        painter.end()