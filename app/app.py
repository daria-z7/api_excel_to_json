import os

from flask import Flask


UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'upload'
    )
TEMP_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'Temp'
    )
ARCHIVE_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'Archive'
    )
ARCHIVE_FAIL_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'Archive_Fail'
    )

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMP_FOLDER'] = TEMP_FOLDER
app.config['ARCHIVE_FOLDER'] = ARCHIVE_FOLDER
app.config['ARCHIVE_FAIL_FOLDER'] = ARCHIVE_FAIL_FOLDER
