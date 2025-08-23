from typing import List

from aiogram import Bot

from config import settings

async def send_message_to_admins(bot: Bot, text: str):
    for admin_id in settings.admins:
        await bot.send_message(chat_id=admin_id, text=text)


# class UserRepository:
#     data: List[dict] = list()
#
#     # UsersGoogleSheet = GoogleSheet(creds_path=settings.credentials_path,
#     #                                sheet_name=settings.sheet_name,
#     #                                worksheet_index=settings.USERS_WORKSHEET_INDEX)
#
#     @classmethod
#     def load_from_google_sheet(cls):
#         cls.data = cls.UsersGoogleSheet.read_all_records()
#
#     @classmethod
#     def append(cls, user: dict):
#         cls.data.append(user)
#         cls.UsersGoogleSheet.append_row(list(map(str, user.values())))
#
# if __name__ == '__main__':
#     UserRepository.UsersGoogleSheet = GoogleSheet(creds_path='../../credentials.json', sheet_name='MotusFreelance', worksheet_index=3)
#     UserRepository.load_from_google_sheet()
#     print(UserRepository.data)
#     user = {
#         'first_name': 'Иван',
#         'last_name': 'Данилов',
#         'username': '@Kapchonka77',
#         'Дата': '2023-04-27'
#     }
#     UserRepository.append(user)



