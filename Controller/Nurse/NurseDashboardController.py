from Model.KPIs.NurseKPIs import NurseKPIs
from Model.Tables.NurseTables import NurseTables
from Model.SessionManager import SessionManager
from View.NurseGUI.NurseDashboardWindow import NurseDashboardWindow

class NurseDashboardController:
    """
    Controller for Nurse Dashboard
    """

    def __init__(self):
        self.loginController = None
        self.kpis = {
            'assignedPatients': self._safeKPI(NurseKPIs.assignedPatientsCount),
            'dueMedications': self._safeKPI(NurseKPIs.dueMedicationsCount),
            'urgentMedications': self._safeKPI(NurseKPIs.urgentMedicationsCount)
        }

        self.user, self.userInfo, self.role = self._getCurrentUser()

        self.completedMedications = self._formatCompletedData(
            self._safeTable(NurseTables.getCompletedMedicationsToday)
        )
        self.preparationStatus = self._safeTable(NurseTables.getMedicationPreparationStatus)

        self.nurseDashboard = None

    def openDashboard(self):
        """Launch the dashboard and connect navigation"""
        self.nurseDashboard = NurseDashboardWindow(
            assignedPatientsKpi=self.kpis['assignedPatients'],
            dueMedicationsKpi=self.kpis['dueMedications'],
            urgentKpi=self.kpis['urgentMedications'],
            userInfo=self.userInfo,
            role=self.role,
            completedMedicationsData=self.completedMedications,
            preparationStatusData=self.preparationStatus
        )
        self._connectNavigation()
        self.nurseDashboard.show()

    def _connectNavigation(self):
        dashboard = self.nurseDashboard
        dashboard.administerOption.mousePressEvent = lambda e: self.navigateToAdminister()
        dashboard.notificationsOption.mousePressEvent = lambda e: self.navigateToNotifications()
        dashboard.logoutOption.mousePressEvent = lambda e: self.logout()

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
        role = user.get("role", "Nurse")
        return user, name or "Unknown User", role

    @staticmethod
    def _formatCompletedData(data):
        """Formats completed medications data for table display."""
        formatted = []
        for item in data:
            formatted.append({
                'administration_id': item.get('administration_id', ''),
                'patient_name': item.get('patient_name', 'Unknown Patient'),
                'medication': item.get('medication', 'Unknown Medication'),
                'dosage': item.get('dosage', ''),
                'administration_time': str(item.get('administration_time', ''))[:19] if item.get(
                    'administration_time') else '',
                'patient_assessment': item.get('patient_assessment', ''),
                'status': item.get('status', 'Administered')
            })
        return formatted

    def navigateToAdminister(self):
        self._closeCurrent()
        from Controller.Nurse.AdministrationController import AdministrationController
        AdministrationController().openAdministrationWindow()

    def navigateToNotifications(self):
        self._closeCurrent()
        from Controller.Nurse.NurseNotificationsController import NurseNotificationsController
        NurseNotificationsController().openNotificationsWindow()

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
        if self.nurseDashboard:
            self.nurseDashboard.close()