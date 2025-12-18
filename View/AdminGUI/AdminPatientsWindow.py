from PyQt6.QtWidgets import QWidget, QFrame, QButtonGroup, QRadioButton, QHeaderView
from PyQt6.QtCore import Qt, QDate
from Utilities.Designers import Designer

class AdminPatientsWindow(QWidget):
    """
    Main Window for Admin Patients Management.
    """

    def __init__(self, userInfo, role):
        super().__init__()
        self.setFixedSize(1500, 800)
        self.setWindowTitle("MEDISYNC Patient Management")
        Designer.setWindowToCenter(self)

        # Store data
        self.userInfo = userInfo
        self.role = role
        self.selectedPatientId = None
        self.selectedPatientData = None

        # Build UI
        self._setupBackground()
        self._createTopBar()
        self._createMainContent()

    def _setupBackground(self):
        """Apply background style"""
        Designer.setBackground(self)

    def _createTopBar(self):
        """Create top navigation bar"""
        self.topCard = Designer.createRoundedCard(self)
        self.topCard.setGeometry(0, -25, 1500, 100)

        # Logo
        Designer.setLogo(self.topCard).setGeometry(60, 10, 90, 90)

        # Menu options (exposed)
        start_x, gap = 400, 180
        self.dashboardOption = Designer.createMenuOption(self.topCard, "Dashboard",
                                                         "../ImageResources/Icon8BGRemoved.png", 170)
        self.dashboardOption.move(start_x, 40)

        self.usersOption = Designer.createMenuOption(self.topCard, "Users",
                                                     "../ImageResources/Icon14BGRemoved.png", 155)
        self.usersOption.move(start_x + gap + 15, 40)

        self.patientsOption = Designer.createClickedOption(self.topCard, "Patients",
                                                           "../ImageResources/Icon1BGRemoved.png", 160)
        self.patientsOption.move(start_x + gap * 2, 40)

        self.reportsOption = Designer.createMenuOption(self.topCard, "Reports",
                                                       "../ImageResources/Icon12BGRemoved.png", 160)
        self.reportsOption.move(start_x + gap * 3, 40)

        self.notificationsOption = Designer.createMenuOption(self.topCard, "Notifications",
                                                             "../ImageResources/Icon4BGRemoved.png", 180)
        self.notificationsOption.move(start_x + gap * 4, 40)

        self.logoutOption = Designer.createMenuOption(self.topCard, "Logout",
                                                      "../ImageResources/Icon6BGRemoved.png", 160)
        self.logoutOption.move(start_x + gap * 5 + 15, 40)

        # User info
        Designer.setImage(self.topCard, "../ImageResources/Icon14BGRemoved.png").setGeometry(215, 40, 45, 45)
        Designer.createLabel(self.userInfo, self.topCard, "#1a1a1a", 700, 13).setGeometry(280, 45, 120, 20)
        Designer.createLabel(self.role, self.topCard, "#333333", 400, 12).setGeometry(280, 65, 120, 20)

    def _createMainContent(self):
        """Create main content with table and buttons"""
        self.mainCard = Designer.createRoundedCard(self)
        self.mainCard.setGeometry(20, 95, 1460, 680)

        # Titles
        Designer.createLabel("Patient Management", self.mainCard, "#1a1a1a", 700, 24).setGeometry(50, 30, 400, 30)
        Designer.createLabel("Manage and register patients to the system.", self.mainCard, "#333333", 400, 13)\
            .setGeometry(50, 65, 400, 20)

        # Patients section
        Designer.createLabel("All Patients", self.mainCard, "#1a1a1a", 700, 18).setGeometry(50, 110, 150, 25)
        Designer.createLabel("Select patient.", self.mainCard, "#333333", 400, 12).setGeometry(50, 140, 150, 20)

        # Search
        self.searchInput = Designer.createInputField(self.mainCard, "white", "#333333", 400, 14, 15, 2, "#185777")
        self.searchInput.setGeometry(1080, 125, 190, 35)
        self.searchInput.setPlaceholderText("  🔍 Search patients")

        self.searchButton = Designer.createPrimaryButton("Search", self.mainCard, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.searchButton.setGeometry(1290, 125, 120, 35)

        # Buttons
        self.registerButton = Designer.createPrimaryButton("Register Patient", self.mainCard, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.registerButton.setGeometry(550, 630, 150, 35)

        self.editButton = Designer.createPrimaryButton("Edit Patient", self.mainCard, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.editButton.setGeometry(730, 630, 150, 35)

        # Table
        columns = ["Patient ID", "Name", "Sex", "Room", "Doctor", "Nurse", "Status"]
        self.patientsTable = Designer.createStandardTable(columns)
        self.patientsTable.setParent(self.mainCard)
        self.patientsTable.setGeometry(50, 175, 1360, 430)
        header = self.patientsTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def clearSelection(self):
        """Reset selected patient"""
        self.selectedPatientId = None
        self.selectedPatientData = None


class RegisterPatientPopup(QWidget):
    """Popup for registering new patients"""

    def __init__(self, title="Register Patient"):
        super().__init__()
        self.setFixedSize(950, 600)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        Designer.setWindowToCenter(self)
        self.setStyleSheet("background-color: #cef2f9;")

        mainFrame = QFrame(self)
        mainFrame.setGeometry(10, 10, 950, 580)
        mainFrame.setStyleSheet("QFrame { background-color: #cef2f9; border-radius: 30px; }")

        # Titles
        Designer.createLabel(title, mainFrame, "#1a1a1a", 700, 24).setGeometry(40, 20, 250, 30)
        Designer.createLabel("Introduce a new patient to the system.", mainFrame, "#333333", 400, 12)\
            .setGeometry(40, 55, 300, 20)

        # Personal info
        Designer.createLabel("Personal Information", mainFrame, "#1a1a1a", 700, 18).setGeometry(40, 90, 250, 25)
        Designer.createLabel("Input personal details of new patient.", mainFrame, "#333333", 400, 11)\
            .setGeometry(40, 115, 250, 20)

        Designer.createLabel("First Name:", mainFrame, "#1a1a1a", 600, 13).setGeometry(60, 150, 100, 20)
        self.firstNameInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.firstNameInput.setGeometry(155, 147, 230, 30)

        Designer.createLabel("Last Name:", mainFrame, "#1a1a1a", 600, 13).setGeometry(60, 195, 100, 20)
        self.lastNameInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.lastNameInput.setGeometry(155, 192, 230, 30)

        Designer.createLabel("Birthdate:", mainFrame, "#1a1a1a", 600, 13).setGeometry(60, 240, 100, 20)
        self.birthdateInput = Designer.createDateEdit(mainFrame, radius=10, borderColor="#185777", fontSize=14)
        self.birthdateInput.setGeometry(155, 237, 180, 30)

        # Sex radios
        Designer.createLabel("Sex:", mainFrame, "#1a1a1a", 600, 13).setGeometry(60, 285, 50, 20)

        radio_style = """
            QRadioButton { color: #333333; font-family: 'Lato'; font-size: 13px; font-weight: bold; }
            QRadioButton::indicator { width: 16px; height: 16px; border: 3px solid #0cc0df; border-radius: 10px; background: #185777; }
            QRadioButton::indicator:checked { background-color: #00A9C9; border: 3px solid #185777; }
            QRadioButton::indicator:hover { border-color: #00A9C9; }
            QRadioButton:checked { color: #00A9C9; }
        """

        self.sexGroup = QButtonGroup(mainFrame)
        self.maleRadio = QRadioButton("Male", mainFrame)
        self.maleRadio.setGeometry(155, 285, 70, 25)
        self.maleRadio.setStyleSheet(radio_style)

        self.femaleRadio = QRadioButton("Female", mainFrame)
        self.femaleRadio.setGeometry(250, 285, 85, 25)
        self.femaleRadio.setStyleSheet(radio_style)

        self.sexGroup.addButton(self.maleRadio, 1)
        self.sexGroup.addButton(self.femaleRadio, 2)

        # Contact info
        Designer.createLabel("Contact Information", mainFrame, "#1a1a1a", 700, 18).setGeometry(40, 335, 250, 25)
        Designer.createLabel("Input contact details of patient.", mainFrame, "#333333", 400, 11)\
            .setGeometry(40, 360, 250, 20)

        Designer.createLabel("Contact Person:", mainFrame, "#1a1a1a", 600, 13).setGeometry(60, 395, 120, 20)
        self.contactPersonInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.contactPersonInput.setGeometry(180, 392, 205, 30)

        Designer.createLabel("Relationship:", mainFrame, "#1a1a1a", 600, 13).setGeometry(60, 440, 100, 20)
        self.relationshipDropdown = Designer.createComboBox(mainFrame, radius=10, borderColor="#185777", fontSize=14)
        self.relationshipDropdown.setGeometry(160, 437, 180, 30)
        self.relationshipDropdown.addItems(["Parent", "Spouse", "Sibling", "Child", "Friend", "Other"])

        # Right column
        Designer.createLabel("Contact Number:", mainFrame, "#1a1a1a", 600, 13).setGeometry(480, 90, 130, 20)
        self.contactNumberInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.contactNumberInput.setGeometry(610, 87, 210, 30)

        # Admission details
        Designer.createLabel("Admission Details", mainFrame, "#1a1a1a", 700, 18).setGeometry(480, 135, 250, 25)
        Designer.createLabel("Input information about patient's admission", mainFrame, "#333333", 400, 11)\
            .setGeometry(480, 160, 300, 20)

        Designer.createLabel("Room Number:", mainFrame, "#1a1a1a", 600, 13).setGeometry(490, 195, 120, 20)
        self.roomNumberInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.roomNumberInput.setGeometry(605, 192, 80, 30)

        Designer.createLabel("Admission date:", mainFrame, "#1a1a1a", 600, 13).setGeometry(490, 240, 115, 20)
        self.admissionDateInput = Designer.createDateEdit(mainFrame, radius=10, borderColor="#185777", fontSize=14)
        self.admissionDateInput.setGeometry(605, 237, 180, 30)

        Designer.createLabel("Diagnosis:", mainFrame, "#1a1a1a", 600, 13).setGeometry(490, 285, 100, 20)
        self.diagnosisInput = Designer.createInputField(mainFrame, "white", "#333333", 400, 14, 10, 2, "#185777")
        self.diagnosisInput.setGeometry(605, 282, 190, 30)

        Designer.createLabel("Doctor:", mainFrame, "#1a1a1a", 600, 13).setGeometry(490, 330, 100, 20)
        self.doctorDropdown = Designer.createComboBox(mainFrame, radius=10, borderColor="#185777", fontSize=14)
        self.doctorDropdown.setGeometry(605, 327, 190, 30)

        Designer.createLabel("Nurse:", mainFrame, "#1a1a1a", 600, 13).setGeometry(490, 375, 100, 20)
        self.nurseDropdown = Designer.createComboBox(mainFrame, radius=10, borderColor="#185777", fontSize=14)
        self.nurseDropdown.setGeometry(605, 372, 190, 30)

        # Buttons
        self.submitButton = Designer.createPrimaryButton("Submit", mainFrame, "#0cc0df", "#1a1a1a", 700, 12, 15)
        self.submitButton.setGeometry(330, 520, 100, 35)

        self.closeButton = Designer.createSecondaryButton("Close", mainFrame, "#e7f9fc", "#1a1a1a", 700, 12, 15, 2, "#185777")
        self.closeButton.setGeometry(450, 520, 100, 35)
        self.closeButton.clicked.connect(self.close)

    def populateDoctors(self, doctors: list[dict]):
        """Populate doctor dropdown"""
        self.doctorDropdown.clear()
        for doc in doctors:
            self.doctorDropdown.addItem(doc['name'], doc['user_id'])

    def populateNurses(self, nurses: list[dict]):
        """Populate nurse dropdown"""
        self.nurseDropdown.clear()
        for nurse in nurses:
            self.nurseDropdown.addItem(nurse['name'], nurse['user_id'])

    def getPatientData(self):
        """Get form data as dict"""
        sex_map = {1: "Male", 2: "Female"}
        sex = sex_map.get(self.sexGroup.checkedId())
        return {
            'first_name': self.firstNameInput.text().strip(),
            'last_name': self.lastNameInput.text().strip(),
            'date_of_birth': self.birthdateInput.date().toPyDate(),
            'sex': sex,
            'emergency_contact_name': self.contactPersonInput.text().strip() or None,
            'emergency_person_relationship': self.relationshipDropdown.currentText(),
            'emergency_contact_number': self.contactNumberInput.text().strip() or None,
            'room_number': self.roomNumberInput.text().strip(),
            'admission_date': self.admissionDateInput.date().toPyDate(),
            'diagnosis': self.diagnosisInput.text().strip(),
            'doctor_id': self.doctorDropdown.currentData(),
            'nurse_id': self.nurseDropdown.currentData()
        }

    def clearForm(self):
        """Reset form fields"""
        for field in [self.firstNameInput, self.lastNameInput, self.contactPersonInput,
                      self.contactNumberInput, self.roomNumberInput, self.diagnosisInput]:
            field.clear()
        self.birthdateInput.setDate(QDate.currentDate())
        self.admissionDateInput.setDate(QDate.currentDate())
        self.relationshipDropdown.setCurrentIndex(0)
        self.doctorDropdown.setCurrentIndex(0)
        self.nurseDropdown.setCurrentIndex(0)
        self.sexGroup.setExclusive(False)
        self.maleRadio.setChecked(False)
        self.femaleRadio.setChecked(False)
        self.sexGroup.setExclusive(True)


class EditPatientPopup(RegisterPatientPopup):
    """Popup for editing patients, extends register with status radios"""

    def __init__(self, title="Edit Patient"):
        super().__init__(title)

        # Add status section
        status_label = Designer.createLabel("Status:", self.findChild(QFrame), "#1a1a1a", 600, 13)
        status_label.setGeometry(490, 420, 100, 20)

        radio_style = """
            QRadioButton { color: #333333; font-family: 'Lato'; font-size: 13px; font-weight: bold; }
            QRadioButton::indicator { width: 16px; height: 16px; border: 3px solid #0cc0df; border-radius: 10px; background: #185777; }
            QRadioButton::indicator:checked { background-color: #00A9C9; border: 3px solid #185777; }
            QRadioButton::indicator:hover { border-color: #00A9C9; }
            QRadioButton:checked { color: #00A9C9; }
        """

        self.statusGroup = QButtonGroup(self.findChild(QFrame))
        self.activeRadio = QRadioButton("Active", self.findChild(QFrame))
        self.activeRadio.setGeometry(605, 420, 80, 25)
        self.activeRadio.setStyleSheet(radio_style)

        self.dischargedRadio = QRadioButton("Discharged", self.findChild(QFrame))
        self.dischargedRadio.setGeometry(695, 420, 100, 25)
        self.dischargedRadio.setStyleSheet(radio_style)

        self.deceasedRadio = QRadioButton("Deceased", self.findChild(QFrame))
        self.deceasedRadio.setGeometry(805, 420, 100, 25)
        self.deceasedRadio.setStyleSheet(radio_style)

        self.statusGroup.addButton(self.activeRadio, 1)
        self.statusGroup.addButton(self.dischargedRadio, 2)
        self.statusGroup.addButton(self.deceasedRadio, 3)

        # Update submit button text
        self.submitButton.setText("Update")

    def getPatientData(self):
        """Get form data including status"""
        data = super().getPatientData()
        status_map = {1: "Active", 2: "Discharged", 3: "Deceased"}
        data['status'] = status_map.get(self.statusGroup.checkedId())
        return data

    def populateForm(self, data: dict):
        """Populate form with existing patient data"""
        self.firstNameInput.setText(data.get('patient_first_name', ''))
        self.lastNameInput.setText(data.get('patient_last_name', ''))
        dob = data.get('date_of_birth')
        if dob:
            self.birthdateInput.setDate(QDate.fromString(str(dob), 'yyyy-MM-dd'))
        sex = data.get('sex')
        if sex == 'Male':
            self.maleRadio.setChecked(True)
        elif sex == 'Female':
            self.femaleRadio.setChecked(True)
        self.contactPersonInput.setText(data.get('emergency_contact_name', ''))
        rel = data.get('emergency_person_relationship', '')
        index = self.relationshipDropdown.findText(rel)
        if index >= 0:
            self.relationshipDropdown.setCurrentIndex(index)
        self.contactNumberInput.setText(data.get('emergency_contact_number', ''))
        self.roomNumberInput.setText(data.get('room_number', ''))
        adm = data.get('admission_date')
        if adm:
            self.admissionDateInput.setDate(QDate.fromString(str(adm), 'yyyy-MM-dd'))
        self.diagnosisInput.setText(data.get('diagnosis', ''))
        doc_id = data.get('doctor_id')
        if doc_id:
            doc_index = self.doctorDropdown.findData(doc_id)
            if doc_index >= 0:
                self.doctorDropdown.setCurrentIndex(doc_index)
        nurse_id = data.get('nurse_id')
        if nurse_id:
            nurse_index = self.nurseDropdown.findData(nurse_id)
            if nurse_index >= 0:
                self.nurseDropdown.setCurrentIndex(nurse_index)
        status = data.get('status')
        if status == 'Active':
            self.activeRadio.setChecked(True)
        elif status == 'Discharged':
            self.dischargedRadio.setChecked(True)
        elif status == 'Deceased':
            self.deceasedRadio.setChecked(True)

class AddSuccessPopup(QWidget):
    """ Popups for successful adding of patient or user. """
    def __init__(self, window="patient"):
        super().__init__()
        self.setFixedSize(400, 250)
        # Messages based on type
        if window == "patient":
            frameTitle = "Patient Registration"
            mainMessage = "Patient Registered!"
            subMessage = "A patient has been successfully registered."
        elif window == "user":
            frameTitle = "User Registration"
            mainMessage = "User Added to the System!"
            subMessage = "A user has been successfully added to the system."
        elif window == "editPatient":
            frameTitle = "Edit Patient Information"
            mainMessage = "Patient Information Edited!"
            subMessage = "A patient's information has been successfully edited."
        elif window == "editUser":
            frameTitle = "Edit User Information"
            mainMessage = "User Information Edited!"
            subMessage = "A user's information has been successfully edited."
        else:
            return
        self.setWindowTitle(frameTitle)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        Designer.setWindowToCenter(self)
        # Background color
        self.setStyleSheet("background-color: #cef2f9;")
        # Main frame
        mainFrame = QFrame(self)
        mainFrame.setGeometry(10, 10, 380, 230)
        mainFrame.setStyleSheet(""" 
            QFrame { 
                background-color: #cef2f9; 
                border-radius: 30px; 
            } 
        """)
        # Logo
        logo = Designer.setLogo(mainFrame)
        logo.setGeometry(145, 20, 90, 90)
        # Message
        messageLabel = Designer.createLabel(mainMessage, mainFrame, "#1a1a1a", 700, 18)
        messageLabel.setGeometry(40, 125, 310, 25)
        messageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Subtext
        subtextLabel = Designer.createLabel(subMessage, mainFrame, "#333333", 400, 13)
        subtextLabel.setGeometry(40, 155, 310, 20)
        subtextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)