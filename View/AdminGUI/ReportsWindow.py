from PyQt6.QtWidgets import QWidget, QFrame, QStackedWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from Utilities.Designers import Designer


class ReportsWindow(QWidget):
    """
    Main Reports Window
    """

    def __init__(self, userInfo, role):
        super().__init__()
        self.setFixedSize(1500, 800)
        self.setWindowTitle("MEDISYNC Reports")
        Designer.setWindowToCenter(self)

        self.userInfo = userInfo
        self.role = role
        self.currentReportType = None
        self.currentReportData = []

        Designer.setBackground(self)

        self._createTopBar()
        self._createMainContent()

    def _createTopBar(self):
        """Creates the top navigation bar"""
        self.topCard = Designer.createRoundedCard(self)
        self.topCard.setGeometry(0, -25, 1500, 100)

        logo = Designer.setLogo(self.topCard)
        logo.setGeometry(60, 10, 90, 90)

        start_x = 400
        gap = 180

        self.dashboardOption = Designer.createMenuOption(
            self.topCard, "Dashboard",
            "../ImageResources/Icon8BGRemoved.png", 170
        )
        self.dashboardOption.move(start_x, 40)

        self.usersOption = Designer.createMenuOption(
            self.topCard, "Users",
            "../ImageResources/Icon14BGRemoved.png", 155
        )
        self.usersOption.move(start_x + gap + 15, 40)

        self.patientsOption = Designer.createMenuOption(
            self.topCard, "Patients",
            "../ImageResources/Icon1BGRemoved.png", 160
        )
        self.patientsOption.move(start_x + gap * 2, 40)

        self.reportsOption = Designer.createClickedOption(
            self.topCard, "Reports",
            "../ImageResources/Icon12BGRemoved.png", 160
        )
        self.reportsOption.move(start_x + gap * 3, 40)

        self.notificationsOption = Designer.createMenuOption(
            self.topCard, "Notifications",
            "../ImageResources/Icon4BGRemoved.png", 180
        )
        self.notificationsOption.move(start_x + gap * 4, 40)

        self.logoutOption = Designer.createMenuOption(
            self.topCard, "Logout",
            "../ImageResources/Icon6BGRemoved.png", 160
        )
        self.logoutOption.move(start_x + gap * 5 + 15, 40)

        profileIcon = Designer.setImage(self.topCard, "../ImageResources/Icon14BGRemoved.png")
        profileIcon.setGeometry(215, 40, 45, 45)

        self.userLabel = Designer.createLabel(self.userInfo, self.topCard, "#1a1a1a", 700, 13)
        self.userLabel.setGeometry(280, 45, 120, 14)

        self.titleLabel = Designer.createLabel(self.role, self.topCard, "#333333", 400, 12)
        self.titleLabel.setGeometry(280, 65, 120, 15)

    def _createMainContent(self):
        """Creates the main reports content area with card-based layout"""
        # Left Card - Report Generator (Fixed)
        self.leftCard = Designer.createRoundedCard(self, 440, 620)
        self.leftCard.move(20, 110)

        reportGenLabel = Designer.createLabel("Report Generator", self.leftCard, "#1a1a1a", 700, 24)
        reportGenLabel.setGeometry(40, 30, 300, 30)
        reportGenSubLabel = Designer.createLabel(
            "Create reports and conclusions.",
            self.leftCard, "#333333", 400, 12
        )
        reportGenSubLabel.setGeometry(40, 65, 250, 20)

        reportTypeLabel = Designer.createLabel("Report Type", self.leftCard, "#1a1a1a", 700, 18)
        reportTypeLabel.setGeometry(50, 110, 150, 25)
        reportTypeSubLabel = Designer.createLabel(
            "Choose type of report to produce.",
            self.leftCard, "#333333", 400, 11
        )
        reportTypeSubLabel.setGeometry(50, 135, 250, 20)

        typeLabel = Designer.createLabel("Type:", self.leftCard, "#1a1a1a", 600, 13)
        typeLabel.setGeometry(65, 175, 50, 20)
        self.typeDropdown = Designer.createComboBox(
            self.leftCard, radius=10, borderColor="#185777", fontSize=14
        )
        self.typeDropdown.setGeometry(120, 172, 250, 30)
        self.typeDropdown.addItems([
            "-- Select Report Type --",
            "Prescription Records",
            "Medication Preparation Records",
            "Medication Verification Records",
            "Nurse Administration Log",
            "Missed Administrations",
            "Controlled Substances Activity"
        ])

        filterLabel = Designer.createLabel("Filter", self.leftCard, "#1a1a1a", 700, 18)
        filterLabel.setGeometry(50, 230, 100, 25)
        filterSubLabel = Designer.createLabel(
            "Filter data and isolate needed information.",
            self.leftCard, "#333333", 400, 11
        )
        filterSubLabel.setGeometry(50, 255, 300, 20)

        fromLabel = Designer.createLabel("From:", self.leftCard, "#1a1a1a", 600, 13)
        fromLabel.setGeometry(70, 290, 50, 20)
        self.fromDateInput = Designer.createDateEdit(
            self.leftCard, radius=10, borderColor="#185777", fontSize=14
        )
        self.fromDateInput.setGeometry(130, 285, 200, 30)

        toLabel = Designer.createLabel("To:", self.leftCard, "#1a1a1a", 600, 13)
        toLabel.setGeometry(70, 340, 30, 20)
        self.toDateInput = Designer.createDateEdit(
            self.leftCard, radius=10, borderColor="#185777", fontSize=14
        )
        self.toDateInput.setGeometry(130, 335, 200, 30)

        patientLabel = Designer.createLabel("Patient:", self.leftCard, "#1a1a1a", 600, 13)
        patientLabel.setGeometry(65, 390, 60, 20)
        self.patientDropdown = Designer.createComboBox(
            self.leftCard, radius=10, borderColor="#185777", fontSize=14
        )
        self.patientDropdown.setGeometry(130, 385, 240, 30)

        doctorLabel = Designer.createLabel("Doctor:", self.leftCard, "#1a1a1a", 600, 13)
        doctorLabel.setGeometry(65, 440, 60, 20)
        self.doctorDropdown = Designer.createComboBox(
            self.leftCard, radius=10, borderColor="#185777", fontSize=14
        )
        self.doctorDropdown.setGeometry(130, 435, 240, 30)

        nurseLabel = Designer.createLabel("Nurse:", self.leftCard, "#1a1a1a", 600, 13)
        nurseLabel.setGeometry(65, 490, 60, 20)
        self.nurseDropdown = Designer.createComboBox(
            self.leftCard, radius=10, borderColor="#185777", fontSize=14
        )
        self.nurseDropdown.setGeometry(130, 485, 240, 30)

        self.generateButton = Designer.createPrimaryButton(
            "Generate", self.leftCard, "#0cc0df", "#1a1a1a", 700, 13, 15
        )
        self.generateButton.setGeometry(155, 560, 130, 40)

        # Right Card - Report Preview (Fixed container)
        self.rightCard = Designer.createRoundedCard(self, 1000, 620)
        self.rightCard.move(480, 110)

        # Card Title
        previewLabel = Designer.createLabel("Report Preview", self.rightCard, "#1a1a1a", 700, 24)
        previewLabel.setGeometry(40, 30, 250, 30)
        previewSubLabel = Designer.createLabel(
            "Generated reports are shown here.",
            self.rightCard, "#333333", 400, 12
        )
        previewSubLabel.setGeometry(40, 65, 300, 20)

        # Stacked Widget for Tables (inside the right card)
        self.tableStack = QStackedWidget(self.rightCard)
        self.tableStack.setGeometry(40, 105, 920, 440)
        self.tableStack.setStyleSheet("background-color: transparent;")

        # Create all report tables
        self._createWelcomeTable()
        self._createPrescriptionTable()
        self._createPreparationTable()
        self._createVerificationTable()
        self._createAdministrationTable()
        self._createMissedTable()
        self._createControlledSubstancesTable()

        # Show welcome table initially
        self.tableStack.setCurrentIndex(0)

        # Action Buttons (centered at bottom of right card)
        self.viewSummaryButton = Designer.createPrimaryButton(
            "View Summary", self.rightCard, "#0cc0df", "#1a1a1a", 700, 12, 15
        )
        self.viewSummaryButton.setGeometry(350, 565, 150, 35)

        self.saveButton = Designer.createPrimaryButton(
            "Save as PDF", self.rightCard, "#0cc0df", "#1a1a1a", 700, 12, 15
        )
        self.saveButton.setGeometry(530, 565, 160, 35)

    def _createWelcomeTable(self):
        """Creates the welcome/default table"""
        welcomeTable = Designer.createStandardTable(["Select a report type to begin"])
        self.tableStack.addWidget(welcomeTable)

    def _createPrescriptionTable(self):
        """Creates Prescription Records table"""
        self.prescriptionTable = Designer.createStandardTable([
            "Prescription ID", "Date", "Patient", "Medication",
            "Dosage", "Prescribed By", "Status"
        ])
        self.tableStack.addWidget(self.prescriptionTable)

    def _createPreparationTable(self):
        """Creates Medication Preparation Records table"""
        self.preparationTable = Designer.createStandardTable([
            "Prep ID", "Date", "Patient", "Medication",
            "Quantity"
        ])
        self.preparationTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableStack.addWidget(self.preparationTable)

    def _createVerificationTable(self):
        """Creates Medication Verification Records table"""
        self.verificationTable = Designer.createStandardTable([
            "Verification ID", "Date", "Patient", "Medication", "Lot Number", "Quantity", "Expiry", "Verified By", "Decision"
        ])
        self.tableStack.addWidget(self.verificationTable)

    def _createAdministrationTable(self):
        """Creates Nurse Administration Log table"""
        self.administrationTable = Designer.createStandardTable([
            "Admin ID", "Date/Time", "Patient", "Medication", "Dosage", "Route", "Site", "Administered By", "Notes"
        ])
        self.tableStack.addWidget(self.administrationTable)

    def _createMissedTable(self):
        """Creates Missed Medications table"""
        self.missedTable = Designer.createStandardTable([
            "Patient", "Room", "Medication", "Dosage", "Status", "Assigned Nurse"
        ])
        self.missedTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableStack.addWidget(self.missedTable)

    def _createControlledSubstancesTable(self):
        """Creates Controlled Substances Activity table"""
        self.controlledTable = Designer.createStandardTable([
            "Prescription ID", "Date", "Medication", "Patient", "Dosage", "Prescribed By", "Qty Dispensed", "Dispensed By", "Status"
        ])
        self.tableStack.addWidget(self.controlledTable)

    # PUBLIC METHODS FOR CONTROLLER
    def updateFiltersForType(self, report_type: str):
        """Dynamically enable/disable filters based on report type"""
        # Disable irrelevant filters
        enable_dates = report_type not in ["Overdue Medications"]
        enable_patient = report_type not in ["Controlled Substances Activity"]
        enable_doctor = report_type == "Controlled Substances Activity"
        enable_nurse = report_type == "Nurse Administration Log"

        self.fromDateInput.setEnabled(enable_dates)
        self.toDateInput.setEnabled(enable_dates)
        self.patientDropdown.setEnabled(enable_patient)
        self.doctorDropdown.setEnabled(enable_doctor)
        self.nurseDropdown.setEnabled(enable_nurse)

    def populateDropdowns(self, patients: list, doctors: list, nurses: list):
        """Populate filter dropdowns"""
        self.patientDropdown.addItem("-- All Patients --", None)
        for p in patients:
            self.patientDropdown.addItem(p['name'], p['patient_id'])

        self.doctorDropdown.addItem("-- All Doctors --", None)
        for d in doctors:
            self.doctorDropdown.addItem(d['name'], d['user_id'])

        self.nurseDropdown.addItem("-- All Nurses --", None)
        for n in nurses:
            self.nurseDropdown.addItem(n['name'], n['user_id'])

    def switchToTable(self, index: int):
        """Switch stacked table"""
        self.tableStack.setCurrentIndex(index)

    def populateTable(self, data: list, columns: list):
        """Generic table population (for controller)"""
        table = self.tableStack.currentWidget()
        table.setHorizontalHeaderLabels(columns)
        table.setRowCount(len(data))
        for row, item in enumerate(data):
            for col, key in enumerate(columns):
                value = str(item.get(key.lower().replace(" ", "_"), "N/A"))
                table_item = QTableWidgetItem(value)
                table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, col, table_item)

