from Model.Transactions.PatientModel import PatientsModel
from Model.Transactions.ReportsModel import ReportsModel
from Model.SessionManager import SessionManager
from View.AdminGUI.ReportsWindow import ReportsWindow, ReportSummaryWindow
from View.GeneralPopups.Dialogs import Dialogs
from PyQt6.QtWidgets import QFileDialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import os

class ReportsController:
    """
    Controller for Admin Reports
    """

    def __init__(self):
        self.loginController = None
        self.reportsWindow = None
        self.summaryWindow = None
        self._loadData()

    def _loadData(self):
        """Fetch current user and dropdown data"""
        self.user, self.userInfo, self.role = self._getCurrentUser()
        self.patients = ReportsModel.getPatientsList()
        self.doctors = PatientsModel.getDoctorsList()
        self.nurses = PatientsModel.getNursesList()

    @staticmethod
    def _getCurrentUser():
        """Gets current user information from session"""
        user = SessionManager.getUser() or {}
        name = f"{user.get('first_name', 'Unknown')} {user.get('last_name', '')}".strip()
        role = user.get("role", "Admin")
        return user, name or "Unknown User", role

    def openReportsWindow(self):
        """Launch the reports window"""
        try:
            self.reportsWindow = ReportsWindow(self.userInfo, self.role)
            self.reportsWindow.populateDropdowns(self.patients, self.doctors, self.nurses)
            self._connectSignals()
            self.reportsWindow.show()
        except Exception as e:
            print(f"Failed to open ReportsWindow: {e}")
            Dialogs.showErrorDialog("Window Error", f"Failed to open: {str(e)}")

    def _connectSignals(self):
        """Connect all UI interactions"""
        try:
            w = self.reportsWindow

            # Navigation
            w.dashboardOption.mousePressEvent = lambda n: self.navigateToDashboard()
            w.usersOption.mousePressEvent = lambda n: self.navigateToUsers()
            w.patientsOption.mousePressEvent = lambda n: self.navigateToPatients()
            w.notificationsOption.mousePressEvent = lambda n: self.navigateToNotifications()
            w.logoutOption.mousePressEvent = lambda n: self.logout()

            # Report actions
            w.typeDropdown.currentTextChanged.connect(self.onReportTypeChanged)
            w.generateButton.clicked.connect(self.generateReport)
            w.viewSummaryButton.clicked.connect(self.viewSummary)
            w.saveButton.clicked.connect(self.saveAsPDF)
        except Exception as e:
            print(f"Failed to connect signals: {e}")

    def onReportTypeChanged(self, report_type: str):
        """Update filters when report type changes"""
        try:
            self.reportsWindow.currentReportType = report_type
            self.reportsWindow.updateFiltersForType(report_type)
            if report_type == "-- Select Report Type --":
                self.reportsWindow.switchToTable(0)
        except Exception as e:
            print(f"Failed to change report type: {e}")

    def generateReport(self):
        """Generate report based on selected type and filters"""
        try:
            report_type = self.reportsWindow.typeDropdown.currentText()
            if report_type == "-- Select Report Type --":
                Dialogs.showErrorDialog("Selection Required", "Please select a report type.")
                return

            from_date = self.reportsWindow.fromDateInput.date().toString('yyyy-MM-dd') if self.reportsWindow.fromDateInput.isEnabled() else None
            to_date = self.reportsWindow.toDateInput.date().toString('yyyy-MM-dd') if self.reportsWindow.toDateInput.isEnabled() else None
            patient_id = self.reportsWindow.patientDropdown.currentData() if self.reportsWindow.patientDropdown.isEnabled() else None
            doctor_id = self.reportsWindow.doctorDropdown.currentData() if self.reportsWindow.doctorDropdown.isEnabled() else None
            nurse_id = self.reportsWindow.nurseDropdown.currentData() if self.reportsWindow.nurseDropdown.isEnabled() else None

            data = self._fetchReportData(report_type, from_date, to_date, patient_id, doctor_id, nurse_id)
            self.reportsWindow.currentReportData = data

            index_map = {
                "Prescription Records": 1,
                "Medication Preparation Records": 2,
                "Medication Verification Records": 3,
                "Nurse Administration Log": 4,
                "Missed Administrations": 5,
                "Controlled Substances Activity": 6
            }
            self.reportsWindow.switchToTable(index_map.get(report_type, 0))

            columns = self._getColumnsForType(report_type)
            self.reportsWindow.populateTable(data, columns)

            print(f"✓ Generated {report_type}: {len(data)} records")
        except Exception as e:
            print(f"Failed to generate report: {e}")
            Dialogs.showErrorDialog("Report Error", f"Failed to generate report: {str(e)}")

    @staticmethod
    def _fetchReportData(report_type, from_date, to_date, patient_id, doctor_id, nurse_id):
        """Call correct model method"""
        if report_type == "Prescription Records":
            return ReportsModel.getPrescriptionRecords(from_date, to_date, patient_id, doctor_id)
        elif report_type == "Medication Preparation Records":
            return ReportsModel.getMedicationPreparationRecords(from_date, to_date, patient_id)
        elif report_type == "Medication Verification Records":
            return ReportsModel.getMedicationVerificationRecords(from_date, to_date, patient_id)
        elif report_type == "Nurse Administration Log":
            return ReportsModel.getNurseAdministrationLog(from_date, to_date, patient_id, nurse_id)
        elif report_type == "Missed Administrations":
            return ReportsModel.getMissedAdministrations(patient_id, nurse_id)
        elif report_type == "Controlled Substances Activity":
            return ReportsModel.getControlledSubstancesActivity(from_date, to_date, doctor_id)
        return []

    @staticmethod
    def _getColumnsForType(report_type):
        """Return correct column headers matching database schema"""
        if report_type == "Prescription Records":
            return ["ID", "Date", "Patient", "Medication", "Dosage", "Frequency", "Prescribed By", "Status"]
        elif report_type == "Medication Preparation Records":
            return ["Prep ID", "Patient", "Medication", "Quantity", "Status"]
        elif report_type == "Medication Verification Records":
            return ["Verification ID", "Verified At", "Patient", "Medication", "Lot Number", "Qty Dispensed", "Expiry", "Pharmacist", "Decision"]
        elif report_type == "Nurse Administration Log":
            return ["Admin ID", "Time", "Patient", "Medication", "Dosage", "Assessment", "Adverse Reactions", "Nurse", "Status", "Remarks"]
        elif report_type == "Missed Administrations":
            return ["Administration ID", "Scheduled Time", "Patient", "Room", "Medication", "Dosage", "Nurse", "Status", "Remarks"]
        elif report_type == "Controlled Substances Activity":
            return ["ID", "Date", "Medication", "Brand", "Patient", "Dosage", "Frequency", "Prescribed By", "Qty Dispensed", "Pharmacist", "Status"]
        return ["No Data"]

    def viewSummary(self):
        """Open ReportSummaryWindow with full data"""
        try:
            report_type = self.reportsWindow.currentReportType
            data = self.reportsWindow.currentReportData

            if not report_type or report_type == "-- Select Report Type --":
                Dialogs.showErrorDialog("No Report", "Please generate a report first.")
                return

            total_records = len(data)
            date_range = "All Time"
            from_date = self.reportsWindow.fromDateInput.date().toString('MMM dd, yyyy')
            to_date = self.reportsWindow.toDateInput.date().toString('MMM dd, yyyy')
            if from_date != "Jan 01, 2000":
                date_range = f"{from_date} to {to_date}"

            if not data:
                statistics = "No records found for the selected filters."
            else:
                statistics = self._generateDetailedStatistics(report_type, data)

            if self.summaryWindow is None:
                self.summaryWindow = ReportSummaryWindow()
            self.summaryWindow.setSummaryData(report_type, date_range, total_records, statistics)
            self.summaryWindow.show()
            self.summaryWindow.raise_()
            self.summaryWindow.activateWindow()
        except Exception as e:
            print(f"Failed to view summary: {e}")
            Dialogs.showErrorDialog("Summary Error", f"Failed to view summary: {str(e)}")

    @staticmethod
    def _generateDetailedStatistics(report_type: str, data: list) -> str:
        """Generate rich, human-readable statistics"""
        lines = []
        total = len(data)

        if report_type == "Prescription Records":
            status_count = {}
            for r in data:
                s = r.get('status', 'Unknown')
                status_count[s] = status_count.get(s, 0) + 1
            lines.append("Status Distribution:")
            for status, count in status_count.items():
                lines.append(f" • {status}: {count}")

        elif report_type == "Medication Verification Records":
            decision_count = {}
            for r in data:
                d = r.get('decision', 'Unknown')
                decision_count[d] = decision_count.get(d, 0) + 1
            lines.append("Verification Outcomes:")
            for dec, count in decision_count.items():
                lines.append(f" • {dec}: {count}")

        elif report_type == "Nurse Administration Log":
            status_count = {}
            for r in data:
                s = r.get('status', 'Unknown')
                status_count[s] = status_count.get(s, 0) + 1
            lines.append("Administration Status:")
            for status, count in status_count.items():
                lines.append(f" • {status}: {count}")

        elif report_type == "Missed Administrations":
            lines.append(f"Total Missed Administrations: {total}")
            lines.append("Immediate nursing review required.")

        elif report_type == "Controlled Substances Activity":
            dispensed = sum(1 for r in data if r.get('qty_dispensed') not in ['Pending', None])
            lines.append(f"Dispensed: {dispensed}")
            lines.append(f"Pending Dispense: {total - dispensed}")
            lines.append("All activity logged for compliance.")

        elif report_type == "Medication Preparation Records":
            status_count = {}
            for r in data:
                s = r.get('status', 'Unknown')
                status_count[s] = status_count.get(s, 0) + 1
            lines.append("Preparation Status:")
            for status, count in status_count.items():
                lines.append(f" • {status}: {count}")

        if not lines:
            lines.append("No additional statistics available.")

        return "\n".join(lines)

    def saveAsPDF(self):
        """Export current report to PDF with header, logo, filters, and summary"""
        try:
            data = self.reportsWindow.currentReportData
            if not data:
                Dialogs.showErrorDialog("No Data", "Generate a report before exporting.")
                return

            report_type = self.reportsWindow.currentReportType

            # More accurate filename: MEDISYNC_{ReportType}_Report_{YYYY-MM-DD}.pdf
            current_date = datetime.now().strftime("%Y-%m-%d")
            sanitized_report_type = report_type.replace(" ", "_")
            default_filename = f"MEDISYNC_{sanitized_report_type}_Report_{current_date}.pdf"

            filename, _ = QFileDialog.getSaveFileName(
                self.reportsWindow, "Save Report as PDF", default_filename, "PDF Files (*.pdf)"
            )
            if not filename:
                return

            # Get filter information
            filters = self._getAppliedFilters()

            # Get statistics
            statistics = self._generateDetailedStatistics(report_type, data)

            # Generate PDF
            self._generatePDFReport(filename, report_type, data, filters, statistics)

            Dialogs.showSuccessDialog("Export Complete", f"Report successfully saved to:\n{filename}")
            print(f"✓ PDF exported: {filename}")
        except Exception as e:
            print(f"Failed to save PDF: {e}")
            Dialogs.showErrorDialog("Export Error", f"Failed to export PDF: {str(e)}")

    def _getAppliedFilters(self):
        """Get current filter values as readable text"""
        filters = []

        # Date Range
        if self.reportsWindow.fromDateInput.isEnabled():
            from_date = self.reportsWindow.fromDateInput.date().toString('MMM dd, yyyy')
            to_date = self.reportsWindow.toDateInput.date().toString('MMM dd, yyyy')
            filters.append(f"Date Range: {from_date} to {to_date}")

        # Patient Filter
        if self.reportsWindow.patientDropdown.isEnabled():
            patient_text = self.reportsWindow.patientDropdown.currentText()
            if patient_text != "-- All Patients --":
                filters.append(f"Patient: {patient_text}")

        # Doctor Filter
        if self.reportsWindow.doctorDropdown.isEnabled():
            doctor_text = self.reportsWindow.doctorDropdown.currentText()
            if doctor_text != "-- All Doctors --":
                filters.append(f"Doctor: {doctor_text}")

        # Nurse Filter
        if self.reportsWindow.nurseDropdown.isEnabled():
            nurse_text = self.reportsWindow.nurseDropdown.currentText()
            if nurse_text != "-- All Nurses --":
                filters.append(f"Nurse: {nurse_text}")

        if not filters:
            filters.append("No filters applied")

        return " | ".join(filters)

    def _generatePDFReport(self, filename, report_type, data, filters, statistics):
        columns = self._getColumnsForType(report_type)
        rows = []
        for record in data:
            row = []
            for col in columns:
                key = col.lower().replace(" ", "_")
                value = record.get(key, "N/A")
                row.append(str(value))
            rows.append(row)

        header_height = 0.8
        logo_title_height = 0.7
        table_height = max(len(rows) * 0.2, 3.0)
        summary_height = 1.5
        total_height = header_height + logo_title_height + table_height + summary_height + 0.5

        with PdfPages(filename) as pdf:
            fig = plt.figure(figsize=(11, total_height))

            content_top = 0.95

            generation_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
            fig.text(0.5, content_top - 0.02, f"Generated on: {generation_date}", ha='center', fontsize=10,
                     color='#333333')

            fig.text(0.5, content_top - 0.05, f"Filters: {filters}", ha='center', fontsize=9, color='#666666',
                     style='italic')

            logo_title_top = content_top - 0.08

            logo_path = "../ImageResources/MEDISYNCLogoBGRemoved.png"
            if os.path.exists(logo_path):
                try:
                    logo_width = 0.085
                    logo_height = 0.06
                    logo_ax = fig.add_axes(
                        [0.5 - (logo_width / 2), logo_title_top - logo_height / 2, logo_width, logo_height])
                    logo_ax.axis('off')
                    logo_img = plt.imread(logo_path)
                    logo_ax.imshow(logo_img, aspect='auto')
                except Exception as e:
                    print(f"Warning: Could not load logo: {e}")

            fig.text(0.5, logo_title_top - 0.025, report_type, ha='center', fontsize=16, weight='bold', color='#1a1a1a')

            table_top = logo_title_top - 0.04
            table_bottom = table_top - (table_height / total_height)
            table_ax = fig.add_axes([0.05, table_bottom, 0.9, table_top - table_bottom])
            table_ax.axis('off')

            table = table_ax.table(
                cellText=rows,
                colLabels=columns,
                loc='center',
                cellLoc='center',
                edges='closed'
            )
            table.auto_set_font_size(False)
            table.set_fontsize(7)
            table.scale(1, 1.2)

            for i in range(len(columns)):
                cell = table[(0, i)]
                cell.set_facecolor('#185777')
                cell.set_text_props(weight='bold', color='white')

            for i in range(1, len(rows) + 1):
                for j in range(len(columns)):
                    cell = table[(i, j)]
                    if i % 2 == 0:
                        cell.set_facecolor('#f0f0f0')

            table.auto_set_column_width(col=list(range(len(columns))))

            summary_y = table_bottom - 0.04
            fig.text(0.05, summary_y, 'Report Summary', ha='left', fontsize=14, weight='bold', color='#185777')

            fig.text(0.05, summary_y - 0.025, f"Total Records: {len(data)}", ha='left', fontsize=11, color='#1a1a1a')

            stats_lines = statistics.split('\n')
            y_offset = summary_y - 0.055
            for line in stats_lines:
                fig.text(0.05, y_offset, line, ha='left', fontsize=9, color='#333333', family='monospace')
                y_offset -= 0.02

            pdf.savefig(fig, bbox_inches='tight', dpi=300)
            plt.close(fig)

    def navigateToDashboard(self):
        """Navigate to Dashboard"""
        try:
            if self.reportsWindow:
                self.reportsWindow.close()
            from Controller.Admin.AdminDashboardController import AdminDashboardController
            AdminDashboardController().openDashboard()
        except Exception as e:
            print(f"Failed to navigate: {e}")

    def navigateToUsers(self):
        """Navigate to Users"""
        try:
            if self.reportsWindow:
                self.reportsWindow.close()
            from Controller.Admin.AdminUsersController import AdminUsersController
            AdminUsersController().openUsersWindow()
        except Exception as e:
            print(f"Failed to navigate: {e}")

    def navigateToPatients(self):
        """Navigate to Patients"""
        try:
            if self.reportsWindow:
                self.reportsWindow.close()
            from Controller.Admin.AdminPatientsController import AdminPatientsController
            AdminPatientsController().openPatientsWindow()
        except Exception as e:
            print(f"Failed to navigate: {e}")

    def navigateToNotifications(self):
        """Navigate to Notifications"""
        try:
            if self.reportsWindow:
                self.reportsWindow.close()
            from Controller.Admin.AdminNotificationsController import AdminNotificationsController
            AdminNotificationsController().openNotificationsWindow()
        except Exception as e:
            print(f"Failed to navigate: {e}")

    def logout(self):
        """Logout"""
        try:
            SessionManager.clear()
            if self.reportsWindow:
                self.reportsWindow.close()
            if self.summaryWindow:
                self.summaryWindow.close()
            from Controller.Login.LoginController import LoginController
            from Model.Authentication.LoginModel import LoginModel
            from View.LoginGUI import Login
            loginModel = LoginModel()
            loginView = Login()
            self.loginController = LoginController(loginModel, loginView)
            loginView.show()
        except Exception as e:
            print(f"Failed to logout: {e}")