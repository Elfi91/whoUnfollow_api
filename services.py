import json
from requests import Response, RequestException
from config import base_url
from client_github import fetch_users
from repository import create_record, save_json_db
import re

def extract_usernames(users: list[dict]) -> list[str]:
    usernames: list[str] = []
    for user in users:
        usernames.append(user["login"])

    return usernames


def has_next_page(response: Response) -> bool:
    "Verifica se esiste un'altra pagina per prender ei followers"
    link_header = response.headers.get("Link", "")
    return "next" in link_header


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

def is_valid_username_format(username: str) -> bool:
    """Controlla che il formato sia accettabile per GitHub"""
    if not username or not username.strip():
        return False
    if username.strip().lower() == "exit":
        return False
    return bool(re.match(r'^[a-zA-Z0-9-]{1,39}$', username.strip()))

def prompt_for_valid_username() -> str | None:
    """Chiede username finché non è valido o l'utente esce"""
    while True:
        username = input("Inserisci l'username GitHub: ").strip()

        if username.lower() == "exit":
            return None

        if not is_valid_username_format(username):
            print("Formato non valido. Usa solo lettere, numeri e trattini.")
            continue

        return username

def get_followers() -> None:
    try:
        username = prompt_for_valid_username()
       
        if username is None:
            print("Operazione annullata.")
            return

        data = get_all_follower_from_pages(username)
        username = extract_usernames(data)
        record = create_record(username)
        save_json_db("db/db.json", record)

        print(f"Salvati {len(username)} follower!")

    except RequestException as e:
        print(f"Errore di connessione: {e}")
    except json.JSONDecodeError as e:
        print(f"Errore nel database: {e}")
    except OSError as e:
        print(f"Errore file system: {e}")

