# import asyncio
# import json
# import os
# from sqlalchemy import select
# from dotenv import load_dotenv
# import users
# import requests
# import db
# from datetime import datetime
# from models import users_in_founds, User

# from crud import found_add_manager

# async def create_user():
#     try:
#         user_data = {}

#         user_data["password"] = "agagagag"
#         user_data["role"] = "admin"
#         user_data["username"] = "admin"
#         user_data["email"] = "admin@mail.com"
#         user_data["contact_fields"] = {"adcd": "1234"}
#         user_data["founds_ids"] = []
#         user_data["is_superuser"] = 1
#         user_data["is_active"] = 1
#         user_data["is_verified"] = 1
#         user_data["created_at"] = datetime.now()
#         user_scheme_data = users.schemas.UserCreate(**user_data)
#         print(user_scheme_data)
#         async for session in db.engine.get_async_session():
#             async for user_db in users.get_user_db(session=session):
#                 user_manager = users.UserManager(user_db)
#                 await user_manager.create(user_scheme_data)
#     except Exception as e:
#             print(f"An error occurred: {e}")


# asyncio.run(create_user())
          


# from users import get_user_manager
            
import json


json_str = "{"FIO":[],"skype":[],"nickname":[{"discipline":"Cash HU"}],"gipsyteam":["https://site.gipsyteam.ru/profile/Prostodron"],"pokerstrategy":[],"case":[{"descr":"Залил 2 транша, перестал отписывать, на вопрос почему не отписываешь: "Стыдно". Просить понять и простить, буквально. На связь не выходит. Есть предположение что день перелил на свои акки.","amount":"750euro"}],"google":["bboysnegok@gmail.com"],"mail":["bboysnegok@gmail.com"],"phone":["79258352805"],"vk":[],"facebook":[],"blog":[],"instagram":[],"forum":[],"location":[],"neteller":[],"skrill":[],"ecopayz":[],"webmoney":[],"old":true,"author":"6038014c2528de31d1deca9f","fundName":"Бастион","nicknameOld":"Prostodron","comments":"\" 4276 5218 7802 0704\" - карта сбербанка . Начинает выплату мейкапа с 23.05.2020","created":"2021-03-10T12:30:25.773Z","updated":"2021-03-10T12:30:25.773Z","id":"6048bbe1b2d91b89fa75fa7a"}"
