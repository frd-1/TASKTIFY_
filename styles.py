APP_STYLE = """
* {
    font-family: "Arial";
}

QMainWindow {
    background: #07152d;
}

QWidget {
    color: #f3f6ff;
}

QFrame#sidebar {
    background: #061226;
    border-right: 1px solid #263e69;
}

QLabel#logo {
    color: #ffffff;
    font-size: 23px;
    font-weight: 800;
}

QLabel#tagline {
    color: #9eafcd;
    font-size: 10px;
}

QPushButton#navButton {
    background: transparent;
    border: none;
    border-radius: 10px;
    color: #d6e1f7;
    padding: 11px 13px;
    text-align: left;
    font-size: 13px;
}

QPushButton#navButton:hover {
    background: #162b50;
}

QPushButton#navButton[selected="true"] {
    background: #355edb;
    color: white;
    font-weight: 700;
}

QLabel#pageTitle {
    color: #ffffff;
    font-size: 27px;
    font-weight: 800;
}

QLabel#subtitle {
    color: #a7b6d0;
    font-size: 11px;
}

QFrame#glassCard {
    background: #102647;
    border: 1px solid #304c7a;
    border-radius: 17px;
}

QFrame#statCard {
    background: #132b50;
    border: 1px solid #2e4a77;
    border-radius: 15px;
}

QLabel#statNumber {
    color: #ffffff;
    font-size: 24px;
    font-weight: 800;
}

QLabel#statLabel {
    color: #9eafcd;
    font-size: 10px;
}

QLineEdit,
QComboBox,
QDateEdit,
QTextEdit {
    background: #0a1b36;
    color: #f4f7ff;
    border: 1px solid #3b5683;
    border-radius: 8px;
    padding: 8px;
}

QLineEdit:focus,
QComboBox:focus,
QDateEdit:focus,
QTextEdit:focus {
    border: 1px solid #718cff;
}

QComboBox QAbstractItemView {
    background: #102442;
    color: white;
    selection-background-color: #355edb;
}

QPushButton#primary {
    background: #4b68e8;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 17px;
    font-weight: 700;
}

QPushButton#primary:hover {
    background: #617bf0;
}

QPushButton#secondary {
    background: #1d3760;
    color: white;
    border: 1px solid #3d5986;
    border-radius: 8px;
    padding: 8px 13px;
}

QPushButton#secondary:hover {
    background: #294977;
}

QPushButton#danger {
    background: #a83d5d;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 12px;
    font-weight: 700;
}

QPushButton#danger:hover {
    background: #c84e70;
}

QTableWidget {
    background: #0a1b36;
    color: #eaf0ff;
    border: 1px solid #2c4773;
    border-radius: 13px;
    gridline-color: #203a63;
    selection-background-color: #294f94;
    selection-color: white;
    outline: none;
}

QTableWidget::item {
    padding: 7px;
}

QHeaderView::section {
    background: #142c52;
    color: #dce7ff;
    border: none;
    padding: 10px;
    font-weight: 700;
}

QScrollBar:vertical {
    background: #08162c;
    width: 9px;
}

QScrollBar::handle:vertical {
    background: #36527e;
    border-radius: 4px;
}

QDialog {
    background: #091a34;
}

QLabel#dialogTitle {
    color: #ffffff;
    font-size: 21px;
    font-weight: 800;
}

QLabel#fieldLabel {
    color: #b8c6df;
    font-size: 11px;
    font-weight: 700;
}

QFrame#verseCard {
    background: #142e54;
    border: 1px solid #4b6590;
    border-radius: 16px;
}
"""

CENTRAL_BACKGROUND_STYLE = """
QWidget#background {
    background:
        qlineargradient(
            x1: 0,
            y1: 0,
            x2: 1,
            y2: 1,
            stop: 0 #162c59,
            stop: 0.42 #172d62,
            stop: 0.72 #102a4f,
            stop: 1 #0a1932
        );
}
"""

DIALOG_STYLE = APP_STYLE