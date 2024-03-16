import asyncio
import json
import os
from dotenv import load_dotenv
import users
import requests
import db
from models import users_in_founds, User


user_data = json.loads(requests.get("http://127.0.0.1:8000/users/1").content)

user_data["password"] = "agagagag"
user_data["role"] = "admin"
user_data["username"] = "loh"
user_scheme_data = users.schemas.UserCreate(**user_data)
async def fetch_user_data():
    response = requests.get("http://127.0.0.1:8000/users/1")
    response.raise_for_status()  # Ensure the request was successful
    return json.loads(response.content)

async def create_user():
    try:
        user_data = await fetch_user_data()

        user_data["password"] = "agagagag"
        user_data["role"] = "admin"
        user_data["username"] = "loh2222"
        user_data["email"] = "loh222@mail.com"
        user_data["contact_fields"] = {"adcd": "1234"}
        user_data["founds_ids"] = [1,]
        user_scheme_data = users.schemas.UserCreate(**user_data)
        print(user_scheme_data)
        async for session in db.engine.get_async_session():
            async for user_db in users.get_user_db(session=session):
                user_manager = users.UserManager(user_db)
                await user_manager.create(user_scheme_data)
    except Exception as e:
            print(f"An error occurred: {e}")

async def add_user_to_found(user_id: int,  found_id: int) -> None:
    try:
        async for session in db.engine.get_async_session():     
            with session as db:
                ...
                # db.
    except Exception as e:
        ...

# async def_get_user 
asyncio.run(create_user())
            


