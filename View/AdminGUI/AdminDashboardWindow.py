from PyQt6.QtWidgets import QWidget, QHeaderView
from PyQt6.QtCore import Qt
from Utilities.Designers import Designer
from View.GeneralPopups.KPIRecordsWindow import KPIRecordsPopup

class AdminDashboardWindow(QWidget):
    """
    Admin Dashboard Window.
    """
    def __init__(
        self,
        activeUsersKpi, activePatientsKpi, activePrescriptionsKpi,
        pendingPrescriptionsKpi, missedMedicationsKpi,
        userInfo, role, todaysActivityData
    ):
        super().__init__()
        self.setFixedSize(1500, 800)
        self.setWindowTitle("MEDISYNC Admin Dashboard")
        Designer.setWindowToCenter(self)

        # Store user & data
        self.userInfo = userInfo
        self.role = role
        self.todaysActivityData = todaysActivityData

        # KPI values for popup details
        self.kpi_values = {
            "Active Users": activeUsersKpi,
            "Active Patients": activePatientsKpi,
            "Active Prescriptions": activePrescriptionsKpi,
            "Pending Prescriptions": pendingPrescriptionsKpi,
            "Missed Medications": missedMedicationsKpi,
        }

        # Build UI
        self._setupBackground()
        self._createTopBar()
        self._createKPICards()
        self._createActivityTable()

    def _setupBackground(self):
        """Apply background style"""
        Designer.setBackground(self)

    def _createTopBar(self):
        """Create top navigation bar with logo, menu, and user info"""
        self.topCard = Designer.createRoundedCard(self)
        self.topCard.setGeometry(0, -25, 1500, 100)

        # Logo
        Designer.setLogo(self.topCard).setGeometry(60, 10, 90, 90)

        # Menu options (exposed for controller)
        start_x, gap = 400, 180
        self.dashboardOption = Designer.createClickedOption(self.topCard, "Dashboard",
                                                           "../ImageResources/Icon8BGRemoved.png", 170)
        self.dashboardOption.move(start_x, 40)

        self.usersOption = Designer.createMenuOption(self.topCard, "Users",
                                                     "../ImageResources/Icon14BGRemoved.png", 155)
        self.usersOption.move(start_x + gap + 15, 40)

        self.patientsOption = Designer.createMenuOption(self.topCard, "Patients",
                                                        "../ImageResources/Icon1BGRemoved.png", 160)
        self.patientsOption.move(start_x + gap * 2, 40)

        self.reportsOption = Designer.createMenuOption(self.topCard, "Reports",
                                                       "../ImageResources/Icon12BGRemoved.png", 160)
        self.reportsOption.move(start_x + gap * 3, 40)

        self.notificationsOption = Designer.createMenuOption(self.topCard, "Notifications",
                                                             "../ImageResources/Icon4BGRemoved.png", 180)
        self.notificationsOption.move(start_x + gap * 4, 40)

        self.logoutOption = Designer.createMenuOption(self.topCard, "Logout",
                                                      "../ImageResources/Icon6BGRemoved.png", 160)
        self.logoutOption.move(start_x + gap * 5 + 15, 40)

        # User Info
        Designer.setImage(self.topCard, "../ImageResources/Icon14BGRemoved.png")\
            .setGeometry(215, 40, 45, 45)
        Designer.createLabel(self.userInfo, self.topCard, "#1a1a1a", 700, 13)\
            .setGeometry(280, 45, 120, 20)
        Designer.createLabel(self.role, self.topCard, "#333333", 400, 12)\
            .setGeometry(280, 65, 120, 20)

    def _createKPICards(self):
        """Create clickable KPI cards"""
        x_start, gap, y_pos = 55, 290, 105
        icons = [
            "../ImageResources/Icon14BGRemoved.png",
            "../ImageResources/Icon1BGRemoved.png",
            "../ImageResources/Icon2BGRemoved.png",
            "../ImageResources/Icon7BGRemoved.png",
            "../ImageResources/Icon13BGRemoved.png",
        ]
        labels = list(self.kpi_values.keys())
        values = list(self.kpi_values.values())

        self.kpi_cards = []
        for i, (icon, label, value) in enumerate(zip(icons, labels, values)):
            card = Designer.createKPI(self, icon, str(value), label,
                                      x=x_start + gap * i, y=y_pos)
            card.setCursor(Qt.CursorShape.PointingHandCursor)
            card.mousePressEvent = lambda e, l=label: self._showKPIDetails(l)
            self.kpi_cards.append(card)

    def _showKPIDetails(self, kpi_label: str):
        """Show detailed records when KPI card is clicked"""
        from Model.KPIs.AdminKPIs import AdminKPIDetails
        data = AdminKPIDetails.get_details(kpi_label.replace(" ", "_").lower())
        columns = AdminKPIDetails.get_columns(kpi_label.replace(" ", "_").lower())

        self.popup = KPIRecordsPopup(f"{kpi_label} - Detailed View", columns, data)
        self.popup.show()

    def _createActivityTable(self):
        """Display today's activity log"""
        columns = ["Activity ID", "Time", "User", "Role", "Type", "Action", "Related"]
        column_map = {
            "Activity ID": "notification_id", "Time": "created_at", "User": "user_name",
            "Role": "role", "Type": "type", "Action": "title", "Related": "related_info"
        }

        self.activityTable, self.activityCard = Designer.createTableCard(
            self, labelText="Today's Activity Summary", fontSize=22,
            columnNames=columns, columnMap=column_map,
            cardWidth=1420, cardHeight=445, tableWidth=1380, tableHeight=350,
            x=40, y=325, data=self.todaysActivityData
        )
        header = self.activityTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)