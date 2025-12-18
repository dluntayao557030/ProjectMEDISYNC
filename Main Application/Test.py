"""
MEDISYNC - Admin Notifications Demo Runner
Launch Notifications with mock session.
"""

import sys
from PyQt6.QtWidgets import QApplication
from Model.SessionManager import SessionManager


def mock_admin_login():
    SessionManager.setUser({
        "user_id": 9,
        "username": "admin",
        "first_name": "Alexander",
        "last_name": "Cruz",
        "role": "Admin",
        "status": "Active"
    })
    print("Mock Admin logged in.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("MEDISYNC")

    mock_admin_login()

    from Controller.Pharmacist.PharmacistDashboardController import PharmacistDashboardController

    controller = PharmacistDashboardController()
    controller.openDashboard()

    sys.exit(app.exec())