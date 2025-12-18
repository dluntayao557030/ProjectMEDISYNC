import mysql.connector

def getConnection():
    """
    Returns a new connection to the database.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="projectmedisync_luntayao"
    )