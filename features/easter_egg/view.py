# PyQt tools for animations, timers, signals, and positions
from PyQt6.QtCore import (
    QEasingCurve, QPoint, QPropertyAnimation,
    QTimer, Qt, pyqtSignal
)

# Tools for drawing shapes and colors
from PyQt6.QtGui import QColor, QPainter, QPen

# PyQt widgets used in the dialog and egg
from PyQt6.QtWidgets import (
    QDialog, QFrame, QLabel, QPushButton,
    QVBoxLayout, QWidget
)

# Service used to get a random Bible verse
from features.easter_egg.service import VerseService

# Style used by the dialog
from styles import DIALOG_STYLE


class VerseDialog(QDialog):
    """Dialog that displays a random Bible verse."""

    def __init__(self, parent=None, verse_service=None):
        # Initialize the dialog
        super().__init__(parent)

        # Use the given service or create a new VerseService
        self.verse_service = verse_service or VerseService()

        # Set the dialog title and size
        self.setWindowTitle("TASKTIFY • Bible Verse")
        self.setFixedSize(550, 400)

        # Make the dialog stay in front until closed
        self.setModal(True)

        # Apply the dialog design
        self.setStyleSheet(DIALOG_STYLE)

        # Get a random Bible verse
        verse_obj = self.verse_service.get_random_verse()

        # Create the main vertical layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 28, 35, 25)
        layout.setSpacing(14)

        # Create the star icon
        icon = QLabel("✦")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet(
            "QLabel { color: #ffd86e; font-size: 32px; }"
        )
        layout.addWidget(icon)

        # Create the dialog title
        title = QLabel("A Little Reminder for You")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        # Create a frame to hold the Bible verse
        card = QFrame()
        card.setObjectName("verseCard")

        # Create a layout inside the verse card
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 25, 30, 25)
        card_layout.setSpacing(18)

        # Display the Bible verse text
        verse_label = QLabel(f"“{verse_obj.text}”")
        verse_label.setWordWrap(True)
        verse_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        verse_label.setStyleSheet(
            "QLabel { color: #fff6d8; font-size: 17px; font-weight: 500; }"
        )
        card_layout.addWidget(verse_label)

        # Display the Bible verse reference
        reference_label = QLabel(f"— {verse_obj.reference}")
        reference_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        reference_label.setStyleSheet(
            "QLabel { color: #b9c9e6; font-size: 12px; font-weight: 700; }"
        )
        card_layout.addWidget(reference_label)

        # Add the verse card to the main layout
        layout.addWidget(card, 1)

        # Create the Amen button
        amen_button = QPushButton("Amen 🙏")
        amen_button.setObjectName("primary")
        amen_button.setFixedSize(160, 44)

        # Close the dialog when the button is clicked
        amen_button.clicked.connect(self.accept)

        # Center the button
        layout.addWidget(
            amen_button,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Start the dialog as invisible
        self.setWindowOpacity(0.0)

        # Create a fade-in animation
        self.fade_animation = QPropertyAnimation(
            self, b"windowOpacity"
        )
        self.fade_animation.setDuration(450)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)

        # Make the animation start slowly and finish smoothly
        self.fade_animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

    # Runs when the dialog is shown
    def showEvent(self, event):
        super().showEvent(event)

        # Start the fade-in animation
        self.fade_animation.start()


