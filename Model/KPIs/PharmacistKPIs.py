from Utilities.DatabaseConnection import getConnection

class PharmacistKPIs:
    """
    KPI count methods for Pharmacist
    """

    @staticmethod
    def activePrescriptionsCount():
        try:
            conn = getConnection()
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM prescriptions WHERE status = 'Active'"
            cursor.execute(query)
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count
        except Exception as e:
            print(f"Error in activePrescriptionsCount: {e}")
            return 0

    @staticmethod
    def pendingVerificationCount():
        try:
            conn = getConnection()
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM prescriptions WHERE status = 'Pending Verification'"
            cursor.execute(query)
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count
        except Exception as e:
            print(f"Error in pendingVerificationCount: {e}")
            return 0

    @staticmethod
    def controlledSubstancesCount():
        try:
            conn = getConnection()
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM prescriptions pr JOIN medicines m ON pr.medicine_id = m.medicine_id WHERE m.is_controlled = TRUE AND pr.status = 'Active'"
            cursor.execute(query)
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count
        except Exception as e:
            print(f"Error in controlledSubstancesCount: {e}")
            return 0

class PharmacistKPIDetails:
    """Detailed records for Pharmacist KPIs"""

    @staticmethod
    def get_details(kpi_key: str):
        details_map = {
            "active_prescriptions": PharmacistKPIDetails._active_prescriptions,
            "pending_verification": PharmacistKPIDetails._pending_verification,
            "controlled_substances": PharmacistKPIDetails._controlled_substances,
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
            "active_prescriptions": ["Prescription ID", "Patient", "Medication", "Prescribed By", "Status"],
            "pending_verification": ["Prescription ID", "Patient", "Medication", "Prescribed By", "Date"],
            "controlled_substances": ["Prescription ID", "Patient", "Medication", "Dosage", "Prescribed By", "Status"],
        }
        return mapping.get(kpi_key, ["No Data"])

    @staticmethod
    def _active_prescriptions():
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                pr.prescription_id, 
                CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient, 
                m.generic_name AS medication, 
                CONCAT(u.first_name, ' ', u.last_name) AS prescribed_by, 
                pr.status
            FROM prescriptions pr
            JOIN patients p ON pr.patient_id = p.patient_id
            JOIN medicines m ON pr.medicine_id = m.medicine_id
            JOIN users u ON pr.doctor_id = u.user_id
            WHERE pr.status = 'Active'
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    @staticmethod
    def _pending_verification():
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                pr.prescription_id, 
                CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient, 
                m.generic_name AS medication, 
                CONCAT(u.first_name, ' ', u.last_name) AS prescribed_by, 
                pr.created_at AS date
            FROM prescriptions pr
            JOIN patients p ON pr.patient_id = p.patient_id
            JOIN medicines m ON pr.medicine_id = m.medicine_id
            JOIN users u ON pr.doctor_id = u.user_id
            WHERE pr.status = 'Pending Verification'
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    @staticmethod
    def _controlled_substances():
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                pr.prescription_id, 
                CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient, 
                m.generic_name AS medication, 
                pr.dosage, 
                CONCAT(u.first_name, ' ', u.last_name) AS prescribed_by, 
                pr.status
            FROM prescriptions pr
            JOIN patients p ON pr.patient_id = p.patient_id
            JOIN medicines m ON pr.medicine_id = m.medicine_id
            JOIN users u ON pr.doctor_id = u.user_id
            WHERE m.is_controlled = TRUE AND pr.status = 'Active'
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data