from Model.Transactions.UserModel import UserModel
from Model.Notifications.NotificationsModel import NotificationsModel
from Model.SessionManager import SessionManager
from View.AdminGUI.AdminUsersWindow import AdminUsersWindow, AddUserPopup, EditUserPopup
from View.AdminGUI.AdminPatientsWindow import AddSuccessPopup
from View.GeneralPopups.Dialogs import Dialogs
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt
import re

class AdminUsersController:
    """
    Controller for Admin Users Management.
    Handles user CRUD operations, search, and navigation related to Users.
    """

    def __init__(self):
        self.addUserPopup = None
        self.editUserPopup = None
        self.addSuccessPopup = None
        self.updateUserPopup = None
        self.loginController = None
        self.usersWindow = None
        self.allUsers = None
        self._loadData()

    def _loadData(self):
        """Fetch current user info from session"""
        self.user, self.userInfo, self.role = self._getCurrentUser()
        self.allUsers = UserModel.getAllUsers()

    @staticmethod
    def _getCurrentUser():
        user = SessionManager.getUser() or {}
        name = f"{user.get('first_name', 'Unknown')} {user.get('last_name', '')}".strip()
        role = user.get("role", "Admin")
        return user, name or "Unknown User", role

    def openUsersWindow(self):
        """Initialize and show the main users window"""
        self.usersWindow = AdminUsersWindow(self.userInfo, self.role)
        self._populateUsersTable(self.allUsers)
        self._connectSignals()
        self.usersWindow.show()

    def _populateUsersTable(self, users):
        """Populate the users table with data"""
        table = self.usersWindow.usersTable
        table.setRowCount(len(users))
        for row, user in enumerate(users):
            full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
            items = [
                QTableWidgetItem(str(user.get('user_id', ''))),
                QTableWidgetItem(user.get('username', '')),
                QTableWidgetItem(full_name or "N/A"),
                QTableWidgetItem(user.get('role', 'Unknown')),
                QTableWidgetItem(user.get('status', 'Inactive'))
            ]
            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)  # Read-only
                table.setItem(row, col, item)

    def _connectSignals(self):
        """Connect all UI signals to controller methods"""
        w = self.usersWindow

        # Navigation
        w.dashboardOption.mousePressEvent = lambda e: self.navigateToDashboard()
        w.patientsOption.mousePressEvent = lambda e: self.navigateToPatients()
        w.reportsOption.mousePressEvent = lambda e: self.navigateToReports()
        w.notificationsOption.mousePressEvent = lambda e: self.navigateToNotifications()
        w.logoutOption.mousePressEvent = lambda e: self.logout()

        # Actions
        w.searchButton.clicked.connect(self.searchUsers)
        w.addUserButton.clicked.connect(self.showAddUserPopup)
        w.editUserButton.clicked.connect(self.showEditUserPopup)
        w.usersTable.itemClicked.connect(self.onUserSelected)

    def onUserSelected(self, item):
        """Handle row selection in users table"""
        row = item.row()
        try:
            self.usersWindow.selectedUserId = int(self.usersWindow.usersTable.item(row, 0).text())
            self.usersWindow.selectedUserData = UserModel.getUserById(self.usersWindow.selectedUserId)
        except (ValueError, Exception):
            self.usersWindow.selectedUserId = None
            self.usersWindow.selectedUserData = None

    def searchUsers(self):
        """Search users by keyword and refresh table"""
        query = self.usersWindow.searchInput.text().strip()
        results = UserModel.searchUsers(query) if query else UserModel.getAllUsers()
        self._populateUsersTable(results)

    def showAddUserPopup(self):
        """Open the Add User popup"""
        self.addUserPopup = AddUserPopup()
        self.addUserPopup.submitButton.clicked.connect(self.addUser)
        self.addUserPopup.show()

    def addUser(self):
        """Handle Add User form submission and create welcome notification"""

        if not self.addUserPopup:
            Dialogs.showErrorDialog("Error", "Add User popup is not available.")
            return

        data = self.addUserPopup.getUserData()

        # Default status for new users
        data.setdefault("status", "Active")

        error = self._validateUserData(data, is_new=True)
        if error:
            Dialogs.showErrorDialog("Validation Error", error)
            return

        success, db_message, new_user_id = UserModel.addUser(
            username=data["username"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            contact=data["contact"],
            role=data["role"],
            license_number=data["license_number"],
        )

        if not success:
            Dialogs.showErrorDialog("Add User Failed", db_message)
            return

        self.addUserPopup.close()
        self.addSuccessPopup = AddSuccessPopup(
            window="user")
        self.addSuccessPopup.show()
        self.loadAllUsers()

        # Create welcome notification
        full_name = f"{data['first_name']} {data['last_name']}".strip()
        title = "Welcome to MEDISYNC!"
        notification_message = (
            f"Hello {full_name}, your account has been created successfully. "
            f"You can now log in with username: {data['username']}."
        )

        NotificationsModel.createNotification(
            user_id=new_user_id,
            related_table="users",
            related_id=new_user_id,
            title=title,
            message=notification_message,
            priority="Info"
        )

        print(f"User created successfully. ID={new_user_id}")

    def showEditUserPopup(self):
        """Open Edit User popup with selected user data"""
        if not self.usersWindow.selectedUserId:
            Dialogs.showErrorDialog("No Selection", "Please select a user from the table to edit.")
            return

        self.editUserPopup = EditUserPopup()
        self.editUserPopup.populateForm(self.usersWindow.selectedUserData)
        self.editUserPopup.submitButton.clicked.connect(self.updateUser)
        self.editUserPopup.show()

    def updateUser(self):
        """Handle Edit User form submission"""
        data = self.editUserPopup.getUserData()
        error = self._validateUserData(data, is_new=False)
        if error:
            Dialogs.showErrorDialog("Validation Error", error)
            return

        success, message = UserModel.updateUser(
            user_id=self.usersWindow.selectedUserId,
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            contact=data['contact'],
            role=data['role'],
            license_number=data['license_number'],
            status=data['status'],
            password=data['password']  # None if not changed
        )

        if success:
            self.editUserPopup.hide()
            self.updateUserPopup = AddSuccessPopup(window="editUser")
            self.updateUserPopup.show()
            self.loadAllUsers()
            self.usersWindow.clearSelection()
        else:
            Dialogs.showErrorDialog("Update Failed", message)

    def loadAllUsers(self):
        """Refresh the users table with latest data"""
        self.allUsers = UserModel.getAllUsers()
        self._populateUsersTable(self.allUsers)

    @staticmethod
    def _validateUserData(data, is_new=True):
        """Shared validation logic for Add/Edit user"""
        if not data['username']:
            return "Username is required."
        if len(data['username']) < 3:
            return "Username must be at least 3 characters long."
        if not data['first_name'] or not data['last_name']:
            return "First name and last name are required."
        if not data['email']:
            return "Email address is required."
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data['email']):
            return "Please enter a valid email address."
        if not data['role']:
            return "Please select a user role."
        if data['contact'] and not re.match(r'^[\d\s\-]+$', data['contact']):
            return "Contact number contains invalid characters."
        if is_new:
            if not data['password']:
                return "Password is required for new users."
            if len(data['password']) < 6:
                return "Password must be at least 6 characters long."
        else:
            if data['password'] and len(data['password']) < 6:
                return "New password must be at least 6 characters long."
        if not is_new and not data.get('status'):
            return "Please select user status (Active/Inactive)."

        return None

    def navigateToDashboard(self):
        self._closeCurrent()
        from Controller.Admin.AdminDashboardController import AdminDashboardController
        AdminDashboardController().openDashboard()

    def navigateToPatients(self):
        self._closeCurrent()
        from Controller.Admin.AdminPatientsController import AdminPatientsController
        AdminPatientsController().openPatientsWindow()

    def navigateToReports(self):
        self._closeCurrent()
        from Controller.Admin.ReportsController import ReportsController
        ReportsController().openReportsWindow()

    def navigateToNotifications(self):
        self._closeCurrent()
        from Controller.Admin.AdminNotificationsController import AdminNotificationsController
        AdminNotificationsController().openNotificationsWindow()

    def logout(self):
        self._closeCurrent()
        SessionManager.clear()
        from Controller.Login.LoginController import LoginController
        from Model.Authentication.LoginModel import LoginModel
        from View.LoginGUI import Login
        loginModel = LoginModel()
        loginView = Login()
        self.loginController = LoginController(loginModel, loginView)
        loginView.show()

    def _closeCurrent(self):
        """Safely close all open windows/popups"""
        if self.usersWindow:
            self.usersWindow.close()
        if self.addUserPopup and self.addUserPopup.isVisible():
            self.addUserPopup.close()
        if self.editUserPopup and self.editUserPopup.isVisible():
            self.editUserPopup.close()
        if self.addSuccessPopup and self.addSuccessPopup.isVisible():
            self.addSuccessPopup.close()
        if self.updateUserPopup and self.updateUserPopup.isVisible():
            self.updateUserPopup.close()