from Model.Notifications.NotificationsModel import NotificationsModel
from Model.SessionManager import SessionManager
from View.AdminGUI.AdminNotificationsWindow import AdminNotificationsWindow

class AdminNotificationsController:
    """
    Controller for Admin Notifications Window.
    Admins see ALL system notifications (across all users) from the past 30 days.
    """

    def __init__(self):
        self.loginController = None
        self.user, self.userInfo, self.role = self._getUserInfo()
        self.notificationsData = self._getNotificationsData()
        self.notificationsWindow = None

    def openNotificationsWindow(self):
        self.notificationsWindow = AdminNotificationsWindow(self.userInfo, self.role)
        self.notificationsWindow.displayNotifications(self.notificationsData)
        self._connectSignals()
        self.notificationsWindow.show()

    def _connectSignals(self):
        w = self.notificationsWindow

        # Navigation
        w.dashboardOption.mousePressEvent = lambda e: self.navigateToDashboard()
        w.usersOption.mousePressEvent = lambda e: self.navigateToUsers()
        w.patientsOption.mousePressEvent = lambda e: self.navigateToPatients()
        w.reportsOption.mousePressEvent = lambda e: self.navigateToReports()
        w.logoutOption.mousePressEvent = lambda e: self.logout()

        # Filtering & Search
        w.filterDropdown.currentTextChanged.connect(self.onFilterChanged)
        w.searchButton.clicked.connect(self.searchNotifications)
        w.searchInput.returnPressed.connect(self.searchNotifications)

    def onFilterChanged(self, filter_text: str):
        """
        Handle priority filter change.
        Admin sees all notifications system-wide.
        """
        if filter_text == "All Notifications":
            self.notificationsData = NotificationsModel.getAllNotificationsForAdmin()
        else:
            # Filter system-wide notifications by priority
            all_notifications = NotificationsModel.getAllNotificationsForAdmin()
            priority_map = {"Urgent": "Urgent", "Attention": "Attention", "Info": "Info"}
            target_priority = priority_map.get(filter_text)

            self.notificationsData = [
                n for n in all_notifications
                if n.get('priority') == target_priority
            ]

        self.notificationsWindow.displayNotifications(self.notificationsData)

    def searchNotifications(self):
        """
        Search across all system notifications (Admin view).
        Falls back to current filter if query is empty.
        """
        query = self.notificationsWindow.getSearchQuery().strip().lower()

        # Base: all admin notifications
        base_notifications = NotificationsModel.getAllNotificationsForAdmin()

        if query:
            # Global search across title and message
            self.notificationsData = [
                n for n in base_notifications
                if query in n.get('title', '').lower() or query in n.get('message', '').lower()
            ]
        else:
            # No query → respect current filter
            filter_selection = self.notificationsWindow.getFilterSelection()
            if filter_selection == "All Notifications":
                self.notificationsData = base_notifications
            else:
                priority_map = {"Urgent": "Urgent", "Attention": "Attention", "Info": "Info"}
                target_priority = priority_map.get(filter_selection)
                self.notificationsData = [
                    n for n in base_notifications
                    if n.get('priority') == target_priority
                ]

        self.notificationsWindow.displayNotifications(self.notificationsData)

    @staticmethod
    def _getUserInfo():
        user = SessionManager.getUser() or {}
        name = f"{user.get('first_name', 'Unknown')} {user.get('last_name', '')}".strip()
        role = user.get("role", "Admin")
        return user, name or "Unknown User", role

    @staticmethod
    def _getNotificationsData():
        """Initial load: all system notifications (past 30 days)"""
        return NotificationsModel.getAllNotificationsForAdmin()

    def _closeCurrent(self):
        if self.notificationsWindow:
            self.notificationsWindow.close()

    def navigateToDashboard(self):
        self._closeCurrent()
        from Controller.Admin.AdminDashboardController import AdminDashboardController
        AdminDashboardController().openDashboard()

    def navigateToUsers(self):
        self._closeCurrent()
        from Controller.Admin.AdminUsersController import AdminUsersController
        AdminUsersController().openUsersWindow()

    def navigateToPatients(self):
        self._closeCurrent()
        from Controller.Admin.AdminPatientsController import AdminPatientsController
        AdminPatientsController().openPatientsWindow()

    def navigateToReports(self):
        self._closeCurrent()
        from Controller.Admin.ReportsController import ReportsController
        ReportsController().openReportsWindow()

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