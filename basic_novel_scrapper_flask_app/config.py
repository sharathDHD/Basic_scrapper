import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Browser settings
    BROWSER_NAME = 'firefox'
    BROWSER_PLATFORM = 'android'
    BROWSER_MOBILE = True
    BROWSER_VERSION = '68.0'  # A common Firefox version for Android
    DEVICE_MODEL = 'Pixel 4'
    ANDROID_VERSION = '10'
    REQUEST_DELAY = 3
    REQUEST_TIMEOUT = 30
    USE_PROXY = False
    PROXY_URL = None  # Set this if USE_PROXY is True