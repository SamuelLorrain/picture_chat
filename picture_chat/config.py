from dotenv.main import load_dotenv
import os


class Config(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        load_dotenv()
        self.secret_key = os.getenv('JWT_SECRET')
        self.front_url = os.getenv('FRONT_URL')
