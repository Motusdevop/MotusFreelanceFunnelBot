# storage.py
import logging
from typing import List

from pydantic import BaseModel

import models
from config import settings

from utils.google_sheet import GoogleSheet

import models


class Table:
    def __init__(self, worksheet_index: int, model: BaseModel):
        self._sheet = GoogleSheet(creds_path=settings.credentials_path,
                                  sheet_name=settings.sheet_name,
                                  worksheet_index=worksheet_index)
        self.model = model
        self.table = self.load_data_from_google_sheet()

    def load_data_from_google_sheet(self) -> List[BaseModel]:
        records = [self.model(**data) for data in self._sheet.read_all_records()]
        return records

    def append(self, data: BaseModel):
        self.table.append(data)

        try:
            self._sheet.append_row(list(map(str, data.dict().values())))
        except Exception as e:
            logging.error(f"Error appending data to Google Sheet: {e}")


UserTable = Table(worksheet_index=settings.USERS_WORKSHEET_INDEX, model=models.User)
