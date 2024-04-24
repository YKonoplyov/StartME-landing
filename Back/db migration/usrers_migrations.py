from datetime import datetime

from models import User, Roles
from engine import sync_session


with open("databases/users.table", "r", encoding="UTF-8") as users_file:
    users_list = users_file.readlines()

colums = ["id", "login", "email", "discord", "username", "role", "password"]

users_ready = []

with sync_session() as db:
    for user in users_list[1:]:
        user_list = user.split("|")
        user_dict = dict(zip(colums, user_list[1:]))

        print(user_dict)

        new_user = User(
            login=user_dict.get("login"),
            email=user_dict.get("email"),
            discord=user_dict.get("discord"),
            username=user_dict.get("username"),
            role="user" if user_dict.get("role") == Roles.USER else Roles.ADMIN,
            hashed_password=user_dict.get("password"),
            created_at=datetime.now(),
            old_id=user_dict.get("id"),
        )

        if new_user.username in users_ready:
            continue

        users_ready.append(new_user.username)

        db.add(new_user)
        db.commit()
