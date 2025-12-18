from PyQt6.QtWidgets import QPushButton
from Model.KPIs.PharmacistKPIs import PharmacistKPIs
from Model.Tables.PharmacistTables import PharmacistTables
from Model.SessionManager import SessionManager
from View.PharmacistGUI.PharmacistDashboardWindow import PharmacistDashboardWindow
from View.GeneralPopups.Dialogs import Dialogs

class PharmacistDashboardController:
    """
    Controller for Pharmacist Dashboard
    """

    def __init__(self):
        self.pharmacistDashboard = None
        self.loginController = None
        self._loadData()

    def _loadData(self):
        """Fetch and prepare all required data"""

        self.kpis = {
            'activePrescriptions': self._safeKPI(PharmacistKPIs.activePrescriptionsCount),
            'pendingVerification': self._safeKPI(PharmacistKPIs.pendingVerificationCount),
            'controlledSubstances': self._safeKPI(PharmacistKPIs.controlledSubstancesCount)
        }

        self.user, self.userInfo, self.role = self._getCurrentUser()

        raw_expiring = self._safeTable(PharmacistTables.getExpiringMedications)
        self.expiringMedications = self._formatExpiringData(raw_expiring)
        self.medicationsToPrep = self._safeTable(PharmacistTables.getMedicationsToPrepare)

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
        role = user.get("role", "Pharmacist")
        return user, name or "Unknown User", role

    @staticmethod
    def _formatExpiringData(data):
        formatted = []
        for item in data:
            patient_name = f"{item.get('patient_first_name', '')} {item.get('patient_last_name', '')}".strip()
            medication = f"{item.get('brand_name', '')} ({item.get('generic_name', '')})".strip()
            formatted.append({
                'prescription_id': item.get('prescription_id', ''),
                'patient_name': patient_name or "Unknown Patient",
                'medication': medication or "Unknown",
                'quantity_dispensed': item.get('quantity_dispensed', 0),
                'expiry_date': str(item.get('expiry_date', '')),
                'days_until_expiry': item.get('days_until_expiry', 0)
            })
        return formatted

    def openDashboard(self):
        """Launch the dashboard and connect signals"""
        self.pharmacistDashboard = PharmacistDashboardWindow(
            activePrescriptionsKpi=self.kpis['activePrescriptions'],
            pendingKpi=self.kpis['pendingVerification'],
            controlledKpi=self.kpis['controlledSubstances'],
            userInfo=self.userInfo,
            role=self.role,
            expiringData=self.expiringMedications,
            medicationsToPrep=self.medicationsToPrep
        )
        self._connectNavigation()
        self._connectMedicationButtons()  # One-way only
        self.pharmacistDashboard.show()

    def _connectNavigation(self):
        """Connects navigation signals"""
        dashboard = self.pharmacistDashboard
        dashboard.verificationOption.mousePressEvent = lambda e: self.navigateToVerification()
        dashboard.notificationsOption.mousePressEvent = lambda e: self.navigateToNotifications()
        dashboard.logoutOption.mousePressEvent = lambda e: self.logout()

    def _connectMedicationButtons(self):
        """Connects 'To be Prepared' buttons."""
        layout = self.pharmacistDashboard.scrollLayout
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if not item:
                continue
            card = item.widget()
            if not card:
                continue

            preparation_id = card.property("preparation_id")
            if not preparation_id:
                continue

            button = card.findChild(QPushButton)
            if button and button.text() == "To be Prepared":
                # Card will be deleted after click
                button.clicked.connect(
                    lambda checked=False, pid=preparation_id, c=card: self.markAsPrepared(pid, c)
                )

    @staticmethod
    def markAsPrepared(preparation_id, card):
        """Marks medication as Prepared and removes card permanently"""
        try:
            success = PharmacistTables.markMedicationAsPrepared(preparation_id)
            if not success:
                Dialogs.showErrorDialog("Error", "Failed to mark as prepared.\nIt may already be processed.")
                return

            # Remove card immediately — prevents any further clicks
            card.deleteLater()

            Dialogs.showSuccessDialog(
                "Success",
                "Medication marked as Prepared.\nReady for nurse administration."
            )

            print(f"Pharmacist marked preparation #{preparation_id} as Prepared")

        except Exception as e:
            print(f"Error in markAsPrepared: {e}")
            Dialogs.showErrorDialog("Error", "An unexpected error occurred.")

    def navigateToVerification(self):
        self._closeCurrent()
        from Controller.Pharmacist.VerificationController import VerificationController
        VerificationController().openVerificationWindow()

    def navigateToNotifications(self):
        self._closeCurrent()
        from Controller.Pharmacist.PharmacistNotificationsController import PharmacistNotificationsController
        PharmacistNotificationsController().openNotificationsWindow()

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
        if self.pharmacistDashboard:
            self.pharmacistDashboard.close()