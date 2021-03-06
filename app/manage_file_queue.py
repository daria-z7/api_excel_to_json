from os import listdir, path, replace, makedirs
import time
import logging

from app import app
from conversion import convert_file
from make_path import create_dir


RETRY_TIME = 100

logging.basicConfig(
    level=logging.INFO,
    filename='manage_queue.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
)


"""Создать директории."""
create_dir()

def check_folder():
    """Прочитать новые файлы к обработке."""
    while True:
        temp_directory = app.config['TEMP_FOLDER']
        file_list = [f for f in listdir(temp_directory) if path.isfile(path.join(temp_directory, f))]

        for file_name in file_list:
            logging.info(f'File {file_name} is proccesing')
            temp_file_path = path.join(app.config['TEMP_FOLDER'], file_name)
            json_name = path.splitext(file_name)[0] + '.json'

            try:
                """Обработать файл - excel в json."""
                convert_file(
                    temp_file_path,
                    app.config['UPLOAD_FOLDER'],
                    json_name
                    )
                logging.info(f'File {file_name} is converted to json')

                """Перенести обработанный файл в архив."""
                archive_path = path.join(
                    app.config['ARCHIVE_FOLDER'],
                    file_name
                    )
                replace(temp_file_path, archive_path)
                logging.info(f'File {file_name} is moved to archive folder')
            except:
                """Перенести необработанный файл в архив ошибок."""
                logging.error(
                    f'There were some problems with file {file_name}'
                    )
                archive_path = path.join(
                    app.config['ARCHIVE_FAIL_FOLDER'],
                    file_name
                    )
                replace(temp_file_path, archive_path)
                logging.error(f'File {file_name} was moved to error folder')

        time.sleep(RETRY_TIME)


if __name__ == "__main__":
    check_folder()
