from Utilities.DatabaseConnection import getConnection

class AdminTables:
    """
    Contains table data retrieval methods for Admin dashboard.
    """

    @staticmethod
    def getTodaysActivitySummary():
        """
        Returns today's activity summary.
        """
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    n.notification_id,
                    n.title,
                    n.message,
                    n.type,
                    n.related_table,
                    n.related_id,
                    n.created_at,
                    CONCAT(u.first_name, ' ', u.last_name) AS user_name,
                    u.role
                FROM notifications n
                JOIN users u ON n.user_id = u.user_id
                WHERE DATE(n.created_at) = CURDATE()
                ORDER BY n.created_at DESC
            """

            cursor.execute(query)
            records = cursor.fetchall()

            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in getTodaysActivitySummary: {e}")
            return []
