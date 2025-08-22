import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict


class GoogleSheet:
    def __init__(self, creds_path: str, sheet_name: str, worksheet_index: int = 0):
        self.creds_path = creds_path
        self.sheet_name = sheet_name
        self.worksheet_index = worksheet_index
        self.client = self._authorize()
        self.sheet = self._open_sheet()

    def _authorize(self):
        # Используем полный доступ к таблицам (чтение + запись)
        return gspread.service_account(filename=self.creds_path)

    def _open_sheet(self):
        try:
            spreadsheet = self.client.open(self.sheet_name)
            return spreadsheet.get_worksheet(self.worksheet_index)  # Первая вкладка по умолчанию
        except Exception as e:
            raise Exception(f"Ошибка при открытии таблицы: {e}")

    def read_all_records(self) -> List[Dict]:
        """Читает все строки как список словарей"""
        try:
            return self.sheet.get_all_records()
        except Exception as e:
            raise Exception(f"Ошибка при чтении данных: {e}")

    def append_row(self, row_values: List[str]):
        """Добавляет новую строку в таблицу"""
        try:
            self.sheet.append_row(row_values)
        except Exception as e:
            raise Exception(f"Ошибка при добавлении строки: {e}")

    def update_cell(self, row: int, col: int, value: str):
        """Изменяет значение в одной ячейке"""
        try:
            self.sheet.update_cell(row, col, value)
        except Exception as e:
            raise Exception(f"Ошибка при обновлении ячейки: {e}")

if __name__ == "__main__":
    # Настройки
    CREDS_FILE = "credentials.json"
    SHEET_NAME = "Test"

    # Создаём объект
    gs = GoogleSheet(creds_path=CREDS_FILE, sheet_name=SHEET_NAME)

    # 🔹 Чтение всех записей
    responses = gs.read_all_records()
    for r in responses:
        print(r)

    # 🔹 Добавление строки
    # gs.append_row(["22.08.2025 12:45", "Иван", "+79990001122", "Хочу бота для консультаций"])
    #
    # # 🔹 Обновление ячейки (например, 2-я строка, 4-й столбец)
    # gs.update_cell(row=2, col=4, value="Комментарий обновлён")
