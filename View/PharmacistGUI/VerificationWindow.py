from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QRadioButton, QButtonGroup, QFrame, QHeaderView
from Utilities.Designers import Designer

class PharmacistVerificationWindow(QWidget):
    """
    Pharmacist Verification Window
    """

    def __init__(self, userInfo, role):
        super().__init__()
        self.setFixedSize(1500, 800)
        self.setWindowTitle("MEDISYNC Verification")
        Designer.setWindowToCenter(self)

        self.userInfo = userInfo
        self.role = role

        self.selectedPrescriptionId = None
        self.selectedPrescriptionData = None

        Designer.setBackground(self)

        self._createTopBar()
        self._createMainContent()

    def _createTopBar(self):
        """Creates the top navigation bar"""
        self.topCard = Designer.createRoundedCard(self)
        self.topCard.setGeometry(0, -25, 1500, 100)

        logo = Designer.setLogo(self.topCard)
        logo.setGeometry(60, 10, 90, 90)

        self.dashboardOption = Designer.createMenuOption(
            self.topCard, "Dashboard",
            "../ImageResources/Icon8BGRemoved.png", 180
        )
        self.dashboardOption.move(500, 40)

        self.verificationOption = Designer.createClickedOption(
            self.topCard, "Verify",
            "../ImageResources/Icon7BGRemoved.png", 160
        )
        self.verificationOption.move(745, 40)

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

        self.userLabel = Designer.createLabel(self.userInfo, self.topCard, "#1a1a1a", 700, 13)
        self.userLabel.setGeometry(280, 45, 150, 14)

        self.titleLabel = Designer.createLabel(self.role, self.topCard, "#333333", 400, 12)
        self.titleLabel.setGeometry(280, 65, 150, 15)

    def _createMainContent(self):
        """Creates the main verification content area"""
        self.mainCard = Designer.createRoundedCard(self)
        self.mainCard.setGeometry(20, 95, 1460, 680)

        verifyLabel = Designer.createLabel("Verify Prescription", self.mainCard, "#1a1a1a", 700, 24)
        verifyLabel.setGeometry(55, 30, 300, 30)
        verifySubLabel = Designer.createLabel("Check, verify and prepare prescriptions.", self.mainCard, "#333333", 400,
                                              13)
        verifySubLabel.setGeometry(55, 70, 300, 20)

        pendingLabel = Designer.createLabel("Pending Prescriptions", self.mainCard, "#1a1a1a", 700, 18)
        pendingLabel.setGeometry(55, 110, 250, 25)
        pendingSubLabel = Designer.createLabel("Select prescription to verify.", self.mainCard, "#333333", 400, 12)
        pendingSubLabel.setGeometry(55, 140, 250, 20)

        self.pendingSearch = Designer.createInputField(self.mainCard, "white", "#333333", 400, 14, 15, 2, "#185777")
        self.pendingSearch.setGeometry(345, 120, 200, 35)
        self.pendingSearch.setPlaceholderText("  🔍 Search prescriptions")

        self.pendingSearchButton = Designer.createPrimaryButton("Search", self.mainCard, "#0cc0df", "#1a1a1a", 700, 12,
                                                                15)
        self.pendingSearchButton.setGeometry(560, 120, 110, 35)

        self.pendingTable = Designer.createStandardTable([ "Prescription ID","Patient Name", "Medication",
            "Dosage", "Prescribed By"
        ])
        self.pendingTable.setParent(self.mainCard)
        self.pendingTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.pendingTable.setGeometry(50, 175, 620, 460)

        batchLabel = Designer.createLabel("Batch Identification", self.mainCard, "#1a1a1a", 700, 18)
        batchLabel.setGeometry(730, 40, 250, 25)
        batchSubLabel = Designer.createLabel("Add batch identification code.", self.mainCard, "#333333", 400, 12)
        batchSubLabel.setGeometry(730, 70, 250, 20)

        lotLabel = Designer.createLabel("Medication Lot Number:", self.mainCard, "#1a1a1a", 600, 13)
        lotLabel.setGeometry(735, 115, 180, 20)
        self.lotInput = Designer.createInputField(self.mainCard, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.lotInput.setGeometry(910, 110, 200, 30)
        self.lotInput.setPlaceholderText("Enter lot number")

        quantityExpiryLabel = Designer.createLabel("Quantity Dispensed and Expiry Date", self.mainCard, "#1a1a1a", 700,
                                                   18)
        quantityExpiryLabel.setGeometry(730, 175, 400, 25)
        quantityExpirySubLabel = Designer.createLabel("Add medication quantity and expiry date.", self.mainCard,
                                                      "#333333", 400, 12)
        quantityExpirySubLabel.setGeometry(730, 205, 300, 20)

        quantityLabel = Designer.createLabel("Quantity:", self.mainCard, "#1a1a1a", 600, 13)
        quantityLabel.setGeometry(735, 250, 80, 20)
        self.quantityInput = Designer.createInputField(self.mainCard, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.quantityInput.setGeometry(810, 245, 100, 30)
        self.quantityInput.setPlaceholderText("0")

        expiryLabel = Designer.createLabel("Expiry Date:", self.mainCard, "#1a1a1a", 600, 13)
        expiryLabel.setGeometry(930, 250, 100, 20)
        self.expiryInput = Designer.createDateEdit(self.mainCard, radius=10, borderColor="#185777", fontSize=14)
        self.expiryInput.setGeometry(1020, 245, 170, 30)

        decisionLabel = Designer.createLabel("Verification Decision", self.mainCard, "#1a1a1a", 700, 18)
        decisionLabel.setGeometry(730, 310, 250, 25)
        decisionSubLabel = Designer.createLabel(
            "Decide whether to approve, request to modify or reject prescription.",
            self.mainCard, "#333333", 400, 12
        )
        decisionSubLabel.setGeometry(730, 340, 500, 20)

        self.decisionGroup = QButtonGroup(self.mainCard)

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

        self.approveRadio = QRadioButton("Approve", self.mainCard)
        self.approveRadio.setGeometry(745, 380, 120, 25)
        self.approveRadio.setStyleSheet(radio_style)

        self.modifyRadio = QRadioButton("Request Modification", self.mainCard)
        self.modifyRadio.setGeometry(880, 380, 200, 25)
        self.modifyRadio.setStyleSheet(radio_style)

        self.rejectRadio = QRadioButton("Reject", self.mainCard)
        self.rejectRadio.setGeometry(1110, 380, 120, 25)
        self.rejectRadio.setStyleSheet(radio_style)

        self.decisionGroup.addButton(self.approveRadio, 1)
        self.decisionGroup.addButton(self.modifyRadio, 2)
        self.decisionGroup.addButton(self.rejectRadio, 3)

        reasonsLabel = Designer.createLabel("Reasons for modification or rejection:", self.mainCard, "#1a1a1a", 600, 13)
        reasonsLabel.setGeometry(740, 430, 300, 20)

        self.reasonsCard, self.reasonsText = Designer.createPlainTextArea(
            parent=self.mainCard,
            backgroundColor="white",
            fontColor="#333333",
            fontSize=14,
            borderRadius=15,
            outlineWeight=2,
            outlineColor="#185777"
        )
        self.reasonsCard.setGeometry(740, 470, 400, 150)
        self.reasonsText.setGeometry(750, 480, 380, 130)
        self.reasonsText.setPlaceholderText("Enter reason if rejecting or requesting modification...")
        self.reasonsText.setEnabled(False)  # Disabled by default

        self.confirmButton = Designer.createPrimaryButton("Confirm", self.mainCard, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.confirmButton.setGeometry(1270, 620, 130, 35)

        # Connect decision radio buttons to toggle input fields
        self.approveRadio.toggled.connect(self._onDecisionChanged)
        self.modifyRadio.toggled.connect(self._onDecisionChanged)
        self.rejectRadio.toggled.connect(self._onDecisionChanged)

    def _onDecisionChanged(self):
        """Handles decision radio button changes to enable/disable fields"""
        if self.approveRadio.isChecked():
            # Approve: Enable batch fields, disable reason
            self.lotInput.setEnabled(True)
            self.quantityInput.setEnabled(True)
            self.expiryInput.setEnabled(True)
            self.reasonsText.setEnabled(False)
            self.reasonsText.clear()
        elif self.modifyRadio.isChecked() or self.rejectRadio.isChecked():
            # Modify/Reject: Disable batch fields, enable reason
            self.lotInput.setEnabled(False)
            self.quantityInput.setEnabled(False)
            self.expiryInput.setEnabled(False)
            self.lotInput.clear()
            self.quantityInput.clear()
            self.reasonsText.setEnabled(True)

    def getVerificationData(self):
        """Returns all verification form data"""
        decision_map = {
            1: "Approve",
            2: "Request Modification",
            3: "Reject"
        }
        selected_id = self.decisionGroup.checkedId()
        decision = decision_map.get(selected_id, None)

        return {
            'lot_number': self.lotInput.text().strip(),
            'quantity': self.quantityInput.text().strip(),
            'expiry_date': self.expiryInput.date().toString('yyyy-MM-dd'),
            'decision': decision,
            'reason': self.reasonsText.toPlainText().strip()
        }

    def clearForm(self):
        """Clears all form fields"""
        self.lotInput.clear()
        self.quantityInput.clear()
        self.reasonsText.clear()
        self.decisionGroup.setExclusive(False)
        self.approveRadio.setChecked(False)
        self.modifyRadio.setChecked(False)
        self.rejectRadio.setChecked(False)
        self.decisionGroup.setExclusive(True)

        # Re-enable all fields
        self.lotInput.setEnabled(True)
        self.quantityInput.setEnabled(True)
        self.expiryInput.setEnabled(True)
        self.reasonsText.setEnabled(False)

        self.selectedPrescriptionId = None
        self.selectedPrescriptionData = None


class VerificationSummaryPopup(QWidget):
    """
    Verification confirmation summary popup
    """

    def __init__(self, title="Verification Summary"):
        super().__init__()
        self.setFixedSize(400, 600)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        Designer.setWindowToCenter(self)

        self.setStyleSheet("background-color: #cef2f9;")

        mainFrame = QFrame(self)
        mainFrame.setGeometry(10, 10, 380, 590)
        mainFrame.setStyleSheet("QFrame {background-color: #cef2f9; border-radius: 30px;}")

        logo = Designer.setLogo(mainFrame)
        logo.setGeometry(145, 20, 90, 90)

        titleLabel = Designer.createLabel(title, mainFrame, "#1a1a1a", 700, 18)
        titleLabel.setGeometry(70, 120, 250, 25)
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        yPos = 165

        Designer.createLabel("Prescription ID:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 130, 20)
        self.prescriptionIdValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.prescriptionIdValue.setGeometry(175, yPos, 170, 20)
        yPos += 30

        Designer.createLabel("Patient Name:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 120, 20)
        self.patientNameValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.patientNameValue.setGeometry(165, yPos, 180, 20)
        yPos += 30

        Designer.createLabel("Medication Name:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 140, 20)
        self.medicationNameValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.medicationNameValue.setGeometry(185, yPos, 160, 20)
        yPos += 30

        Designer.createLabel("Prescribed by:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 120, 20)
        self.prescribedByValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.prescribedByValue.setGeometry(160, yPos, 185, 20)
        yPos += 30

        Designer.createLabel("Medication Lot Number:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 180, 20)
        self.lotValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.lotValue.setGeometry(225, yPos, 120, 20)
        yPos += 30

        Designer.createLabel("Quantity:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 80, 20)
        self.quantityValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.quantityValue.setGeometry(125, yPos, 220, 20)
        yPos += 30

        Designer.createLabel("Expiry Date:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 100, 20)
        self.expiryValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.expiryValue.setGeometry(145, yPos, 200, 20)
        yPos += 30

        Designer.createLabel("Decision:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 80, 20)
        self.decisionValue = Designer.createLabel("", mainFrame, "#1a1a1a", 400, 14)
        self.decisionValue.setGeometry(125, yPos, 220, 20)
        yPos += 40

        Designer.createLabel("Reason:", mainFrame, "#1a1a1a", 600, 14).setGeometry(40, yPos, 80, 20)
        yPos += 30

        self.reasonCard, self.reasonText = Designer.createPlainTextArea(
            parent=mainFrame,
            backgroundColor="white",
            fontColor="#333333",
            fontSize=13,
            borderRadius=15,
            outlineWeight=2,
            outlineColor="#185777"
        )
        self.reasonCard.setGeometry(40, yPos, 310, 90)
        self.reasonText.setGeometry(50, yPos + 10, 290, 70)
        self.reasonText.setReadOnly(True)

        self.submitButton = Designer.createPrimaryButton("Submit", mainFrame, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.submitButton.setGeometry(80, 535, 100, 30)

        self.closeButton = Designer.createSecondaryButton("Close", mainFrame, "#e7f9fc", "#1a1a1a", 700, 12, 15, 2,
                                                          "#185777")
        self.closeButton.setGeometry(200, 535, 100, 30)
        self.closeButton.clicked.connect(self.close)

    def setSummaryData(self, prescription_id, patient_name, medication_name,
                       prescribed_by, lot_number, quantity, expiry_date, decision, reason):
        """Sets all summary data"""
        self.prescriptionIdValue.setText(str(prescription_id))
        self.patientNameValue.setText(patient_name)
        self.medicationNameValue.setText(medication_name)
        self.prescribedByValue.setText(prescribed_by)
        self.lotValue.setText(lot_number)
        self.quantityValue.setText(quantity)
        self.expiryValue.setText(expiry_date)
        self.decisionValue.setText(decision)
        self.reasonText.setPlainText(reason or "N/A")