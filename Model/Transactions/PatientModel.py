from Utilities.DatabaseConnection import getConnection
from Model.SessionManager import SessionManager

class PatientsModel:
    """
    Handles database operations for Patient Management.
    """

    @staticmethod
    def getAllPatients():
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT p.patient_id, p.patient_first_name, p.patient_last_name, p.sex, p.room_number,
                       p.diagnosis, p.status, p.admission_date, p.date_of_birth,
                       p.emergency_contact_name, p.emergency_person_relationship, p.emergency_contact_number,
                       CONCAT(d.first_name, ' ', d.last_name) AS doctor_name, d.user_id AS doctor_id,
                       CONCAT(n.first_name, ' ', n.last_name) AS nurse_name, n.user_id AS nurse_id
                FROM patients p
                LEFT JOIN users d ON p.doctor_id = d.user_id
                LEFT JOIN users n ON p.nurse_id = n.user_id
                ORDER BY p.admission_date DESC
            """
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in getAllPatients: {e}")
            return []

    @staticmethod
    def searchPatients(query):
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            sql = """
                SELECT p.patient_id, p.patient_first_name, p.patient_last_name, p.sex, p.room_number,
                       p.diagnosis, p.status, p.admission_date, p.date_of_birth,
                       p.emergency_contact_name, p.emergency_person_relationship, p.emergency_contact_number,
                       CONCAT(d.first_name, ' ', d.last_name) AS doctor_name, d.user_id AS doctor_id,
                       CONCAT(n.first_name, ' ', n.last_name) AS nurse_name, n.user_id AS nurse_id
                FROM patients p
                LEFT JOIN users d ON p.doctor_id = d.user_id
                LEFT JOIN users n ON p.nurse_id = n.user_id
                WHERE p.patient_first_name LIKE %s OR p.patient_last_name LIKE %s OR p.room_number LIKE %s
                ORDER BY p.admission_date DESC
            """
            term = f"%{query}%"
            cursor.execute(sql, (term, term, term))
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in searchPatients: {e}")
            return []

    @staticmethod
    def getPatientById(patient_id):
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT p.patient_id, p.patient_first_name, p.patient_last_name, p.sex, p.room_number,
                       p.diagnosis, p.status, p.admission_date, p.date_of_birth,
                       p.emergency_contact_name, p.emergency_person_relationship, p.emergency_contact_number,
                       CONCAT(d.first_name, ' ', d.last_name) AS doctor_name, d.user_id AS doctor_id,
                       CONCAT(n.first_name, ' ', n.last_name) AS nurse_name, n.user_id AS nurse_id
                FROM patients p
                LEFT JOIN users d ON p.doctor_id = d.user_id
                LEFT JOIN users n ON p.nurse_id = n.user_id
                WHERE p.patient_id = %s
            """
            cursor.execute(query, (patient_id,))
            record = cursor.fetchone()
            cursor.close()
            conn.close()
            return record
        except Exception as e:
            print(f"Error in getPatientById: {e}")
            return None

    @staticmethod
    def registerPatient(**kwargs):
        """Register a new patient (no notifications for now)"""
        try:
            added_by = SessionManager.getUser().get('user_id')
            conn = getConnection()
            cursor = conn.cursor()
            query = """
                INSERT INTO patients (patient_first_name, patient_last_name, date_of_birth, sex,
                                      emergency_contact_name, emergency_person_relationship, emergency_contact_number,
                                      room_number, admission_date, diagnosis, doctor_id, nurse_id, added_by, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Active')
            """
            params = (
                kwargs['first_name'], kwargs['last_name'], kwargs['date_of_birth'], kwargs['sex'],
                kwargs['emergency_contact_name'], kwargs['emergency_person_relationship'], kwargs['emergency_contact_number'],
                kwargs['room_number'], kwargs['admission_date'], kwargs['diagnosis'], kwargs['doctor_id'], kwargs['nurse_id'],
                added_by
            )
            cursor.execute(query, params)
            conn.commit()
            patient_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return patient_id
        except Exception as e:
            print(f"Error in registerPatient: {e}")
            return None

    @staticmethod
    def updatePatient(patient_id, **kwargs):
        try:
            conn = getConnection()
            cursor = conn.cursor()
            query = """
                UPDATE patients SET patient_first_name=%s, patient_last_name=%s, date_of_birth=%s, sex=%s,
                                    emergency_contact_name=%s, emergency_person_relationship=%s, emergency_contact_number=%s,
                                    room_number=%s, admission_date=%s, diagnosis=%s, doctor_id=%s, nurse_id=%s, status=%s,
                                    updated_at=CURRENT_TIMESTAMP WHERE patient_id=%s
            """
            params = (
                kwargs['first_name'], kwargs['last_name'], kwargs['date_of_birth'], kwargs['sex'],
                kwargs['emergency_contact_name'], kwargs['emergency_person_relationship'], kwargs['emergency_contact_number'],
                kwargs['room_number'], kwargs['admission_date'], kwargs['diagnosis'], kwargs['doctor_id'], kwargs['nurse_id'],
                kwargs['status'], patient_id
            )
            cursor.execute(query, params)
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            conn.close()
            return affected > 0
        except Exception as e:
            print(f"Error in updatePatient: {e}")
            return False

    @staticmethod
    def getDoctorsList():
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT user_id, CONCAT(first_name, ' ', last_name) AS name
                FROM users WHERE role = 'Doctor' AND status = 'Active'
            """
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in getDoctorsList: {e}")
            return []

    @staticmethod
    def getNursesList():
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT user_id, CONCAT(first_name, ' ', last_name) AS name
                FROM users WHERE role = 'Nurse' AND status = 'Active'
            """
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in getNursesList: {e}")
            return []