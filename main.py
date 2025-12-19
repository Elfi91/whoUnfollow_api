from console import print_menu
from services import get_followers, get_last_record_time, get_statistiche

def main() -> None: 

    while True:
        print_menu()

        option = input("Seleziona l'operazion che vuoi eseguire:")

        match option:
            case "1":
                get_followers()
            case "2":
                get_statistiche()
            case "3":
                print("Di guardare i dati di un giorno specifico")
            case "4":
                print(get_last_record_time())
            case "exit":
                print("Perfetto, programma terminato")
                break
            case _:
                print("Inserisci un'opzione valida")



if __name__ == "__main__":
    main()