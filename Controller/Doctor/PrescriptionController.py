from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import QDate
from Model.Transactions.PrescriptionModel import PrescriptionModel
from Model.Tables.DoctorTables import DoctorTables
from Model.SessionManager import SessionManager
from View.DoctorGUI.PrescriptionWindow import PrescriptionWindow, PrescriptionSummaryPopup
from View.GeneralPopups.Dialogs import Dialogs

class PrescriptionController:
    """
    Controller for Prescription Window
    """

    def __init__(self):
        self.loginController = None
        self._loadUserData()

        # Selected Data Storage
        self.selectedPatientId = None
        self.selectedPatientName = None
        self.selectedMedicineId = None
        self.selectedMedicineName = None
        self.selectedPrescriptionId = None

        # Window Reference
        self.prescriptionWindow = None

    def _loadUserData(self):
        """Load user information from session"""
        self.user = SessionManager.getUser() or {}
        self.userInfo = f"{self.user.get('first_name', 'Unknown')} {self.user.get('last_name', '')}"
        self.role = self.user.get("role", "Doctor")
        self.doctorId = self.user.get("user_id")

    def openPrescriptionWindow(self):
        """Opens the Prescription window"""
        try:
            self.prescriptionWindow = PrescriptionWindow(
                userInfo=self.userInfo or "Unknown",
                role=self.role or "Doctor"
            )
            self._connectSignals()
            self.prescriptionWindow.show()
        except Exception as e:
            print(f"Failed to open PrescriptionWindow: {e}")
            Dialogs.showErrorDialog("Window Error", f"Failed to open: {str(e)}")

    def _connectSignals(self):
        """Connects all UI signals"""
        try:
            # === NEW PRESCRIPTION VIEW ===
            w = self.prescriptionWindow

            # Patient search
            w.newPatientSearchButton.clicked.connect(self.searchPatients)
            w.newPatientSearch.returnPressed.connect(self.searchPatients)
            w.newPatientTable.itemSelectionChanged.connect(self.onPatientSelected)

            # Medication search
            w.newMedicationSearchButton.clicked.connect(self.searchMedications)
            w.newMedicationSearch.returnPressed.connect(self.searchMedications)
            w.newMedicationTable.itemSelectionChanged.connect(self.onMedicationSelected)

            # Confirm button
            w.newConfirmButton.clicked.connect(self.createNewPrescription)

            # === EDIT PRESCRIPTION VIEW ===
            # Prescription search
            w.editPrescriptionSearchButton.clicked.connect(self.searchPrescriptions)
            w.editPrescriptionSearch.returnPressed.connect(self.searchPrescriptions)
            w.editPrescriptionTable.itemSelectionChanged.connect(self.onPrescriptionSelected)

            # Confirm button
            w.editConfirmButton.clicked.connect(self.updatePrescription)

            # === NAVIGATION ===
            w.dashboardOption.mousePressEvent = lambda er: self.navigateToDashboard()
            w.notificationsOption.mousePressEvent = lambda er: self.navigateToNotifications()
            w.logoutOption.mousePressEvent = lambda er: self.logout()

        except Exception as e:
            print(f"Failed to connect signals: {e}")

    # === PATIENT SEARCH ===

    def searchPatients(self):
        """Searches for patients"""
        try:
            query = self.prescriptionWindow.newPatientSearch.text().strip()

            if query:
                patients = DoctorTables.searchPatientsByDoctor(query) or []
            else:
                patients = DoctorTables.getPatientsByDoctor() or []

            if not isinstance(patients, list):
                patients = []

            self._populatePatientTable(patients)
            print(f"✓ Patient search: {len(patients)} results")
        except Exception as e:
            print(f"Patient search failed: {e}")
            Dialogs.showErrorDialog("Search Error", f"Failed to search patients: {str(e)}")

    def _populatePatientTable(self, patients):
        """Populates the patient table"""
        try:
            table = self.prescriptionWindow.newPatientTable
            table.setRowCount(0)

            if not patients:
                return

            table.setRowCount(len(patients))

            for row, patient in enumerate(patients):
                items = [
                    str(patient.get('patient_id', '')),
                    str(patient.get('patient_first_name', '')),
                    str(patient.get('patient_last_name', '')),
                    str(patient.get('date_of_birth', '')),
                    str(patient.get('sex', ''))
                ]

                for col, value in enumerate(items):
                    item = QTableWidgetItem(value)
                    table.setItem(row, col, item)
        except Exception as e:
            print(f"Failed to populate patient table: {e}")

    def onPatientSelected(self):
        """Handles patient selection"""
        try:
            table = self.prescriptionWindow.newPatientTable
            row = table.currentRow()

            if row < 0:
                self.selectedPatientId = None
                self.selectedPatientName = None
                return

            self.selectedPatientId = table.item(row, 0).text()
            first_name = table.item(row, 1).text()
            last_name = table.item(row, 2).text()
            self.selectedPatientName = f"{first_name} {last_name}"

            print(f"Selected Patient: {self.selectedPatientName} (ID: {self.selectedPatientId})")
        except Exception as e:
            print(f"Failed to select patient: {e}")

    # === MEDICATION SEARCH ===

    def searchMedications(self):
        """Searches for medications"""
        try:
            query = self.prescriptionWindow.newMedicationSearch.text().strip()

            if query:
                medications = DoctorTables.searchMedicines(query) or []
            else:
                medications = DoctorTables.getAllMedicines() or []

            if not isinstance(medications, list):
                medications = []

            self._populateMedicationTable(medications)
            print(f"✓ Medication search: {len(medications)} results")
        except Exception as e:
            print(f"Medication search failed: {e}")
            Dialogs.showErrorDialog("Search Error", f"Failed to search medications: {str(e)}")

    def _populateMedicationTable(self, medications):
        """Populates the medication table"""
        try:
            table = self.prescriptionWindow.newMedicationTable
            table.setRowCount(0)

            if not medications:
                return

            table.setRowCount(len(medications))

            for row, med in enumerate(medications):
                controlled = "Yes" if med.get('is_controlled', False) else "No"
                items = [
                    str(med.get('medicine_id', '')),
                    str(med.get('brand_name', '')),
                    str(med.get('generic_name', '')),
                    str(med.get('formulation', '')),
                    str(med.get('strength', '')),
                    controlled
                ]

                for col, value in enumerate(items):
                    item = QTableWidgetItem(value)
                    table.setItem(row, col, item)
        except Exception as e:
            print(f"Failed to populate medication table: {e}")

    def onMedicationSelected(self):
        """Handles medication selection"""
        try:
            table = self.prescriptionWindow.newMedicationTable
            row = table.currentRow()

            if row < 0:
                self.selectedMedicineId = None
                self.selectedMedicineName = None
                return

            self.selectedMedicineId = table.item(row, 0).text()
            brand_name = table.item(row, 1).text()
            generic_name = table.item(row, 2).text()
            self.selectedMedicineName = f"{brand_name} ({generic_name})"

            print(f"Selected Medication: {self.selectedMedicineName} (ID: {self.selectedMedicineId})")
        except Exception as e:
            print(f"Failed to select medication: {e}")

    # === CREATE NEW PRESCRIPTION ===

    def createNewPrescription(self):
        """Prepares a new prescription for review"""
        try:
            if not self.selectedPatientId:
                Dialogs.showErrorDialog("Validation Error", "Please select a patient.")
                return

            if not self.selectedMedicineId:
                Dialogs.showErrorDialog("Validation Error", "Please select a medication.")
                return

            data = self.prescriptionWindow.getNewPrescriptionData()

            if not data['amount'].strip():
                Dialogs.showErrorDialog("Validation Error", "Please enter the dosage amount.")
                return

            dosage = f"{data['amount']} {data['unit']}"

            self._showPrescriptionSummary(
                title="New Prescription Summary",
                patient_name=self.selectedPatientName,
                medication_name=self.selectedMedicineName,
                dosage=dosage,
                frequency=data['frequency'],
                duration=f"{data['start_date']} to {data['end_date']}",
                instructions=data['instructions'] or "None",
                onSubmit=lambda: self._createPrescriptionFromData(data)
            )
        except Exception as e:
            print(f"Failed to prepare prescription: {e}")
            Dialogs.showErrorDialog("Error", f"Failed to prepare prescription: {str(e)}")

    def _createPrescriptionFromData(self, data):
        """Creates a new prescription in the database"""
        try:
            prescription_id = PrescriptionModel.createPrescription(
                patient_id=self.selectedPatientId,
                medicine_id=self.selectedMedicineId,
                dosage=f"{data['amount']} {data['unit']}",
                duration_start=data['start_date'],
                duration_end=data['end_date'],
                frequency=data['frequency'],
                special_instructions=data['instructions'] if data['instructions'].strip() else None
            )

            if prescription_id:
                # Create notifications for pharmacists and assigned nurse
                self._createNotificationsForPrescription(prescription_id)

                print(f"✓ Prescription created successfully! ID: {prescription_id}")
                Dialogs.showSuccessDialog("Success", "Prescription created successfully!")

                self.prescriptionWindow.clearNewPrescriptionForm()
                self.selectedPatientId = None
                self.selectedPatientName = None
                self.selectedMedicineId = None
                self.selectedMedicineName = None
            else:
                Dialogs.showErrorDialog("Creation Error", "Failed to create prescription.")
        except Exception as e:
            print(f"Failed to create prescription: {e}")
            Dialogs.showErrorDialog("Creation Error", f"Failed to create prescription: {str(e)}")

    def _createNotificationsForPrescription(self, prescription_id):
        """Creates notifications for pharmacists and assigned nurse"""
        try:
            # Get prescription details for notification message
            prescription_details = PrescriptionModel.getPrescriptionNotificationDetails(prescription_id)

            if not prescription_details:
                print("Warning: Could not fetch prescription details for notification")
                return

            patient_name = f"{prescription_details.get('patient_first_name', '')} {prescription_details.get('patient_last_name', '')}"
            medication = f"{prescription_details.get('brand_name', '')} ({prescription_details.get('generic_name', '')})"
            nurse_id = prescription_details.get('nurse_id')

            # Notification for Pharmacists (all active pharmacists)
            pharmacist_ids = PrescriptionModel.getAllPharmacistIds()

            for pharmacist_id in pharmacist_ids:
                PrescriptionModel.createNotification(
                    user_id=pharmacist_id,
                    related_table='prescriptions',
                    related_id=prescription_id,
                    title='New Prescription - Verification Required',
                    message=f'New prescription for {patient_name} - {medication} requires verification by {self.userInfo}',
                    notification_type='Attention'
                )

            print(f"✓ Notifications sent to {len(pharmacist_ids)} pharmacist(s)")

            # Notification for Assigned Nurse (if patient has assigned nurse)
            if nurse_id:
                PrescriptionModel.createNotification(
                    user_id=nurse_id,
                    related_table='prescriptions',
                    related_id=prescription_id,
                    title='New Prescription - Patient Update',
                    message=f'New prescription created for your patient {patient_name} - {medication} by Dr. {self.userInfo}',
                    notification_type='Info'
                )
                print(f"✓ Notification sent to assigned nurse (ID: {nurse_id})")
            else:
                print("Note: No nurse assigned to this patient")

        except Exception as e:
            print(f"Failed to create notifications: {e}")

    # === PRESCRIPTION SEARCH (FOR EDITING) ===

    def searchPrescriptions(self):
        """Searches for prescriptions"""
        try:
            query = self.prescriptionWindow.editPrescriptionSearch.text().strip()

            if not self.doctorId:
                Dialogs.showErrorDialog("Error", "Doctor ID not found.")
                return

            if query:
                prescriptions = DoctorTables.searchPrescriptionsByDoctor(self.doctorId, query) or []
            else:
                prescriptions = DoctorTables.getAllPrescriptionsByDoctor(self.doctorId) or []

            if not isinstance(prescriptions, list):
                prescriptions = []

            self._populatePrescriptionTable(prescriptions)
            print(f"✓ Prescription search: {len(prescriptions)} results")
        except Exception as e:
            print(f"Prescription search failed: {e}")
            Dialogs.showErrorDialog("Search Error", f"Failed to search prescriptions: {str(e)}")

    def _populatePrescriptionTable(self, prescriptions):
        """Populates the prescription table"""
        try:
            table = self.prescriptionWindow.editPrescriptionTable
            table.setRowCount(0)

            if not prescriptions:
                return

            table.setRowCount(len(prescriptions))

            for row, prescription in enumerate(prescriptions):
                patient_name = f"{prescription.get('patient_first_name', '')} {prescription.get('patient_last_name', '')}"
                medication = f"{prescription.get('brand_name', '')} ({prescription.get('generic_name', '')})"

                items = [
                    str(prescription.get('prescription_id', '')),
                    patient_name,
                    medication,
                    str(prescription.get('dosage', '')),
                    str(prescription.get('status', ''))
                ]

                for col, value in enumerate(items):
                    item = QTableWidgetItem(value)
                    table.setItem(row, col, item)
        except Exception as e:
            print(f"Failed to populate prescription table: {e}")

    def onPrescriptionSelected(self):
        """Handles prescription selection and loads data into form"""
        try:
            table = self.prescriptionWindow.editPrescriptionTable
            row = table.currentRow()

            if row < 0:
                self.selectedPrescriptionId = None
                return

            self.selectedPrescriptionId = table.item(row, 0).text()
            self._loadPrescriptionDetails(self.selectedPrescriptionId)

            print(f"Selected Prescription ID: {self.selectedPrescriptionId}")
        except Exception as e:
            print(f"Failed to select prescription: {e}")

    def _loadPrescriptionDetails(self, prescription_id):
        """Loads prescription details into the edit form"""
        try:
            prescription = DoctorTables.getPrescriptionById(prescription_id)

            if not prescription:
                Dialogs.showErrorDialog("Error", "Prescription not found.")
                return

            # Parse dosage (e.g., "500 mg" -> amount: "500", unit: "mg")
            dosage_parts = prescription.get('dosage', '').split()
            amount = dosage_parts[0] if len(dosage_parts) > 0 else ""
            unit = dosage_parts[1] if len(dosage_parts) > 1 else "mg"

            # Populate form fields
            self.prescriptionWindow.editAmountInput.setText(amount)

            unit_index = self.prescriptionWindow.editUnitDropdown.findText(unit)
            if unit_index >= 0:
                self.prescriptionWindow.editUnitDropdown.setCurrentIndex(unit_index)

            frequency = prescription.get('frequency', '')
            freq_index = self.prescriptionWindow.editFrequencyDropdown.findText(frequency)
            if freq_index >= 0:
                self.prescriptionWindow.editFrequencyDropdown.setCurrentIndex(freq_index)

            start_date = prescription.get('duration_start')
            if start_date:
                self.prescriptionWindow.editStartDateInput.setDate(QDate.fromString(str(start_date), 'yyyy-MM-dd'))

            end_date = prescription.get('duration_end')
            if end_date:
                self.prescriptionWindow.editEndDateInput.setDate(QDate.fromString(str(end_date), 'yyyy-MM-dd'))

            instructions = prescription.get('special_instructions', '')
            self.prescriptionWindow.editInstructionsText.setPlainText(instructions or "")

            print(f"✓ Loaded prescription details for ID: {prescription_id}")
        except Exception as e:
            print(f"Failed to load prescription details: {e}")
            Dialogs.showErrorDialog("Load Error", f"Failed to load: {str(e)}")

    # === UPDATE PRESCRIPTION ===

    def updatePrescription(self):
        """Prepares an existing prescription for review"""
        try:
            if not self.selectedPrescriptionId:
                Dialogs.showErrorDialog("Validation Error", "Please select a prescription to edit.")
                return

            data = self.prescriptionWindow.getEditPrescriptionData()

            if not data['amount'].strip():
                Dialogs.showErrorDialog("Validation Error", "Please enter the dosage amount.")
                return

            dosage = f"{data['amount']} {data['unit']}"

            table = self.prescriptionWindow.editPrescriptionTable
            row = table.currentRow()
            patient_name = table.item(row, 1).text() if row >= 0 else "Unknown Patient"
            medication_name = table.item(row, 2).text() if row >= 0 else "Unknown Medication"

            self._showPrescriptionSummary(
                title="Prescription Edit Summary",
                patient_name=patient_name,
                medication_name=medication_name,
                dosage=dosage,
                frequency=data['frequency'],
                duration=f"{data['start_date']} to {data['end_date']}",
                instructions=data['instructions'] or "None",
                onSubmit=lambda: self._updatePrescriptionFromData(data)
            )
        except Exception as e:
            print(f"Failed to prepare prescription update: {e}")
            Dialogs.showErrorDialog("Error", f"Failed to prepare update: {str(e)}")

    def _updatePrescriptionFromData(self, data):
        """Updates the existing prescription in the database"""
        try:
            success = PrescriptionModel.updatePrescription(
                prescription_id=self.selectedPrescriptionId,
                dosage=f"{data['amount']} {data['unit']}",
                duration_start=data['start_date'],
                duration_end=data['end_date'],
                frequency=data['frequency'],
                special_instructions=data['instructions'] if data['instructions'].strip() else None
            )

            if success:
                print(f"✓ Prescription updated successfully! ID: {self.selectedPrescriptionId}")
                Dialogs.showSuccessDialog("Success", "Prescription updated successfully!")

                self.searchPrescriptions()
                self.prescriptionWindow.clearEditPrescriptionForm()
                self.selectedPrescriptionId = None
            else:
                Dialogs.showErrorDialog("Update Error", "No changes were made to the prescription.")
        except Exception as e:
            print(f"Failed to update prescription: {e}")
            Dialogs.showErrorDialog("Update Error", f"Failed to update: {str(e)}")

    # === SUMMARY POPUP ===

    def _showPrescriptionSummary(self, title, patient_name, medication_name,
                                 dosage, frequency, duration, instructions, onSubmit=None):
        """Displays the prescription summary popup"""
        try:
            self.popup = PrescriptionSummaryPopup(title)
            self.popup.setSummaryData(
                patient_name=patient_name,
                medication_name=medication_name,
                dosage=dosage,
                frequency=frequency,
                duration=duration,
                instructions=instructions
            )

            if onSubmit:
                self.popup.submitButton.clicked.connect(lambda: (onSubmit(), self.popup.close()))
            else:
                self.popup.submitButton.clicked.connect(self.popup.close)

            self.popup.show()
        except Exception as e:
            print(f"Failed to show summary popup: {e}")

    # === NAVIGATION ===

    def navigateToDashboard(self):
        """Navigate to Dashboard"""
        try:
            if self.prescriptionWindow:
                self.prescriptionWindow.close()
            from Controller.Doctor.DoctorDashboardController import DoctorDashboardController
            DoctorDashboardController().openDashboard()
        except Exception as e:
            print(f"Failed to navigate: {e}")

    def navigateToNotifications(self):
        """Navigate to Notifications"""
        try:
            if self.prescriptionWindow:
                self.prescriptionWindow.close()
            from Controller.Doctor.DoctorNotificationsController import DoctorNotificationsController
            DoctorNotificationsController().openNotificationsWindow()
        except Exception as e:
            print(f"Failed to navigate: {e}")

    def logout(self):
        """Logout"""
        try:
            SessionManager.clear()
            if self.prescriptionWindow:
                self.prescriptionWindow.close()
            from Controller.Login.LoginController import LoginController
            from Model.Authentication.LoginModel import LoginModel
            from View.LoginGUI import Login
            loginModel = LoginModel()
            loginView = Login()
            self.loginController = LoginController(loginModel, loginView)
            loginView.show()
        except Exception as e:
            print(f"Failed to navigate: {e}")