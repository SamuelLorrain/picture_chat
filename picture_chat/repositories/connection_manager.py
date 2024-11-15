from picture_chat.config import Config
import psycopg2

class ConnectionManager():
    def __init__(self):
        self.connection = psycopg2.connect(Config().database_connection_string)

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    def __enter__(self):
        return self.get_cursor()

    def __exit__(self, type, value, traceback):
        self.get_connection().commit()
        self.close_connection()
