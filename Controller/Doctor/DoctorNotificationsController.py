from Model.Notifications.NotificationsModel import NotificationsModel
from Model.SessionManager import SessionManager
from View.DoctorGUI.DoctorNotificationsWindow import DoctorNotificationsWindow

class DoctorNotificationsController:
    """
    Controller for Doctor Notifications Window
    """

    def __init__(self):
        self.loginController = None
        self.user, self.userInfo, self.role = self._getUserInfo()
        self.notificationsData = self._getNotificationsData()
        self.notificationsWindow = None

    def openNotificationsWindow(self):
        self.notificationsWindow = DoctorNotificationsWindow(self.userInfo, self.role)
        self.notificationsWindow.displayNotifications(self.notificationsData)
        self._connectSignals()
        self.notificationsWindow.show()

    def _connectSignals(self):
        w = self.notificationsWindow

        w.dashboardOption.mousePressEvent = lambda e: self.navigateToDashboard()
        w.prescriptionOption.mousePressEvent = lambda e: self.navigateToPrescription()
        w.logoutOption.mousePressEvent = lambda e: self.logout()

        w.filterDropdown.currentTextChanged.connect(self.onFilterChanged)
        w.searchButton.clicked.connect(self.searchNotifications)
        w.searchInput.returnPressed.connect(self.searchNotifications)

    def onFilterChanged(self, filter_text: str):
        if filter_text == "All Notifications":
            self.notificationsData = NotificationsModel.getAllNotifications(self.user['user_id'])
        else:
            self.notificationsData = NotificationsModel.getNotificationsByPriority(
                self.user['user_id'], filter_text
            )
        self.notificationsWindow.displayNotifications(self.notificationsData)

    def searchNotifications(self):
        query = self.notificationsWindow.getSearchQuery()

        if query:
            self.notificationsData = NotificationsModel.searchNotifications(
                self.user['user_id'], query
            )
        else:
            filter_selection = self.notificationsWindow.getFilterSelection()
            if filter_selection == "All Notifications":
                self.notificationsData = NotificationsModel.getAllNotifications(self.user['user_id'])
            else:
                self.notificationsData = NotificationsModel.getNotificationsByPriority(
                    self.user['user_id'], filter_selection
                )

        self.notificationsWindow.displayNotifications(self.notificationsData)

    @staticmethod
    def _getUserInfo():
        user = SessionManager.getUser() or {}
        name = f"{user.get('first_name', 'Unknown')} {user.get('last_name', '')}".strip()
        role = user.get("role", "Doctor")
        return user, name or "Unknown User", role

    def _getNotificationsData(self):
        return NotificationsModel.getAllNotifications(self.user['user_id'])

    def _closeCurrent(self):
        if self.notificationsWindow:
            self.notificationsWindow.close()

    def navigateToDashboard(self):
        self._closeCurrent()
        from Controller.Doctor.DoctorDashboardController import DoctorDashboardController
        DoctorDashboardController().openDashboard()

    def navigateToPrescription(self):
        self._closeCurrent()
        from Controller.Doctor.PrescriptionController import PrescriptionController
        PrescriptionController().openPrescriptionWindow()

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