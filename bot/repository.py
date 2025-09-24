import asyncio
import pandas as pd
from loguru import logger
from pydantic import BaseModel

import models
from config import settings
from utils.google_sheet import GoogleSheet


class Table:
    """
    Base abstraction for working with Google Sheets as a table.
    Handles loading, uploading and local caching of dataframe.
    """

    def __init__(self, spreadsheet_name: str, worksheet: str, model: BaseModel, creds_path: str):
        self.model = model
        self.worksheet = worksheet
        self._google_sheet = GoogleSheet(creds_path=creds_path, sheet_name=spreadsheet_name)
        self.df = self._load_data()
        self.auto_upload_task = None
        self.auto_load_task = None

    def get_dataframe(self) -> pd.DataFrame:
        """
        Returns a local dataframe representing the table.
        """
        return self.df

    def _load_data(self) -> pd.DataFrame:
        """
        Load data from Google Sheet into local dataframe.
        """
        df = self._google_sheet.load_to_dataframe(self.worksheet)

        if df.empty:
            df = pd.DataFrame(columns=self.model.model_fields.keys())

        logger.info(f"Data loaded from worksheet '{self.worksheet}', rows={len(df)}")
        self.df = df
        return df

    async def _auto_load_data(self) -> None:
        """
        Periodically reloads data from Google Sheets every 30 minutes.
        """
        while True:
            self._load_data()
            await asyncio.sleep(60 * settings.LOAD_DELAY_MINUTS)

    async def enable_auto_load(self) -> None:
        """
        Starts automatic reloading of data.
        """
        if self.auto_load_task is None:
            self.auto_load_task = asyncio.create_task(self._auto_load_data())
            logger.info(f"Auto-load enabled for worksheet '{self.worksheet}'")

    def _upload_data(self) -> None:
        """
        Upload local dataframe to Google Sheets.
        """
        try:
            self._google_sheet.upload_dataframe(self.worksheet, self.df, include_header=True)
            logger.info(f"Data uploaded to worksheet '{self.worksheet}', rows={len(self.df)}")
        except Exception as e:
            logger.error(f"Error uploading data to worksheet '{self.worksheet}': {e}")

    async def _auto_upload_data(self) -> None:
        """
        Periodically uploads data to Google Sheets every 30 minutes.
        """
        while True:
            self._upload_data()
            await asyncio.sleep(60 * settings.UPLOAD_DELAY_MINUTS)

    async def enable_auto_update(self) -> None:
        """
        Starts automatic uploading of data.
        """
        if self.auto_upload_task is None:
            self.auto_upload_task = asyncio.create_task(self._auto_upload_data())
            logger.info(f"Auto-upload enabled for worksheet '{self.worksheet}'")

    async def append(self, data: BaseModel) -> None:
        """
        Append new row to local dataframe.
        """
        new_row_df = pd.DataFrame([data.model_dump()])
        self.df = pd.concat([self.df, new_row_df], ignore_index=True)
        logger.info(f"New row appended to '{self.worksheet}', total rows={len(self.df)}")


class ReviewTable(Table):
    """
    Specialized table for handling customer reviews.
    """

    def get_reviews(self) -> list[models.Review]:
        """
        Returns list of reviews sorted by date (newest first).
        """
        df = self.get_dataframe()
        reviews = [models.Review(**row) for row in df.to_dict("records")]
        return sorted(reviews, key=lambda r: r.date)


# Global table instances
USERS_TABLE = Table(
    model=models.User,
    spreadsheet_name=settings.SHEET_NAME,
    worksheet=settings.USERS_WORKSHEET,
    creds_path=settings.CREDENTIALS_PATH,
)

REVIEWS_TABLE = ReviewTable(
    model=models.Review,
    spreadsheet_name=settings.SHEET_NAME,
    worksheet=settings.REVIEWS_WORKSHEET,
    creds_path=settings.CREDENTIALS_PATH,
)
