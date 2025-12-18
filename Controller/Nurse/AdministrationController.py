from PyQt6.QtWidgets import QTableWidgetItem
from Model.Transactions.AdministrationModel import AdministrationModel
from Model.Tables.NurseTables import NurseTables
from Model.SessionManager import SessionManager
from View.NurseGUI.AdministrationWindow import AdministrationWindow, RecordConfirmationPopup
from View.GeneralPopups.Dialogs import Dialogs

class AdministrationController:
    """
    Controller for Nurse Medication Administration
    """

    def __init__(self):
        self.loginController = None
        self._loadUserData()

        # Selected Data
        self.selectedPatientId = None
        self.selectedPatientData = None
        self.selectedPrescriptionId = None
        self.selectedPrescriptionData = None
        self.availablePrescriptions = []

        # Window Reference
        self.administerWindow = None

    def _loadUserData(self):
        """Load user information from session"""

        self.user = SessionManager.getUser() or {}
        self.userInfo = f"{self.user.get('first_name', 'Unknown')} {self.user.get('last_name', '')}"
        self.role = self.user.get("role", "Nurse")
        self.nurseId = self.user.get("user_id")

    def openAdministrationWindow(self):
        """Opens the Administration window"""
        try:
            self.administerWindow = AdministrationWindow(
                userInfo=self.userInfo or "Unknown",
                role=self.role or "Nurse"
            )

            self._connectSignals()
            self.loadAssignedPatients()

            self.administerWindow.show()
        except Exception as e:
            print(f"Failed to open AdministrationWindow: {e}")
            Dialogs.showErrorDialog("Window Error", f"Failed to open: {str(e)}")

    def _connectSignals(self):
        """Connects all UI signals"""
        try:
            # Patient Selection
            self.administerWindow.patientSearchButton.clicked.connect(self.searchPatients)
            self.administerWindow.patientSearch.returnPressed.connect(self.searchPatients)
            self.administerWindow.patientsTable.itemSelectionChanged.connect(self.onPatientSelected)
            self.administerWindow.nextButton.clicked.connect(self.proceedToRecording)

            # Recording View
            self.administerWindow.recordButton.clicked.connect(self.recordAdministration)

            # "Other" input toggle
            self.administerWindow.otherRadio.toggled.connect(self._toggleOtherInput)

            # Navigation
            self.administerWindow.dashboardOption.mousePressEvent = lambda er: self.navigateToDashboard()
            self.administerWindow.notificationsOption.mousePressEvent = lambda er: self.navigateToNotifications()
            self.administerWindow.logoutOption.mousePressEvent = lambda er: self.logout()

        except Exception as e:
            print(f"Failed to connect signals: {e}")

    def _toggleOtherInput(self, checked):
        """Enable/disable 'Other' input field based on radio button"""
        self.administerWindow.otherInput.setEnabled(checked)
        if not checked:
            self.administerWindow.otherInput.clear()

    # Patient Selection

    def loadAssignedPatients(self):
        """Loads assigned patients"""
        try:
            patients = NurseTables.getAssignedPatients() or []
            if not isinstance(patients, list):
                patients = []

            self._populatePatientTable(patients)
            print(f"✓ Loaded {len(patients)} assigned patients")

        except Exception as e:
            print(f"Failed to load patients: {e}")
            Dialogs.showErrorDialog("Load Error", f"Failed to load patients: {str(e)}")

    def searchPatients(self):
        """Searches assigned patients"""
        try:
            query = self.administerWindow.patientSearch.text().strip()

            if query:
                patients = NurseTables.searchAssignedPatients(query) or []
            else:
                patients = NurseTables.getAssignedPatients() or []

            if not isinstance(patients, list):
                patients = []

            self._populatePatientTable(patients)
            print(f"✓ Search: {len(patients)} results")

        except Exception as e:
            print(f"Failed to search: {e}")
            Dialogs.showErrorDialog("Search Error", f"Failed to search: {str(e)}")

    def _populatePatientTable(self, patients):
        """Populates patient table with data"""
        try:
            table = self.administerWindow.patientsTable
            table.setRowCount(0)  # Clear existing rows

            if not patients:
                return

            table.setRowCount(len(patients))

            for row, patient in enumerate(patients):
                items = [
                    str(patient.get('patient_id', '')),
                    patient.get('patient_first_name', ''),
                    patient.get('patient_last_name', ''),
                    patient.get('generic_name', ''),
                    patient.get('brand_name', ''),
                    str(patient.get('date_of_birth', '')),
                    patient.get('sex', ''),
                    patient.get('room_number', ''),
                    patient.get('diagnosis', '')
                ]

                for col, value in enumerate(items):
                    item = QTableWidgetItem(value)
                    table.setItem(row, col, item)

        except Exception as e:
            print(f"Failed to populate table: {e}")

    def onPatientSelected(self):
        """Handles patient selection from the table"""
        try:
            table = self.administerWindow.patientsTable
            row = table.currentRow()
            if row < 0:
                self.selectedPatientId = None
                self.selectedPatientData = None
                return

            self.selectedPatientId = table.item(row, 0).text()

            self.selectedPatientData = {
                'patient_id': self.selectedPatientId,
                'patient_first_name': table.item(row, 1).text(),
                'patient_last_name': table.item(row, 2).text(),
                'generic_name': table.item(row, 3).text(),
                'brand_name': table.item(row, 4).text(),
                'date_of_birth': table.item(row, 5).text(),
                'sex': table.item(row, 6).text(),
                'room_number': table.item(row, 7).text(),
                'diagnosis': table.item(row, 8).text()
            }

            print(
                f"Selected Patient ID: {self.selectedPatientId} - {self.selectedPatientData['patient_first_name']} {self.selectedPatientData['patient_last_name']} ({self.selectedPatientData['brand_name']})")

        except Exception as e:
            print(f"Failed to select patient: {e}")
            self.selectedPatientId = None
            self.selectedPatientData = None

    # Record Administration

    def proceedToRecording(self):
        """Validates and loads prescription for recording"""
        try:
            if not self.selectedPatientId or not self.selectedPatientData:
                Dialogs.showErrorDialog("Validation Error", "Please select a patient.")
                return

            self.availablePrescriptions = NurseTables.getActivePrescriptionsForPatient(
                self.selectedPatientId, self.selectedPatientData['generic_name'], self.selectedPatientData['brand_name']) or []

            if not self.availablePrescriptions:
                Dialogs.showErrorDialog("No Prescriptions",
                                        "This patient has no active prescriptions.")
                return

            # Use first active prescription
            self.selectedPrescriptionData = self.availablePrescriptions[0]
            self.selectedPrescriptionId = self.selectedPrescriptionData.get('prescription_id')

            self.administerWindow.loadPrescriptionDetails(
                self.selectedPrescriptionData,
                self.selectedPatientData
            )

            self.administerWindow.stackedWidget.setCurrentIndex(1)
            print(f"✓ Loaded prescription {self.selectedPrescriptionId}")

        except Exception as e:
            print(f"Failed to proceed: {e}")
            Dialogs.showErrorDialog("Error", f"Failed to load prescription: {str(e)}")

    # === RECORD ADMINISTRATION ===

    def recordAdministration(self):
        """Records medication administration"""
        try:
            if not self.selectedPrescriptionId:
                Dialogs.showErrorDialog("Error", "No prescription selected.")
                return

            # Get form data
            data = self.administerWindow.getAdministrationData()

            # Validate
            if not data['patient_assessment']:
                Dialogs.showErrorDialog("Validation Error", "Please select patient assessment.")
                return

            # Calculate status based on frequency
            frequency = self.selectedPrescriptionData.get('frequency', '')
            status = AdministrationModel.calculateAdministrationStatus(
                self.selectedPrescriptionId, frequency
            )

            # Record in database
            success = AdministrationModel.recordMedicationAdministration(
                prescription_id=self.selectedPrescriptionId,
                administration_time=data['administration_time'],
                patient_assessment=data['patient_assessment'],
                adverse_reactions=data['adverse_reactions'],
                remarks=None,
                status=status
            )

            if success:
                # Create notification
                self._createNotificationRecord(status)

                # Write audit log
                self._writeAuditLog(data, status)

                print(f"✓ Medication administration recorded!")
                self._showRecordConfirmation()
            else:
                Dialogs.showErrorDialog("Recording Error", "Failed to record.")

        except Exception as e:
            print(f"Failed to record: {e}")
            Dialogs.showErrorDialog("Recording Error", f"Failed: {str(e)}")

    def _createNotificationRecord(self, status):
        """Creates notification for the administration"""
        try:
            # Get doctor ID from prescription
            doctor_id = self.selectedPrescriptionData.get('doctor_id')
            if not doctor_id:
                return

            patient_name = f"{self.selectedPatientData.get('patient_first_name', '')} {self.selectedPatientData.get('patient_last_name', '')}"
            medication = self.selectedPrescriptionData.get('generic_name', '')

            title = f"Medication {'Administered' if status == 'Administered' else 'Missed (Late)'}"
            message = f"{patient_name} - {medication} administered by {self.userInfo}"
            notification_type = 'Info' if status == 'Administered' else 'Attention'

            AdministrationModel.createNotification(
                user_id=doctor_id,
                related_table='medication_administration',
                related_id=self.selectedPrescriptionId,
                title=title,
                message=message,
                notification_type=notification_type
            )

            print(f"✓ Notification created")

        except Exception as e:
            print(f"Failed to create notification: {e}")

    def _writeAuditLog(self, data, status):
        """Writes audit log for the administration"""
        try:
            patient_name = f"{self.selectedPatientData.get('patient_first_name', '')} {self.selectedPatientData.get('patient_last_name', '')}"
            medication = f"{self.selectedPrescriptionData.get('brand_name', '')} ({self.selectedPrescriptionData.get('generic_name', '')})"

            audit_data = {
                'prescription_id': self.selectedPrescriptionId,
                'patient_name': patient_name,
                'medication': medication,
                'dosage': self.selectedPrescriptionData.get('dosage', ''),
                'frequency': self.selectedPrescriptionData.get('frequency', ''),
                'administration_time': data['administration_time'],
                'patient_assessment': data['patient_assessment'],
                'adverse_reactions': data['adverse_reactions'],
                'status': status,
                'nurse_name': self.userInfo,
                'nurse_id': self.nurseId,
                'remarks': None
            }

            AdministrationModel.writeAuditLog(audit_data)
            print(f"✓ Audit log written")

        except Exception as e:
            print(f"Failed to write audit log: {e}")

    def _showRecordConfirmation(self):
        """Displays confirmation popup"""
        try:
            popup = RecordConfirmationPopup()

            popup.closeButton.clicked.connect(lambda: (
                self.administerWindow.resetToPatientSelection(),
                self.loadAssignedPatients(),
                popup.close()
            ))

            popup.show()

        except Exception as e:
            print(f"Failed to show confirmation: {e}")

    # === NAVIGATION ===

    def navigateToDashboard(self):
        """Navigate to Nurse Dashboard"""
        try:
            if self.administerWindow:
                self.administerWindow.close()

            from Controller.Nurse.NurseDashboardController import NurseDashboardController
            NurseDashboardController().openDashboard()

        except Exception as e:
            print(f"Failed to navigate: {e}")

    def navigateToNotifications(self):
        """Navigate to Notifications"""
        try:
            if self.administerWindow:
                self.administerWindow.close()

            from Controller.Nurse.NurseNotificationsController import NurseNotificationsController
            NurseNotificationsController().openNotificationsWindow()

        except Exception as e:
            print(f"Failed to navigate: {e}")

    def logout(self):
        """Logout"""
        try:
            SessionManager.clear()

            if self.administerWindow:
                self.administerWindow.close()

            from Controller.Login.LoginController import LoginController
            from Model.Authentication.LoginModel import LoginModel
            from View.LoginGUI import Login

            loginModel = LoginModel()
            loginView = Login()
            self.loginController = LoginController(loginModel, loginView)
            loginView.show()

        except Exception as e:
            print(f"Failed to logout: {e}")