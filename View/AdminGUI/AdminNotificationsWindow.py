from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout
from Utilities.Designers import Designer
from View.GeneralPopups.NotificationDetailWindow import NotificationDetailPopup

class AdminNotificationsWindow(QWidget):
    """
    Admin Notifications Window
    """

    def __init__(self, userInfo, role):
        super().__init__()
        self.popup = None
        self.setFixedSize(1500, 800)
        self.setWindowTitle("MEDISYNC Notifications")
        Designer.setWindowToCenter(self)

        self.userInfo = userInfo
        self.role = role
        self.notificationsData = []

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

        self.reportsOption = Designer.createMenuOption(
            self.topCard, "Reports",
            "../ImageResources/Icon12BGRemoved.png", 160
        )
        self.reportsOption.move(start_x + gap * 3, 40)

        self.notificationsOption = Designer.createClickedOption(
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
        """Creates the main notifications content area"""
        self.mainCard = Designer.createRoundedCard(self)
        self.mainCard.setGeometry(20, 95, 1460, 680)

        filterLabel = Designer.createLabel("Filter by:", self.mainCard, "#1a1a1a", 600, 14)
        filterLabel.setGeometry(50, 30, 80, 30)

        self.filterDropdown = Designer.createComboBox(
            self.mainCard, radius=15, borderColor="#185777", fontSize=14
        )
        self.filterDropdown.setGeometry(135, 30, 185, 35)
        self.filterDropdown.addItems(["All Notifications", "Urgent", "Attention", "Info"])

        self.searchInput = Designer.createInputField(
            self.mainCard, "white", "#333333", 400, 14, 15, 2, "#185777"
        )
        self.searchInput.setGeometry(1080, 30, 200, 35)
        self.searchInput.setPlaceholderText("  🔍 Search")

        self.searchButton = Designer.createPrimaryButton(
            "Search", self.mainCard, "#0cc0df", "#1a1a1a", 700, 12, 15
        )
        self.searchButton.setGeometry(1295, 30, 115, 35)

        self.scrollArea = QScrollArea(self.mainCard)
        self.scrollArea.setGeometry(50, 90, 1360, 490)
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
        self.scrollArea.setWidget(self.scrollWidget)

        legendLabel = Designer.createLabel("Priority Legend:", self.mainCard, "#1a1a1a", 600, 14)
        legendLabel.setGeometry(50, 610, 150, 30)

        urgentCircle = self._createPriorityCircle(self.mainCard, "#ff6b6b")
        urgentCircle.setGeometry(185, 615, 20, 20)
        Designer.createLabel("Urgent", self.mainCard, "#1a1a1a", 600, 13).setGeometry(225, 615, 80, 25)

        attentionCircle = self._createPriorityCircle(self.mainCard, "#ffa500")
        attentionCircle.setGeometry(325, 615, 20, 20)
        Designer.createLabel("Attention", self.mainCard, "#1a1a1a", 600, 13).setGeometry(360, 615, 100, 25)

        infoCircle = self._createPriorityCircle(self.mainCard, "#7bc96f")
        infoCircle.setGeometry(455, 615, 20, 20)
        Designer.createLabel("Info", self.mainCard, "#1a1a1a", 600, 13).setGeometry(490, 615, 80, 25)

    @staticmethod
    def _createPriorityCircle(parent, color):
        circle = QWidget(parent)
        circle.setFixedSize(20, 20)
        circle.setStyleSheet(f"QWidget {{background-color: {color}; border-radius: 10px;}}")
        return circle

    def _createNotificationCard(self, notification):
        card = QWidget(self.scrollWidget)
        card.setFixedSize(1330, 90)
        card.setStyleSheet("QWidget {background-color: white; border-radius: 20px;}")

        priorityColors = {
            "Urgent": "#ff6b6b", "urgent": "#ff6b6b",
            "Attention": "#ffa500", "attention": "#ffa500",
            "Info": "#7bc96f", "info": "#7bc96f"
        }
        priority = notification.get('priority', 'Info')
        color = priorityColors.get(priority, "#7bc96f")

        priorityBar = QWidget(card)
        priorityBar.setGeometry(0, 0, 8, 90)
        priorityBar.setStyleSheet(f"""
            QWidget {{background-color: {color};
                     border-top-left-radius: 20px;
                     border-bottom-left-radius: 20px;}}
        """)

        priorityCircle = self._createPriorityCircle(card, color)
        priorityCircle.setGeometry(25, 30, 25, 25)

        titleLabel = Designer.createLabel(
            notification.get('title', ''), card, "#1a1a1a", 700, 15
        )
        titleLabel.setGeometry(70, 20, 1100, 25)

        messageLabel = Designer.createLabel(
            notification.get('message', ''), card, "#333333", 400, 13
        )
        messageLabel.setGeometry(70, 45, 1100, 30)
        messageLabel.setWordWrap(True)

        timeLabel = Designer.createLabel(
            notification.get('time', ''), card, "#666666", 400, 11
        )
        timeLabel.setGeometry(1180, 20, 130, 20)
        timeLabel.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Make card clickable
        card.mousePressEvent = lambda e, n=notification: self.showNotificationDetail(n)

        return card

    def showNotificationDetail(self, notification):
        """Opens detail popup for a notification"""
        self.popup = NotificationDetailPopup(notification, self)
        self.popup.show()

    def displayNotifications(self, notifications):
        while self.scrollLayout.count():
            child = self.scrollLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.notificationsData = notifications

        if not notifications:
            self._displayEmptyState()
            return

        for notification in notifications:
            card = self._createNotificationCard(notification)
            self.scrollLayout.addWidget(card)

    def _displayEmptyState(self):
        emptyLabel = Designer.createLabel(
            "No notifications to display",
            self.scrollWidget, "#666666", 400, 16
        )
        emptyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scrollLayout.addWidget(emptyLabel)

    def clearNotifications(self):
        while self.scrollLayout.count():
            child = self.scrollLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.notificationsData = []

    def getSearchQuery(self):
        return self.searchInput.text().strip()

    def getFilterSelection(self):
        return self.filterDropdown.currentText()