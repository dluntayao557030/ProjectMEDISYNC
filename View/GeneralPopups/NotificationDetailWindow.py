from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QFrame
from Utilities.Designers import Designer

class NotificationDetailPopup(QWidget):

    def __init__(self, notification_data, parent=None):
        super().__init__()
        self.setFixedSize(500, 400)
        self.setWindowTitle("Notification Details")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        Designer.setWindowToCenter(self)

        # Store notification data
        self.notificationData = notification_data

        # Background
        self.setStyleSheet("background-color: #cef2f9;")

        # Main frame
        mainFrame = QFrame(self)
        mainFrame.setGeometry(10, 10, 480, 380)
        mainFrame.setStyleSheet("""
                        QFrame {
                            background-color: #cef2f9;
                            border-radius: 30px;
                        }
                    """)

        # Priority color mapping
        priorityColors = {
            "urgent": "#ff6b6b",
            "attention": "#ffa500",
            "info": "#7bc96f"
        }

        priority = notification_data.get("priority", "info").lower()
        color = priorityColors.get(priority, "#7bc96f")

        # Priority indicator bar
        priorityBar = QWidget(mainFrame)
        priorityBar.setGeometry(0, 0, 480, 8)
        priorityBar.setStyleSheet(f"""
            QWidget {{
                background-color: {color};
                border-top-left-radius: 30px;
                border-top-right-radius: 30px;
            }}
        """)

        # Title
        titleLabel = Designer.createLabel(
            notification_data.get("title", "No Title"),
            mainFrame, "#1a1a1a", 700, 18
        )
        titleLabel.setGeometry(30, 30, 420, 30)
        titleLabel.setWordWrap(True)

        # Timestamp
        timeLabel = Designer.createLabel(
            notification_data.get("time", "Unknown time"),
            mainFrame, "#666666", 400, 12
        )
        timeLabel.setGeometry(30, 65, 420, 20)

        # Priority badge
        priorityLabel = Designer.createLabel(
            priority.capitalize(), mainFrame, "white", 700, 13
        )
        priorityLabel.setGeometry(30, 95, 100, 25)
        priorityLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        priorityLabel.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                font-weight: 700;
                font-family: 'Lato';
                font-size: 13px;
                border-radius: 12px;
                padding: 5px;
            }}
        """)

        # Message
        messageLabel = Designer.createLabel("Message:", mainFrame, "#1a1a1a", 600, 14)
        messageLabel.setGeometry(30, 135, 100, 20)

        # Message text area
        messageCard, messageText = Designer.createPlainTextArea(
            parent=mainFrame,
            backgroundColor="white",
            fontColor="#333333",
            fontSize=13,
            borderRadius=15,
            outlineWeight=2,
            outlineColor="#185777"
        )
        messageCard.setGeometry(30, 165, 420, 160)
        messageText.setGeometry(40, 175, 400, 140)
        messageText.setPlainText(notification_data.get("message", "No message"))
        messageText.setReadOnly(True)

        # Close button
        closeButton = Designer.createPrimaryButton(
            "Close", mainFrame, "#0cc0df", "#1a1a1a", 700, 12, 15
        )
        closeButton.setGeometry(190, 340, 100, 30)
        closeButton.clicked.connect(self.close)