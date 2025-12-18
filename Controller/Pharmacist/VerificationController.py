from PyQt6.QtWidgets import QTableWidgetItem
from Model.Transactions.VerificationModel import VerificationModel
from Model.SessionManager import SessionManager
from View.PharmacistGUI.VerificationWindow import PharmacistVerificationWindow, VerificationSummaryPopup
from View.GeneralPopups.Dialogs import Dialogs

class VerificationController:
    """
    Controller for Pharmacist Verification Window
    """

    def __init__(self):
        self.loginController = None
        self._loadUserData()

        self.selectedPrescriptionId = None
        self.selectedPrescriptionData = None
        self.verificationWindow = None

    def _loadUserData(self):
        """Load user information from session"""
        self.user = SessionManager.getUser() or {}
        self.userInfo = f"{self.user.get('first_name', 'Unknown')} {self.user.get('last_name', '')}"
        self.role = self.user.get("role", "Pharmacist")
        self.pharmacistId = self.user.get("user_id")

    def openVerificationWindow(self):
        """Opens the Verification window"""
        try:
            self.verificationWindow = PharmacistVerificationWindow(
                userInfo=self.userInfo or "Unknown",
                role=self.role or "Pharmacist"
            )
            self._connectSignals()
            self.loadPendingPrescriptions()
            self.verificationWindow.show()
        except Exception as e:
            print(f"Failed to open VerificationWindow: {e}")
            Dialogs.showErrorDialog("Window Error", f"Failed to open: {str(e)}")

    def _connectSignals(self):
        """Connects all UI signals"""
        try:
            w = self.verificationWindow

            w.pendingSearchButton.clicked.connect(self.searchPendingPrescriptions)
            w.pendingSearch.returnPressed.connect(self.searchPendingPrescriptions)
            w.pendingTable.itemSelectionChanged.connect(self.onPrescriptionSelected)
            w.confirmButton.clicked.connect(self.verifyPrescription)

            w.dashboardOption.mousePressEvent = lambda er: self.navigateToDashboard()
            w.notificationsOption.mousePressEvent = lambda er: self.navigateToNotifications()
            w.logoutOption.mousePressEvent = lambda er: self.logout()
        except Exception as e:
            print(f"Failed to connect signals: {e}")

    def loadPendingPrescriptions(self):
        """Loads all pending prescriptions into the table"""
        try:
            prescriptions = VerificationModel.getPendingPrescriptions() or []
            if not isinstance(prescriptions, list):
                prescriptions = []

            self._populatePrescriptionTable(prescriptions)
            print(f"✓ Loaded {len(prescriptions)} pending prescriptions")
        except Exception as e:
            print(f"Failed to load prescriptions: {e}")
            Dialogs.showErrorDialog("Load Error", f"Failed to load prescriptions: {str(e)}")

    def searchPendingPrescriptions(self):
        """Searches pending prescriptions"""
        try:
            query = self.verificationWindow.pendingSearch.text().strip()

            if query:
                prescriptions = VerificationModel.searchPendingPrescriptions(query) or []
            else:
                prescriptions = VerificationModel.getPendingPrescriptions() or []

            if not isinstance(prescriptions, list):
                prescriptions = []

            self._populatePrescriptionTable(prescriptions)
            print(f"✓ Search: {len(prescriptions)} results")
        except Exception as e:
            print(f"Failed to search: {e}")
            Dialogs.showErrorDialog("Search Error", f"Failed to search: {str(e)}")

    def _populatePrescriptionTable(self, prescriptions):
        """Populates the prescription table"""
        try:
            table = self.verificationWindow.pendingTable
            table.setRowCount(0)

            if not prescriptions:
                return

            table.setRowCount(len(prescriptions))

            for row, prescription in enumerate(prescriptions):
                table.setItem(row, 0, QTableWidgetItem(str(prescription.get('prescription_id', ''))))
                patient_name = f"{prescription.get('patient_first_name', '')} {prescription.get('patient_last_name', '')}"
                table.setItem(row, 1, QTableWidgetItem(patient_name))
                medication = f"{prescription.get('brand_name', '')} ({prescription.get('generic_name', '')})"
                table.setItem(row, 2, QTableWidgetItem(medication))
                table.setItem(row, 3, QTableWidgetItem(str(prescription.get('dosage', ''))))
                table.setItem(row, 4, QTableWidgetItem(str(prescription.get('prescribed_by', ''))))

        except Exception as e:
            print(f"Failed to populate table: {e}")

    def onPrescriptionSelected(self):
        """Handles prescription selection"""
        try:
            table = self.verificationWindow.pendingTable
            row = table.currentRow()

            if row < 0:
                self.selectedPrescriptionId = None
                self.selectedPrescriptionData = None
                return

            self.selectedPrescriptionId = table.item(row, 0).text()
            self.selectedPrescriptionData = VerificationModel.getPrescriptionDetailsForVerification(
                self.selectedPrescriptionId
            )

            if self.selectedPrescriptionData:
                print(f"Selected Prescription ID: {self.selectedPrescriptionId}")
        except Exception as e:
            print(f"Failed to select prescription: {e}")
            self.selectedPrescriptionId = None
            self.selectedPrescriptionData = None

    def verifyPrescription(self):
        """Prepares verification for review"""
        try:
            if not self.selectedPrescriptionId or not self.selectedPrescriptionData:
                Dialogs.showErrorDialog("Validation Error", "Please select a prescription to verify.")
                return

            data = self.verificationWindow.getVerificationData()

            if not data['decision']:
                Dialogs.showErrorDialog("Validation Error", "Please select a verification decision.")
                return

            # Validation for Approve decision
            if data['decision'] == 'Approve':
                if not data['lot_number']:
                    Dialogs.showErrorDialog("Validation Error", "Please enter medication lot number.")
                    return

                if not data['quantity']:
                    Dialogs.showErrorDialog("Validation Error", "Please enter quantity dispensed.")
                    return

                try:
                    quantity = int(data['quantity'])
                    if quantity <= 0:
                        raise ValueError
                except ValueError:
                    Dialogs.showErrorDialog("Validation Error", "Please enter a valid quantity (positive number).")
                    return

            # Validation for Modify/Reject decisions
            if data['decision'] in ['Request Modification', 'Reject'] and not data['reason']:
                Dialogs.showErrorDialog("Validation Error", "Please provide a reason for modification or rejection.")
                return

            self._showVerificationSummary(data)
        except Exception as e:
            print(f"Failed to verify prescription: {e}")
            Dialogs.showErrorDialog("Verification Error", f"Failed: {str(e)}")

    def _submitVerification(self, data):
        """Submits the verification to database"""
        try:
            success = VerificationModel.verifyPrescription(
                prescription_id=self.selectedPrescriptionId,
                pharmacist_id=self.pharmacistId,
                decision=data['decision'],
                lot_number=data['lot_number'] if data['decision'] == 'Approve' else None,
                quantity=int(data['quantity']) if data['decision'] == 'Approve' and data['quantity'] else None,
                expiry_date=data['expiry_date'] if data['decision'] == 'Approve' else None,
                reason=data['reason'] if data['reason'] else None
            )

            if success:
                self._createNotificationRecord(data['decision'])
                print(f"✓ Prescription {self.selectedPrescriptionId} verified successfully!")
                Dialogs.showSuccessDialog("Success", "Prescription verified successfully!")
                self.verificationWindow.clearForm()
                self.loadPendingPrescriptions()
            else:
                Dialogs.showErrorDialog("Verification Error", "Failed to submit verification.")
        except Exception as e:
            print(f"Failed to submit verification: {e}")
            Dialogs.showErrorDialog("Verification Error", f"Failed: {str(e)}")

    def _createNotificationRecord(self, decision):
        """Creates notification for the doctor"""
        try:
            doctor_id = self.selectedPrescriptionData.get('doctor_id')
            if not doctor_id:
                return

            patient_name = f"{self.selectedPrescriptionData.get('patient_first_name', '')} {self.selectedPrescriptionData.get('patient_last_name', '')}"
            medication = f"{self.selectedPrescriptionData.get('brand_name', '')} ({self.selectedPrescriptionData.get('generic_name', '')})"

            decision_map = {
                "Approve": ("Approved", "Info"),
                "Request Modification": ("Modification Requested", "Attention"),
                "Reject": ("Rejected", "Urgent")
            }

            status_text, notification_type = decision_map.get(decision, ("Updated", "Info"))

            title = f"Prescription {status_text}"
            message = f"Prescription for {patient_name} - {medication} has been {status_text.lower()} by {self.userInfo}"

            VerificationModel.createNotification(
                user_id=doctor_id,
                related_table='prescription_verification',
                related_id=self.selectedPrescriptionId,
                title=title,
                message=message,
                notification_type=notification_type
            )

            print(f"✓ Notification created for doctor")
        except Exception as e:
            print(f"Failed to create notification: {e}")

    def _showVerificationSummary(self, data):
        """Displays the verification summary popup"""
        try:
            popup = VerificationSummaryPopup("Verification Summary")

            patient_name = f"{self.selectedPrescriptionData.get('patient_first_name', '')} {self.selectedPrescriptionData.get('patient_last_name', '')}"
            medication_name = f"{self.selectedPrescriptionData.get('brand_name', '')} ({self.selectedPrescriptionData.get('generic_name', '')})"
            prescribed_by = self.selectedPrescriptionData.get('prescribed_by', 'Unknown')

            # Display N/A for batch fields if decision is not Approve
            lot_number = data['lot_number'] if data['decision'] == 'Approve' else 'N/A'
            quantity = f"{data['quantity']} units" if data['decision'] == 'Approve' and data['quantity'] else 'N/A'
            expiry_date = data['expiry_date'] if data['decision'] == 'Approve' else 'N/A'

            popup.setSummaryData(
                prescription_id=self.selectedPrescriptionId,
                patient_name=patient_name,
                medication_name=medication_name,
                prescribed_by=prescribed_by,
                lot_number=lot_number,
                quantity=quantity,
                expiry_date=expiry_date,
                decision=data['decision'],
                reason=data['reason'] or "N/A"
            )

            popup.submitButton.clicked.connect(lambda: (self._submitVerification(data), popup.close()))
            popup.show()
        except Exception as e:
            print(f"Failed to show summary: {e}")

    def navigateToDashboard(self):
        """Navigate to Pharmacist Dashboard"""
        try:
            if self.verificationWindow:
                self.verificationWindow.close()
            from Controller.Pharmacist.PharmacistDashboardController import PharmacistDashboardController
            PharmacistDashboardController().openDashboard()
        except Exception as e:
            print(f"Failed to navigate: {e}")

    def navigateToNotifications(self):
        """Navigate to Notifications"""
        try:
            if self.verificationWindow:
                self.verificationWindow.close()
            from Controller.Pharmacist.PharmacistNotificationsController import PharmacistNotificationsController
            PharmacistNotificationsController().openNotificationsWindow()
        except Exception as e:
            print(f"Failed to navigate: {e}")

    def logout(self):
        """Logout"""
        try:
            SessionManager.clear()
            if self.verificationWindow:
                self.verificationWindow.close()
            from Controller.Login.LoginController import LoginController
            from Model.Authentication.LoginModel import LoginModel
            from View.LoginGUI import Login
            loginModel = LoginModel()
            loginView = Login()
            self.loginController = LoginController(loginModel, loginView)
            loginView.show()
        except Exception as e:
            print(f"Failed to logout: {e}")