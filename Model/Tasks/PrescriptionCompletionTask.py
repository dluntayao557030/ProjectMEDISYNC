from Utilities.DatabaseConnection import getConnection
from Model.Notifications.NotificationsModel import NotificationsModel
from datetime import date

def complete_expired_prescriptions():
    """
    Checks all Active prescriptions.
    If duration_end < today, changes status to 'Completed'
    and creates a notification for the prescribing doctor.

    Safe to call on every login (idempotent).
    """
    today = date.today()

    try:
        conn = getConnection()
        cursor = conn.cursor(dictionary=True)

        # Step 1: Find all Active prescriptions where duration_end has passed
        find_query = """
            SELECT 
                pr.prescription_id,
                pr.doctor_id,
                CONCAT(p.patient_first_name, ' ', p.patient_last_name) AS patient_name,
                m.brand_name,
                m.generic_name
            FROM prescriptions pr
            JOIN patients p ON pr.patient_id = p.patient_id
            JOIN medicines m ON pr.medicine_id = m.medicine_id
            WHERE pr.status = 'Active'
              AND pr.duration_end < %s
        """
        cursor.execute(find_query, (today,))
        expired_prescriptions = cursor.fetchall()

        if not expired_prescriptions:
            # Nothing to do
            cursor.close()
            conn.close()
            return

        updated_count = 0

        for pr in expired_prescriptions:
            prescription_id = pr['prescription_id']
            doctor_id = pr['doctor_id']
            patient_name = pr['patient_name']
            drug = pr['brand_name'] or pr['generic_name']

            # Step 2: Update prescription status to Completed
            update_query = """
                UPDATE prescriptions
                SET status = 'Completed',
                    updated_at = NOW()
                WHERE prescription_id = %s
                  AND status = 'Active'
            """
            cursor.execute(update_query, (prescription_id,))

            if cursor.rowcount > 0:
                updated_count += 1

                # Step 3: Create notification for the doctor
                title = "Prescription Completed Automatically"
                message = (
                    f"Prescription #{prescription_id} ({drug}) "
                    f"for patient {patient_name} has reached its end date "
                    f"and has been marked as Completed."
                )

                success, _ = NotificationsModel.createNotification(
                    user_id=doctor_id,
                    related_table='prescriptions',
                    related_id=prescription_id,
                    title=title,
                    message=message,
                    priority='Info'
                )

                if not success:
                    print(
                        f"[PrescriptionCompletionTask] Failed to notify doctor {doctor_id} about completed prescription #{prescription_id}")

        conn.commit()
        print(f"[PrescriptionCompletionTask] Successfully completed {updated_count} expired prescription(s).")

    except Exception as e:
        print(f"[PrescriptionCompletionTask] Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()