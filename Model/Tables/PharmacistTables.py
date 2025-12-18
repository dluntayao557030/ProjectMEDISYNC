from Utilities.DatabaseConnection import getConnection

class PharmacistTables:
    """
    Table data retrieval methods for Pharmacist
    """

    @staticmethod
    def getExpiringMedications(days=365):
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                    SELECT 
                        pv.verification_id,
                        pr.prescription_id,
                        p.patient_first_name,
                        p.patient_last_name,
                        m.brand_name,
                        m.generic_name,
                        pv.quantity_dispensed,
                        pv.expiry_date,
                        DATEDIFF(pv.expiry_date, CURDATE()) AS days_until_expiry
                    FROM prescription_verification pv
                    JOIN prescriptions pr ON pv.prescription_id = pr.prescription_id
                    JOIN patients p ON pr.patient_id = p.patient_id
                    JOIN medicines m ON pr.medicine_id = m.medicine_id
                    WHERE pv.expiry_date > CURDATE()
                      AND pv.expiry_date <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
                      AND pr.status = 'Active'
                    ORDER BY pv.expiry_date ASC
                """
            cursor.execute(query, (days,))
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in getExpiringMedications: {e}")
            return []

    @staticmethod
    def getMedicationsToPrepare():
        """
        Returns medications that need preparation.
        Shows prescriptions where next administration is within 30 minutes,
        based on last administration time and frequency.
        Only shows 'To be Prepared' status for active prescriptions.
        """
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    mp.preparation_id,
                    pr.prescription_id,
                    p.patient_first_name,
                    p.patient_last_name,
                    m.brand_name,
                    m.generic_name,
                    pr.dosage,
                    pr.frequency,
                    mp.quantity_prepared,
                    mp.status,
                    (SELECT MAX(ma.administration_time)
                     FROM medication_administration ma
                     WHERE ma.prescription_id = pr.prescription_id
                    ) AS last_admin_time
                FROM medicine_preparation mp
                JOIN prescriptions pr ON mp.prescription_id = pr.prescription_id
                JOIN patients p ON pr.patient_id = p.patient_id
                JOIN medicines m ON pr.medicine_id = m.medicine_id
                WHERE pr.status = 'Active'
                  AND p.status = 'Active'
                  AND pr.duration_start <= CURDATE()
                  AND pr.duration_end >= CURDATE()
                  AND mp.status = 'To be Prepared'
                ORDER BY pr.created_at DESC
            """
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            conn.close()

            # Filter records based on 30-minute preparation window
            filtered_records = []
            frequency_intervals = {
                "Once a day": 24,
                "Twice a day": 12,
                "Three times a day": 8,
                "Four times a day": 6,
                "Every 6 hours": 6,
                "Every 8 hours": 8,
                "Every 12 hours": 12
            }

            from datetime import datetime, timedelta
            now = datetime.now()

            for record in records:
                frequency = record.get('frequency')
                last_admin = record.get('last_admin_time')

                # Get interval hours for this frequency
                interval_hours = frequency_intervals.get(frequency)

                if not interval_hours:
                    # Unknown frequency, include it to be safe
                    filtered_records.append(record)
                    continue

                # If never administered, include it (first dose)
                if not last_admin:
                    filtered_records.append(record)
                    continue

                # Calculate when next dose is due
                next_dose_time = last_admin + timedelta(hours=interval_hours)

                # Calculate time 30 minutes before next dose
                preparation_window_start = next_dose_time - timedelta(minutes=30)

                # Include if we're within the 30-minute preparation window
                if now >= preparation_window_start:
                    filtered_records.append(record)

            return filtered_records

        except Exception as e:
            print(f"Error in getMedicationsToPrepare: {e}")
            return []

    @staticmethod
    def markMedicationAsPrepared(preparation_id):
        try:
            conn = getConnection()
            cursor = conn.cursor()
            query = """
                UPDATE medicine_preparation 
                SET status = 'Prepared'
                WHERE preparation_id = %s AND status = 'To be Prepared'
            """
            cursor.execute(query, (preparation_id,))
            conn.commit()
            success = cursor.rowcount > 0
            cursor.close()
            conn.close()
            return success
        except Exception as e:
            print(f"Error in markMedicationAsPrepared: {e}")
            return False