import datetime
import uuid
import os
import json
from requests import get, Response
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("BASE_URL")
github_token = os.getenv("GITHUB_TOKEN")


def get_all_follower_from_pages(username: str) -> list [dict]:
    "Prende tutte le pagine con i follower e ne restituisce la lista accorpata"
    url = f"{base_url}/users/{username}/followers"
    page: int = 1
    users: list = []

    while True: 
        print(f"Sto contattando pagina:{page}")
        response = fetch_users(url, page,)

        users.extend(response.json())

        if not has_next_page(response):
            break

        page = page + 1

    return users

def has_next_page(response: Response) -> bool:
    "Verifica se esiste un'altra pagina per prender ei followers"
    link_header = response.headers.get("Link", "")
    return "next" in link_header


def fetch_users(url: str, page: int) -> list[dict]:
    headers = {
            "Authorization": f"Bearer {github_token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    return get(f"{url}?page={page}", headers=headers)

def extract_usernames(users: list[dict]) -> list[str]:
    usernames: list[str] = []
    for user in users:
        usernames.append(user["login"])

    return usernames

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


def main() -> None:
    print("Inizio programma")
    '''
    lista_test = extract_usernames(DATA)

    record = create_record(lista_test)

    save_json_db("db/db.json", record)
    print("fine programma)
    '''

    data = get_all_follower_from_pages("emanuelegurini")
    print(extract_usernames(data))


if __name__ == "__main__":
    main()