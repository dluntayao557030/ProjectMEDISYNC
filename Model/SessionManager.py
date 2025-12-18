class SessionManager:
    """
    SessionManager stores information about the currently logged-in user.
    It acts as a global session handler for the entire application.
    This allows all controllers and models to access user details securely.
    """
    #Shared data for entire application
    _current_user = None

    @classmethod
    def setUser(cls, user_data: dict):
        """
        Stores the logged-in user's data.

        :param user_data: Dictionary returned from the database, e.g.:
            {
                "user_id": 1,
                "username": "doctor123",
                "first_name": "John",
                "last_name": "Doe",
                "role": "Doctor"
            }
        """
        cls._current_user = user_data

    @classmethod
    def getUser(cls):
        """
        Returns the current logged-in user data dictionary.
        Returns None if no user is logged-in.
        """
        return cls._current_user

    @classmethod
    def getUserId(cls):
        """
        Shortcut: returns the logged-in user's ID.
        """
        if cls._current_user:
            return cls._current_user.get("user_id")
        return None

    @classmethod
    def getUserRole(cls):
        """
        Shortcut: returns the logged-in user's role (Doctor, Nurse, Pharmacist, Admin.)
        """
        if cls._current_user:
            return cls._current_user.get("role")
        return None

    @classmethod
    def clear(cls):
        """
        Logs the user out by clearing the session.
        """
        cls._current_user = None