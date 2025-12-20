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
                """
                1. Seleziono il giorno
                    L'utente scrive una data (es: "19-12-2025").
                        La stringa deve essere identica a come è salvata nel JSON (o devo cercare solo la parte iniziale della data).

                2. Cerca nel Database le informazioni che mi servono:
                    Come?
                    a. scorro la lista db_content.
                    b. Trovo il record che corrisponde alla data inserita (record_scelto).
                    c. Trovo il record immediatamente precedente a quello (record_precedente).
                        E se il giorno scelto è il primissimo del database? (Non c'è un precedente con cui confrontarsi - ERROR). 
                
                3. Calcolo delle Differenze (Il cuore dell'algoritmo)
                    Logica degli insiemi (Set Theory).
                    a. Nuovi Follower: Sono le persone che sono nel record_scelto MA non sono nel record_precedente.
                    b. Unfollow: Sono le persone che erano nel record_precedente MA non sono nel record_scelto.      
                
                4. Creo il report 
                    report = 
                    {
                    "data": "...",
                    "totale_ad oggi": 105,
                    "nuovi_follower": 
                    "persi":
                    }
                            +
                5. Invio a Gemini
                    a. Passo questo report: Dict a Gemini e gli chiedo di stampare un riassunto 
                        nuovi_follower = 
                        persi =
                        totale =
                """
            case "4":
                print(get_last_record_time())
            case "exit":
                print("Perfetto, programma terminato")
                break
            case _:
                print("Inserisci un'opzione valida")



if __name__ == "__main__":
    main()