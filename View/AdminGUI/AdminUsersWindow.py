from PyQt6.QtWidgets import QWidget, QFrame, QButtonGroup, QRadioButton, QHeaderView
from PyQt6.QtCore import Qt
from Utilities.Designers import Designer

class AdminUsersWindow(QWidget):
    """
    Main window for Admin User Management
    """

    def __init__(self, userInfo, role):
        super().__init__()
        self.setFixedSize(1500, 800)
        self.setWindowTitle("MEDISYNC User Management")
        Designer.setWindowToCenter(self)

        # Store data
        self.userInfo = userInfo
        self.role = role
        self.selectedUserId = None
        self.selectedUserData = None

        # Build UI
        self._setupBackground()
        self._createTopBar()
        self._createMainContent()

    def _setupBackground(self):
        """Apply background style"""
        Designer.setBackground(self)

    def _createTopBar(self):
        """Create top navigation bar"""
        self.topCard = Designer.createRoundedCard(self)
        self.topCard.setGeometry(0, -25, 1500, 100)

        # Logo
        Designer.setLogo(self.topCard).setGeometry(60, 10, 90, 90)

        # Menu options
        start_x, gap = 400, 180
        self.dashboardOption = Designer.createMenuOption(self.topCard, "Dashboard",
                                                         "../ImageResources/Icon8BGRemoved.png", 170)
        self.dashboardOption.move(start_x, 40)

        self.usersOption = Designer.createClickedOption(self.topCard, "Users",
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

        # User info
        Designer.setImage(self.topCard, "../ImageResources/Icon14BGRemoved.png").setGeometry(215, 40, 45, 45)
        Designer.createLabel(self.userInfo, self.topCard, "#1a1a1a", 700, 13).setGeometry(280, 45, 120, 20)
        Designer.createLabel(self.role, self.topCard, "#333333", 400, 12).setGeometry(280, 65, 120, 20)

    def _createMainContent(self):
        """Create main content area with table and buttons"""
        self.mainCard = Designer.createRoundedCard(self)
        self.mainCard.setGeometry(20, 95, 1460, 680)

        # Titles
        Designer.createLabel("User Management", self.mainCard, "#1a1a1a", 700, 24).setGeometry(50, 30, 400, 30)
        Designer.createLabel("Manage and add users to the system.", self.mainCard, "#333333", 400, 13)\
            .setGeometry(50, 65, 400, 20)

        # Users section
        Designer.createLabel("All Users", self.mainCard, "#1a1a1a", 700, 18).setGeometry(50, 110, 150, 25)
        Designer.createLabel("Select user.", self.mainCard, "#333333", 400, 12).setGeometry(50, 140, 150, 20)

        # Search
        self.searchInput = Designer.createInputField(self.mainCard, "white", "#333333", 400, 14, 15, 2, "#185777")
        self.searchInput.setGeometry(1100, 125, 180, 35)
        self.searchInput.setPlaceholderText("  🔍 Search users")

        self.searchButton = Designer.createPrimaryButton("Search", self.mainCard, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.searchButton.setGeometry(1300, 125, 110, 35)

        # Table
        columns = ["User ID", "Username", "Full Name", "Role", "Status"]
        self.usersTable = Designer.createStandardTable(columns)
        self.usersTable.setParent(self.mainCard)
        self.usersTable.setGeometry(50, 175, 1360, 430)
        header = self.usersTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Buttons
        self.addUserButton = Designer.createPrimaryButton("Add User", self.mainCard, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.addUserButton.setGeometry(590, 630, 130, 35)

        self.editUserButton = Designer.createPrimaryButton("Edit User", self.mainCard, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.editUserButton.setGeometry(750, 630, 130, 35)

    def clearSelection(self):
        """Reset selected user"""
        self.selectedUserId = None
        self.selectedUserData = None


class AddUserPopup(QWidget):
    """Popup for adding new users with dynamic license field"""

    def __init__(self):
        super().__init__()
        self.setFixedSize(990, 500)
        self.setWindowTitle("Add User")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        Designer.setWindowToCenter(self)
        self.setStyleSheet("background-color: #cef2f9;")

        mainFrame = QFrame(self)
        mainFrame.setGeometry(10, 10, 950, 480)
        mainFrame.setStyleSheet("QFrame { background-color: #cef2f9; border-radius: 30px; }")

        # Titles
        Designer.createLabel("Add User", mainFrame, "#1a1a1a", 700, 24).setGeometry(40, 20, 200, 30)
        Designer.createLabel("Introduce a new user to the system.", mainFrame, "#333333", 400, 12)\
            .setGeometry(40, 55, 300, 20)

        # Account info
        Designer.createLabel("Account Information", mainFrame, "#1a1a1a", 700, 18).setGeometry(40, 95, 250, 25)
        Designer.createLabel("Input account details for new user.", mainFrame, "#333333", 400, 11)\
            .setGeometry(40, 120, 250, 20)

        Designer.createLabel("Username:", mainFrame, "#1a1a1a", 600, 13).setGeometry(60, 155, 100, 20)
        self.usernameInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.usernameInput.setGeometry(170, 152, 250, 32)

        Designer.createLabel("Password:", mainFrame, "#1a1a1a", 600, 13).setGeometry(60, 200, 100, 20)
        self.passwordInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.passwordInput.setGeometry(170, 197, 250, 32)
        self.passwordInput.setEchoMode(self.passwordInput.EchoMode.Password)

        # Personal info
        Designer.createLabel("Personal Information", mainFrame, "#1a1a1a", 700, 18).setGeometry(40, 255, 250, 25)
        Designer.createLabel("Input personal details of new user.", mainFrame, "#333333", 400, 11)\
            .setGeometry(40, 280, 250, 20)

        Designer.createLabel("First Name:", mainFrame, "#1a1a1a", 600, 13).setGeometry(60, 315, 100, 20)
        self.firstNameInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.firstNameInput.setGeometry(170, 312, 250, 32)

        Designer.createLabel("Last Name:", mainFrame, "#1a1a1a", 600, 13).setGeometry(60, 360, 100, 20)
        self.lastNameInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.lastNameInput.setGeometry(170, 357, 250, 32)

        # Contact & Email
        Designer.createLabel("Email Address:", mainFrame, "#1a1a1a", 600, 13).setGeometry(500, 95, 120, 20)
        self.emailInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.emailInput.setGeometry(635, 92, 240, 32)

        Designer.createLabel("Contact Number:", mainFrame, "#1a1a1a", 600, 13).setGeometry(500, 140, 150, 20)
        self.contactInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.contactInput.setGeometry(650, 137, 225, 32)

        # Role
        Designer.createLabel("Role", mainFrame, "#1a1a1a", 700, 18).setGeometry(500, 185, 100, 25)
        Designer.createLabel("Choose the role of new user.", mainFrame, "#333333", 400, 11)\
            .setGeometry(500, 210, 200, 20)

        radio_style = """
            QRadioButton { color: #333333; font-family: 'Lato'; font-size: 13px; font-weight: bold; }
            QRadioButton::indicator { width: 16px; height: 16px; border: 3px solid #0cc0df; border-radius: 10px; background: #185777; }
            QRadioButton::indicator:checked { background-color: #00A9C9; border: 3px solid #185777; }
            QRadioButton::indicator:hover { border-color: #00A9C9; }
            QRadioButton:checked { color: #00A9C9; }
        """

        self.roleGroup = QButtonGroup(mainFrame)
        self.doctorRadio = QRadioButton("Doctor", mainFrame)
        self.pharmacistRadio = QRadioButton("Pharmacist", mainFrame)
        self.nurseRadio = QRadioButton("Nurse", mainFrame)
        self.adminRadio = QRadioButton("Admin", mainFrame)

        for radio in [self.doctorRadio, self.pharmacistRadio, self.nurseRadio, self.adminRadio]:
            radio.setStyleSheet(radio_style)

        self.doctorRadio.setGeometry(500, 245, 100, 25)
        self.pharmacistRadio.setGeometry(620, 245, 120, 25)
        self.nurseRadio.setGeometry(760, 245, 80, 25)
        self.adminRadio.setGeometry(860, 245, 80, 25)

        self.roleGroup.addButton(self.doctorRadio, 1)
        self.roleGroup.addButton(self.pharmacistRadio, 2)
        self.roleGroup.addButton(self.nurseRadio, 3)
        self.roleGroup.addButton(self.adminRadio, 4)

        # License
        Designer.createLabel("License Number:", mainFrame, "#1a1a1a", 600, 13).setGeometry(500, 300, 130, 20)
        self.licenseInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.licenseInput.setGeometry(640, 297, 240, 32)

        # Connect role change to toggle license
        self.roleGroup.buttonClicked.connect(self._toggleLicenseField)

        # Buttons
        self.submitButton = Designer.createPrimaryButton("Submit", mainFrame, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.submitButton.setGeometry(380, 430, 110, 35)

        self.closeButton = Designer.createSecondaryButton("Close", mainFrame, "#e7f9fc", "#1a1a1a", 700, 12, 15, 2, "#185777")
        self.closeButton.setGeometry(510, 430, 110, 35)
        self.closeButton.clicked.connect(self.close)

    def _toggleLicenseField(self):
        """Enable/disable license based on role (improvement)"""
        selected_id = self.roleGroup.checkedId()
        is_admin = selected_id == 4
        self.licenseInput.setEnabled(not is_admin)
        if is_admin:
            self.licenseInput.clear()

    def getUserData(self):
        """Get form data as dict"""
        role_map = {1: "Doctor", 2: "Pharmacist", 3: "Nurse", 4: "Admin"}
        role = role_map.get(self.roleGroup.checkedId())
        return {
            'username': self.usernameInput.text().strip(),
            'password': self.passwordInput.text().strip(),
            'first_name': self.firstNameInput.text().strip(),
            'last_name': self.lastNameInput.text().strip(),
            'email': self.emailInput.text().strip(),
            'contact': self.contactInput.text().strip(),
            'role': role,
            'license_number': self.licenseInput.text().strip() if self.licenseInput.isEnabled() else None
        }

    def clearForm(self):
        """Reset form"""
        for field in [self.usernameInput, self.passwordInput, self.firstNameInput, self.lastNameInput,
                      self.emailInput, self.contactInput, self.licenseInput]:
            field.clear()
        self.roleGroup.setExclusive(False)
        for radio in [self.doctorRadio, self.pharmacistRadio, self.nurseRadio, self.adminRadio]:
            radio.setChecked(False)
        self.roleGroup.setExclusive(True)


class EditUserPopup(QWidget):
    """Popup for editing users with dynamic license and status radios"""

    def __init__(self):
        super().__init__()
        self.setFixedSize(990, 500)
        self.setWindowTitle("Edit User")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        Designer.setWindowToCenter(self)
        self.setStyleSheet("background-color: #cef2f9;")

        mainFrame = QFrame(self)
        mainFrame.setGeometry(10, 10, 950, 480)
        mainFrame.setStyleSheet("QFrame { background-color: #cef2f9; border-radius: 30px; }")

        # Titles
        Designer.createLabel("Edit User", mainFrame, "#1a1a1a", 700, 24).setGeometry(40, 20, 200, 30)
        Designer.createLabel("Edit existing user information.", mainFrame, "#333333", 400, 12)\
            .setGeometry(40, 55, 300, 20)

        # Account info
        Designer.createLabel("Account Information", mainFrame, "#1a1a1a", 700, 18).setGeometry(40, 90, 250, 25)
        Designer.createLabel("Input edited account details for user.", mainFrame, "#333333", 400, 11)\
            .setGeometry(40, 115, 250, 20)

        Designer.createLabel("Username:", mainFrame, "#1a1a1a", 600, 13).setGeometry(60, 150, 100, 20)
        self.usernameInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.usernameInput.setGeometry(155, 147, 230, 30)

        Designer.createLabel("Password:", mainFrame, "#1a1a1a", 600, 13).setGeometry(60, 195, 100, 20)
        self.passwordInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.passwordInput.setGeometry(155, 192, 230, 30)
        self.passwordInput.setEchoMode(self.passwordInput.EchoMode.Password)
        self.passwordInput.setPlaceholderText("Leave blank to keep current")

        # Personal info
        Designer.createLabel("Personal Information", mainFrame, "#1a1a1a", 700, 18).setGeometry(40, 245, 250, 25)
        Designer.createLabel("Modify personal details of user.", mainFrame, "#333333", 400, 11)\
            .setGeometry(40, 270, 250, 20)

        Designer.createLabel("First Name:", mainFrame, "#1a1a1a", 600, 13).setGeometry(60, 305, 100, 20)
        self.firstNameInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.firstNameInput.setGeometry(155, 302, 230, 30)

        Designer.createLabel("Last Name:", mainFrame, "#1a1a1a", 600, 13).setGeometry(60, 350, 100, 20)
        self.lastNameInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.lastNameInput.setGeometry(155, 347, 230, 30)

        # Contact & Email
        Designer.createLabel("Email Address:", mainFrame, "#1a1a1a", 600, 13).setGeometry(480, 90, 120, 20)
        self.emailInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.emailInput.setGeometry(605, 87, 230, 30)

        Designer.createLabel("Contact Number:", mainFrame, "#1a1a1a", 600, 13).setGeometry(480, 135, 150, 20)
        self.contactInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.contactInput.setGeometry(625, 132, 210, 30)

        # Role
        Designer.createLabel("Role", mainFrame, "#1a1a1a", 700, 18).setGeometry(480, 180, 100, 25)
        Designer.createLabel("Choose new role of user.", mainFrame, "#333333", 400, 11)\
            .setGeometry(480, 205, 200, 20)

        radio_style = """
            QRadioButton { color: #333333; font-family: 'Lato'; font-size: 13px; font-weight: bold; }
            QRadioButton::indicator { width: 16px; height: 16px; border: 3px solid #0cc0df; border-radius: 10px; background: #185777; }
            QRadioButton::indicator:checked { background-color: #00A9C9; border: 3px solid #185777; }
            QRadioButton::indicator:hover { border-color: #00A9C9; }
            QRadioButton:checked { color: #00A9C9; }
        """

        self.roleGroup = QButtonGroup(mainFrame)
        self.doctorRadio = QRadioButton("Doctor", mainFrame)
        self.pharmacistRadio = QRadioButton("Pharmacist", mainFrame)
        self.nurseRadio = QRadioButton("Nurse", mainFrame)
        self.adminRadio = QRadioButton("Admin", mainFrame)

        for radio in [self.doctorRadio, self.pharmacistRadio, self.nurseRadio, self.adminRadio]:
            radio.setStyleSheet(radio_style)

        self.doctorRadio.setGeometry(480, 245, 100, 25)
        self.pharmacistRadio.setGeometry(600, 245, 120, 25)
        self.nurseRadio.setGeometry(740, 245, 80, 25)
        self.adminRadio.setGeometry(840, 245, 80, 25)

        self.roleGroup.addButton(self.doctorRadio, 1)
        self.roleGroup.addButton(self.pharmacistRadio, 2)
        self.roleGroup.addButton(self.nurseRadio, 3)
        self.roleGroup.addButton(self.adminRadio, 4)

        # License (dynamic)
        Designer.createLabel("License Number:", mainFrame, "#1a1a1a", 600, 13).setGeometry(480, 290, 130, 20)
        self.licenseInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.licenseInput.setGeometry(620, 287, 240, 32)

        # Status radios (improvement: added as per code)
        Designer.createLabel("Status", mainFrame, "#1a1a1a", 700, 18).setGeometry(480, 330, 100, 25)
        Designer.createLabel("Set user status.", mainFrame, "#333333", 400, 11).setGeometry(480, 355, 200, 20)

        self.statusGroup = QButtonGroup(mainFrame)
        self.activeRadio = QRadioButton("Active", mainFrame)
        self.inactiveRadio = QRadioButton("Inactive", mainFrame)

        for radio in [self.activeRadio, self.inactiveRadio]:
            radio.setStyleSheet(radio_style)

        self.activeRadio.setGeometry(480, 380, 100, 25)
        self.inactiveRadio.setGeometry(600, 380, 120, 25)

        self.statusGroup.addButton(self.activeRadio, 1)
        self.statusGroup.addButton(self.inactiveRadio, 2)

        # Connect role change
        self.roleGroup.buttonClicked.connect(self._toggleLicenseField)

        # Buttons
        self.submitButton = Designer.createPrimaryButton("Update", mainFrame, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.submitButton.setGeometry(380, 430, 110, 35)

        self.closeButton = Designer.createSecondaryButton("Close", mainFrame, "#e7f9fc", "#1a1a1a", 700, 12, 15, 2, "#185777")
        self.closeButton.setGeometry(510, 430, 110, 35)
        self.closeButton.clicked.connect(self.close)

    def _toggleLicenseField(self):
        """Enable/disable license based on role"""
        selected_id = self.roleGroup.checkedId()
        is_admin = selected_id == 4
        self.licenseInput.setEnabled(not is_admin)
        if is_admin:
            self.licenseInput.clear()

    def populateForm(self, data: dict):
        """Fill form with existing user data"""
        self.usernameInput.setText(data.get('username', ''))
        self.firstNameInput.setText(data.get('first_name', ''))
        self.lastNameInput.setText(data.get('last_name', ''))
        self.emailInput.setText(data.get('email', ''))
        self.contactInput.setText(data.get('contact', ''))
        self.licenseInput.setText(data.get('license_number', ''))

        # Set role radio
        role_map = {"Doctor": self.doctorRadio, "Pharmacist": self.pharmacistRadio,
                    "Nurse": self.nurseRadio, "Admin": self.adminRadio}
        role_radio = role_map.get(data.get('role'))
        if role_radio:
            role_radio.setChecked(True)
            self._toggleLicenseField()

        # Set status radio
        if data.get('status') == 'Active':
            self.activeRadio.setChecked(True)
        elif data.get('status') == 'Inactive':
            self.inactiveRadio.setChecked(True)

    def getUserData(self):
        """Get updated form data"""
        role_map = {1: "Doctor", 2: "Pharmacist", 3: "Nurse", 4: "Admin"}
        status_map = {1: "Active", 2: "Inactive"}
        role = role_map.get(self.roleGroup.checkedId())
        status = status_map.get(self.statusGroup.checkedId())
        password = self.passwordInput.text().strip() or None  # None if blank
        inlicense = self.licenseInput.text().strip() if self.licenseInput.isEnabled() else None
        return {
            'username': self.usernameInput.text().strip(),
            'password': password,
            'first_name': self.firstNameInput.text().strip(),
            'last_name': self.lastNameInput.text().strip(),
            'email': self.emailInput.text().strip(),
            'contact': self.contactInput.text().strip(),
            'role': role,
            'license_number': inlicense,
            'status': status
        }

    def clearForm(self):
        """Reset form (optional, but good for reuse)"""
        for field in [self.usernameInput, self.passwordInput, self.firstNameInput, self.lastNameInput,
                      self.emailInput, self.contactInput, self.licenseInput]:
            field.clear()
        self.roleGroup.setExclusive(False)
        for radio in [self.doctorRadio, self.pharmacistRadio, self.nurseRadio, self.adminRadio]:
            radio.setChecked(False)
        self.roleGroup.setExclusive(True)
        self.statusGroup.setExclusive(False)
        for radio in [self.activeRadio, self.inactiveRadio]:
            radio.setChecked(False)
        self.statusGroup.setExclusive(True)