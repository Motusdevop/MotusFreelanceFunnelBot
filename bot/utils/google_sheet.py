import gspread
import pandas as pd
from typing import List, Dict, Any
from gspread import Client, Worksheet
from loguru import logger


class GoogleSheet:
    """
    Wrapper for interacting with Google Sheets via gspread.
    Provides methods to load and upload data as Pandas DataFrames.
    """

    def __init__(self, creds_path: str, sheet_name: str):
        self.creds_path = creds_path
        self.sheet_name = sheet_name
        self.client = self._authorize()

    def _authorize(self) -> Client:
        """
        Authorize and return a gspread client using service account credentials.
        """
        try:
            return gspread.service_account(filename=self.creds_path)
        except Exception as e:
            logger.error(f"Authorization failed: {e}")
            raise

    def _open_sheet(self, worksheet: str) -> Worksheet:
        """
        Open worksheet by name.
        """
        try:
            spreadsheet = self.client.open(self.sheet_name)
            return spreadsheet.worksheet(worksheet)
        except Exception as e:
            logger.error(f"Failed to open worksheet '{worksheet}' in '{self.sheet_name}': {e}")
            raise

    def load_to_dataframe(self, worksheet: str) -> pd.DataFrame:
        """
        Load data from worksheet into a Pandas DataFrame.
        """
        ws = self._open_sheet(worksheet)
        data: List[Dict[str, Any]] = ws.get_all_records()
        logger.info(f"Loaded {len(data)} rows from {self.sheet_name}:{worksheet}")
        return pd.DataFrame(data)

    def _prepare_dataframe_for_upload(self, dataframe: pd.DataFrame) -> List[List[Any]]:
        """
        Prepare DataFrame values for uploading (convert dates, add headers).
        """
        df_copy = dataframe.copy()
        for col in df_copy.columns:
            df_copy[col] = df_copy[col].apply(
                lambda x: x.strftime("%d.%m.%y %H:%M") if hasattr(x, "strftime") else x
            )
        return [list(df_copy.columns)] + df_copy.values.tolist()

    def upload_dataframe(
        self,
        worksheet: str,
        dataframe: pd.DataFrame,
        include_header: bool = True,
    ) -> None:
        """
        Upload DataFrame to worksheet (overwrite existing content).
        """
        ws = self._open_sheet(worksheet)
        ws.clear()

        values: List[List[Any]] = (
            self._prepare_dataframe_for_upload(dataframe)
            if include_header
            else dataframe.values.tolist()
        )

        ws.update(values, "A1")
        logger.info(f"Uploaded {len(dataframe)} rows to {self.sheet_name}:{worksheet}")