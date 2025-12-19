from google import genai
from config import gemini_api_key

client = genai.Client(api_key=gemini_api_key)

def get_stat_from_gemini(data: list) -> str:
    response = client.models.generate_content_stream(
        model="gemini-3-flash-preview", 
        contents=f"""
        Analizza i dati che trovi in allegato e fanno riferimento al profilo github di Elfi91.
        Restituisci un'analisi dettagliata con delle statistiche di andamento del suo profilo.
        Restituisci anche una serie di consigli che gli permetta di crescere nella
        
        Dati:
        {str(data)}
        """
    )

    for chunk in response:
        print(chunk.text, end="", flush=True)