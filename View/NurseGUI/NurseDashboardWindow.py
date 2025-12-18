from PyQt6.QtWidgets import QWidget, QHeaderView, QScrollArea, QVBoxLayout
from PyQt6.QtCore import Qt
from Utilities.Designers import Designer
from View.GeneralPopups.KPIRecordsWindow import KPIRecordsPopup

class NurseDashboardWindow(QWidget):
    """
    Nurse Dashboard Window
    """

    def __init__(
        self,
        assignedPatientsKpi, dueMedicationsKpi, urgentKpi,
        userInfo, role, completedMedicationsData, preparationStatusData
    ):
        super().__init__()
        self.setFixedSize(1500, 800)
        self.setWindowTitle("MEDISYNC Nurse Dashboard")
        Designer.setWindowToCenter(self)

        self.userInfo = userInfo
        self.role = role
        self.completedMedicationsData = completedMedicationsData
        self.preparationStatusData = preparationStatusData

        self.kpi_values = {
            "Assigned Patients": assignedPatientsKpi,
            "Due Medications": dueMedicationsKpi,
            "Urgent": urgentKpi,
        }

        self._setupBackground()
        self._createTopBar()
        self._createKPICards()
        self._createCompletedMedicationsTable()
        self._createPreparationStatusCard()

    def _setupBackground(self):
        """Apply background style"""
        Designer.setBackground(self)

    def _createTopBar(self):
        """Create top navigation bar with logo, menu, and user info"""
        self.topCard = Designer.createRoundedCard(self)
        self.topCard.setGeometry(0, -25, 1500, 100)

        Designer.setLogo(self.topCard).setGeometry(60, 10, 90, 90)

        start_x, gap = 500, 225
        self.dashboardOption = Designer.createClickedOption(
            self.topCard, "Dashboard",
            "../ImageResources/Icon8BGRemoved.png", 170
        )
        self.dashboardOption.move(start_x, 40)

        self.administerOption = Designer.createMenuOption(
            self.topCard, "Administer",
            "../ImageResources/Icon5BGRemoved.png", 180
        )
        self.administerOption.move(start_x + gap, 40)

        self.notificationsOption = Designer.createMenuOption(
            self.topCard, "Notifications",
            "../ImageResources/Icon4BGRemoved.png", 180
        )
        self.notificationsOption.move(start_x + gap * 2, 40)

        self.logoutOption = Designer.createMenuOption(
            self.topCard, "Logout",
            "../ImageResources/Icon6BGRemoved.png", 160
        )
        self.logoutOption.move(start_x + gap * 3 + 50, 40)

        Designer.setImage(self.topCard, "../ImageResources/Icon14BGRemoved.png").setGeometry(215, 40, 45, 45)
        Designer.createLabel(self.userInfo, self.topCard, "#1a1a1a", 700, 13).setGeometry(280, 45, 120, 14)
        Designer.createLabel(self.role, self.topCard, "#333333", 400, 12).setGeometry(280, 65, 120, 15)

    def _createKPICards(self):
        """Create clickable KPI cards"""
        x_start, gap, y_pos = 45, 290, 105
        icons = [
            "../ImageResources/Icon1BGRemoved.png",
            "../ImageResources/Icon5BGRemoved.png",
            "../ImageResources/Icon3BGRemoved.png",
        ]
        labels = list(self.kpi_values.keys())
        values = list(self.kpi_values.values())

        self.kpi_cards = []
        for i, (icon, label, value) in enumerate(zip(icons, labels, values)):
            card = Designer.createKPI(self, icon, str(value), label, x=x_start + gap * i, y=y_pos)
            card.setCursor(Qt.CursorShape.PointingHandCursor)
            card.mousePressEvent = lambda e, l=label: self._showKPIDetails(l)
            self.kpi_cards.append(card)

    def _showKPIDetails(self, kpi_label: str):
        """Show detailed records when KPI card is clicked"""
        from Model.KPIs.NurseKPIs import NurseKPIDetails
        data = NurseKPIDetails.get_details(kpi_label.replace(" ", "_").lower())
        columns = NurseKPIDetails.get_columns(kpi_label.replace(" ", "_").lower())

        self.popup = KPIRecordsPopup(f"{kpi_label} - Detailed View", columns, data)
        self.popup.show()

    def _createCompletedMedicationsTable(self):
        """Display completed medications table"""
        columns = [
            "Patient Name", "Medication",
            "Dosage", "Time", "Assessment", "Status"
        ]
        column_map = {
            "Patient Name": "patient_name",
            "Medication": "medication",
            "Dosage": "dosage",
            "Time": "administration_time",
            "Assessment": "patient_assessment",
            "Status": "status"
        }

        self.completedTable, self.completedCard = Designer.createTableCard(
            self, labelText="Completed Medications Today", fontSize=22,
            columnNames=columns, columnMap=column_map,
            cardWidth=815, cardHeight=400, tableWidth=770, tableHeight=305,
            x=45, y=345, data=self.completedMedicationsData
        )
        header = self.completedTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _createPreparationStatusCard(self):
        """Display medication preparation status in scrollable cards"""
        self.statusCard = Designer.createRoundedCard(self, 545, 635)
        self.statusCard.move(915, 110)

        Designer.createLabel(
            "Medication Preparation Status",
            self.statusCard, "#1a1a1a", 700, 22
        ).setGeometry(35, 25, 350, 30)

        self.scrollArea = QScrollArea(self.statusCard)
        self.scrollArea.setGeometry(35, 70, 510, 545)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("""
            QScrollArea {background-color: transparent; border: none;}
            QScrollBar:vertical {background-color: #cef2f9; width: 12px; border-radius: 6px;}
            QScrollBar::handle:vertical {background-color: #0cc0df; border-radius: 6px; min-height: 20px;}
            QScrollBar::handle:vertical:hover {background-color: #26d6ec;}
        """)

        self.scrollWidget = QWidget()
        self.scrollWidget.setStyleSheet("background-color: #cef2f9;")
        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setContentsMargins(0, 0, 10, 0)
        self.scrollLayout.setSpacing(15)
        self.scrollLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._loadPreparationStatusCards()

        self.scrollArea.setWidget(self.scrollWidget)

    def _loadPreparationStatusCards(self):
        while self.scrollLayout.count():
            child = self.scrollLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for item in self.preparationStatusData:
            patient_name = f"{item.get('patient_first_name', '')} {item.get('patient_last_name', '')}"
            medication = f"{item.get('brand_name', '')} {item.get('dosage', '')}"
            time = self._formatTime(item.get('frequency', 'As needed'))
            status = "Ready" if item.get('status') == "Prepared" else "Pending"

            card = self._createStatusItemCard(patient_name, medication, time, status)
            self.scrollLayout.addWidget(card)

    @staticmethod
    def _formatTime(frequency):
        freq_map = {
            "Once a day": "09:00 AM",
            "Twice a day": "09:00 AM, 09:00 PM",
            "Three times a day": "08:00 AM, 02:00 PM, 08:00 PM",
            "Every 6 hours": "Every 6 hours",
            "Every 8 hours": "Every 8 hours",
            "As needed": "As needed"
        }
        return freq_map.get(frequency, "See schedule")

    def _createStatusItemCard(self, patientName, medication, time, status):
        card = QWidget(self.scrollWidget)
        card.setFixedSize(480, 110)

        statusColor = "#7bc96f" if status == "Ready" else "#ffa500"

        card.setStyleSheet(f"""
            QWidget {{background-color: white; border-radius: 20px; border-left: 8px solid {statusColor};}}
            QLabel {{border: none; background-color: transparent;}}
        """)

        Designer.createLabel(patientName, card, "#1a1a1a", 700, 15).setGeometry(25, 15, 300, 20)

        Designer.createLabel(medication, card, "#333333", 600, 13).setGeometry(25, 40, 300, 20)

        Designer.createLabel(f"Due: {time}", card, "#666666", 400, 12).setGeometry(25, 62, 200, 20)

        statusBadge = Designer.createLabel(status, card, "#1a1a1a", 700, 13)
        statusBadge.setGeometry(330, 30, 90, 30)
        statusBadge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        statusBadge.setStyleSheet(f"""
            QLabel {{background-color: {statusColor}; color: #1a1a1a; border-radius: 15px;  font: 13px 'Lato'; font-weight: bold;}}
        """)

        return card