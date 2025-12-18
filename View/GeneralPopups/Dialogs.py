from PyQt6.QtWidgets import QMessageBox

class Dialogs:
    @staticmethod
    def showErrorDialog(title, message):
        """
        Displays an error dialog.

        Parameters:
            title (str): Dialog title
            message (str): Error message
        """
        try:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle(title)
            msg.setText(message)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        except Exception as e:
            print(f"Failed to show error dialog: {e}")

    @staticmethod
    def showSuccessDialog(title, message):
        """
        Displays success dialog
        """

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()