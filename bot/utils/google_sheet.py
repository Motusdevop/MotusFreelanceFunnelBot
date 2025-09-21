import gspread
import loguru
import pandas as pd
from typing import List, Dict, Optional, Any

from gspread import Client, Worksheet

from config import logger


class GoogleSheet:
    def __init__(self, creds_path: str, sheet_name: str):
        self.creds_path = creds_path
        self.sheet_name = sheet_name
        self.client = self._authorize()

    def _authorize(self) -> Client:
        # Используем полный доступ к таблицам (чтение + запись)
        return gspread.service_account(filename=self.creds_path)

    def _open_sheet(self, worksheet: str) -> Worksheet:
        try:
            spreadsheet = self.client.open(self.sheet_name)
            return spreadsheet.worksheet(worksheet)  # Первая вкладка по умолчанию
        except Exception as e:
            raise Exception(f"Ошибка при открытии таблицы: {e}")

    def load_to_dataframe(self, worksheet: str) -> pd.DataFrame:
        """
        Загружает данные из Google Sheets в pandas.DataFrame.
        """
        ws = self._open_sheet(worksheet)
        data: List[Dict[str, Any]] = ws.get_all_records()
        logger.info(
            f"Загружено {len(data)} строк из "
            f"{self.sheet_name}:{worksheet or 'sheet1'}"
        )
        return pd.DataFrame(data)

    def upload_dataframe(
            self,
            worksheet: str,
            dataframe: pd.DataFrame,
            include_header: bool = True,
    ) -> None:
        """
        Загружает DataFrame в Google Sheets (заменяет содержимое листа).
        :param dataframe: DataFrame для загрузки
        :param include_header: выгружать ли заголовки столбцов
        """
        ws = self._open_sheet(worksheet)
        ws.clear()

        # Преобразуем даты в строки (YYYY-MM-DD)
        dataframe = dataframe.copy()
        for col in dataframe.columns:
            dataframe[col] = dataframe[col].apply(
                lambda x: x.strftime("%d.%m.%y %H:%M") if hasattr(x, "strftime") else x
            )

        # Формируем данные для выгрузки
        values: List[List[Any]] = []
        if include_header:
            values.append(list(dataframe.columns))
        values.extend(dataframe.values.tolist())

        ws.update(values, "A1")
        logger.info(
            f"DataFrame ({len(dataframe)} строк) выгружен в "
            f"{self.sheet_name}:{worksheet or 'sheet1'}"
        )


if __name__ == "__main__":
    # Настройки
    CREDS_FILE = "../../credentials.json"
    SHEET_NAME = "Test"

    # Создаём объект
    gs = GoogleSheet(creds_path=CREDS_FILE, sheet_name=SHEET_NAME)

    df = gs.load_to_dataframe(worksheet='Users')

    print(df.head())

    df.loc[len(df)] = ['Motus', '12:00']

    print(df.head())

    gs.upload_dataframe(worksheet='Users', dataframe=df)
