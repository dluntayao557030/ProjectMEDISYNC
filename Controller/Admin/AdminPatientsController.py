from Model.Transactions.PatientModel import PatientsModel
from Model.Notifications.NotificationsModel import NotificationsModel
from Model.SessionManager import SessionManager
from View.AdminGUI.AdminPatientsWindow import AdminPatientsWindow, RegisterPatientPopup, EditPatientPopup, AddSuccessPopup
from View.GeneralPopups.Dialogs import Dialogs
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt

class AdminPatientsController:
    """
    Controller for Admin Patients Management.
    Handles patient CRUD operations, search, and navigation related to Patients.
    """

    def __init__(self):
        self.updatePatientPopup = None
        self.addPopup = None
        self.loginController = None
        self.allPatients = None
        self.patientsWindow = None
        self.registerPopup = None
        self.editPopup = None
        self._loadData()

    def _loadData(self):
        """Fetch initial data"""
        self.user, self.userInfo, self.role = self._getCurrentUser()
        self.allPatients = PatientsModel.getAllPatients()

    @staticmethod
    def _getCurrentUser():
        user = SessionManager.getUser() or {}
        name = f"{user.get('first_name', 'Unknown')} {user.get('last_name', '')}".strip()
        role = user.get("role", "Admin")
        return user, name or "Unknown User", role

    def openPatientsWindow(self):
        """Launch patients window and connect signals"""
        self.patientsWindow = AdminPatientsWindow(self.userInfo, self.role)
        self._populatePatientsTable(self.allPatients)
        self._connectSignals()
        self.patientsWindow.show()

    def _populatePatientsTable(self, patients):
        """Fill patients table"""
        table = self.patientsWindow.patientsTable
        table.setRowCount(len(patients))
        for row, patient in enumerate(patients):
            name = f"{patient.get('patient_first_name', '')} {patient.get('patient_last_name', '')}".strip()
            items = [
                QTableWidgetItem(str(patient.get('patient_id', ''))),
                QTableWidgetItem(name),
                QTableWidgetItem(patient.get('sex', '')),
                QTableWidgetItem(patient.get('room_number', '')),
                QTableWidgetItem(patient.get('doctor_name', '')),
                QTableWidgetItem(patient.get('nurse_name', '')),
                QTableWidgetItem(patient.get('status', ''))
            ]
            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                table.setItem(row, col, item)

    def _connectSignals(self):
        """Connect UI elements"""
        w = self.patientsWindow
        w.dashboardOption.mousePressEvent = lambda e: self.navigateToDashboard()
        w.usersOption.mousePressEvent = lambda e: self.navigateToUsers()
        w.reportsOption.mousePressEvent = lambda e: self.navigateToReports()
        w.notificationsOption.mousePressEvent = lambda e: self.navigateToNotifications()
        w.logoutOption.mousePressEvent = lambda e: self.logout()

        w.searchButton.clicked.connect(self.searchPatients)
        w.registerButton.clicked.connect(self.showRegisterPatientPopup)
        w.editButton.clicked.connect(self.showEditPatientPopup)
        w.patientsTable.itemClicked.connect(self.onPatientSelected)

    def onPatientSelected(self, item):
        """Handle table selection"""
        row = item.row()
        try:
            self.patientsWindow.selectedPatientId = int(self.patientsWindow.patientsTable.item(row, 0).text())
            self.patientsWindow.selectedPatientData = PatientsModel.getPatientById(self.patientsWindow.selectedPatientId)
        except (ValueError, Exception):
            self.patientsWindow.selectedPatientId = None
            self.patientsWindow.selectedPatientData = None

    def searchPatients(self):
        """Search and update table"""
        query = self.patientsWindow.searchInput.text().strip()
        results = PatientsModel.searchPatients(query) if query else PatientsModel.getAllPatients()
        self._populatePatientsTable(results)

    def showRegisterPatientPopup(self):
        """Open register popup"""
        self.registerPopup = RegisterPatientPopup()
        doctors = PatientsModel.getDoctorsList()
        nurses = PatientsModel.getNursesList()
        self.registerPopup.populateDoctors(doctors)
        self.registerPopup.populateNurses(nurses)
        self.registerPopup.submitButton.clicked.connect(self.registerPatient)
        self.registerPopup.show()

    def registerPatient(self):
        """Handle register submission and send welcome notification"""
        data = self.registerPopup.getPatientData()
        error = self._validatePatientData(data)
        if error:
            Dialogs.showErrorDialog("Validation Error", error)
            return

        patient_id = PatientsModel.registerPatient(**data)
        if patient_id:
            self.registerPopup.hide()
            self.addPopup = AddSuccessPopup(window="patient")
            self.addPopup.show()
            self.loadAllPatients()

            # === CREATE WELCOME NOTIFICATION FOR DOCTOR AND NURSE ===
            full_name = f"{data['first_name']} {data['last_name']}".strip()
            room = data['room_number']

            title = "New Patient Admitted"
            message = f"A new patient '{full_name}' has been admitted to Room {room}. Please review their record."

            # Notify the assigned Doctor
            if data['doctor_id']:
                NotificationsModel.createNotification(
                    user_id=data['doctor_id'],
                    related_table="patients",
                    related_id=patient_id,
                    title=title,
                    message=message,
                    priority="Attention"
                )

            # Notify the assigned Nurse
            if data['nurse_id']:
                NotificationsModel.createNotification(
                    user_id=data['nurse_id'],
                    related_table="patients",
                    related_id=patient_id,
                    title=title,
                    message=message,
                    priority="Attention"
                )

            print(f"Welcome notifications sent for new patient ID {patient_id}")

        else:
            Dialogs.showErrorDialog("Registration Failed", "Failed to register patient.")

    def showEditPatientPopup(self):
        """Open edit popup"""
        if not self.patientsWindow.selectedPatientId:
            Dialogs.showErrorDialog("No Selection", "Select a patient to edit.")
            return

        self.editPopup = EditPatientPopup()
        doctors = PatientsModel.getDoctorsList()
        nurses = PatientsModel.getNursesList()
        self.editPopup.populateDoctors(doctors)
        self.editPopup.populateNurses(nurses)
        self.editPopup.populateForm(self.patientsWindow.selectedPatientData)
        self.editPopup.submitButton.clicked.connect(self.updatePatient)
        self.editPopup.show()

    def updatePatient(self):
        """Handle update submission"""
        data = self.editPopup.getPatientData()
        error = self._validatePatientData(data)
        if error:
            Dialogs.showErrorDialog("Validation Error", error)
            return

        success = PatientsModel.updatePatient(self.patientsWindow.selectedPatientId, **data)
        if success:
            self.editPopup.hide()
            self.updatePatientPopup = AddSuccessPopup(window="editPatient")
            self.updatePatientPopup.show()
            self.loadAllPatients()

        else:
            Dialogs.showErrorDialog("Update Failed", "Failed to update patient.")

    def loadAllPatients(self):
        """Refresh table"""
        self.allPatients = PatientsModel.getAllPatients()
        self._populatePatientsTable(self.allPatients)

    @staticmethod
    def _validatePatientData(data):
        """Validate form data"""
        if not data['first_name'] or not data['last_name']:
            return "First and last name required."
        if not data['sex']:
            return "Select sex."
        if not data['room_number']:
            return "Room number required."
        if not data['diagnosis']:
            return "Diagnosis required."
        if not data['doctor_id']:
            return "Select doctor."
        if not data['nurse_id']:
            return "Select nurse."
        if 'status' in data and not data['status']:
            return "Select status."
        return None

    def navigateToDashboard(self):
        self._closeCurrent()
        from Controller.Admin.AdminDashboardController import AdminDashboardController
        AdminDashboardController().openDashboard()

    def navigateToUsers(self):
        self._closeCurrent()
        from Controller.Admin.AdminUsersController import AdminUsersController
        AdminUsersController().openUsersWindow()

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
        if self.patientsWindow:
            self.patientsWindow.close()
        if self.registerPopup and self.registerPopup.isVisible():
            self.registerPopup.close()
        if self.editPopup and self.editPopup.isVisible():
            self.editPopup.close()