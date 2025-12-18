from Model.SessionManager import SessionManager
from Utilities.DatabaseConnection import getConnection

class DoctorKPIs:
    """
    Contains all KPI-related methods for a Doctor user.
    """

    @staticmethod
    def activePatientsCount():
        """
        Returns the count of active patients assigned to the logged-in doctor.
        """

        doctorId = SessionManager.getUserId()
        if not doctorId:
            return 0

        conn = getConnection()
        cursor = conn.cursor()
        query = """
            SELECT COUNT(*) FROM patients
            WHERE doctor_id = %s AND status = 'Active'
        """
        cursor.execute(query, (doctorId,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count

    @staticmethod
    def activePrescriptionsCount():
        """
        Returns the count of active prescriptions for this doctor.
        """

        doctorId = SessionManager.getUserId()
        if not doctorId:
            return 0

        conn = getConnection()
        cursor = conn.cursor()
        query = """
            SELECT COUNT(*) FROM prescriptions
            WHERE doctor_id = %s AND status = 'Active'
        """
        cursor.execute(query, (doctorId,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count

    @staticmethod
    def urgentCasesCount():
        """
        Returns the count of urgent notifications or prescriptions for this doctor.
        """

        doctorId = SessionManager.getUserId()
        if not doctorId:
            return 0

        conn = getConnection()
        cursor = conn.cursor()
        query = """
            SELECT COUNT(*) FROM notifications
            WHERE user_id = %s AND type = 'Urgent'
        """
        cursor.execute(query, (doctorId,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count

class DoctorKPIDetails:
    """
    Detailed records for each KPI.
    """

    @staticmethod
    def get_details(kpi_key: str):
        """Fetch details based on KPI key"""
        details_map = {
            "active_patients": DoctorKPIDetails._active_patients,
            "active_prescriptions": DoctorKPIDetails._active_prescriptions,
            "urgent": DoctorKPIDetails._urgent_notifications
        }
        func = details_map.get(kpi_key)
        if func:
            try:
                return func()
            except Exception as e:
                print(f"Error fetching details for {kpi_key}: {e}")
                return []
        return []

    @staticmethod
    def get_columns(kpi_key: str):
        """Get column names for the KPI"""
        mapping = {
            "active_patients": ["Patient ID", "Name", "Room Number", "Diagnosis"],
            "active_prescriptions": ["Prescription ID", "Patient", "Drug", "Dosage"],
            "urgent": ["Notification ID", "Title", "Message", "Time"]
        }
        return mapping.get(kpi_key, ["No Data"])

    @staticmethod
    def _active_patients():
        doctor_id = SessionManager.getUserId()
        if not doctor_id:
            return []

        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                p.patient_id,
                CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS name,
                p.room_number,
                p.diagnosis
            FROM patients p
            WHERE p.doctor_id = %s
              AND p.status = 'Active'
            GROUP BY p.patient_id
        """, (doctor_id,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    @staticmethod
    def _active_prescriptions():
        doctor_id = SessionManager.getUserId()
        if not doctor_id:
            return []

        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                pr.prescription_id,
                CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient,
                m.generic_name AS drug,
                pr.dosage
            FROM prescriptions pr
            JOIN patients p ON pr.patient_id = p.patient_id
            JOIN medicines m ON pr.medicine_id = m.medicine_id
            WHERE pr.doctor_id = %s
              AND pr.status = 'Active'
        """, (doctor_id,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    @staticmethod
    def _urgent_notifications():
        doctor_id = SessionManager.getUserId()
        if not doctor_id:
            return []

        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                notification_id,
                title,
                message,
                created_at AS time
            FROM notifications
            WHERE user_id = %s
              AND type = 'Urgent'
            ORDER BY created_at DESC
        """, (doctor_id,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data