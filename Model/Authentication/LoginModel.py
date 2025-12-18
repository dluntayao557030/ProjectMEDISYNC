from Utilities.DatabaseConnection import getConnection
from mysql.connector import Error

class LoginModel:
    """
    Handles Login validation.
    """
    def __init__(self):
        self.connection = None
        try:
            self.connection = getConnection()
        except Error as e:
            print("Database connection error:", e)

    # Validates username and password
    def validateUser(self, username, password):
        try:
            # Return dictionary of user information for Session Manager
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT user_id, first_name, last_name, role, username 
                FROM users
                WHERE username=%s AND password=%s AND status='Active'
            """
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()
            return user

        except Error as e:
            print("Error validating user:", e)
            return None