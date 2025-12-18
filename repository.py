import json
import datetime
import uuid
import os

def create_record(usernames: list[str]) -> dict:
    """Crea l'oggetto record da salvare nel db"""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    clean_date = now_utc.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    return {
        'id' : str(uuid.uuid4()),
        'creationAt' : clean_date,
        'users' : usernames,
        'numberOfUsers' : len(usernames),
    }

def create_json_db(db_name: str) -> bool:
    """Crea un nuovo file db con lista vuota."""
    # Crea la cartella se non esiste
    os.makedirs(os.path.dirname(db_name), exist_ok=True)

    with open(db_name, "w") as f:
        f.write("[]")
    return True

def check_if_json_db_has_correct_shape(db_name: str) -> bool:
    """Verifica che il db esiste ed è nella forma corretta."""
    if not os.path.isfile(db_name):
        return False
    
    with open(db_name, "r") as f:
        data = json.load(f)
        return isinstance(data, list)
        

def save_json_db(db_name: str, new_value: dict) -> None:
    """Salva il nuovo oggetto nel db."""
    if not check_if_json_db_has_correct_shape(db_name):
        create_json_db(db_name)
    
    db: list[dict] = []

    with open(db_name, "r") as f:
        db.extend(json.load(f))

    db.append(new_value)

    with open(db_name, "w") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)