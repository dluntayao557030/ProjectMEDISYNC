from Model.KPIs.AdminKPIs import AdminKPIs
from Model.Tables.AdminTables import AdminTables
from Model.SessionManager import SessionManager
from View.AdminGUI.AdminDashboardWindow import AdminDashboardWindow

class AdminDashboardController:
    """
    Controller for Admin Dashboard.
    Orchestrates data fetching, formatting, and navigation.
    """

    def __init__(self):
        self.loginController = None
        self.adminDashboard = None
        self._loadData()

    def _loadData(self):
        """Fetch and prepare all required data"""
        self.kpis = {
            'activeUsers': self._safeKPI(AdminKPIs.activeUsersCount),
            'activePatients': self._safeKPI(AdminKPIs.activePatientsCount),
            'activePrescriptions': self._safeKPI(AdminKPIs.activePrescriptionsCount),
            'pendingPrescriptions': self._safeKPI(AdminKPIs.pendingPrescriptionsCount),
            'missedMedications': self._safeKPI(AdminKPIs.missedMedicationsCount)
        }

        self.user, self.userInfo, self.role = self._getCurrentUser()
        self.todaysActivity = self._formatActivityData(
            self._safeTable(AdminTables.getTodaysActivitySummary)
        )
    @staticmethod
    def _safeKPI(func):
        try: return func() or 0
        except Exception as e: print(f"KPI Error: {e}"); return 0

    @staticmethod
    def _safeTable(func):
        try: return func() or []
        except Exception as e: print(f"Table Error: {e}"); return []

    @staticmethod
    def _getCurrentUser():
        user = SessionManager.getUser() or {}
        name = f"{user.get('first_name', 'Unknown')} {user.get('last_name', '')}".strip()
        role = user.get("role", "Admin")
        return user, name or "Unknown User", role

    @staticmethod
    def _formatActivityData(data):
        formatted = []
        for item in data:
            related = (f"{item.get('related_table')} #{item.get('related_id')}"
                       if item.get('related_table') and item.get('related_id') else "N/A")
            formatted.append({
                'notification_id': item.get('notification_id', ''),
                'created_at': str(item.get('created_at', ''))[:19],
                'user_name': item.get('user_name', 'Unknown'),
                'role': item.get('role', 'Unknown'),
                'type': item.get('type', 'Info'),
                'title': item.get('title', 'No title'),
                'related_info': related
            })
        return formatted

    def openDashboard(self):
        """Launch the dashboard and connect navigation"""
        self.adminDashboard = AdminDashboardWindow(
            activeUsersKpi=self.kpis['activeUsers'],
            activePatientsKpi=self.kpis['activePatients'],
            activePrescriptionsKpi=self.kpis['activePrescriptions'],
            pendingPrescriptionsKpi=self.kpis['pendingPrescriptions'],
            missedMedicationsKpi=self.kpis['missedMedications'],
            userInfo=self.userInfo,
            role=self.role,
            todaysActivityData=self.todaysActivity
        )
        self._connectNavigation()
        self.adminDashboard.show()

    def _connectNavigation(self):
        dashboard = self.adminDashboard
        dashboard.usersOption.mousePressEvent = lambda e: self.navigateToUsers()
        dashboard.patientsOption.mousePressEvent = lambda e: self.navigateToPatients()
        dashboard.reportsOption.mousePressEvent = lambda e: self.navigateToReports()
        dashboard.notificationsOption.mousePressEvent = lambda e: self.navigateToNotifications()
        dashboard.logoutOption.mousePressEvent = lambda e: self.logout()

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
        if self.adminDashboard:
            self.adminDashboard.close()