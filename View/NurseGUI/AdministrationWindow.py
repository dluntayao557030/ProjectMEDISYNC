from PyQt6.QtCore import Qt, QTime
from PyQt6.QtWidgets import QWidget, QStackedWidget, QFrame, QButtonGroup, QRadioButton, QTimeEdit, QHeaderView
from Utilities.Designers import Designer

class AdministrationWindow(QWidget):
    """
    Nurse Medication Administration Window
    """

    def __init__(self, userInfo, role):
        super().__init__()
        self.setFixedSize(1500, 800)
        self.setWindowTitle("MEDISYNC Administer Medication")
        Designer.setWindowToCenter(self)

        self.userInfo = userInfo
        self.role = role

        # Store selected data
        self.selectedPatientId = None
        self.selectedPatientData = None
        self.selectedPrescriptionId = None
        self.selectedPrescriptionData = None

        Designer.setBackground(self)
        self._createTopBar()

        # Stacked Widget for switching views
        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setGeometry(0, 95, 1500, 705)
        self.stackedWidget.setStyleSheet("background-color: transparent;")

        # Create views
        self.patientSelectionView = self._createPatientSelectionView()
        self.recordingView = self._createRecordingView()

        self.stackedWidget.addWidget(self.patientSelectionView)
        self.stackedWidget.addWidget(self.recordingView)

    def _createTopBar(self):
        """Creates the top navigation bar"""
        self.topCard = Designer.createRoundedCard(self)
        self.topCard.setGeometry(0, -25, 1500, 100)

        logo = Designer.setLogo(self.topCard)
        logo.setGeometry(60, 10, 90, 90)

        self.dashboardOption = Designer.createMenuOption(
            self.topCard, "Dashboard", "../ImageResources/Icon8BGRemoved.png", 180
        )
        self.dashboardOption.move(500, 40)

        self.administerOption = Designer.createClickedOption(
            self.topCard, "Administer", "../ImageResources/Icon5BGRemoved.png", 180
        )
        self.administerOption.move(725, 40)

        self.notificationsOption = Designer.createMenuOption(
            self.topCard, "Notifications", "../ImageResources/Icon4BGRemoved.png", 180
        )
        self.notificationsOption.move(950, 40)

        self.logoutOption = Designer.createMenuOption(
            self.topCard, "Logout", "../ImageResources/Icon6BGRemoved.png", 150
        )
        self.logoutOption.move(1300, 40)

        profileIcon = Designer.setImage(self.topCard, "../ImageResources/Icon14BGRemoved.png")
        profileIcon.setGeometry(215, 40, 45, 45)

        self.userLabel = Designer.createLabel(self.userInfo, self.topCard, "#1a1a1a", 700, 13)
        self.userLabel.setGeometry(280, 45, 150, 14)

        self.titleLabel = Designer.createLabel(self.role, self.topCard, "#333333", 400, 12)
        self.titleLabel.setGeometry(280, 65, 150, 15)

    def _createPatientSelectionView(self):
        """Creates the Patient Selection view"""
        view = QWidget()
        view.setStyleSheet("background-color: transparent;")

        mainCard = Designer.createRoundedCard(view, 1460, 680)
        mainCard.move(20, 0)

        titleLabel = Designer.createLabel("Administer Medication", mainCard, "#1a1a1a", 700, 24)
        titleLabel.setGeometry(50, 30, 400, 30)
        subtitleLabel = Designer.createLabel("Record medication administration.", mainCard, "#333333", 400, 13)
        subtitleLabel.setGeometry(50, 65, 400, 20)

        patientsLabel = Designer.createLabel("Assigned Patients", mainCard, "#1a1a1a", 700, 18)
        patientsLabel.setGeometry(50, 105, 250, 25)
        patientsSubLabel = Designer.createLabel("Select patient.", mainCard, "#333333", 400, 12)
        patientsSubLabel.setGeometry(50, 135, 250, 20)

        self.patientSearch = Designer.createInputField(mainCard, "white", "#333333", 400, 14, 15, 2, "#185777")
        self.patientSearch.setGeometry(1100, 120, 180, 35)
        self.patientSearch.setPlaceholderText("  🔍 Search patients")

        self.patientSearchButton = Designer.createPrimaryButton("Search", mainCard, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.patientSearchButton.setGeometry(1300, 120, 110, 35)

        self.patientsTable = Designer.createStandardTable([
            "Patient ID", "First Name", "Last Name","Generic",'Brand',"DOB", "Sex", "Room", "Diagnosis"
        ])
        self.patientsTable.setParent(mainCard)
        header = self.patientsTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.patientsTable.setGeometry(50, 170, 1360, 425)

        self.nextButton = Designer.createPrimaryButton("Next", mainCard, "#0cc0df", "#1a1a1a", 700, 13, 15)
        self.nextButton.setGeometry(680, 625, 100, 35)

        return view

    def _createRecordingView(self):
        """Creates the Recording view with improvements"""
        view = QWidget()
        view.setStyleSheet("background-color: transparent;")

        # === LEFT CARD ===
        leftCard = Designer.createRoundedCard(view, 690, 680)
        leftCard.move(20, 0)

        patientMedLabel = Designer.createLabel("Patient and Medicine Information", leftCard, "#1a1a1a", 700, 24)
        patientMedLabel.setGeometry(35, 25, 450, 30)
        patientMedSubLabel = Designer.createLabel("Summary about patient and prescription.", leftCard, "#333333", 400, 12)
        patientMedSubLabel.setGeometry(35, 60, 300, 20)

        yPos = 110

        Designer.createLabel("Prescription ID:", leftCard, "#1a1a1a", 600, 14).setGeometry(40, yPos, 120, 20)
        self.prescriptionIdValue = Designer.createLabel("", leftCard, "#185777", 400, 15)
        self.prescriptionIdValue.setGeometry(170, yPos, 200, 20)

        Designer.createLabel("Medication Lot Number:", leftCard, "#1a1a1a", 600, 14).setGeometry(340, yPos, 180, 20)
        self.lotValue = Designer.createLabel("", leftCard, "#185777", 400, 15)
        self.lotValue.setGeometry(530, yPos, 150, 20)
        yPos += 55

        Designer.createLabel("Patient Name:", leftCard, "#1a1a1a", 600, 14).setGeometry(40, yPos, 120, 20)
        self.patientNameValue = Designer.createLabel("", leftCard, "#185777", 400, 15)
        self.patientNameValue.setGeometry(170, yPos, 200, 20)
        yPos += 60

        Designer.createLabel("Medication Name:", leftCard, "#1a1a1a", 600, 14).setGeometry(40, yPos, 140, 20)
        self.medicationNameValue = Designer.createLabel("", leftCard, "#185777", 400, 15)
        self.medicationNameValue.setGeometry(185, yPos, 300, 20)
        yPos += 55

        Designer.createLabel("Expiry Date:", leftCard, "#1a1a1a", 600, 14).setGeometry(40, yPos, 100, 20)
        self.expiryValue = Designer.createLabel("", leftCard, "#185777", 400, 15)
        self.expiryValue.setGeometry(135, yPos, 100, 20)

        Designer.createLabel("Dosage:", leftCard, "#1a1a1a", 600, 14).setGeometry(340, yPos, 70, 20)
        self.dosageValue = Designer.createLabel("", leftCard, "#185777", 400, 15)
        self.dosageValue.setGeometry(410, yPos, 100, 20)
        yPos += 55

        Designer.createLabel("Frequency:", leftCard, "#1a1a1a", 600, 14).setGeometry(40, yPos, 90, 20)
        self.frequencyValue = Designer.createLabel("", leftCard, "#185777", 400, 15)
        self.frequencyValue.setGeometry(135, yPos, 200, 20)
        yPos += 55

        Designer.createLabel("Prescribed by:", leftCard, "#1a1a1a", 600, 14).setGeometry(40, yPos, 120, 20)
        self.prescribedValue = Designer.createLabel("", leftCard, "#185777", 400, 15)
        self.prescribedValue.setGeometry(160, yPos, 200, 20)
        yPos += 55

        Designer.createLabel("Special Instructions:", leftCard, "#1a1a1a", 600, 14).setGeometry(40, yPos, 150, 20)
        yPos += 45

        self.instructionsDisplay = QFrame(leftCard)
        self.instructionsDisplay.setGeometry(60, yPos, 570, 150)
        self.instructionsDisplay.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #185777;
                border-radius: 15px;
                padding: 10px;
            }
        """)

        self.instructionsText = Designer.createLabel("", self.instructionsDisplay, "#333333", 400, 12)
        self.instructionsText.setGeometry(10, 10, 550, 130)
        self.instructionsText.setWordWrap(True)
        self.instructionsText.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.instructionsText.setStyleSheet("border: none; background-color: transparent;")

        # === RIGHT CARD ===
        rightCard = Designer.createRoundedCard(view, 750, 680)
        rightCard.move(730, 0)

        administerLabel = Designer.createLabel("Administer Medication", rightCard, "#1a1a1a", 700, 24)
        administerLabel.setGeometry(35, 30, 400, 30)
        administerSubLabel = Designer.createLabel("Record medication administration.", rightCard, "#333333", 400, 12)
        administerSubLabel.setGeometry(35, 65, 300, 20)

        # Time Section (Read-only)
        timeLabel = Designer.createLabel("Actual Time Administered", rightCard, "#1a1a1a", 700, 18)
        timeLabel.setGeometry(35, 105, 300, 25)
        timeSubLabel = Designer.createLabel("Current time (auto-filled).", rightCard, "#333333", 400, 12)
        timeSubLabel.setGeometry(40, 135, 250, 20)

        timeAutoLabel = Designer.createLabel("Time:", rightCard, "#1a1a1a", 600, 13)
        timeAutoLabel.setGeometry(55, 175, 60, 20)

        self.timeAutoInput = QTimeEdit(rightCard)
        self.timeAutoInput.setGeometry(115, 170, 130, 30)
        self.timeAutoInput.setTime(QTime.currentTime())
        self.timeAutoInput.setDisplayFormat("hh:mm AP")
        self.timeAutoInput.setReadOnly(True)  # READ-ONLY
        self.timeAutoInput.setStyleSheet("""
            QTimeEdit {
                background-color: #f0f0f0;
                color: #333333;
                font-family: 'Lato';
                font-size: 14px;
                border: 2px solid #185777;
                border-radius: 10px;
                padding: 5px;
            }
        """)

        # Patient Assessment Section
        assessmentLabel = Designer.createLabel("Patient Assessment", rightCard, "#1a1a1a", 700, 18)
        assessmentLabel.setGeometry(40, 225, 250, 25)
        assessmentSubLabel = Designer.createLabel("Assess patient status during medication.", rightCard, "#333333", 400, 12)
        assessmentSubLabel.setGeometry(40, 255, 300, 20)

        radio_style = """
            QRadioButton {
                color: #333333;
                font-family: 'Lato';
                font-size: 13px;
                font-weight: bold;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border: 3px solid #0cc0df;
                border-radius: 10px;
                background: #185777;
            }
            QRadioButton::indicator:checked {
                background-color: #00A9C9;
                border: 3px solid #185777;
            }
            QRadioButton::indicator:hover {
                border-color: #00A9C9;
            }
            QRadioButton:checked {
                color: #00A9C9;
            }
        """

        self.assessmentGroup = QButtonGroup(rightCard)

        self.activeRadio = QRadioButton("Active", rightCard)
        self.activeRadio.setGeometry(60, 295, 90, 25)
        self.activeRadio.setStyleSheet(radio_style)

        self.drowsyRadio = QRadioButton("Drowsy", rightCard)
        self.drowsyRadio.setGeometry(210, 295, 90, 25)
        self.drowsyRadio.setStyleSheet(radio_style)

        self.sleepingRadio = QRadioButton("Sleeping", rightCard)
        self.sleepingRadio.setGeometry(390, 295, 100, 25)
        self.sleepingRadio.setStyleSheet(radio_style)

        self.confusedRadio = QRadioButton("Confused", rightCard)
        self.confusedRadio.setGeometry(570, 295, 110, 25)
        self.confusedRadio.setStyleSheet(radio_style)

        self.assessmentGroup.addButton(self.activeRadio, 1)
        self.assessmentGroup.addButton(self.drowsyRadio, 2)
        self.assessmentGroup.addButton(self.sleepingRadio, 3)
        self.assessmentGroup.addButton(self.confusedRadio, 4)

        # Adverse Reactions Section
        adverseLabel = Designer.createLabel("Adverse Reactions", rightCard, "#1a1a1a", 700, 18)
        adverseLabel.setGeometry(40, 350, 250, 25)
        adverseSubLabel = Designer.createLabel("Observe patient reactions during medication.", rightCard, "#333333", 400, 12)
        adverseSubLabel.setGeometry(40, 380, 350, 20)

        self.adverseGroup = QButtonGroup(rightCard)
        self.adverseGroup.setExclusive(False)

        self.nauseaRadio = QRadioButton("Nausea", rightCard)
        self.nauseaRadio.setGeometry(60, 420, 100, 25)
        self.nauseaRadio.setStyleSheet(radio_style)

        self.vomitingRadio = QRadioButton("Vomiting", rightCard)
        self.vomitingRadio.setGeometry(60, 470, 100, 25)
        self.vomitingRadio.setStyleSheet(radio_style)

        self.dizzinessRadio = QRadioButton("Dizziness", rightCard)
        self.dizzinessRadio.setGeometry(210, 420, 110, 25)
        self.dizzinessRadio.setStyleSheet(radio_style)

        self.rashRadio = QRadioButton("Rash", rightCard)
        self.rashRadio.setGeometry(210, 470, 100, 25)
        self.rashRadio.setStyleSheet(radio_style)

        self.confusionReactionRadio = QRadioButton("Confusion", rightCard)
        self.confusionReactionRadio.setGeometry(390, 420, 110, 25)
        self.confusionReactionRadio.setStyleSheet(radio_style)

        self.respiratoryRadio = QRadioButton("Respiratory Issues", rightCard)
        self.respiratoryRadio.setGeometry(390, 470, 170, 25)
        self.respiratoryRadio.setStyleSheet(radio_style)

        self.adverseGroup.addButton(self.nauseaRadio, 1)
        self.adverseGroup.addButton(self.dizzinessRadio, 2)
        self.adverseGroup.addButton(self.confusionReactionRadio, 3)
        self.adverseGroup.addButton(self.vomitingRadio, 4)
        self.adverseGroup.addButton(self.rashRadio, 5)
        self.adverseGroup.addButton(self.respiratoryRadio, 6)

        # Other option with conditional input (IMPROVED)
        self.otherRadio = QRadioButton("Other:", rightCard)
        self.otherRadio.setGeometry(60, 520, 70, 25)
        self.otherRadio.setStyleSheet(radio_style)
        self.adverseGroup.addButton(self.otherRadio, 7)

        self.otherInput = Designer.createInputField(rightCard, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.otherInput.setGeometry(145, 520, 220, 30)
        self.otherInput.setPlaceholderText("Specify other reaction")
        self.otherInput.setEnabled(False)  # Disabled by default

        # Buttons
        center_x = 750 // 2
        button_width = 110
        button_y = 620

        self.recordButton = Designer.createPrimaryButton("Record", rightCard, "#0cc0df", "#1a1a1a", 700, 13, 15)
        self.recordButton.setGeometry(center_x - button_width - 10, button_y, button_width, 35)

        self.backButton = Designer.createSecondaryButton("Back", rightCard, "#e7f9fc", "#1a1a1a", 700, 13, 15, 2, "#185777")
        self.backButton.setGeometry(center_x + 10, button_y, button_width, 35)
        self.backButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        return view

    def loadPrescriptionDetails(self, prescription_data, patient_data):
        """Loads prescription and patient details"""
        self.prescriptionIdValue.setText(str(prescription_data.get('prescription_id', '')))
        self.lotValue.setText(prescription_data.get('medication_lot_number', 'N/A'))

        patient_name = f"{patient_data.get('patient_first_name', '')} {patient_data.get('patient_last_name', '')}"
        self.patientNameValue.setText(patient_name)

        medication = f"{prescription_data.get('brand_name', '')} ({prescription_data.get('generic_name', '')})"
        self.medicationNameValue.setText(medication)

        self.expiryValue.setText(str(prescription_data.get('expiry_date', 'N/A')))
        self.dosageValue.setText(prescription_data.get('dosage', ''))
        self.frequencyValue.setText(prescription_data.get('frequency', ''))
        self.prescribedValue.setText(prescription_data.get('prescribed_by', ''))

        instructions = prescription_data.get('special_instructions', 'No special instructions')
        self.instructionsText.setText(instructions or 'No special instructions')

    def getAdministrationData(self):
        """Returns all administration form data"""
        assessment_map = {1: "Active", 2: "Drowsy", 3: "Sleeping", 4: "Confused"}
        assessment = assessment_map.get(self.assessmentGroup.checkedId(), None)

        adverse_reactions = []
        if self.nauseaRadio.isChecked():
            adverse_reactions.append("Nausea")
        if self.vomitingRadio.isChecked():
            adverse_reactions.append("Vomiting")
        if self.dizzinessRadio.isChecked():
            adverse_reactions.append("Dizziness")
        if self.rashRadio.isChecked():
            adverse_reactions.append("Rash")
        if self.confusionReactionRadio.isChecked():
            adverse_reactions.append("Confusion")
        if self.respiratoryRadio.isChecked():
            adverse_reactions.append("Respiratory Issues")
        if self.otherRadio.isChecked() and self.otherInput.text().strip():
            adverse_reactions.append(self.otherInput.text().strip())

        adverse_str = ", ".join(adverse_reactions) if adverse_reactions else "None"

        return {
            'administration_time': self.timeAutoInput.time().toString('HH:mm:ss'),
            'patient_assessment': assessment,
            'adverse_reactions': adverse_str
        }

    def clearRecordingForm(self):
        """Clears the recording form"""
        self.timeAutoInput.setTime(QTime.currentTime())
        self.assessmentGroup.setExclusive(False)
        self.activeRadio.setChecked(False)
        self.drowsyRadio.setChecked(False)
        self.sleepingRadio.setChecked(False)
        self.confusedRadio.setChecked(False)
        self.assessmentGroup.setExclusive(True)

        self.nauseaRadio.setChecked(False)
        self.vomitingRadio.setChecked(False)
        self.dizzinessRadio.setChecked(False)
        self.rashRadio.setChecked(False)
        self.confusionReactionRadio.setChecked(False)
        self.respiratoryRadio.setChecked(False)
        self.otherRadio.setChecked(False)
        self.otherInput.clear()
        self.otherInput.setEnabled(False)

    def resetToPatientSelection(self):
        """Resets to patient selection view"""
        self.stackedWidget.setCurrentIndex(0)
        self.clearRecordingForm()


class RecordConfirmationPopup(QWidget):
    """Popup for record confirmation"""
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 250)
        self.setWindowTitle("Medication Recorded")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        Designer.setWindowToCenter(self)

        self.setStyleSheet("background-color: #cef2f9;")

        mainFrame = QFrame(self)
        mainFrame.setGeometry(10, 10, 380, 230)
        mainFrame.setStyleSheet("QFrame{background-color:#cef2f9;border-radius:30px;}")

        logo = Designer.setLogo(mainFrame)
        logo.setGeometry(145, 20, 90, 90)

        messageLabel = Designer.createLabel("Medication Successfully Recorded", mainFrame, "#1a1a1a", 700, 18)
        messageLabel.setGeometry(40, 125, 310, 25)
        messageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtextLabel = Designer.createLabel("The medication administration has been documented.", mainFrame, "#333333", 400, 13)
        subtextLabel.setGeometry(40, 155, 310, 20)
        subtextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.closeButton = Designer.createPrimaryButton("Close", mainFrame, "#0cc0df", "#1a1a1a", 700, 13, 15)
        self.closeButton.setGeometry(150, 190, 100, 40)
        self.closeButton.clicked.connect(self.close)