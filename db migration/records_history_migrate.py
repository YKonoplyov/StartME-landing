from datetime import datetime
import json
import models
import engine
from sqlalchemy import select

def migrate_records():
    with open("databases/arb-history.nosql", "r", encoding="UTF-8") as funds_json:
        records_list = funds_json.readlines()
    with engine.sync_session() as db:
        for record in records_list[:-1]:
            try:
                record_dict = json.loads(record)
            except json.JSONDecodeError as e:
                # print(e.msg.split(" "))
                # print(record[:e.colno + 3])
                # print(e)
                break
            case = record_dict.pop("case")
            if case:   
                case = case[0] 
                record_dict["description"] = case.get("descr")
                record_dict["amount"] = case.get("amount")
            initials = record_dict.pop("FIO")
            # print(initials)
            if initials:
                initials = initials[0]
                record_dict["first_name"] = initials.get("firstname")
                record_dict["last_name"] = initials.get("lastname")
                record_dict["by_fathers_name"] = initials.get("middlename")
            record_dict["old"] = record_dict.get("old", False)
            new_arb = models.RecordHistory()
            new_arb.old_id = record_dict.pop("id")
            new_arb.nicknames = json.dumps(record_dict.pop("nickname"))
            new_arb.webmoney = json.dumps(record_dict.pop("webmoney"))
            new_arb.created_at = datetime.strptime(
                record_dict.pop("created"),
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            new_arb.updated_at = datetime.strptime(
                record_dict.pop("updated"),
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            created_by =  db.scalar(select(models.User).where(
                    models.User.old_id == record_dict.pop("author")
                ))
            if created_by:
                new_arb.created_by_id = created_by.id

            for key, value in record_dict.items():
                if value and isinstance(value, list):
                    setattr(new_arb, key, value[0])
                    continue
                setattr(new_arb, key, value)
            current_version = db.scalar(select(models.Record).where(models.Record.old_id.ilike(record_dict.get("parent"))))
            print(record_dict.get("parent"))
            if current_version:
                current_version.previous_versions.append(new_arb)
                new_arb.current_version.append(current_version.id)
                db.add(new_arb)
                db.commit()
            
migrate_records()