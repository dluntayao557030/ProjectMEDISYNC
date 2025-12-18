from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QFrame
from Utilities.Designers import Designer

class Login(QWidget):
    """
    Creates Login Window.
    """

    def __init__(self):
        super().__init__()
        self.setFixedSize(1500, 800)
        self.setWindowTitle("MEDISYNC Login")
        Designer.setWindowToCenter(self)

        # Background
        background = Designer.setBackground(self)

        # Layout
        layout = QVBoxLayout(background)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Main Card
        card = Designer.createRoundedCard(self,400,550)
        layout.addWidget(card)

        # Logo
        logo = Designer.setLogo(card)
        logo.setGeometry(120, 10, 150, 150)

        # Welcome Message
        message = Designer.createLabel("Welcome Back",card,"#1a1a1a",700,30)
        message.setGeometry(90, 170, 280, 40)

        # Login Labels
        usernameLabel = Designer.createLabel("Username",card,"#1a1a1a",400,14)
        usernameLabel.setGeometry(50, 230, 280, 40)
        passwordLabel = Designer.createLabel("Password",card,"#1a1a1a",400,14)
        passwordLabel.setGeometry(50, 330, 280, 40)

        # Login Input Fields
        self.username = Designer.createInputField(card,"#e7f9fc","#1a1a1a",
                                             400,13,10,1,"#185777")
        self.username.setGeometry(40, 280, 320, 40)
        self.username.setPlaceholderText("  Enter username")
        self.password = Designer.createInputField(card,"#e7f9fc","#1a1a1a",
                                               400,13,10,1,"#185777")
        self.password.setGeometry(40, 380, 320, 40)
        self.password.setPlaceholderText("  Enter password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        # Login Button
        self.loginButton = Designer.createPrimaryButton("Login",card,"#0cc0df","#1A1A1A",
                                              700,12,10)
        self.loginButton.setGeometry(40, 450, 320, 40)

class LoginErrorPopup(QWidget):
    """
    Popups for unsuccessful login.
    """

    def __init__(self, errorType="empty", parent=None):
        super().__init__()
        self.parent_window = parent
        self.setFixedSize(400, 250)
        self.setWindowTitle("Login Failed")
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

        # Error messages based on type
        if errorType == "empty":
            mainMessage = "Missing Credentials"
            subMessage = "Please enter both username and password."
        else:  # invalid credentials
            mainMessage = "Login Failed"
            subMessage = "Invalid username or password."

        # Error Message
        messageLabel = Designer.createLabel(mainMessage, mainFrame, "#1a1a1a", 700, 18)
        messageLabel.setGeometry(40, 125, 310, 25)
        messageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtext
        subtextLabel = Designer.createLabel(subMessage, mainFrame, "#333333", 400, 13)
        subtextLabel.setGeometry(40, 155, 310, 20)
        subtextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Close Button
        self.closeButton = Designer.createPrimaryButton("Close", mainFrame, "#0cc0df", "#1a1a1a", 700, 13, 15)
        self.closeButton.setGeometry(140, 190, 100, 35)

class LoginSuccessPopup(QWidget):
    """
    Popup for successful login.
    """

    def __init__(self, user_name, role, parent=None):
        super().__init__()
        self.parent_window = parent
        self.user_name = user_name
        self.role = role
        self.setFixedSize(400, 250)
        self.setWindowTitle("Login Successful")
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

        # Success Message
        messageLabel = Designer.createLabel(f"Welcome {user_name}!", mainFrame, "#1a1a1a", 700, 18)
        messageLabel.setGeometry(40, 125, 310, 25)
        messageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtext
        subtextLabel = Designer.createLabel(f"You are logged in as {role}.", mainFrame, "#333333", 400, 13)
        subtextLabel.setGeometry(40, 155, 310, 20)
        subtextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Continue Button
        self.continueButton = Designer.createPrimaryButton("Continue", mainFrame, "#0cc0df", "#1a1a1a", 700, 13, 15)
        self.continueButton.setGeometry(140, 190, 100, 35)