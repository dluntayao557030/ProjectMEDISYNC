from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QWidget, QStackedWidget, QLabel, QFrame
from Utilities.Designers import Designer

class PrescriptionWindow(QWidget):
    """
    Prescription Window for creating and editing prescriptions
    """

    def __init__(self, userInfo, role="Doctor"):
        super().__init__()
        self.setFixedSize(1500, 800)
        self.setWindowTitle("MEDISYNC Prescription Management")
        Designer.setWindowToCenter(self)

        self.userInfo = userInfo
        self.role = role

        Designer.setBackground(self)
        self._createTopBar()

        # Main Content Card
        self.mainCard = Designer.createRoundedCard(self)
        self.mainCard.setGeometry(20, 95, 1460, 680)

        # Stacked Widget for switching between New and Edit views
        self.stackedWidget = QStackedWidget(self.mainCard)
        self.stackedWidget.setGeometry(0, 0, 1460, 680)

        # Create both views
        self.newPrescriptionView = self._createNewPrescriptionView()
        self.editPrescriptionView = self._createEditPrescriptionView()

        # Add views to stacked widget
        self.stackedWidget.addWidget(self.newPrescriptionView)
        self.stackedWidget.addWidget(self.editPrescriptionView)

        # Navigation arrow
        self._createNavigationArrow()

        # Track current view state
        self.isNewPrescription = True

    def _createTopBar(self):
        """Creates the top navigation bar with menu options"""
        self.topCard = Designer.createRoundedCard(self)
        self.topCard.setGeometry(0, -25, 1500, 100)

        logo = Designer.setLogo(self.topCard)
        logo.setGeometry(60, 10, 90, 90)

        self.dashboardOption = Designer.createMenuOption(
            self.topCard, "Dashboard",
            "../ImageResources/Icon8BGRemoved.png", 180
        )
        self.dashboardOption.move(500, 40)

        self.prescriptionOption = Designer.createClickedOption(
            self.topCard, "Prescribe",
            "../ImageResources/Icon5BGRemoved.png", 160
        )
        self.prescriptionOption.move(745, 40)

        self.notificationsOption = Designer.createMenuOption(
            self.topCard, "Notifications",
            "../ImageResources/Icon4BGRemoved.png", 180
        )
        self.notificationsOption.move(950, 40)

        self.logoutOption = Designer.createMenuOption(
            self.topCard, "Logout",
            "../ImageResources/Icon6BGRemoved.png", 150
        )
        self.logoutOption.move(1300, 40)

        profileIcon = Designer.setImage(self.topCard, "../ImageResources/Icon14BGRemoved.png")
        profileIcon.setGeometry(215, 40, 45, 45)

        self.userLabel = Designer.createLabel(self.userInfo or "Unknown User", self.topCard, "#1a1a1a", 700, 13)
        self.userLabel.setGeometry(280, 45, 150, 14)

        self.titleLabel = Designer.createLabel(self.role, self.topCard, "#333333", 400, 12)
        self.titleLabel.setGeometry(280, 65, 150, 15)

    def _createNavigationArrow(self):
        """Creates the navigation arrow for switching views"""
        self.navigationArrow = QLabel(self.mainCard)
        self.navigationArrow.setGeometry(1390, 20, 40, 40)
        self.navigationArrow.setScaledContents(True)
        self.arrowPixmap = QPixmap("../ImageResources/Icon9BGRemoved.png")
        self.navigationArrow.setPixmap(self.arrowPixmap)
        self.navigationArrow.setCursor(Qt.CursorShape.PointingHandCursor)

        def toggleView():
            if self.isNewPrescription:
                self.stackedWidget.setCurrentIndex(1)
                transform = QTransform().scale(-1, 1)
                flippedPixmap = self.arrowPixmap.transformed(transform)
                self.navigationArrow.setPixmap(flippedPixmap)
                self.isNewPrescription = False
            else:
                self.stackedWidget.setCurrentIndex(0)
                self.navigationArrow.setPixmap(self.arrowPixmap)
                self.isNewPrescription = True

        def onArrowPress(event):
            self.navigationArrow.setGeometry(1393, 23, 34, 34)

        def onArrowRelease(event):
            self.navigationArrow.setGeometry(1390, 20, 40, 40)
            toggleView()

        self.navigationArrow.mousePressEvent = onArrowPress
        self.navigationArrow.mouseReleaseEvent = onArrowRelease

    def _createNewPrescriptionView(self):
        """Creates the New Prescription view"""
        view = QWidget()

        titleLabel = Designer.createLabel("New Prescription", view, "#1a1a1a", 700, 28)
        titleLabel.setGeometry(55, 30, 400, 35)
        subtitleLabel = Designer.createLabel("Create new prescriptions.", view, "#333333", 400, 13)
        subtitleLabel.setGeometry(55, 70, 400, 20)

        # === PATIENT SECTION ===
        patientLabel = Designer.createLabel("Patient", view, "#1a1a1a", 700, 18)
        patientLabel.setGeometry(55, 125, 150, 25)
        patientSubLabel = Designer.createLabel("Search and select patient.", view, "#333333", 400, 12)
        patientSubLabel.setGeometry(55, 155, 200, 20)

        self.newPatientSearch = Designer.createInputField(view, "white", "#333333", 400, 14, 15, 2, "#185777")
        self.newPatientSearch.setGeometry(320, 140, 210, 35)
        self.newPatientSearch.setPlaceholderText("  🔍 Search patient")

        self.newPatientSearchButton = Designer.createPrimaryButton("Search", view, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.newPatientSearchButton.setGeometry(545, 140, 115, 35)

        self.newPatientTable = Designer.createStandardTable(["ID", "First Name", "Last Name", "DOB", "Sex"])
        self.newPatientTable.setParent(view)
        self.newPatientTable.setGeometry(55, 185, 605, 160)

        # === MEDICATION SECTION ===
        medicationLabel = Designer.createLabel("Medication Name", view, "#1a1a1a", 700, 18)
        medicationLabel.setGeometry(55, 385, 250, 25)
        medicationSubLabel = Designer.createLabel("Select medication to prescribe.", view, "#333333", 400, 12)
        medicationSubLabel.setGeometry(55, 415, 250, 20)

        self.newMedicationSearch = Designer.createInputField(view, "white", "#333333", 400, 14, 15, 2, "#185777")
        self.newMedicationSearch.setGeometry(320, 400, 210, 35)
        self.newMedicationSearch.setPlaceholderText("  🔍 Search medication")

        self.newMedicationSearchButton = Designer.createPrimaryButton("Search", view, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.newMedicationSearchButton.setGeometry(545, 400, 115, 35)

        self.newMedicationTable = Designer.createStandardTable(
            ["ID", "Brand Name", "Generic Name", "Formulation", "Strength", "Controlled"]
        )
        self.newMedicationTable.setParent(view)
        self.newMedicationTable.setGeometry(55, 450, 605, 165)

        # === DOSAGE SECTION ===
        dosageLabel = Designer.createLabel("Dosage", view, "#1a1a1a", 700, 18)
        dosageLabel.setGeometry(730, 55, 150, 25)
        dosageSubLabel = Designer.createLabel("Adjust medication dosage.", view, "#333333", 400, 12)
        dosageSubLabel.setGeometry(730, 85, 250, 20)

        amountLabel = Designer.createLabel("Amount:", view, "#1a1a1a", 600, 13)
        amountLabel.setGeometry(735, 140, 70, 25)
        self.newAmountInput = Designer.createInputField(view, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.newAmountInput.setGeometry(800, 140, 165, 30)
        self.newAmountInput.setPlaceholderText("e.g., 500")

        common_units = ["mg", "g", "mL", "tablet", "capsule", "drop", "suppository", "patch", "inhaler"]
        unitLabel = Designer.createLabel("Unit:", view, "#1a1a1a", 600, 13)
        unitLabel.setGeometry(993, 140, 50, 25)
        self.newUnitDropdown = Designer.createComboBox(view, radius=10, borderColor="#185777", fontSize=14)
        self.newUnitDropdown.setGeometry(1035, 140, 120, 30)
        self.newUnitDropdown.addItems(common_units)

        # === FREQUENCY AND DURATION SECTION ===
        common_frequencies = [
            "Once a day", "Twice a day", "Three times a day", "Four times a day",
            "Every 6 hours", "Every 8 hours","Every 12 hours"]
        frequencyLabel = Designer.createLabel("Frequency and Duration", view, "#1a1a1a", 700, 18)
        frequencyLabel.setGeometry(730, 200, 300, 25)
        frequencySubLabel = Designer.createLabel("Schedule medicine intake.", view, "#333333", 400, 12)
        frequencySubLabel.setGeometry(730, 230, 250, 20)

        frequencyDropdownLabel = Designer.createLabel("Frequency:", view, "#1a1a1a", 600, 13)
        frequencyDropdownLabel.setGeometry(738, 260, 100, 25)
        self.newFrequencyDropdown = Designer.createComboBox(view, radius=10, borderColor="#185777", fontSize=14)
        self.newFrequencyDropdown.setGeometry(820, 260, 200, 30)
        self.newFrequencyDropdown.addItems(common_frequencies)

        startLabel = Designer.createLabel("Start:", view, "#1a1a1a", 600, 13)
        startLabel.setGeometry(738, 300, 50, 25)
        self.newStartDateInput = Designer.createDateEdit(view, radius=10, borderColor="#185777", fontSize=14)
        self.newStartDateInput.setGeometry(782, 300, 170, 30)

        endLabel = Designer.createLabel("End:", view, "#1a1a1a", 600, 13)
        endLabel.setGeometry(970, 300, 50, 25)
        self.newEndDateInput = Designer.createDateEdit(view, radius=10, borderColor="#185777", fontSize=14)
        self.newEndDateInput.setGeometry(1009, 300, 170, 30)

        # === SPECIAL INSTRUCTIONS SECTION ===
        instructionsLabel = Designer.createLabel("Special Instructions (Optional)", view, "#1a1a1a", 700, 18)
        instructionsLabel.setGeometry(730, 360, 400, 25)
        instructionsSubLabel = Designer.createLabel("Additional instructions for administration.", view, "#333333", 400,
                                                    12)
        instructionsSubLabel.setGeometry(730, 390, 350, 20)

        instructionsCard, self.newInstructionsText = Designer.createPlainTextArea(
            parent=view,
            backgroundColor="white",
            fontColor="#333333",
            fontSize=14,
            borderRadius=10,
            outlineWeight=2,
            outlineColor="#185777"
        )
        instructionsCard.setGeometry(738, 430, 570, 140)
        self.newInstructionsText.setGeometry(748, 440, 540, 120)
        self.newInstructionsText.setPlaceholderText("Enter special instructions here...")

        self.newConfirmButton = Designer.createPrimaryButton("Confirm", view, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.newConfirmButton.setGeometry(1270, 620, 130, 35)

        return view

    def _createEditPrescriptionView(self):
        """Creates the Edit Prescription view"""
        view = QWidget()

        titleLabel = Designer.createLabel("Edit Prescription", view, "#1a1a1a", 700, 28)
        titleLabel.setGeometry(55, 30, 400, 35)
        subtitleLabel = Designer.createLabel("Update and edit existing prescriptions.", view, "#333333", 400, 13)
        subtitleLabel.setGeometry(55, 70, 400, 20)

        # === MY PRESCRIPTIONS SECTION ===
        prescriptionsLabel = Designer.createLabel("My Prescriptions", view, "#1a1a1a", 700, 18)
        prescriptionsLabel.setGeometry(55, 125, 250, 25)
        prescriptionsSubLabel = Designer.createLabel("Select prescription to edit.", view, "#333333", 400, 12)
        prescriptionsSubLabel.setGeometry(55, 155, 250, 20)

        self.editPrescriptionSearch = Designer.createInputField(view, "white", "#333333", 400, 14, 15, 2, "#185777")
        self.editPrescriptionSearch.setGeometry(320, 140, 210, 35)
        self.editPrescriptionSearch.setPlaceholderText("  🔍 Search prescriptions")

        self.editPrescriptionSearchButton = Designer.createPrimaryButton("Search", view, "#0cc0df", "#1a1a1a", 700, 12,
                                                                         15)
        self.editPrescriptionSearchButton.setGeometry(545, 140, 115, 35)

        self.editPrescriptionTable = Designer.createStandardTable(
            ["Prescription ID", "Patient", "Medication", "Dosage", "Status"]
        )
        self.editPrescriptionTable.setParent(view)
        self.editPrescriptionTable.setGeometry(55, 185, 605, 430)

        # === DOSAGE SECTION ===
        dosageLabel = Designer.createLabel("Dosage", view, "#1a1a1a", 700, 18)
        dosageLabel.setGeometry(730, 55, 150, 25)
        dosageSubLabel = Designer.createLabel("Adjust new medication dosage.", view, "#333333", 400, 12)
        dosageSubLabel.setGeometry(730, 85, 250, 20)

        amountLabel = Designer.createLabel("Amount:", view, "#1a1a1a", 600, 13)
        amountLabel.setGeometry(735, 140, 70, 25)
        self.editAmountInput = Designer.createInputField(view, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.editAmountInput.setGeometry(800, 140, 165, 30)
        self.editAmountInput.setPlaceholderText("e.g., 500")

        common_units = ["mg", "g", "mL", "tablet", "capsule", "drop", "suppository", "patch", "inhaler"]
        unitLabel = Designer.createLabel("Unit:", view, "#1a1a1a", 600, 13)
        unitLabel.setGeometry(993, 140, 50, 25)
        self.editUnitDropdown = Designer.createComboBox(view, radius=10, borderColor="#185777", fontSize=14)
        self.editUnitDropdown.setGeometry(1035, 140, 120, 30)
        self.editUnitDropdown.addItems(common_units)

        # === FREQUENCY AND DURATION SECTION ===
        common_frequencies = [
            "Once a day", "Twice a day", "Three times a day", "Four times a day",
            "Every 6 hours", "Every 8 hours", "Before bedtime", "As needed"
        ]
        frequencyLabel = Designer.createLabel("Frequency and Duration", view, "#1a1a1a", 700, 18)
        frequencyLabel.setGeometry(730, 200, 300, 25)
        frequencySubLabel = Designer.createLabel("Schedule medicine intake.", view, "#333333", 400, 12)
        frequencySubLabel.setGeometry(730, 230, 250, 20)

        frequencyDropdownLabel = Designer.createLabel("Frequency:", view, "#1a1a1a", 600, 13)
        frequencyDropdownLabel.setGeometry(738, 260, 100, 25)
        self.editFrequencyDropdown = Designer.createComboBox(view, radius=10, borderColor="#185777", fontSize=14)
        self.editFrequencyDropdown.setGeometry(820, 260, 200, 30)
        self.editFrequencyDropdown.addItems(common_frequencies)

        startLabel = Designer.createLabel("Start:", view, "#1a1a1a", 600, 13)
        startLabel.setGeometry(738, 300, 50, 25)
        self.editStartDateInput = Designer.createDateEdit(view, radius=10, borderColor="#185777", fontSize=14)
        self.editStartDateInput.setGeometry(782, 300, 170, 30)

        endLabel = Designer.createLabel("End:", view, "#1a1a1a", 600, 13)
        endLabel.setGeometry(970, 300, 50, 25)
        self.editEndDateInput = Designer.createDateEdit(view, radius=10, borderColor="#185777", fontSize=14)
        self.editEndDateInput.setGeometry(1009, 300, 170, 30)

        # === SPECIAL INSTRUCTIONS SECTION ===
        instructionsLabel = Designer.createLabel("Special Instructions (Optional)", view, "#1a1a1a", 700, 18)
        instructionsLabel.setGeometry(730, 360, 400, 25)
        instructionsSubLabel = Designer.createLabel("Add new instructions for administration.", view, "#333333", 400,
                                                    12)
        instructionsSubLabel.setGeometry(730, 390, 350, 20)

        instructionsCard, self.editInstructionsText = Designer.createPlainTextArea(
            parent=view,
            backgroundColor="white",
            fontColor="#333333",
            fontSize=14,
            borderRadius=10,
            outlineWeight=2,
            outlineColor="#185777"
        )
        instructionsCard.setGeometry(738, 430, 570, 140)
        self.editInstructionsText.setGeometry(748, 440, 540, 120)
        self.editInstructionsText.setPlaceholderText("Enter special instructions here...")

        self.editConfirmButton = Designer.createPrimaryButton("Confirm", view, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.editConfirmButton.setGeometry(1270, 620, 130, 35)

        return view

    def getNewPrescriptionData(self):
        """Returns all data from the New Prescription form"""
        return {
            'amount': self.newAmountInput.text(),
            'unit': self.newUnitDropdown.currentText(),
            'frequency': self.newFrequencyDropdown.currentText(),
            'start_date': self.newStartDateInput.date().toString('yyyy-MM-dd'),
            'end_date': self.newEndDateInput.date().toString('yyyy-MM-dd'),
            'instructions': self.newInstructionsText.toPlainText()
        }

    def getEditPrescriptionData(self):
        """Returns all data from the Edit Prescription form"""
        return {
            'amount': self.editAmountInput.text(),
            'unit': self.editUnitDropdown.currentText(),
            'frequency': self.editFrequencyDropdown.currentText(),
            'start_date': self.editStartDateInput.date().toString('yyyy-MM-dd'),
            'end_date': self.editEndDateInput.date().toString('yyyy-MM-dd'),
            'instructions': self.editInstructionsText.toPlainText()
        }

    def clearNewPrescriptionForm(self):
        """Clears all fields in the New Prescription form"""
        self.newPatientSearch.clear()
        self.newMedicationSearch.clear()
        self.newAmountInput.clear()
        self.newUnitDropdown.setCurrentIndex(0)
        self.newFrequencyDropdown.setCurrentIndex(0)
        self.newInstructionsText.clear()
        self.newPatientTable.setRowCount(0)
        self.newMedicationTable.setRowCount(0)

    def clearEditPrescriptionForm(self):
        """Clears all fields in the Edit Prescription form"""
        self.editPrescriptionSearch.clear()
        self.editAmountInput.clear()
        self.editUnitDropdown.setCurrentIndex(0)
        self.editFrequencyDropdown.setCurrentIndex(0)
        self.editInstructionsText.clear()
        self.editPrescriptionTable.setRowCount(0)


class PrescriptionSummaryPopup(QWidget):
    """
    Popup for displaying prescription summary
    """

    def __init__(self, title="Prescription Summary"):
        super().__init__()
        self.setFixedSize(400, 600)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        Designer.setWindowToCenter(self)

        self.setStyleSheet("background-color: #cef2f9;")

        mainFrame = QFrame(self)
        mainFrame.setGeometry(10, 10, 380, 580)
        mainFrame.setStyleSheet("QFrame {background-color: #cef2f9; border-radius: 30px;}")

        logo = Designer.setLogo(mainFrame)
        logo.setGeometry(145, 20, 90, 90)

        self.titleLabel = Designer.createLabel(title, mainFrame, "#1a1a1a", 700, 18)
        self.titleLabel.setGeometry(70, 120, 250, 25)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        yPos = 165
        spacing = 30

        Designer.createLabel("Patient Name:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 120, 20)
        self.patientNameValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.patientNameValue.setGeometry(165, yPos, 180, 20)
        yPos += spacing

        Designer.createLabel("Medication Name:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 140, 20)
        self.medicationNameValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.medicationNameValue.setGeometry(185, yPos, 160, 20)
        yPos += spacing

        Designer.createLabel("Dosage:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 80, 20)
        self.dosageValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.dosageValue.setGeometry(105, yPos, 240, 20)
        yPos += spacing

        Designer.createLabel("Frequency:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 180, 20)
        self.frequencyValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.frequencyValue.setGeometry(115, yPos, 230, 20)
        yPos += spacing

        Designer.createLabel("Duration:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 180, 20)
        self.durationValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.durationValue.setGeometry(115, yPos, 230, 20)
        yPos += 40

        Designer.createLabel("Special Instructions:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 160, 20)
        yPos += 30

        instructionsCard, self.instructionsText = Designer.createPlainTextArea(
            parent=mainFrame,
            backgroundColor="white",
            fontColor="#333333",
            fontSize=13,
            borderRadius=15,
            outlineWeight=2,
            outlineColor="#185777"
        )
        instructionsCard.setGeometry(35, yPos, 310, 120)
        self.instructionsText.setGeometry(45, yPos + 10, 284, 100)
        self.instructionsText.setReadOnly(True)

        self.submitButton = Designer.createPrimaryButton("Submit", mainFrame, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.submitButton.setGeometry(80, 540, 100, 30)

        self.closeButton = Designer.createSecondaryButton("Close", mainFrame, "#e7f9fc", "#1a1a1a", 700, 12, 15, 2,
                                                          "#185777")
        self.closeButton.setGeometry(200, 540, 100, 30)
        self.closeButton.clicked.connect(self.close)

    def setSummaryData(self, patient_name, medication_name, dosage, frequency, duration, instructions):
        """Sets all summary data"""
        self.patientNameValue.setText(patient_name)
        self.medicationNameValue.setText(medication_name)
        self.dosageValue.setText(dosage)
        self.frequencyValue.setText(frequency)
        self.durationValue.setText(duration)
        self.instructionsText.setPlainText(instructions)