from Utilities.DatabaseConnection import getConnection
from Model.SessionManager import SessionManager

class PrescriptionModel:
    """
    Handles prescription creation and updates
    """

    @staticmethod
    def createPrescription(patient_id, medicine_id, dosage, duration_start, duration_end,
                           frequency, special_instructions=None):
        """
        Creates a new prescription and related records.
        Inserts into prescriptions and prescription_verification tables atomically.
        """
        try:
            doctor_id = SessionManager.getUserId()
            if not doctor_id:
                print("Error: Doctor ID not found")
                return None

            conn = getConnection()
            cursor = conn.cursor()

            # Insert prescription
            prescription_query = """
                INSERT INTO prescriptions
                (patient_id, doctor_id, medicine_id, dosage, duration_start, 
                 duration_end, frequency, special_instructions, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Pending Verification')
            """

            cursor.execute(prescription_query, (
                patient_id, doctor_id, medicine_id, dosage,
                duration_start, duration_end, frequency, special_instructions
            ))

            prescription_id = cursor.lastrowid

            # Create corresponding prescription_verification record
            verification_query = """
                INSERT INTO prescription_verification
                (prescription_id, pharmacist_id, decision)
                VALUES (%s, NULL, NULL)
            """

            cursor.execute(verification_query, (prescription_id,))

            conn.commit()
            cursor.close()
            conn.close()

            print(f"✓ Prescription {prescription_id} created with verification record")
            return prescription_id

        except Exception as e:
            print(f"Error in createPrescription: {e}")
            if conn:
                conn.rollback()
            return None

    @staticmethod
    def updatePrescription(prescription_id, dosage=None, duration_start=None, duration_end=None,
                           frequency=None, special_instructions=None, medicine_id=None):
        """
        Updates an existing prescription record.
        Only provided fields are updated.
        """
        try:
            conn = getConnection()
            cursor = conn.cursor()

            # Build dynamic SQL for non-None fields
            fields = []
            values = []

            if dosage is not None:
                fields.append("dosage=%s")
                values.append(dosage)
            if duration_start is not None:
                fields.append("duration_start=%s")
                values.append(duration_start)
            if duration_end is not None:
                fields.append("duration_end=%s")
                values.append(duration_end)
            if frequency is not None:
                fields.append("frequency=%s")
                values.append(frequency)
            if special_instructions is not None:
                fields.append("special_instructions=%s")
                values.append(special_instructions)
            if medicine_id is not None:
                fields.append("medicine_id=%s")
                values.append(medicine_id)

            if not fields:
                cursor.close()
                conn.close()
                return False

            # Reset status to Pending Verification when updated
            fields.append("status='Pending Verification'")
            fields.append("updated_at=NOW()")

            values.append(prescription_id)
            query = f"UPDATE prescriptions SET {', '.join(fields)} WHERE prescription_id=%s"

            cursor.execute(query, tuple(values))
            conn.commit()

            success = cursor.rowcount > 0
            cursor.close()
            conn.close()

            print(f"✓ Prescription {prescription_id} updated")
            return success

        except Exception as e:
            print(f"Error in updatePrescription: {e}")
            if conn:
                conn.rollback()
            return False

    @staticmethod
    def getPrescriptionNotificationDetails(prescription_id):
        """
        Gets prescription details needed for notifications
        """
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    pr.prescription_id,
                    p.patient_first_name,
                    p.patient_last_name,
                    p.nurse_id,
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
            print(f"Error in getPrescriptionNotificationDetails: {e}")
            return None

    @staticmethod
    def getAllPharmacistIds():
        """
        Gets all active pharmacist user IDs for notifications
        """
        try:
            conn = getConnection()
            cursor = conn.cursor()

            query = """
                SELECT user_id 
                FROM users 
                WHERE role = 'Pharmacist' 
                  AND status = 'Active'
            """

            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()

            # Extract IDs from tuples
            pharmacist_ids = [row[0] for row in results]
            return pharmacist_ids

        except Exception as e:
            print(f"Error in getAllPharmacistIds: {e}")
            return []

    @staticmethod
    def createNotification(user_id, related_table, related_id, title, message, notification_type):
        """
        Creates a notification record
        """
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

            return True

        except Exception as e:
            print(f"Error in createNotification: {e}")
            return False