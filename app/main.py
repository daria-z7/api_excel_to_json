import os
import logging

from flask import request, jsonify
from werkzeug.utils import secure_filename
from http import HTTPStatus

from app import app
from make_path import create_dir


ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'xlsm'])

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
)


"""Создать директории."""
create_dir()

def allowed_file(filename):
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)


@app.route('/upload/excel', methods=['POST'])
def upload_file():

    """Проверить наличие файла в структуре запроса."""
    if 'file' not in request.files:
        logging.info('No file part in the request')
        response = jsonify({'message': 'Запрос выполнен без файла'})
        response.status_code = HTTPStatus.BAD_REQUEST
        return response

    """Проверить наличие файла в запросе."""
    file = request.files['file']
    if file.filename == '':
        logging.info('Request does not include file')
        response = jsonify({'message': 'Файл отсутсвует в запросе'})
        response.status_code = HTTPStatus.BAD_REQUEST
        return response

    """Проверить наличие одноименного файла."""
    filename = secure_filename(file.filename)
    base = os.path.basename(filename)
    json_name = os.path.splitext(base)[0] + '.json'
    outfile = os.path.join(app.config['UPLOAD_FOLDER'], json_name)
    if os.path.exists(outfile):
        logging.info(f'File {json_name} already exists')
        response = jsonify({'message': 'Файл с таким именем уже существует'})
        response.status_code = HTTPStatus.OK
        return response

    """Проверить соответствие файла условиям."""
    if file and allowed_file(file.filename):
        temp_file_path = os.path.join(app.config['TEMP_FOLDER'], filename)
        file.save(temp_file_path)
        logging.info('File is taken in work')
        response = jsonify({'message': 'Файл принят в обработку'})
        response.status_code = HTTPStatus.CREATED
        return response
    else:
        logging.info('Allowed extensions are xls, xlsx, xlsm')
        response = jsonify(
            {'message': 'Файлы допустимы только в формате xls, xlsx, xlsm'}
            )
        response.status_code = HTTPStatus.BAD_REQUEST
        return response


if __name__ == "__main__":
    app.run(debug=False)
