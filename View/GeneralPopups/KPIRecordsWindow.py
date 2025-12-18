from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from Utilities.Designers import Designer

class KPIRecordsPopup(QWidget):
    """
    Reusable popup window for displaying KPI results.
    """

    def __init__(self, title: str, columnNames: list, dataset: list):
        super().__init__()

        # Window settings
        self.setWindowTitle(title)
        self.setFixedSize(900, 600)
        Designer.setWindowToCenter(self)
        self.setStyleSheet("""
                QWidget {
                 background-color: #cef2f9
                }
                """)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Header label
        label = Designer.createLabel(title, self, "#1a1a1a", 700, 20)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)

        # Table
        table = Designer.createStandardTable(columnNames)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(table)

        # Populate table
        table.setRowCount(len(dataset))
        for row_idx, row in enumerate(dataset):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row_idx, col_idx, item)

        self.table = table