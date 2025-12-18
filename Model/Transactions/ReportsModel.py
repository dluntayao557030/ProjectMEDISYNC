from Utilities.DatabaseConnection import getConnection

class ReportsModel:
    """
    Model for generating reports in MEDISYNC
    """

    @staticmethod
    def getPrescriptionRecords(from_date=None, to_date=None, patient_id=None, doctor_id=None):
        """Prescription Records Report - Matches prescriptions table schema"""
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                    SELECT 
                        pr.prescription_id AS id,
                        DATE(pr.created_at) AS date,
                        CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient,
                        CONCAT(m.generic_name, ' (', m.brand_name, ')') AS medication,
                        pr.dosage,
                        pr.frequency,
                        CONCAT(u.first_name, ' ', u.last_name) AS prescribed_by,
                        pr.status
                    FROM prescriptions pr
                    JOIN patients p ON pr.patient_id = p.patient_id
                    JOIN medicines m ON pr.medicine_id = m.medicine_id
                    JOIN users u ON pr.doctor_id = u.user_id
                    WHERE 1=1
                """
            params = []
            if from_date:
                query += " AND DATE(pr.created_at) >= %s"
                params.append(from_date)
            if to_date:
                query += " AND DATE(pr.created_at) <= %s"
                params.append(to_date)
            if patient_id:
                query += " AND pr.patient_id = %s"
                params.append(patient_id)
            if doctor_id:
                query += " AND pr.doctor_id = %s"
                params.append(doctor_id)
            query += " ORDER BY pr.created_at DESC"

            cursor.execute(query, params)
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error getPrescriptionRecords: {e}")
            return []

    @staticmethod
    def getMedicationPreparationRecords(from_date=None, to_date=None, patient_id=None):
        """Medication Preparation Records - Matches medicine_preparation table schema"""
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                    SELECT 
                        mp.preparation_id AS prep_id,
                        CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient,
                        m.generic_name AS medication,
                        mp.quantity_prepared AS quantity,
                        mp.status
                    FROM medicine_preparation mp
                    JOIN prescriptions pr ON mp.prescription_id = pr.prescription_id
                    JOIN patients p ON pr.patient_id = p.patient_id
                    JOIN medicines m ON pr.medicine_id = m.medicine_id
                    WHERE mp.lot_number IS NOT NULL
                """
            params = []
            if from_date:
                query += " AND DATE(pr.created_at) >= %s"
                params.append(from_date)
            if to_date:
                query += " AND DATE(pr.created_at) <= %s"
                params.append(to_date)
            if patient_id:
                query += " AND pr.patient_id = %s"
                params.append(patient_id)
            query += " ORDER BY mp.preparation_id DESC"

            cursor.execute(query, params)
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error getMedicationPreparationRecords: {e}")
            return []

    @staticmethod
    def getMedicationVerificationRecords(from_date=None, to_date=None, patient_id=None):
        """Medication Verification Records - Matches prescription_verification table schema"""
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                    SELECT 
                        pv.verification_id,
                        DATE(pv.verified_at) AS verified_at,
                        CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient,
                        m.generic_name AS medication,
                        pv.medication_lot_number AS lot_number,
                        pv.quantity_dispensed AS qty_dispensed,
                        DATE(pv.expiry_date) AS expiry,
                        CONCAT(u.first_name, ' ', u.last_name) AS pharmacist,
                        pv.decision
                    FROM prescription_verification pv
                    JOIN prescriptions pr ON pv.prescription_id = pr.prescription_id
                    JOIN patients p ON pr.patient_id = p.patient_id
                    JOIN medicines m ON pr.medicine_id = m.medicine_id
                    JOIN users u ON pv.pharmacist_id = u.user_id
                    WHERE 1=1
                """
            params = []
            if from_date:
                query += " AND DATE(pv.verified_at) >= %s"
                params.append(from_date)
            if to_date:
                query += " AND DATE(pv.verified_at) <= %s"
                params.append(to_date)
            if patient_id:
                query += " AND pr.patient_id = %s"
                params.append(patient_id)
            query += " ORDER BY pv.verified_at DESC"

            cursor.execute(query, params)
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error getMedicationVerificationRecords: {e}")
            return []

    @staticmethod
    def getNurseAdministrationLog(from_date=None, to_date=None, patient_id=None, nurse_id=None):
        """Nurse Administration Log - Matches medication_administration table schema"""
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                    SELECT 
                        ma.administration_id AS admin_id,
                        ma.administration_time AS time,
                        CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient,
                        m.generic_name AS medication,
                        pr.dosage,
                        ma.patient_assessment AS assessment,
                        ma.adverse_reactions,
                        CONCAT(u.first_name, ' ', u.last_name) AS nurse,
                        ma.status,
                        ma.remarks
                    FROM medication_administration ma
                    JOIN prescriptions pr ON ma.prescription_id = pr.prescription_id
                    JOIN patients p ON pr.patient_id = p.patient_id
                    JOIN medicines m ON pr.medicine_id = m.medicine_id
                    JOIN users u ON ma.nurse_id = u.user_id
                    WHERE 1=1
                """
            params = []
            if from_date:
                query += " AND DATE(ma.administration_time) >= %s"
                params.append(from_date)
            if to_date:
                query += " AND DATE(ma.administration_time) <= %s"
                params.append(to_date)
            if patient_id:
                query += " AND pr.patient_id = %s"
                params.append(patient_id)
            if nurse_id:
                query += " AND ma.nurse_id = %s"
                params.append(nurse_id)
            query += " ORDER BY ma.administration_time DESC"

            cursor.execute(query, params)
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error getNurseAdministrationLog: {e}")
            return []

    @staticmethod
    def getMissedAdministrations(patient_id=None, nurse_id=None):
        """Retrieves all medication administrations marked as 'Missed'"""
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    ma.administration_id,
                    ma.administration_time AS scheduled_time,
                    CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient,
                    IFNULL(p.room_number, 'N/A') AS room,
                    m.generic_name AS medication,
                    pr.dosage,
                    CONCAT(u.first_name, ' ', u.last_name) AS nurse,
                    ma.status,
                    ma.remarks
                FROM medication_administration ma
                JOIN prescriptions pr ON ma.prescription_id = pr.prescription_id
                JOIN patients p ON pr.patient_id = p.patient_id
                JOIN medicines m ON pr.medicine_id = m.medicine_id
                JOIN users u ON ma.nurse_id = u.user_id
                WHERE ma.status = 'Missed'
            """
            params = []

            if patient_id:
                query += " AND pr.patient_id = %s"
                params.append(patient_id)
            if nurse_id:
                query += " AND ma.nurse_id = %s"
                params.append(nurse_id)

            query += " ORDER BY ma.administration_time DESC"

            cursor.execute(query, params)
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in getMissedAdministrations: {e}")
            return []

    @staticmethod
    def getControlledSubstancesActivity(from_date=None, to_date=None, doctor_id=None):
        """Controlled Substances Activity - Prescriptions with is_controlled = TRUE"""
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                    SELECT 
                        pr.prescription_id AS id,
                        DATE(pr.created_at) AS date,
                        m.generic_name AS medication,
                        IFNULL(m.brand_name, 'N/A') AS brand,
                        CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient,
                        pr.dosage,
                        pr.frequency,
                        CONCAT(d.first_name, ' ', d.last_name) AS prescribed_by,
                        IFNULL(pv.quantity_dispensed, 'Pending') AS qty_dispensed,
                        IFNULL(CONCAT(ph.first_name, ' ', ph.last_name), 'Not Verified') AS pharmacist,
                        pr.status
                    FROM prescriptions pr
                    JOIN medicines m ON pr.medicine_id = m.medicine_id
                    JOIN patients p ON pr.patient_id = p.patient_id
                    JOIN users d ON pr.doctor_id = d.user_id
                    LEFT JOIN prescription_verification pv ON pr.prescription_id = pv.prescription_id
                    LEFT JOIN users ph ON pv.pharmacist_id = ph.user_id
                    WHERE m.is_controlled = TRUE
                """
            params = []
            if from_date:
                query += " AND DATE(pr.created_at) >= %s"
                params.append(from_date)
            if to_date:
                query += " AND DATE(pr.created_at) <= %s"
                params.append(to_date)
            if doctor_id:
                query += " AND pr.doctor_id = %s"
                params.append(doctor_id)
            query += " ORDER BY pr.created_at DESC"

            cursor.execute(query, params)
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error getControlledSubstancesActivity: {e}")
            return []

    @staticmethod
    def getPatientsList():
        """Returns list of active patients for dropdowns"""
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    patient_id, 
                    CONCAT(patient_first_name, ' ', patient_last_name) AS name
                FROM patients
                WHERE status = 'Active'
                ORDER BY patient_first_name, patient_last_name
            """
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in getPatientsList: {e}")
            return []