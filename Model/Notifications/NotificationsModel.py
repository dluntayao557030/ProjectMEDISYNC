from Utilities.DatabaseConnection import getConnection
from datetime import datetime

class NotificationsModel:
    """
    Model for handling notifications
    """

    @staticmethod
    def getAllNotifications(user_id: int):
        """
        Fetch all notifications for a user from the past 30 days.
        Ordered by creation date (newest first).
        """
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT
                    notification_id,
                    title,
                    message,
                    type AS priority,
                    created_at
                FROM notifications
                WHERE user_id = %s
                  AND created_at BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW()
                ORDER BY created_at DESC
            """

            cursor.execute(query, (user_id,))
            records = cursor.fetchall()

            for record in records:
                record['time'] = NotificationsModel._formatTimeAgo(record.get('created_at'))

            cursor.close()
            conn.close()
            return records

        except Exception as e:
            print(f"Error in getAllNotifications: {e}")
            return []

    @staticmethod
    def getAllNotificationsForAdmin():
        """
        Fetches ALL notifications across ALL users from the past 30 days.
        Ordered by creation date (newest first).
        Includes username and role for context.
        """
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT
                    n.notification_id,
                    n.title,
                    n.message,
                    n.type AS priority,
                    n.created_at,
                    CONCAT(u.first_name, ' ', u.last_name) AS user_name,
                    u.role
                FROM notifications n
                JOIN users u ON n.user_id = u.user_id
                WHERE n.created_at BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW()
                ORDER BY n.created_at DESC
            """

            cursor.execute(query)
            records = cursor.fetchall()

            for record in records:
                record['time'] = NotificationsModel._formatTimeAgo(record.get('created_at'))

            cursor.close()
            conn.close()
            return records

        except Exception as e:
            print(f"Error in getAllNotificationsForAdmin: {e}")
            return []

    @staticmethod
    def getNotificationsByPriority(user_id: int, priority: str):
        """
        Get notifications filtered by priority from the past 30 days.
        Ordered by creation date (newest first).
        """
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT
                    notification_id,
                    title,
                    message,
                    type AS priority,
                    created_at
                FROM notifications
                WHERE user_id = %s
                  AND type = %s
                  AND created_at BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW()
                ORDER BY created_at DESC
            """

            cursor.execute(query, (user_id, priority))
            records = cursor.fetchall()

            for record in records:
                record['time'] = NotificationsModel._formatTimeAgo(record.get('created_at'))

            cursor.close()
            conn.close()
            return records

        except Exception as e:
            print(f"Error in getNotificationsByPriority: {e}")
            return []

    @staticmethod
    def searchNotifications(user_id: int, query: str):
        """
        Search notifications by title or message from the past 30 days.
        Ordered by creation date (newest first).
        """
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            sql_query = """
                SELECT
                    notification_id,
                    title,
                    message,
                    type AS priority,
                    created_at
                FROM notifications
                WHERE user_id = %s
                  AND (title LIKE %s OR message LIKE %s)
                  AND created_at BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW()
                ORDER BY created_at DESC
            """

            search_term = f"%{query}%"
            cursor.execute(sql_query, (user_id, search_term, search_term))
            records = cursor.fetchall()

            for record in records:
                record['time'] = NotificationsModel._formatTimeAgo(record.get('created_at'))

            cursor.close()
            conn.close()
            return records

        except Exception as e:
            print(f"Error in searchNotifications: {e}")
            return []

    @staticmethod
    def createNotification(user_id: int, title: str, message: str, priority: str,
                           related_table: str = None, related_id: int = None):
        """
        Creates a new notification.
        Returns tuple (success: bool, notification_id: int)
        """
        try:
            conn = getConnection()
            cursor = conn.cursor()

            query = """
                INSERT INTO notifications
                (user_id, related_table, related_id, title, message, type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (user_id, related_table, related_id, title, message, priority)
            )
            conn.commit()

            notification_id = cursor.lastrowid
            cursor.close()
            conn.close()

            return True, notification_id

        except Exception as e:
            print(f"Error in createNotification: {e}")
            return False, None

    @staticmethod
    def _formatTimeAgo(created_at):
        """
        Formats a datetime into a human-readable relative time string.
        """
        if not created_at:
            return "Unknown"

        now = datetime.now()
        diff = now - created_at

        seconds = diff.total_seconds()
        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24

        if seconds < 60:
            return "Just now"
        elif minutes < 60:
            return f"{int(minutes)} minute{'s' if int(minutes) != 1 else ''} ago"
        elif hours < 24:
            return f"{int(hours)} hour{'s' if int(hours) != 1 else ''} ago"
        elif days < 7:
            return f"{int(days)} day{'s' if int(days) != 1 else ''} ago"
        elif days < 30:
            weeks = int(days / 7)
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        else:
            months = int(days / 30)
            return f"{months} month{'s' if months != 1 else ''} ago"