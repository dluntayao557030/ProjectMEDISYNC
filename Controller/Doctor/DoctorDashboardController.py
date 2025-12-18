from Model.KPIs.DoctorKPIs import DoctorKPIs
from Model.Tables.DoctorTables import DoctorTables
from Model.SessionManager import SessionManager
from View.DoctorGUI.DoctorDashboardWindow import DoctorDashboardWindow

class DoctorDashboardController:
    """
    Controller for Doctor Dashboard.
    Orchestrates data fetching, formatting, and navigation.
    """

    def __init__(self):
        self.loginController = None
        self.doctorDashboard = None
        self._loadData()

    def _loadData(self):
        """Fetch and prepare all required data"""
        self.kpis = {
            'activePatients': self._safeKPI(DoctorKPIs.activePatientsCount),
            'activePrescriptions': self._safeKPI(DoctorKPIs.activePrescriptionsCount),
            'urgentCases': self._safeKPI(DoctorKPIs.urgentCasesCount)
        }

        self.user, self.userInfo, self.role = self._getCurrentUser()
        self.patientHistory = self._safeTable(DoctorTables.getPatientHistory)
        self.pendingPrescriptions = self._safeTable(DoctorTables.getPendingPrescriptions)

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
        role = user.get("role", "Doctor")
        return user, name or "Unknown User", role

    def openDashboard(self):
        """Launch the dashboard and connect navigation"""
        self.doctorDashboard = DoctorDashboardWindow(
            patientKpi=self.kpis['activePatients'],
            prescriptionKpi=self.kpis['activePrescriptions'],
            urgentKpi=self.kpis['urgentCases'],
            userInfo=self.userInfo,
            dataHistory=self.patientHistory,
            dataPending=self.pendingPrescriptions
        )
        self._connectNavigation()
        self.doctorDashboard.show()

    def _connectNavigation(self):
        dashboard = self.doctorDashboard
        dashboard.prescriptionOption.mousePressEvent = lambda e: self.navigateToPrescription()
        dashboard.notificationsOption.mousePressEvent = lambda e: self.navigateToNotifications()
        dashboard.logoutOption.mousePressEvent = lambda e: self.logout()

    def navigateToPrescription(self):
        self._closeCurrent()
        from Controller.Doctor.PrescriptionController import PrescriptionController
        PrescriptionController().openPrescriptionWindow()

    def navigateToNotifications(self):
        self._closeCurrent()
        from Controller.Doctor.DoctorNotificationsController import DoctorNotificationsController
        DoctorNotificationsController().openNotificationsWindow()

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
        if self.doctorDashboard:
            self.doctorDashboard.close()
