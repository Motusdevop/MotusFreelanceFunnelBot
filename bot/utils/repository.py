# repository.py
import logging

import pandas as pd

import models
from config import logger, settings
from models import User, BaseModel

import asyncio

from utils.google_sheet import GoogleSheet


class Table:
    def __init__(
            self,
            spreadsheet_name: str,
            worksheet: str,
            model: BaseModel,
            creds_path: str,
    ):
        self.model = model
        self.worksheet = worksheet
        self._google_sheet = GoogleSheet(creds_path=creds_path, sheet_name=spreadsheet_name)
        self.df = self._load_data()
        self.upload_task = None

    def _load_data(self):

        df = self._google_sheet.load_to_dataframe(self.worksheet)

        if df.empty:
            df = pd.DataFrame(columns=self.model.model_fields.keys())

        return df

        print(self.df.head())

        # for header, field_info in self.model.model_fields.items():
        #     if header in load_df.columns:
        #         load_df[header] = load_df[header].astype(field_info.annotation)
        #     else:
        #         logger.error(
        #             f"Header {header} not found in model {self.model.__name__}"
        #         )
        #         raise KeyError(f"{header} not in {self.model.model_fields}")

    async def upload_data(self):
        while True:
            try:
                self._google_sheet.upload_dataframe(self.worksheet, self.df, include_header=True)
            except Exception as e:
                logging.error(f"Error appending data to Google Sheet: {e}")

            await asyncio.sleep(60 * 30)

    async def append(self, data: BaseModel):
        # создаём df из одной строки
        new_row_df = pd.DataFrame([data.model_dump()])
        # конкатенация
        df_new = pd.concat([self.df, new_row_df], ignore_index=True)
        self.df = df_new

        if self.upload_task is None:
            self.upload_task = asyncio.create_task(self.upload_data())


UserTable = Table(model=models.User,
                  spreadsheet_name=settings.SHEET_NAME,
                  worksheet=settings.USERS_WORKSHEET,
                  creds_path=settings.CREDENTIALS_PATH)
