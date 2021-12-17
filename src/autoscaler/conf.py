import os

class EnvironmentConf:
    SECRET_TOKEN = os.getenv('SECRET_TOKEN', '')
