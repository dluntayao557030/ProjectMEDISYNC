from Utilities.DatabaseConnection import getConnection
from Model.SessionManager import SessionManager

class DoctorTables:
    """
    Contains all Table-related methods for Doctor user
    """

    @staticmethod
    def getPatientHistory():
        """
        Returns patient history records for the logged-in doctor.
        Focuses on admission date, patient name, diagnosis, and prescription summary.
        """
        try:
            user_id = SessionManager.getUserId()
            if not user_id:
                return []

            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    p.patient_id,
                    CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient_name,
                    p.date_of_birth,
                    p.sex,
                    p.admission_date,
                    p.diagnosis,
                    GROUP_CONCAT(
                        CONCAT(m.brand_name, ' (', pr.dosage, '/', pr.frequency, ')') 
                        SEPARATOR ', '
                    ) AS prescriptions
                FROM prescriptions pr
                JOIN patients p ON pr.patient_id = p.patient_id
                JOIN medicines m ON pr.medicine_id = m.medicine_id
                WHERE pr.doctor_id = %s
                GROUP BY p.patient_id
                ORDER BY p.admission_date DESC
            """

            cursor.execute(query, (user_id,))
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records

        except Exception as e:
            print(f"Error in getPatientHistory: {e}")
            return []

    @staticmethod
    def getPendingPrescriptions():
        """Returns pending prescriptions for the logged-in doctor"""
        try:
            user_id = SessionManager.getUserId()
            if not user_id:
                return []

            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    pr.prescription_id,
                    CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient_name,
                    m.brand_name AS medicine_brand,
                    pr.dosage,
                    pr.frequency,
                    CONCAT(
                        DATE_FORMAT(pr.duration_start, '%Y-%m-%d'), 
                        ' → ', 
                        DATE_FORMAT(pr.duration_end, '%Y-%m-%d')
                    ) AS duration,
                    pr.status AS prescription_status
                FROM prescriptions pr
                JOIN patients p ON pr.patient_id = p.patient_id
                JOIN medicines m ON pr.medicine_id = m.medicine_id
                WHERE pr.doctor_id = %s 
                  AND pr.status = 'Pending Verification'
                ORDER BY pr.duration_start DESC
            """

            cursor.execute(query, (user_id,))
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records

        except Exception as e:
            print(f"Error in getPendingPrescriptions: {e}")
            return []

    @staticmethod
    def getPatientsByDoctor():
        """Returns only patients assigned to or prescribed by the current doctor"""
        try:
            doctor_id = SessionManager.getUserId()
            if not doctor_id:
                return []

            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                    SELECT DISTINCT
                        p.patient_id,
                        p.patient_first_name,
                        p.patient_last_name,
                        p.date_of_birth,
                        p.sex
                    FROM patients p
                    WHERE p.doctor_id = %s
                      AND p.status = 'Active'
                    ORDER BY p.patient_last_name, p.patient_first_name
                """

            cursor.execute(query, (doctor_id,))
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in getPatientsByDoctor: {e}")
            return []

    @staticmethod
    def searchPatientsByDoctor(query):
        """
        Search doctor's patients by name or ID
        """
        try:
            doctor_id = SessionManager.getUserId()
            if not doctor_id:
                return []

            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            search_term = f"%{query}%"
            query_str = """
                    SELECT DISTINCT
                        p.patient_id,
                        p.patient_first_name,
                        p.patient_last_name,
                        p.date_of_birth,
                        p.sex
                    FROM patients p
                    JOIN prescriptions pr ON p.patient_id = pr.patient_id
                    WHERE pr.doctor_id = %s
                      AND p.status = 'Active'
                      AND (
                          p.patient_first_name LIKE %s OR
                          p.patient_last_name LIKE %s OR
                          CAST(p.patient_id AS CHAR) LIKE %s
                      )
                    ORDER BY p.patient_last_name, p.patient_first_name
                """

            cursor.execute(query_str, (doctor_id, search_term, search_term, search_term))
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except Exception as e:
            print(f"Error in searchPatientsByDoctor: {e}")
            return []

    @staticmethod
    def searchMedicines(query):
        """Search medicines by brand or generic name"""
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query_str = """
                SELECT 
                    medicine_id,
                    brand_name,
                    generic_name,
                    formulation,
                    strength,
                    is_controlled
                FROM medicines
                WHERE brand_name LIKE %s 
                   OR generic_name LIKE %s
                ORDER BY brand_name
            """

            search_term = f"%{query}%"
            cursor.execute(query_str, (search_term, search_term))
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results

        except Exception as e:
            print(f"Error in searchMedicines: {e}")
            return []

    @staticmethod
    def getAllMedicines():
        """Get all medicines"""
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    medicine_id,
                    brand_name,
                    generic_name,
                    formulation,
                    strength,
                    is_controlled
                FROM medicines
                ORDER BY brand_name
            """

            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results

        except Exception as e:
            print(f"Error in getAllMedicines: {e}")
            return []

    @staticmethod
    def searchPrescriptionsByDoctor(doctor_id, query):
        """Search prescriptions by patient name or prescription ID"""
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query_str = """
                SELECT 
                    pr.prescription_id,
                    p.patient_first_name,
                    p.patient_last_name,
                    m.brand_name,
                    m.generic_name,
                    pr.dosage,
                    pr.status
                FROM prescriptions pr
                JOIN patients p ON pr.patient_id = p.patient_id
                JOIN medicines m ON pr.medicine_id = m.medicine_id
                WHERE pr.doctor_id = %s 
                  AND (p.patient_first_name LIKE %s 
                       OR p.patient_last_name LIKE %s 
                       OR pr.prescription_id LIKE %s)
                  AND pr.status IN ('Pending Verification', 'Modification Requested')
                ORDER BY pr.created_at DESC
            """

            search_term = f"%{query}%"
            cursor.execute(query_str, (doctor_id, search_term, search_term, search_term))
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results

        except Exception as e:
            print(f"Error in searchPrescriptionsByDoctor: {e}")
            return []

    @staticmethod
    def getAllPrescriptionsByDoctor(doctor_id):
        """Get all prescriptions for a doctor"""
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    pr.prescription_id,
                    p.patient_first_name,
                    p.patient_last_name,
                    m.brand_name,
                    m.generic_name,
                    pr.dosage,
                    pr.status
                FROM prescriptions pr
                JOIN patients p ON pr.patient_id = p.patient_id
                JOIN medicines m ON pr.medicine_id = m.medicine_id
                WHERE pr.doctor_id = %s
                  AND pr.status IN ('Pending Verification', 'Modification Requested')
                ORDER BY pr.created_at DESC
            """

            cursor.execute(query, (doctor_id,))
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results

        except Exception as e:
            print(f"Error in getAllPrescriptionsByDoctor: {e}")
            return []

    @staticmethod
    def getPrescriptionById(prescription_id):
        """Get full details of a prescription"""
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    pr.*,
                    p.patient_first_name,
                    p.patient_last_name,
                    m.brand_name,
                    m.generic_name
                FROM prescriptions pr
                JOIN patients p ON pr.patient_id = p.patient_id
                JOIN medicines m ON pr.medicine_id = m.medicine_id
                WHERE pr.prescription_id = %s
            """

            cursor.execute(query, (prescription_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result

        except Exception as e:
            print(f"Error in getPrescriptionById: {e}")
            return None