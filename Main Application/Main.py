import sys
from PyQt6.QtWidgets import QApplication
from Model.Authentication.LoginModel import LoginModel
from View.LoginGUI import Login
from Controller.Login.LoginController import LoginController

# =====================================================
# ENTRY POINT to "MEDISYNC" Medicine Monitoring System
# =====================================================

app = QApplication(sys.argv)
loginView = Login()
loginModel = LoginModel()
loginController = LoginController(loginModel, loginView)
loginView.show()
sys.exit(app.exec())