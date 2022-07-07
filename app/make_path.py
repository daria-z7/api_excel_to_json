import os

from app import app


"""Создать директории."""
def create_dir():
    dir_exists =  os.path.exists(app.config['TEMP_FOLDER'])
    if not dir_exists:
        os.makedirs(app.config['TEMP_FOLDER'])
    dir_exists =  os.path.exists(app.config['UPLOAD_FOLDER'])
    if not dir_exists:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    dir_exists =  os.path.exists(app.config['ARCHIVE_FOLDER'])
    if not dir_exists:
        os.makedirs(app.config['ARCHIVE_FOLDER'])
    dir_exists =  os.path.exists(app.config['ARCHIVE_FAIL_FOLDER'])
    if not dir_exists:
        os.makedirs(app.config['ARCHIVE_FAIL_FOLDER'])
