import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

firebaseConfig = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': "project-dga.firebaseapp.com",
    'databaseURL': "https://project-dga-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "project-dga",
    'storageBucket': "project-dga.appspot.com",
    'messagingSenderId': "713322540106",
    'appId': "1:713322540106:web:10b2ad2045953722364ab3",
    'measurementId': "G-824K53MBXG"
}

firebase = pyrebase.initialize_app(firebaseConfig)
