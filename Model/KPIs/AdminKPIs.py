from Utilities.DatabaseConnection import getConnection

class AdminKPIs:
    """
    KPI count methods for Admin.
    """

    @staticmethod
    def activeUsersCount():
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'Active'")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count
        except Exception as e:
            print(f"Error in activeUsersCount: {e}")
            return 0

    @staticmethod
    def activePatientsCount():
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM patients WHERE status = 'Active'")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count
        except Exception as e:
            print(f"Error in activePatientsCount: {e}")
            return 0

    @staticmethod
    def activePrescriptionsCount():
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM prescriptions WHERE status = 'Active'")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count
        except Exception as e:
            print(f"Error in activePrescriptionsCount: {e}")
            return 0

    @staticmethod
    def pendingPrescriptionsCount():
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM prescriptions WHERE status = 'Pending Verification'")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count
        except Exception as e:
            print(f"Error in pendingPrescriptionsCount: {e}")
            return 0

    @staticmethod
    def missedMedicationsCount():
        try:
            conn = getConnection()
            cursor = conn.cursor()
            query = """
                SELECT COUNT(*)
                FROM medication_administration ma
                JOIN prescriptions pr ON ma.prescription_id = pr.prescription_id
                JOIN patients p ON pr.patient_id = p.patient_id
                WHERE ma.status = 'Missed'
                  AND pr.status = 'Active'
                  AND p.status = 'Active'
                  AND DATE(ma.administration_time) = CURDATE()
            """
            cursor.execute(query)
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count
        except Exception as e:
            print(f"Error in missedMedicationsCount: {e}")
            return 0

class AdminKPIDetails:
    """
    Detailed records for each KPI.
    """

    @staticmethod
    def get_details(kpi_key: str):
        """Fetch details based on KPI key"""
        details_map = {
            "active_users": AdminKPIDetails._active_users,
            "active_patients": AdminKPIDetails._active_patients,
            "active_prescriptions": AdminKPIDetails._active_prescriptions,
            "pending_prescriptions": AdminKPIDetails._pending_prescriptions,
            "missed_medications": AdminKPIDetails._missed_medications,
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
            "active_users": ["User ID", "Name", "Role", "Status"],
            "active_patients": ["Patient ID", "Name", "Room Number", "Status"],
            "active_prescriptions": ["Prescription ID", "Patient", "Drug", "Status"],
            "pending_prescriptions": ["Prescription ID", "Patient", "Prescribed By", "Date"],
            "missed_medications": ["Nurse", "Patient", "Room", "Drug","Dosage","Frequency","Time (Late)"]
        }
        return mapping.get(kpi_key, ["No Data"])

    @staticmethod
    def _active_users():
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""
            SELECT user_id, CONCAT(first_name, ' ', last_name) AS name, 
                   role, status 
            FROM users 
            WHERE status = 'Active'
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    @staticmethod
    def _active_patients():
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""
            SELECT patient_id, CONCAT(patient_first_name, ' ', patient_last_name) AS name, 
                   room_number, status 
            FROM patients 
            WHERE status = 'Active'
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    @staticmethod
    def _active_prescriptions():
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""
            SELECT pr.prescription_id, 
                   CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient, 
                   m.generic_name AS drug, 
                   pr.status 
            FROM prescriptions pr
            JOIN patients p ON pr.patient_id = p.patient_id
            JOIN medicines m ON pr.medicine_id = m.medicine_id
            WHERE pr.status = 'Active'
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    @staticmethod
    def _pending_prescriptions():
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""
            SELECT pr.prescription_id, 
                   CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient, 
                   CONCAT(u.first_name, ' ', u.last_name) AS prescribed_by, 
                   pr.created_at AS date
            FROM prescriptions pr
            JOIN patients p ON pr.patient_id = p.patient_id
            JOIN users u ON pr.doctor_id = u.user_id
            WHERE pr.status = 'Pending Verification'
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    @staticmethod
    def _missed_medications():
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""
            SELECT CONCAT(u.first_name, ' ', u.last_name) AS nurse,
                   CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient, 
                   p.room_number,
                   m.generic_name AS drug, 
                   pr.dosage,
                   pr.frequency,
                   ma.administration_time
            FROM medication_administration ma
            JOIN prescriptions pr ON ma.prescription_id = pr.prescription_id
            JOIN patients p ON pr.patient_id = p.patient_id
            JOIN medicines m ON pr.medicine_id = m.medicine_id
            LEFT JOIN users u ON ma.nurse_id = u.user_id
            WHERE ma.status = 'Missed'
              AND pr.status = 'Active'
              AND p.status = 'Active'
              AND DATE(ma.administration_time) = CURDATE()
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
