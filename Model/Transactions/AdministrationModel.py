from Utilities.DatabaseConnection import getConnection
from Model.SessionManager import SessionManager
from datetime import datetime, date
import os

class AdministrationModel:
    """
    Handles medication administration records for nurses.
    """

    @staticmethod
    def recordMedicationAdministration(prescription_id, administration_time, patient_assessment, adverse_reactions,
                                       remarks=None, status='Administered'):
        """
        Records medication administration by the nurse.
        After successful recording, resets the corresponding medicine_preparation status
        back to 'To be Prepared' for the next dose cycle.
        """

        try:
            nurse_id = SessionManager.getUserId()
            if not nurse_id:
                print("Error: Nurse ID not found")
                return False

            conn = getConnection()
            cursor = conn.cursor()

            # Combine current date with provided time
            today = date.today()
            admin_datetime = f"{today} {administration_time}"

            # Insert administration record
            insert_query = """
                INSERT INTO medication_administration 
                (prescription_id, nurse_id, administration_time, patient_assessment, 
                 adverse_reactions, remarks, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                prescription_id,
                nurse_id,
                admin_datetime,
                patient_assessment,
                adverse_reactions,
                remarks,
                status
            ))

            # Reset preparation status to 'To be Prepared' for next dose
            reset_query = """
                UPDATE medicine_preparation 
                SET status = 'To be Prepared'
                WHERE prescription_id = %s 
                  AND status = 'Prepared'
            """
            cursor.execute(reset_query, (prescription_id,))

            conn.commit()

            cursor.close()
            conn.close()

            print(f"Medication administration recorded and preparation reset for prescription #{prescription_id}")
            return True

        except Exception as e:
            print(f"Error in recordMedicationAdministration: {e}")
            if conn:
                conn.rollback()
            return False

    @staticmethod
    def getLastAdministrationTime(prescription_id):
        """
        Gets the last administration time for a prescription.
        """
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT administration_time
                FROM medication_administration
                WHERE prescription_id = %s
                ORDER BY administration_time DESC
                LIMIT 1
            """

            cursor.execute(query, (prescription_id,))
            result = cursor.fetchone()

            cursor.close()
            conn.close()

            if result:
                return result['administration_time']
            return None

        except Exception as e:
            print(f"Error in getLastAdministrationTime: {e}")
            return None

    @staticmethod
    def calculateAdministrationStatus(prescription_id, frequency):
        """
        Calculates if administration is on time or missed based on frequency.
        """
        try:
            frequency_intervals = {
                "Once a day": 24,
                "Twice a day": 12,
                "Three times a day": 8,
                "Every 6 hours": 6,
                "Every 8 hours": 8
            }

            interval_hours = frequency_intervals.get(frequency)
            if not interval_hours:
                return 'Administered'  # Default if frequency unknown

            last_admin = AdministrationModel.getLastAdministrationTime(prescription_id)
            if not last_admin:
                return 'Administered'  # First administration

            # Calculate time difference
            now = datetime.now()
            time_diff = now - last_admin
            hours_since_last = time_diff.total_seconds() / 3600

            # If current time exceeds interval, it's missed (late)
            if hours_since_last > interval_hours:
                return 'Missed'
            else:
                return 'Administered'

        except Exception as e:
            print(f"Error in calculateAdministrationStatus: {e}")
            return 'Administered'

    @staticmethod
    def createNotification(user_id, related_table, related_id, title, message, notification_type):
        """
        Creates a notification record.
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

            print(f"✓ Notification created for user {user_id}")
            return True

        except Exception as e:
            print(f"Error in createNotification: {e}")
            return False

    @staticmethod
    def writeAuditLog(admin_data):
        """
        Writes administration record to temporary audit log file.
        """
        try:
            # Create audit log directory if it doesn't exist
            log_dir = "Logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # Create log file with current date
            log_filename = f"{log_dir}/medication_admin_{datetime.now().strftime('%Y%m%d')}.txt"

            # Format log entry
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"""
{'='*80}
MEDICATION ADMINISTRATION AUDIT LOG
{'='*80}
Timestamp: {timestamp}
Prescription ID: {admin_data.get('prescription_id', 'N/A')}
Patient: {admin_data.get('patient_name', 'N/A')}
Medication: {admin_data.get('medication', 'N/A')}
Dosage: {admin_data.get('dosage', 'N/A')}
Frequency: {admin_data.get('frequency', 'N/A')}
Administration Time: {admin_data.get('administration_time', 'N/A')}
Patient Assessment: {admin_data.get('patient_assessment', 'N/A')}
Adverse Reactions: {admin_data.get('adverse_reactions', 'None')}
Status: {admin_data.get('status', 'Administered')}
Administered By: {admin_data.get('nurse_name', 'N/A')} (ID: {admin_data.get('nurse_id', 'N/A')})
Remarks: {admin_data.get('remarks', 'None')}
{'='*80}

"""
            # Append to log file
            with open(log_filename, 'a', encoding='utf-8') as f:
                f.write(log_entry)

            print(f"✓ Audit log written to {log_filename}")
            return True

        except Exception as e:
            print(f"Error writing audit log: {e}")
            return False