from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout
from Utilities.Designers import Designer

class PharmacistDashboardWindow(QWidget):
    """
    Pharmacist Dashboard Window
    """

    def __init__(self, activePrescriptionsKpi, pendingKpi, controlledKpi,
                 userInfo, role, expiringData, medicationsToPrep):
        super().__init__()
        self.setFixedSize(1500, 800)
        self.setWindowTitle("MEDISYNC Pharmacist Dashboard")
        Designer.setWindowToCenter(self)

        self.userInfo = userInfo
        self.role = role
        self.medicationsToPrep = medicationsToPrep

        Designer.setBackground(self)

        self._createTopBar()
        self._createKPICards(activePrescriptionsKpi, pendingKpi, controlledKpi)
        self._createExpiringTable(expiringData)
        self._createMedicationsPrepareCard(medicationsToPrep)

    def _createTopBar(self):
        """Creates the top navigation bar"""
        self.topCard = Designer.createRoundedCard(self)
        self.topCard.setGeometry(0, -25, 1500, 100)

        logo = Designer.setLogo(self.topCard)
        logo.setGeometry(60, 10, 90, 90)

        self.dashboardOption = Designer.createClickedOption(
            self.topCard, "Dashboard",
            "../ImageResources/Icon8BGRemoved.png", 180
        )
        self.dashboardOption.move(500, 40)

        self.verificationOption = Designer.createMenuOption(
            self.topCard, "Verify",
            "../ImageResources/Icon7BGRemoved.png", 160
        )
        self.verificationOption.move(745, 40)

        self.notificationsOption = Designer.createMenuOption(
            self.topCard, "Notifications",
            "../ImageResources/Icon4BGRemoved.png", 180
        )
        self.notificationsOption.move(950, 40)

        self.logoutOption = Designer.createMenuOption(
            self.topCard, "Logout",
            "../ImageResources/Icon6BGRemoved.png", 150
        )
        self.logoutOption.move(1300, 40)

        profileIcon = Designer.setImage(self.topCard, "../ImageResources/Icon14BGRemoved.png")
        profileIcon.setGeometry(215, 40, 45, 45)

        self.userLabel = Designer.createLabel(self.userInfo, self.topCard, "#1a1a1a", 700, 13)
        self.userLabel.setGeometry(280, 45, 150, 14)

        self.titleLabel = Designer.createLabel(self.role, self.topCard, "#333333", 400, 12)
        self.titleLabel.setGeometry(280, 65, 150, 15)

    def _createKPICards(self, activePrescriptionsKpi, pendingKpi, controlledKpi):
        """Creates clickable KPI cards"""
        x_start, gap, y_pos = 50, 275, 110
        icons = [
            "../ImageResources/Icon2BGRemoved.png",
            "../ImageResources/Icon7BGRemoved.png",
            "../ImageResources/Icon10BGRemoved.png"
        ]
        labels = ["Active Prescriptions", "Pending Verification", "Controlled Substances"]
        values = [activePrescriptionsKpi, pendingKpi, controlledKpi]

        self.kpi_cards = []
        for i, (icon, label, value) in enumerate(zip(icons, labels, values)):
            card = Designer.createKPI(self, icon, str(value), label,
                                      x=x_start + gap * i, y=y_pos)
            card.setCursor(Qt.CursorShape.PointingHandCursor)
            card.mousePressEvent = lambda e, l=label: self._showKPIDetails(l)
            self.kpi_cards.append(card)

    def _showKPIDetails(self, kpi_label: str):
        """Show detailed records when KPI card is clicked"""
        from Model.KPIs.PharmacistKPIs import PharmacistKPIDetails
        data = PharmacistKPIDetails.get_details(kpi_label.replace(" ", "_").lower())
        columns = PharmacistKPIDetails.get_columns(kpi_label.replace(" ", "_").lower())

        from View.GeneralPopups.KPIRecordsWindow import KPIRecordsPopup
        self.popup = KPIRecordsPopup(f"{kpi_label} - Detailed View", columns, data)
        self.popup.show()

    def _createExpiringTable(self, expiringData):
        """Creates the Expiring Soon table"""
        columns = [
            "Prescription ID", "Patient Name", "Medication",
            "Quantity", "Expiry Date", "Days Until Expiry"
        ]

        column_map = {
            "Prescription ID": "prescription_id",
            "Patient Name": "patient_name",
            "Medication": "medication",
            "Quantity": "quantity_dispensed",
            "Expiry Date": "expiry_date",
            "Days Until Expiry": "days_until_expiry"
        }

        self.expiringTable, self.expiringCard = Designer.createTableCard(
            self,
            labelText="Medications Expiry",
            fontSize=22,
            columnNames=columns,
            columnMap=column_map,
            cardWidth=775,
            cardHeight=400,
            tableWidth=735,
            tableHeight=305,
            x=50,
            y=345,
            data=expiringData
        )

    def _createMedicationsPrepareCard(self, medicationsData):
        """Creates the Medications To Prepare scrollable card"""
        self.prepareMedicationsCard = Designer.createRoundedCard(self, 580, 635)
        self.prepareMedicationsCard.move(875, 110)

        prepareTitleLabel = Designer.createLabel(
            "Medications To Prepare",
            self.prepareMedicationsCard, "#1a1a1a", 700, 22
        )
        prepareTitleLabel.setGeometry(35, 25, 300, 30)

        self.scrollArea = QScrollArea(self.prepareMedicationsCard)
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

        self.displayMedicationCards(medicationsData)
        self.scrollArea.setWidget(self.scrollWidget)

    def displayMedicationCards(self, medicationsData):
        """Loads medication cards from data"""
        while self.scrollLayout.count():
            item = self.scrollLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not medicationsData:
            self._displayEmptyState()
            return

        for med in medicationsData:
            card = self._createMedicationCard(med)
            self.scrollLayout.addWidget(card)

    def _displayEmptyState(self):
        """Displays empty state message"""
        placeholder = Designer.createLabel(
            "No medications to prepare at the moment.\nAll preparations are up to date.",
            self.scrollWidget, "#666666", 400, 16
        )
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("QLabel {background-color: transparent; border: none; padding: 100px 20px;}")
        self.scrollLayout.addWidget(placeholder)

    def _createMedicationCard(self, med):
        """Creates a single medication card"""
        card = QWidget(self.scrollWidget)
        card.setFixedSize(480, 110)
        card.setStyleSheet("""
            QWidget {background-color: white; border-radius: 20px; border: 1px solid #b8e6f0;}
            QLabel {border: none; background-color: transparent;}
        """)

        preparation_id = med.get('preparation_id')
        card.setProperty("preparation_id", preparation_id)

        rx_id = med.get('prescription_id', 'N/A')
        patient_first = med.get('patient_first_name', 'Unknown')
        patient_last = med.get('patient_last_name', '')
        patient_name = f"{patient_first} {patient_last}".strip() or "Unknown Patient"

        brand = med.get('brand_name', '')
        generic = med.get('generic_name', 'Unknown Medicine')
        medication = f"{brand} ({generic})" if brand else generic

        quantity_prepared = med.get('quantity_prepared', 0)
        quantity = f"{quantity_prepared} units"

        status = med.get('status', 'To be Prepared')
        statusColor = "#7bc96f" if status == "Prepared" else "#ffa500"

        statusBar = QWidget(card)
        statusBar.setGeometry(0, 0, 8, 110)
        statusBar.setStyleSheet(f"""
            QWidget {{
                background-color: {statusColor};
                border-top-left-radius: 20px;
                border-bottom-left-radius: 20px;
                border: none;
            }}
        """)

        Designer.createLabel(f"RX ID: {rx_id}", card, "#1a1a1a", 700, 14).setGeometry(25, 15, 200, 20)
        Designer.createLabel(f"Patient: {patient_name}", card, "#333333", 600, 13).setGeometry(25, 40, 300, 20)
        Designer.createLabel(f"Medication: {medication}", card, "#333333", 400, 12).setGeometry(25, 62, 380, 20)
        Designer.createLabel(f"Quantity: {quantity}", card, "#333333", 400, 12).setGeometry(25, 82, 200, 20)

        self.statusButton = Designer.createPrimaryButton(
            "To be Prepared", card, statusColor, "#1a1a1a", 700, 12, 15
        )
        self.statusButton.setGeometry(330, 35, 120, 35)

        return card