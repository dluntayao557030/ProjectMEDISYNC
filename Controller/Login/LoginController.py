from Controller.Pharmacist.PharmacistDashboardController import PharmacistDashboardController
from Controller.Doctor.DoctorDashboardController import DoctorDashboardController
from Controller.Nurse.NurseDashboardController import NurseDashboardController
from Controller.Admin.AdminDashboardController import AdminDashboardController
from Model.Authentication.LoginModel import LoginModel
from View.LoginGUI import Login, LoginErrorPopup, LoginSuccessPopup
from Model.SessionManager import SessionManager
from Model.Tasks.PrescriptionCompletionTask import complete_expired_prescriptions

class LoginController:
    """
    Controller for Login. Handles getting user input and directing users after
    successful login.
    """

    def __init__(self, model: LoginModel, view: Login):
        self.model = model
        self.view = view
        self.view.loginButton.clicked.connect(self.handleLogin)

        self.popup = None
        self.doctorDashboardController = None
        self.pharmacistDashboardController = None
        self.nurseDashboardController = None
        self.adminDashboardController = None

    def handleLogin(self):
        username = self.view.username.text().strip()
        password = self.view.password.text().strip()

        # Checks for empty fields
        if not username or not password:
            self.popup = LoginErrorPopup("empty", self.view)
            self.popup.show()
            self.popup.closeButton.clicked.connect(self.clearLoginFields)
            return

        # Validates user
        user = self.model.validateUser(username, password)

        if not user:
            self.popup = LoginErrorPopup("invalid", self.view)
            self.popup.show()
            self.popup.closeButton.clicked.connect(self.clearLoginFields)
            return

        # Successful login
        self.popup = LoginSuccessPopup(user['first_name'], user['role'], self.view)
        self.popup.show()
        self.popup.continueButton.clicked.connect(self.continueAfterLogin)

        # Setting user information in Session Manager for referencing
        SessionManager.setUser(user)
        complete_expired_prescriptions()

    def clearLoginFields(self):
        # Closes popup and clears login input fields
        if self.popup:
            self.popup.close()
            self.view.username.setText("")
            self.view.password.setText("")
            self.view.username.setFocus()

    def continueAfterLogin(self):

        if self.popup:
            self.popup.close()
        self.view.close()

        # Checks user role from Session Manager
        role = SessionManager.getUserRole()

        if role == "Doctor":
            self.openDoctorDashboard()
        elif role == "Nurse":
            self.openNurseDashboard()
        elif role == "Pharmacist":
            self.openPharmacistDashboard()
        elif role == "Admin":
            self.openAdminDashboard()

    # ======================================================
    # REDIRECTION METHODS: Directs to the GUI for each role
    # ======================================================

    def openDoctorDashboard(self):
        self.doctorDashboardController = DoctorDashboardController()
        self.doctorDashboardController.openDashboard()

    def openNurseDashboard(self):
        self.nurseDashboardController = NurseDashboardController()
        self.nurseDashboardController.openDashboard()

    def openPharmacistDashboard(self):
        self.pharmacistDashboardController = PharmacistDashboardController()
        self.pharmacistDashboardController.openDashboard()

    def openAdminDashboard(self):
        self.adminDashboardController = AdminDashboardController()
        self.adminDashboardController.openDashboard()