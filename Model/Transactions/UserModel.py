from Utilities.DatabaseConnection import getConnection

class UserModel:
    """
    Handles database operations for User Management.
    """

    @staticmethod
    def getAllUsers():
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT user_id, username, first_name, last_name, email_address AS email,
                       contact_number AS contact, role, license_number, status,
                       created_at, updated_at
                FROM users ORDER BY created_at DESC
            """
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in getAllUsers: {e}")
            return []

    @staticmethod
    def searchUsers(query):
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            sql = """
                SELECT user_id, username, first_name, last_name, email_address AS email,
                       contact_number AS contact, role, license_number, status,
                       created_at, updated_at
                FROM users
                WHERE username LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR role LIKE %s
                ORDER BY created_at DESC
            """
            term = f"%{query}%"
            cursor.execute(sql, (term, term, term, term))
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except Exception as e:
            print(f"Error in searchUsers: {e}")
            return []

    @staticmethod
    def getUserById(user_id):
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT user_id, username, first_name, last_name, email_address AS email,
                       contact_number AS contact, role, license_number, status,
                       created_at, updated_at
                FROM users WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            record = cursor.fetchone()
            cursor.close()
            conn.close()
            return record
        except Exception as e:
            print(f"Error in getUserById: {e}")
            return None

    @staticmethod
    def addUser(username, password, first_name, last_name, email, contact, role, license_number):
        try:
            if UserModel.usernameExists(username):
                return False, "Username already exists", None
            conn = getConnection()
            cursor = conn.cursor()
            query = """
                INSERT INTO users (username, password, first_name, last_name, email_address,
                                   contact_number, role, license_number, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Active')
            """
            cursor.execute(query, (username, password, first_name, last_name, email, contact, role, license_number))
            conn.commit()
            user_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return True, "User added successfully", user_id
        except Exception as e:
            print(f"Error in addUser: {e}")
            return False, f"Error adding user: {str(e)}", None

    @staticmethod
    def updateUser(user_id, username, first_name, last_name, email, contact, role, license_number, status, password=None):
        try:
            existing = UserModel.getUserByUsername(username)
            if existing and existing['user_id'] != user_id:
                return False, "Username taken"
            conn = getConnection()
            cursor = conn.cursor()
            if password:
                query = """
                    UPDATE users SET username=%s, password=%s, first_name=%s, last_name=%s,
                                     email_address=%s, contact_number=%s, role=%s, license_number=%s,
                                     status=%s, updated_at=CURRENT_TIMESTAMP WHERE user_id=%s
                """
                params = (username, password, first_name, last_name, email, contact, role, license_number, status, user_id)
            else:
                query = """
                    UPDATE users SET username=%s, first_name=%s, last_name=%s, email_address=%s,
                                     contact_number=%s, role=%s, license_number=%s, status=%s,
                                     updated_at=CURRENT_TIMESTAMP WHERE user_id=%s
                """
                params = (username, first_name, last_name, email, contact, role, license_number, status, user_id)
            cursor.execute(query, params)
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            conn.close()
            return (True, "User updated") if affected > 0 else (False, "User not found")
        except Exception as e:
            print(f"Error in updateUser: {e}")
            return False, f"Error updating: {str(e)}"

    @staticmethod
    def usernameExists(username):
        try:
            conn = getConnection()
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM users WHERE username = %s AND status != 'Deleted'"
            cursor.execute(query, (username,))
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count > 0
        except Exception as e:
            print(f"Error in usernameExists: {e}")
            return False

    @staticmethod
    def getUserByUsername(username):
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT user_id, username, first_name, last_name, email_address AS email,
                       contact_number AS contact, role, license_number, status
                FROM users WHERE username = %s
            """
            cursor.execute(query, (username,))
            record = cursor.fetchone()
            cursor.close()
            conn.close()
            return record
        except Exception as e:
            print(f"Error in getUserByUsername: {e}")
            return None