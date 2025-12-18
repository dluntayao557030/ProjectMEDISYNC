from Utilities.DatabaseConnection import getConnection
from Model.SessionManager import SessionManager

class NurseKPIs:
    """
    KPI count methods for Nurse
    """

    @staticmethod
    def assignedPatientsCount():
        try:
            nurse_id = SessionManager.getUserId()
            if not nurse_id:
                return 0

            conn = getConnection()
            cursor = conn.cursor()

            query = "SELECT COUNT(*) FROM patients WHERE nurse_id = %s AND status = 'Active'"
            cursor.execute(query, (nurse_id,))
            count = cursor.fetchone()[0]

            cursor.close()
            conn.close()
            return count
        except Exception as e:
            print(f"Error in assignedPatientsCount: {e}")
            return 0

    @staticmethod
    def dueMedicationsCount():
        """
        Counts due medications for the nurse today
        """
        try:
            nurse_id = SessionManager.getUserId()
            if not nurse_id:
                return 0

            conn = getConnection()
            cursor = conn.cursor()

            query = """
                SELECT COUNT(*) 
                FROM prescriptions pr
                JOIN patients p ON pr.patient_id = p.patient_id
                JOIN medicine_preparation mp ON pr.prescription_id = mp.prescription_id
                WHERE p.nurse_id = %s
                  AND p.status = 'Active'
                  AND pr.status = 'Active'
                  AND pr.duration_start <= CURDATE()
                  AND pr.duration_end >= CURDATE()
                  AND mp.status = 'Prepared'
            """

            cursor.execute(query, (nurse_id,))
            count = cursor.fetchone()[0]

            cursor.close()
            conn.close()
            return count

        except Exception as e:
            print(f"Error in dueMedicationsCount: {e}")
            return 0

    @staticmethod
    def urgentMedicationsCount():
        try:
            nurse_id = SessionManager.getUserId()
            if not nurse_id:
                return 0

            conn = getConnection()
            cursor = conn.cursor()

            query = """
                SELECT COUNT(*) FROM medication_administration ma
                JOIN prescriptions pr ON ma.prescription_id = pr.prescription_id
                JOIN patients p ON pr.patient_id = p.patient_id
                WHERE ma.nurse_id = %s
                  AND ma.status = 'Missed'
                  AND DATE(ma.administration_time) = CURDATE()
            """
            cursor.execute(query, (nurse_id,))
            count = cursor.fetchone()[0]

            cursor.close()
            conn.close()
            return count
        except Exception as e:
            print(f"Error in urgentMedicationsCount: {e}")
            return 0

class NurseKPIDetails:
    """
    Detailed records for each KPI
    """

    @staticmethod
    def get_details(kpi_key: str):
        details_map = {
            "assigned_patients": NurseKPIDetails._assigned_patients,
            "due_medications": NurseKPIDetails._due_medications,
            "urgent": NurseKPIDetails._urgent_medications,
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
        mapping = {
            "assigned_patients": ["Patient ID", "Name", "Room Number", "Diagnosis"],
            "due_medications": ["Prescription ID", "Patient", "Medication", "Dosage", "Due Time"],
            "urgent": ["Prescription ID", "Patient", "Medication", "Dosage", "Scheduled Time","Status"],
        }
        return mapping.get(kpi_key, ["No Data"])

    @staticmethod
    def _assigned_patients():
        nurse_id = SessionManager.getUserId()
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""
            SELECT patient_id, CONCAT(patient_first_name, ' ', patient_last_name) AS name, 
                   room_number, diagnosis 
            FROM patients 
            WHERE nurse_id = %s AND status = 'Active'
        """, (nurse_id,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    @staticmethod
    def _due_medications():
        """
        Returns detailed list of due medications for the nurse for the day.
        """
        try:
            nurse_id = SessionManager.getUserId()
            if not nurse_id:
                return []

            conn = getConnection()
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    pr.prescription_id,
                    CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient,
                    CONCAT (m.generic_name,' ',m.brand_name) AS medication,
                    pr.dosage,
                    pr.frequency AS due_time_info
                FROM prescriptions pr
                JOIN patients p ON pr.patient_id = p.patient_id
                JOIN medicines m ON pr.medicine_id = m.medicine_id
                JOIN medicine_preparation mp ON pr.prescription_id = mp.prescription_id
                WHERE p.nurse_id = %s
                  AND p.status = 'Active'
                  AND pr.status = 'Active'
                  AND pr.duration_start <= CURDATE()
                  AND pr.duration_end >= CURDATE()
                  AND mp.status = 'Prepared'
                ORDER BY p.room_number, p.patient_last_name
            """, (nurse_id,))
            data = cur.fetchall()
            cur.close()
            conn.close()
            return data

        except Exception as e:
            print(f"Error in _due_medications: {e}")
            return []

    @staticmethod
    def _urgent_medications():
        nurse_id = SessionManager.getUserId()
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""
            SELECT ma.prescription_id, 
                   CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient, 
                   m.generic_name AS medication, pr.dosage, ma.administration_time AS scheduled_time, 
                   ma.status
            FROM medication_administration ma
            JOIN prescriptions pr ON ma.prescription_id = pr.prescription_id
            JOIN patients p ON pr.patient_id = p.patient_id
            JOIN medicines m ON pr.medicine_id = m.medicine_id
            WHERE ma.nurse_id = %s AND ma.status = 'Missed' AND DATE(ma.administration_time) = CURDATE()
        """, (nurse_id,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data