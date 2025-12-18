from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHeaderView
from Utilities.Designers import Designer
from View.GeneralPopups.KPIRecordsWindow import KPIRecordsPopup

class DoctorDashboardWindow(QWidget):
    """
    Doctor Dashboard Window.
    """

    def __init__(
        self, patientKpi, prescriptionKpi, urgentKpi,
        userInfo, dataHistory, dataPending
    ):
        super().__init__()
        self.setFixedSize(1500, 800)
        self.setWindowTitle("MEDISYNC Doctor Dashboard")
        Designer.setWindowToCenter(self)

        # Store user & data
        self.userInfo = userInfo
        self.kpi_values = {
            "Active Patients": patientKpi,
            "Active Prescriptions": prescriptionKpi,
            "Urgent": urgentKpi
        }

        Designer.setBackground(self)
        self._createTopBar()
        self._createKPICards()
        self._createPatientHistoryTable(dataHistory)
        self._createPendingPrescriptionsTable(dataPending)

    def _createTopBar(self):
        """Create top navigation bar with logo, menu, and user info"""
        self.topCard = Designer.createRoundedCard(self)
        self.topCard.setGeometry(0, -25, 1500, 100)

        # Logo
        Designer.setLogo(self.topCard).setGeometry(60, 10, 90, 90)

        # Menu options
        start_x, gap = 500, 225
        self.dashboardOption = Designer.createClickedOption(self.topCard, "Dashboard",
                                                            "../ImageResources/Icon8BGRemoved.png", 180)
        self.dashboardOption.move(start_x, 40)

        self.prescriptionOption = Designer.createMenuOption(self.topCard, "Prescribe",
                                                             "../ImageResources/Icon5BGRemoved.png", 180)
        self.prescriptionOption.move(start_x + gap, 40)

        self.notificationsOption = Designer.createMenuOption(self.topCard, "Notifications",
                                                             "../ImageResources/Icon4BGRemoved.png", 180)
        self.notificationsOption.move(start_x + gap * 2, 40)

        self.logoutOption = Designer.createMenuOption(self.topCard, "Logout",
                                                      "../ImageResources/Icon6BGRemoved.png", 150)
        self.logoutOption.move(start_x + gap * 3 + 50, 40)

        # User Info
        Designer.setImage(self.topCard, "../ImageResources/Icon14BGRemoved.png")\
            .setGeometry(215, 40, 45, 45)
        Designer.createLabel(self.userInfo, self.topCard, "#1a1a1a", 700, 13)\
            .setGeometry(280, 45, 150, 14)
        Designer.createLabel("Doctor", self.topCard, "#333333", 400, 12)\
            .setGeometry(280, 65, 150, 15)

    def _createKPICards(self):
        """Create clickable KPI cards"""
        icons = [
            "../ImageResources/Icon1BGRemoved.png",
            "../ImageResources/Icon2BGRemoved.png",
            "../ImageResources/Icon3BGRemoved.png"
        ]
        labels = ["Active Patients", "Active Prescriptions", "Urgent"]
        values = [self.kpi_values["Active Patients"], self.kpi_values["Active Prescriptions"], self.kpi_values["Urgent"]]

        self.kpi_cards = []
        x_start, gap, y_pos = 50, 275, 110
        for i, (icon, label, value) in enumerate(zip(icons, labels, values)):
            card = Designer.createKPI(self, icon, str(value), label,
                                      x=x_start + gap * i, y=y_pos)
            card.setCursor(Qt.CursorShape.PointingHandCursor)
            card.mousePressEvent = lambda e, l=label: self._showKPIDetails(l)
            self.kpi_cards.append(card)

    def _showKPIDetails(self, kpi_label: str):
        """Show detailed records when KPI card is clicked"""
        from Model.KPIs.DoctorKPIs import DoctorKPIDetails
        data = DoctorKPIDetails.get_details(kpi_label.replace(" ", "_").lower())
        columns = DoctorKPIDetails.get_columns(kpi_label.replace(" ", "_").lower())

        self.popup = KPIRecordsPopup(f"{kpi_label} - Detailed View", columns, data)
        self.popup.show()

    def _createPatientHistoryTable(self, dataHistory):
        """Display patient history"""
        columns = ["Patient", "DOB", "Sex", "Admission Date", "Diagnosis", "Prescriptions"]
        column_map = {
            "Patient": "patient_name", "DOB": "date_of_birth", "Sex": "sex",
            "Admission Date": "admission_date", "Diagnosis": "diagnosis",
            "Prescriptions": "prescriptions"
        }

        self.patientHistoryTable, self.patientHistoryCard = Designer.createTableCard(
            self, labelText="Patient History", fontSize=22,
            columnNames=columns, columnMap=column_map,
            cardWidth=775, cardHeight=400, tableWidth=735, tableHeight=315,
            x=50, y=345, data=dataHistory
        )
        header = self.patientHistoryTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _createPendingPrescriptionsTable(self,dataPending):
        """Display pending prescriptions"""
        columns = ["ID", "Patient", "Brand", "Dosage", "Frequency", "Duration", "Status"]
        column_map = {
            "ID": "prescription_id", "Patient": "patient_name", "Brand": "medicine_brand",
            "Dosage": "dosage", "Frequency": "frequency", "Duration": "duration",
            "Status": "prescription_status"
        }

        self.pendingPrescriptionsTable, self.pendingPrescriptionsCard = Designer.createTableCard(
            self, labelText="Pending Prescriptions", fontSize=22,
            columnNames=columns, columnMap=column_map,
            cardWidth=580, cardHeight=635, tableWidth=540, tableHeight=540,
            x=875, y=110, data=dataPending
        )
        header = self.pendingPrescriptionsTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)