class ReportSummaryWindow(QWidget):
    """Popup for displaying report summary statistics"""

    def __init__(self, title="Report Summary"):
        super().__init__()
        self.setFixedSize(500, 600)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        Designer.setWindowToCenter(self)

        self.setStyleSheet("background-color: #cef2f9;")

        mainFrame = QFrame(self)
        mainFrame.setGeometry(10, 10, 480, 580)
        mainFrame.setStyleSheet("QFrame{background-color:#cef2f9;border-radius:30px;}")

        logo = Designer.setLogo(mainFrame)
        logo.setGeometry(195, 20, 90, 90)

        titleLabel = Designer.createLabel(title, mainFrame, "#1a1a1a", 700, 18)
        titleLabel.setGeometry(70, 120, 340, 25)
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        Designer.createLabel("Report Type:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, 165, 120, 20)
        self.reportTypeValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.reportTypeValue.setGeometry(165, 165, 280, 20)

        Designer.createLabel("Date Range:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, 200, 120, 20)
        self.dateRangeValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.dateRangeValue.setGeometry(165, 200, 280, 20)

        Designer.createLabel("Total Records:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, 235, 120, 20)
        self.totalRecordsValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.totalRecordsValue.setGeometry(165, 235, 280, 20)

        statsLabel = Designer.createLabel("Statistics", mainFrame, "#1a1a1a", 700, 16)
        statsLabel.setGeometry(40, 280, 150, 25)

        self.statisticsCard, self.statisticsText = Designer.createPlainTextArea(
            parent=mainFrame, backgroundColor="white", fontColor="#333333",
            fontSize=13, borderRadius=15, outlineWeight=2, outlineColor="#185777"
        )
        self.statisticsCard.setGeometry(40, 320, 400, 180)
        self.statisticsText.setGeometry(50, 330, 380, 160)
        self.statisticsText.setReadOnly(True)

        self.closeButton = Designer.createSecondaryButton(
            "Close", mainFrame, "#e7f9fc", "#1a1a1a", 700, 12, 15, 2, "#185777"
        )
        self.closeButton.setGeometry(190, 520, 100, 35)
        self.closeButton.clicked.connect(self.close)

    def setSummaryData(self, report_type, date_range, total_records, statistics):
        """Sets all summary data"""
        self.reportTypeValue.setText(report_type)
        self.dateRangeValue.setText(date_range)
        self.totalRecordsValue.setText(str(total_records))
        self.statisticsText.setPlainText(statistics)