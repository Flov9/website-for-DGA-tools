import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

firebaseConfig = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': "dga-tools.firebaseapp.com",
    'databaseURL': "https://dga-tools-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "dga-tools",
    'storageBucket': "dga-tools.appspot.com",
    'messagingSenderId': "607330409462",
    'appId': "1:607330409462:web:fc8fe095424b2f518b45d7"
}

firebase = pyrebase.initialize_app(firebaseConfig)
