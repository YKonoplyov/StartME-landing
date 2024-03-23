import json
import models
import engine
from sqlalchemy import select
def process_managers(found: models.Found, managers_list: list, db: engine.AsyncSession):
    
    if managers_list is None:
        return found
    managers = db.scalars(select(models.User).where(models.User.old_id.in_(managers_list)))
    for manager in managers:
        manager.role = models.Roles.MANAGER
        found.managers.append(manager)
    return found
def process_users(found: models.Found, users_list: list, db: engine.AsyncSession):
    if users_list is None:
        return found
    users = db.scalars(select(models.User).where(models.User.old_id.in_(users_list)))
    for user in users:
        user.role = models.Roles.USER
        found.users.append(user)
    return found

def process_ro(found: models.Found, ro_list: list, db: engine.AsyncSession):
    if ro_list is None:
        return found
    ros = db.scalars(select(models.User).where(models.User.old_id.in_(ro_list)))
    
    for ro in ros:
        ro.role = models.Roles.READ_ONLY
        found.users.append(ro)
    return found
def migrate_founds():
    with open("databases/funds.nosql", "r", encoding="UTF-8") as founds_json:
        founds_list = founds_json.readlines()
    with engine.sync_session() as db:
        for found in founds_list:
            found_dict = json.loads(found)
            print(found_dict)
            try:
                managers = found_dict.pop("managers")
            except KeyError:
                managers = None
            try:
                users = found_dict.pop("users")
            except KeyError:
                users = None
            try:
                readonlys = found_dict.pop("readonlys")
            except KeyError:
                users = None
            found = models.Found(
                name=found_dict.get("name"),
                email=found_dict.get("email"),
                link=found_dict.get("site"),
                old_id=found_dict.get("id")
            )
            found = process_managers(found=found, managers_list=managers, db=db)
            found = process_users(found=found, users_list=users, db=db)
            found = process_ro(found=found, ro_list=readonlys, db=db)

            db.add(found)
            db.commit()

migrate_founds()
        