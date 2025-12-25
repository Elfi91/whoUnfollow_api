import json
from requests import Response, RequestException
from client_gemini import get_stat_from_gemini
from client_github import fetch_users
from config import base_url
import re
from repository import create_record, save_json_db, get_data_from_db

def get_report_by_data(data_str: str) -> None:
    db_content = get_data_from_db("db/db.json")
    trovato = False

    for i, record in enumerate(db_content):
        data_record = record['creationAt']
        trovato = False

        # Ci mostra cosa sta confrontando. (Rimuovila quando hai risolto!)
        print(f"👀 Controllo: '{data_record}' inizia con '{data_str}'?")
        # -------------------

        if data_record.startswith(data_str):
            trovato = True

            if i == 0:
                print("⚠️ Questo è il primo giorno del database: impossibile fare confronti con il passato.")
                print(f"Follower totali: {record['numberOfUsers']}")
                break

            if i > 0:
                record_oggi = record
                record_ieri = db_content[i - 1]
                print(f"Confornta i dati del {data_record} con quelli del {record_ieri['creationAt']}")
        
            set_oggi = set(record_oggi['users'])
            set_ieri = set(record_ieri['users'])

            nuovi = set_oggi - set_ieri
            persi = set_ieri - set_oggi

            print(f"👋🏽 Nuovi followers: {len(nuovi)} -> {nuovi}")
            print(f"😢 Hanno smesso di seguirti: {len(persi)} -> {persi}")

            break

    if not trovato:
        print(f"❌Nessun recordo trovato in questa data")


def get_last_record_time() -> str:
    "Recupera l'orario di creazione dell'ultimo record salvato."
    db_content = get_data_from_db("db/db.json")

    if not db_content:
        return "Nessun record trovato nel database"
    
    ultimo_record = db_content[-1]
    return f"Record creato il: {ultimo_record['creationAt']}"

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
        print(f"Sto contattando pagina:{page}...")
        response = fetch_users(url, page)

        if response.status_code != 200:
            print(f"⚠ ERRORE GITHUB: {response.status_code}")
            print(f"Messaggio: {response.json()}")
            break

        data = response.json()

        if not isinstance(data, list):
            print(f"⚠️Risposta inattesa da GitHub: {data}")
            break

        users.extend(data)

        if len(data) == 0 or not has_next_page(response):
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
        username_list = extract_usernames(data)
        record = create_record(username_list)
        save_json_db("db/db.json", record)

        print(f"Salvati {len(username_list)} follower!")

    except RequestException as e:
        print(f"Errore di connessione: {e}")
    except json.JSONDecodeError as e:
        print(f"Errore nel database: {e}")
    except OSError as e:
        print(f"Errore file system: {e}")


def get_statistiche() -> None:
    print("Hai scelto di prendere le statistiche")
    db_content = get_data_from_db("db/db.json")
    get_stat_from_gemini(db_content)