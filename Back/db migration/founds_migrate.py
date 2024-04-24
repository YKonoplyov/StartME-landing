import json

from sqlalchemy import select

import models
import engine


def process_managers(fund: models.Fund, managers_list: list, db: engine.AsyncSession):
    if managers_list is None:
        return fund

    managers = db.scalars(
        select(models.User).where(models.User.old_id.in_(managers_list))
    )

    for manager in managers:
        manager.role = models.Roles.MANAGER

        fund.managers.append(manager)

    return fund


def process_users(fund: models.Fund, users_list: list, db: engine.AsyncSession):
    if users_list is None:
        return fund

    users = db.scalars(select(models.User).where(models.User.old_id.in_(users_list)))

    for user in users:
        user.role = models.Roles.USER

        fund.users.append(user)

    return fund


def process_ro(fund: models.Fund, ro_list: list, db: engine.AsyncSession):
    if ro_list is None:
        return fund

    ros = db.scalars(select(models.User).where(models.User.old_id.in_(ro_list)))

    for ro in ros:
        ro.role = models.Roles.READ_ONLY

        fund.users.append(ro)

    return fund


def migrate_funds():
    with open("databases/funds.nosql", "r", encoding="UTF-8") as funds_json:
        funds_list = funds_json.readlines()

    with engine.sync_session() as db:
        for fund in funds_list:
            fund_dict = json.loads(fund)

            print(fund_dict)

            try:
                managers = fund_dict.pop("managers")
            except KeyError:
                managers = None

            try:
                users = fund_dict.pop("users")
            except KeyError:
                users = None

            try:
                readonlys = fund_dict.pop("readonlys")
            except KeyError:
                users = None

            fund = models.Fund(
                name=fund_dict.get("name"),
                email=fund_dict.get("email"),
                link=fund_dict.get("site"),
                old_id=fund_dict.get("id"),
            )

            fund = process_managers(fund=fund, managers_list=managers, db=db)
            fund = process_users(fund=fund, users_list=users, db=db)
            fund = process_ro(fund=fund, ro_list=readonlys, db=db)

            db.add(fund)
            db.commit()


migrate_funds()