class EggWidget(QFrame):
    """Interactive egg that reveals a random Bible verse."""

    # Signal used to tell the main window that the verse is ready
    verse_ready = pyqtSignal()

    def __init__(self, parent=None):
        # Initialize the egg widget
        super().__init__(parent)

        # Set the size of the egg
        self.setFixedSize(230, 245)

        # 0 = normal, 1 = shaking, 2 = cracked, 3 = revealed
        self.stage = 0

        # Prevent the egg from being clicked while it is animating
        self.busy = False

        # Store the shaking animation
        self.shake_animation = None

        # Change the mouse cursor when hovering over the egg
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Show a helpful message when the mouse is over the egg
        self.setToolTip("Tap the egg for a surprise!")

    # Runs when the user clicks the egg
    def mousePressEvent(self, event):

        # Only respond to a left click when the egg is not busy
        if (
            event.button() == Qt.MouseButton.LeftButton
            and not self.busy
        ):
            self.start_cracking()

    # Starts the egg cracking animation
    def start_cracking(self):

        # Mark the egg as busy
        self.busy = True

        # Change the egg to the shaking stage
        self.stage = 1
        self.update()

        # Save the egg's original position
        original_position = self.pos()

        # Create a shaking animation
        self.shake_animation = QPropertyAnimation(
            self, b"pos"
        )
        self.shake_animation.setDuration(850)
        self.shake_animation.setEasingCurve(
            QEasingCurve.Type.InOutQuad
        )

        # Set the starting position
        self.shake_animation.setStartValue(
            original_position
        )

        # Move the egg left and right several times
        self.shake_animation.setKeyValueAt(
            0.10, original_position + QPoint(-8, 0)
        )
        self.shake_animation.setKeyValueAt(
            0.20, original_position + QPoint(8, 0)
        )
        self.shake_animation.setKeyValueAt(
            0.30, original_position + QPoint(-9, 0)
        )
        self.shake_animation.setKeyValueAt(
            0.40, original_position + QPoint(9, 0)
        )
        self.shake_animation.setKeyValueAt(
            0.50, original_position + QPoint(-7, 0)
        )
        self.shake_animation.setKeyValueAt(
            0.60, original_position + QPoint(7, 0)
        )
        self.shake_animation.setKeyValueAt(
            0.70, original_position + QPoint(-4, 0)
        )

        # Return the egg to its original position
        self.shake_animation.setEndValue(
            original_position
        )

        # Show the crack after the shaking finishes
        self.shake_animation.finished.connect(
            self.show_crack
        )

        # Start the shaking animation
        self.shake_animation.start()

    # Shows the crack on the egg
    def show_crack(self):

        # Change to the cracked stage
        self.stage = 2
        self.update()

        # Wait 750 milliseconds before revealing the verse
        QTimer.singleShot(750, self.reveal_verse)

    # Reveals that the verse is ready
    def reveal_verse(self):

        # Stop if the egg is no longer active
        if not self.busy:
            return

        # Change to the revealed stage
        self.stage = 3
        self.update()

        # Tell the main window that the verse is ready
        self.verse_ready.emit()

    # Resets the egg to its original state
    def reset(self):

        # Return to the normal stage
        self.stage = 0

        # Allow the egg to be clicked again
        self.busy = False

        # Redraw the egg
        self.update()

    # Draws the egg and its decorations
    def paintEvent(self, event):

        # Create the painter
        painter = QPainter(self)

        # Make the drawing smoother
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        # Find the center of the widget
        center_x = self.width() // 2

        # Set the vertical position of the egg
        base_y = 150

        # Draw the glowing effect when the egg is active
        if self.stage in (1, 2, 3):

            for radius in range(92, 45, -8):

                # Calculate the transparency
                alpha = max(
                    4, 48 - (radius - 45)
                )

                # Set the glow color
                painter.setBrush(
                    QColor(255, 213, 100, alpha)
                )

                painter.setPen(Qt.PenStyle.NoPen)

                # Draw the glow circle
                painter.drawEllipse(
                    center_x - radius,
                    base_y - radius,
                    radius * 2,
                    radius * 2
                )

        # Draw the shadow below the egg
        painter.setBrush(
            QColor(3, 10, 25, 190)
        )
        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawEllipse(
            center_x - 70,
            base_y + 35,
            140,
            23
        )

        # Draw the leaves below the egg
        painter.setBrush(QColor("#3c765a"))

        leaves = [
            (32, 165, 42, 15),
            (50, 179, 34, 13),
            (130, 174, 43, 14),
            (151, 160, 35, 13),
            (76, 177, 35, 12)
        ]

        # Draw each leaf
        for x, y, width, height in leaves:
            painter.drawEllipse(
                x, y, width, height
            )

        # Positions of the flowers
        flowers = [
            (47, 180),
            (155, 176),
            (78, 187)
        ]

        # Draw each flower
        for x, y in flowers:

            # Draw the flower petals
            painter.setBrush(QColor("#f6d8ed"))
            painter.drawEllipse(x, y, 10, 10)
            painter.drawEllipse(x + 7, y, 10, 10)
            painter.drawEllipse(x + 3, y - 7, 10, 10)

            # Draw the yellow center of the flower
            painter.setBrush(QColor("#f4c85b"))
            painter.drawEllipse(
                x + 5, y + 3, 8, 8
            )

        # Points used to create the egg shape
        egg_points = [
            QPoint(center_x, 40),
            QPoint(center_x - 36, 51),
            QPoint(center_x - 54, 92),
            QPoint(center_x - 51, 140),
            QPoint(center_x - 31, 167),
            QPoint(center_x, 176),
            QPoint(center_x + 31, 167),
            QPoint(center_x + 51, 140),
            QPoint(center_x + 54, 92),
            QPoint(center_x + 36, 51)
        ]

        # Set the egg color
        painter.setBrush(QColor("#fff0ba"))

        # Set the egg outline
        painter.setPen(
            QPen(QColor("#dfbd67"), 2)
        )

        # Draw the egg
        painter.drawPolygon(egg_points)

        # Remove the outline for the egg spots
        painter.setPen(Qt.PenStyle.NoPen)

        # Set the spot color
        painter.setBrush(QColor("#e8bb5b"))

        # Positions and sizes of the egg spots
        spots = [
            (center_x - 26, 73, 12, 16),
            (center_x + 16, 68, 12, 14),
            (center_x - 31, 115, 11, 14),
            (center_x + 21, 109, 14, 17),
            (center_x - 5, 145, 14, 11)
        ]

        # Draw each spot
        for x, y, width, height in spots:
            painter.drawEllipse(
                x, y, width, height
            )

        # Draw the crack when the egg reaches stage 2
        if self.stage >= 2:

            painter.setPen(
                QPen(QColor("#c78b32"), 3)
            )

            crack_points = [
                QPoint(center_x - 52, 110),
                QPoint(center_x - 29, 104),
                QPoint(center_x - 9, 116),
                QPoint(center_x + 9, 103),
                QPoint(center_x + 29, 113),
                QPoint(center_x + 52, 105)
            ]

            # Draw the crack line
            painter.drawPolyline(crack_points)

        # Draw spark effects when the verse is revealed
        if self.stage == 3:

            painter.setPen(
                QPen(QColor("#ffe79a"), 3)
            )

            sparks = [
                (
                    center_x - 67, 74,
                    center_x - 82, 59
                ),
                (
                    center_x + 67, 74,
                    center_x + 82, 59
                ),
                (
                    center_x - 70, 135,
                    center_x - 86, 145
                ),
                (
                    center_x + 70, 135,
                    center_x + 86, 145
                ),
                (
                    center_x - 5, 29,
                    center_x - 5, 10
                ),
                (
                    center_x + 20, 36,
                    center_x + 29, 20
                )
            ]

            # Draw each spark
            for x1, y1, x2, y2 in sparks:
                painter.drawLine(
                    x1, y1, x2, y2
                )

        # Finish drawing
        painter.end()
