from Utilities.DatabaseConnection import getConnection
from Model.SessionManager import SessionManager

class NurseTables:
    """
    Table data retrieval methods for Nurse
    """

    @staticmethod
    def getCompletedMedicationsToday():
        """
        Returns medications administered today by the logged-in nurse.
        """
        try:
            nurse_id = SessionManager.getUserId()
            if not nurse_id:
                return []

            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient_name,
                    COALESCE(m.generic_name, m.brand_name, 'Unknown Medication') AS medication,
                    pr.dosage,
                    ma.administration_time,
                    ma.patient_assessment,
                    ma.status
                FROM medication_administration ma
                JOIN prescriptions pr ON ma.prescription_id = pr.prescription_id
                JOIN patients p ON pr.patient_id = p.patient_id
                JOIN medicines m ON pr.medicine_id = m.medicine_id
                WHERE ma.nurse_id = %s
                  AND DATE(ma.administration_time) = CURDATE()
                  AND ma.status IN ('Administered','Missed')
                ORDER BY ma.administration_time DESC
            """

            cursor.execute(query, (nurse_id,))
            records = cursor.fetchall()

            # Format time for better display (optional, but consistent with other modules)
            for record in records:
                if record['administration_time']:
                    record['administration_time'] = record['administration_time'].strftime('%Y-%m-%d %H:%M:%S')

            cursor.close()
            conn.close()
            return records

        except Exception as e:
            print(f"Error in getCompletedMedicationsToday: {e}")
            return []

    @staticmethod
    def getMedicationPreparationStatus():
        try:
            nurse_id = SessionManager.getUserId()
            if not nurse_id:
                return []

            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                        SELECT 
                            mp.preparation_id,
                            pr.prescription_id,
                            p.patient_first_name,
                            p.patient_last_name,
                            m.brand_name,
                            pr.dosage,
                            mp.status,
                            pr.frequency
                        FROM medicine_preparation mp
                        JOIN prescriptions pr ON mp.prescription_id = pr.prescription_id
                        JOIN patients p ON pr.patient_id = p.patient_id
                        JOIN medicines m ON pr.medicine_id = m.medicine_id
                        WHERE p.nurse_id = %s
                          AND p.status = 'Active'
                          AND pr.status = 'Active'
                          AND pr.duration_start <= CURDATE()
                          AND pr.duration_end >= CURDATE()
                          AND (
                            mp.status = 'To be Prepared'
                            OR (
                              mp.status = 'Prepared'
                            )
                          )
                        ORDER BY 
                            CASE mp.status 
                                WHEN 'To be Prepared' THEN 1 
                                WHEN 'Prepared' THEN 2 
                            END,
                            pr.created_at DESC
                    """

            cursor.execute(query, (nurse_id,))
            records = cursor.fetchall()

            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in getMedicationPreparationStatus: {e}")
            return []

    @staticmethod
    def getAssignedPatients():
        """
        Returns active patients assigned to the nurse.
        """
        try:
            nurse_id = SessionManager.getUserId()
            if not nurse_id:
                return []

            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT DISTINCT
                    p.patient_id,
                    p.patient_first_name,
                    p.patient_last_name,
                    p.date_of_birth,
                    p.sex,
                    p.room_number,
                    p.diagnosis,
                    m.generic_name,
                    m.brand_name
                FROM patients p
                JOIN prescriptions pr ON p.patient_id = pr.patient_id
                JOIN medicine_preparation mp ON pr.prescription_id = mp.prescription_id
                JOIN medicines m ON pr.medicine_id = m.medicine_id
                WHERE p.nurse_id = %s
                  AND p.status = 'Active'
                  AND pr.status = 'Active'
                  AND pr.duration_start <= CURDATE()
                  AND pr.duration_end >= CURDATE()
                  AND mp.status = 'Prepared'
                ORDER BY p.room_number, p.patient_last_name
            """

            cursor.execute(query, (nurse_id,))
            records = cursor.fetchall()

            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in getAssignedPatients: {e}")
            return []

    @staticmethod
    def searchAssignedPatients(query):
        """
        Searches assigned patients by name, room number, or ID
        — includes generic and brand name of ready medication.
        """
        try:
            nurse_id = SessionManager.getUserId()
            if not nurse_id:
                return []

            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            sql_query = """
                SELECT DISTINCT
                    p.patient_id,
                    p.patient_first_name,
                    p.patient_last_name,
                    p.date_of_birth,
                    p.sex,
                    p.room_number,
                    p.diagnosis,
                    m.generic_name,
                    m.brand_name
                FROM patients p
                JOIN prescriptions pr ON p.patient_id = pr.patient_id
                JOIN medicine_preparation mp ON pr.prescription_id = mp.prescription_id
                JOIN medicines m ON pr.medicine_id = m.medicine_id
                WHERE p.nurse_id = %s
                  AND p.status = 'Active'
                  AND pr.status = 'Active'
                  AND pr.duration_start <= CURDATE()
                  AND pr.duration_end >= CURDATE()
                  AND mp.status = 'Prepared'
                  AND NOT EXISTS (
                      SELECT 1 
                      FROM medication_administration ma 
                      WHERE ma.prescription_id = pr.prescription_id
                        AND ma.status = 'Administered'
                        AND DATE(ma.administration_time) = CURDATE()
                  )
                  AND (
                      p.patient_first_name LIKE %s 
                      OR p.patient_last_name LIKE %s 
                      OR p.room_number LIKE %s
                      OR CAST(p.patient_id AS CHAR) LIKE %s
                  )
                ORDER BY p.room_number, p.patient_last_name
            """

            search_term = f"%{query}%"
            cursor.execute(sql_query, (nurse_id, search_term, search_term, search_term, search_term))
            records = cursor.fetchall()

            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in searchAssignedPatients: {e}")
            return []

    @staticmethod
    def getActivePrescriptionsForPatient(patient_id,generic_name, brand_name):
        """
        Gets all active prescriptions for a specific patient.
        """
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                        SELECT 
                            pr.doctor_id,
                            pr.prescription_id,
                            pr.patient_id,
                            m.medicine_id,
                            m.brand_name,
                            m.generic_name,
                            pr.dosage,
                            pr.frequency,
                            pr.duration_start,
                            pr.duration_end,
                            pr.special_instructions,
                            CONCAT(u.first_name, ' ', u.last_name) AS prescribed_by,
                            pv.medication_lot_number,
                            pv.expiry_date
                        FROM prescriptions pr
                        JOIN medicines m ON pr.medicine_id = m.medicine_id
                        JOIN users u ON pr.doctor_id = u.user_id
                        LEFT JOIN prescription_verification pv ON pr.prescription_id = pv.prescription_id
                        WHERE pr.patient_id = %s
                          AND pr.status = 'Active'
                          AND pr.duration_start <= CURDATE()
                          AND pr.duration_end >= CURDATE()
                          AND m.generic_name = %s
                          AND m.brand_name = %s
                        ORDER BY pr.created_at DESC
                    """

            cursor.execute(query, (patient_id,generic_name, brand_name))
            records = cursor.fetchall()

            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in getActivePrescriptionsForPatient: {e}")
            return []