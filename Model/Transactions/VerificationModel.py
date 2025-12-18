from Utilities.DatabaseConnection import getConnection

class VerificationModel:
    """
    Handles prescription verification transactions
    """

    @staticmethod
    def getPendingPrescriptions():
        """Returns all prescriptions pending verification"""
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
                    CONCAT(u.first_name, ' ', u.last_name) AS prescribed_by,
                    pr.created_at
                FROM prescriptions pr
                JOIN patients p ON pr.patient_id = p.patient_id
                JOIN medicines m ON pr.medicine_id = m.medicine_id
                JOIN users u ON pr.doctor_id = u.user_id
                WHERE pr.status = 'Pending Verification'
                ORDER BY pr.created_at DESC
            """

            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in getPendingPrescriptions: {e}")
            return []

    @staticmethod
    def searchPendingPrescriptions(query):
        """Searches pending prescriptions"""
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            sql_query = """
                SELECT
                    pr.prescription_id,
                    p.patient_first_name,
                    p.patient_last_name,
                    m.brand_name,
                    m.generic_name,
                    pr.dosage,
                    CONCAT(u.first_name, ' ', u.last_name) AS prescribed_by,
                    pr.created_at
                FROM prescriptions pr
                JOIN patients p ON pr.patient_id = p.patient_id
                JOIN medicines m ON pr.medicine_id = m.medicine_id
                JOIN users u ON pr.doctor_id = u.user_id
                WHERE pr.status = 'Pending Verification'
                  AND (p.patient_first_name LIKE %s 
                       OR p.patient_last_name LIKE %s
                       OR m.brand_name LIKE %s
                       OR m.generic_name LIKE %s
                       OR pr.prescription_id LIKE %s)
                ORDER BY pr.created_at DESC
            """

            search_term = f"%{query}%"
            cursor.execute(sql_query, (search_term, search_term, search_term, search_term, search_term))
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in searchPendingPrescriptions: {e}")
            return []

    @staticmethod
    def getPrescriptionDetailsForVerification(prescription_id):
        """Gets full prescription details for verification"""
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    pr.prescription_id,
                    pr.patient_id,
                    pr.doctor_id,
                    p.patient_first_name,
                    p.patient_last_name,
                    m.brand_name,
                    m.generic_name,
                    m.medicine_id,
                    pr.dosage,
                    pr.frequency,
                    CONCAT(u.first_name, ' ', u.last_name) AS prescribed_by
                FROM prescriptions pr
                JOIN patients p ON pr.patient_id = p.patient_id
                JOIN medicines m ON pr.medicine_id = m.medicine_id
                JOIN users u ON pr.doctor_id = u.user_id
                WHERE pr.prescription_id = %s
            """

            cursor.execute(query, (prescription_id,))
            record = cursor.fetchone()
            cursor.close()
            conn.close()
            return record
        except Exception as e:
            print(f"Error in getPrescriptionDetailsForVerification: {e}")
            return None

    @staticmethod
    def verifyPrescription(prescription_id, pharmacist_id, decision, lot_number,
                           quantity, expiry_date, reason=None):
        """
        Verifies a prescription and updates its status.
        Updates verification record, prescription status, and creates medicine_preparation record if approved.
        """
        try:
            conn = getConnection()
            cursor = conn.cursor()

            # Map decision to prescription status
            status_map = {
                "Approve": "Active",
                "Request Modification": "Modification Requested",
                "Reject": "Rejected"
            }

            new_prescription_status = status_map.get(decision)
            if not new_prescription_status:
                print(f"Invalid decision: {decision}")
                return False

            # Update verification record
            update_verification_query = """
                UPDATE prescription_verification
                SET pharmacist_id = %s,
                    medication_lot_number = %s,
                    quantity_dispensed = %s,
                    expiry_date = %s,
                    decision = %s,
                    reason = %s,
                    verified_at = NOW()
                WHERE prescription_id = %s
            """

            cursor.execute(update_verification_query, (
                pharmacist_id, lot_number, quantity,
                expiry_date, decision, reason, prescription_id
            ))

            # Update prescription status
            update_prescription_query = """
                UPDATE prescriptions 
                SET status = %s, updated_at = NOW()
                WHERE prescription_id = %s
            """

            cursor.execute(update_prescription_query, (new_prescription_status, prescription_id))

            # If approved, create medicine_preparation record
            if decision == "Approve":
                # Check if medicine_preparation record already exists
                check_prep_query = """
                    SELECT preparation_id 
                    FROM medicine_preparation 
                    WHERE prescription_id = %s
                """
                cursor.execute(check_prep_query, (prescription_id,))
                existing_prep = cursor.fetchone()

                if not existing_prep:
                    # Insert new medicine_preparation record
                    insert_prep_query = """
                        INSERT INTO medicine_preparation
                        (prescription_id, quantity_prepared, lot_number, status)
                        VALUES (%s, %s, %s, 'To be Prepared')
                    """
                    cursor.execute(insert_prep_query, (prescription_id, quantity, lot_number))
                    print(f"✓ Medicine preparation record created for prescription {prescription_id}")

            conn.commit()
            cursor.close()
            conn.close()

            print(f"✓ Prescription {prescription_id} verified: {decision} → Status: {new_prescription_status}")
            return True

        except Exception as e:
            print(f"Error in verifyPrescription: {e}")
            if conn:
                conn.rollback()
            return False

    @staticmethod
    def createNotification(user_id, related_table, related_id, title, message, notification_type):
        """Creates a notification record"""
        try:
            conn = getConnection()
            cursor = conn.cursor()

            query = """
                INSERT INTO notifications
                (user_id, related_table, related_id, title, message, type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                user_id, related_table, related_id, title, message, notification_type
            ))

            conn.commit()
            cursor.close()
            conn.close()

            print(f"✓ Notification created for user {user_id}")
            return True

        except Exception as e:
            print(f"Error in createNotification: {e}")
            return False