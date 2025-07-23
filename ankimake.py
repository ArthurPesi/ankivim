import base64
from gtts import gTTS
import sys
import requests

decks = {
    "いや": "ja",
    "ARRIBA DOS": "es",
    "GESCHWINDIGKEITSBEGRENZUNG": "ge"
}

def get_models():
    payload = {
        "action": "modelNames",
        "version": 6
    }

    response = requests.post("http://localhost:8765", json=payload)
    result = response.json()
            
    if 'result' not in result:
        print('erro grgr')
        return
        
    for model in result['result']:
        print(model)


def add_anki_card(deck_name, front_text, back_text):
    audio_obj = gTTS(text=front_text, lang='ja')
    audio_filename = front_text + ".mp3"
    audio_path = "/home/pesi/dsa/autoanki/audio/" + audio_filename
    audio_obj.save(audio_path)
    with open(audio_path, 'rb') as audio_file:
        audio_data = audio_file.read()

    store_audio_payload = {
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": audio_filename,
            "data": base64.b64encode(audio_data).decode('utf-8')
            }
        }

    response = requests.post("http://localhost:8765", json=store_audio_payload)
    result = response.json()

    if result.get('error') is not None:
        print("Error:", result)
        return


    back = f"{back_text}<br>[sound:{audio_filename}]"

        
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": "Basic-2e928",
                "fields": {
                    "Front": front_text,
                    "Back": back
                },
                "options": {
                    "allowDuplicate": True
                },
                "tags": []
            }
        }
    }

    # Send request to AnkiConnect
    response = requests.post("http://localhost:8765", json=payload)
    result = response.json()

    if 'error' in result and result['error'] is not None:
        print('Error:', result)
        return


if __name__ == "__main__":
    file = sys.argv[1]
    decks_list = list(decks.keys())
    curr_deck = "いや"
    with open(file) as f:
        for line in f:
            line_string = line[:-1]
            if line_string in decks_list:
                curr_deck = line_string
                continue
            final_form = line.split(' - ')
            add_anki_card(curr_deck, final_form[0], final_form[1])
