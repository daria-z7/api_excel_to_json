import os
import re
from datetime import datetime

import pandas as pd
import json

from app import app


def convert_file(file_path, upload_directory, file_name_json):
    """Прочитать файл."""
    df = pd.read_excel(file_path, engine='openpyxl', sheet_name=None)
    sheet_names = df.keys()

    result = dict()
    json_sheet = False

    for sheet in sheet_names:
        """Прочитать лист."""
        df = pd.read_excel(file_path, engine='openpyxl', sheet_name=sheet)

        """Преобразовать даты в формат YYYY-MM-DDThh:mm:ss.sssZ."""
        date_columns = df.select_dtypes(include=['datetime']).columns.tolist()
        for col in date_columns:
            df[col] = df[col].dt.strftime('%Y-%m-%dT%H:%M:%SZ')

        """Заменить пустые значения на null."""
        df = df.fillna('null')

        column_number = len(df.columns)

        json_columns = []
        for i in range(0, column_number):
            if '{' in str(df.iat[0, i]):
                json_columns.append(list(df.columns.values)[i])
        if len(json_columns) > 0:
            json_sheet = True

        """Создать json объект из листа."""
        jsonfile = df.to_json(orient='records', indent=4)
        json_object = json.loads(jsonfile)
        """Преобразовать вложенные json строки."""
        if json_sheet:
            for element in json_object:
                for col in json_columns:
                    re_match = re.findall(
                        r'\d{4}\-\d{2}\-\d{2}.\d{2}:\d{2}:\d{2}.\d{3}',
                        element[col]
                        )
                    for date in re_match:
                        element[col] = element[col].replace(
                            date,
                            str(datetime.strptime(
                                date,
                                '%Y-%m-%d %H:%M:%S.%f'))[:-3]+'Z'
                                ).replace(' ', 'T')
                    element[col] = json.loads(element[col])

        """Добавить json объект общему json объекту."""
        result[sheet] = json_object

    """Создать json файл."""
    with open(os.path.join(
        upload_directory,
        file_name_json
        ), 'w', encoding='utf8') as outfile:
        json.dump(result, outfile, indent=3, ensure_ascii=False)
