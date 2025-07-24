import base64
from gtts import gTTS
import os
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
    audio_obj = gTTS(text=front_text, lang=decks[deck_name])
    audio_filename = front_text + ".mp3"
    try:
        cwd = os.getcwd()
        audio_path = cwd + "/" + audio_filename
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
            print("Audio file upload failed:", result['error'])
            sys.exit(1)

        os.remove(audio_filename)
    except(IOError, OSError) as file_error:
        print(f"Error in audio file operation: {file_error}")
        sys.exit(1)
    except Exception as e:
        print("An inexpected error has occurred during audio file creation:", e)
        sys.exit(1)

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
                    "allowDuplicate": False
                },
                "tags": []
            }
        }
    }

    # Send request to AnkiConnect
    response = requests.post("http://localhost:8765", json=payload)
    result = response.json()

    if 'error' in result and result['error'] is not None:
        print(f'The card {front_text} produced an error:', result['error'])
        sys.exit(1)


if __name__ == "__main__":
    file = 'cards.txt'
    decks_list = list(decks.keys())
    curr_deck = "いや"
    empty_file = True

    try:
        with open(file) as f:
            for line in f:
                line_string = line[:-1]
                if line_string in decks_list:
                    curr_deck = line_string
                    continue
                final_form = line.split(' - ')
                if len(final_form) != 2:
                    print("Error: malformed statement:", line_string)
                    sys.exit(1)
                empty_file = False
                add_anki_card(curr_deck, final_form[0], final_form[1])

    except (IOError, OSError) as file_error:
        print(f"An error has occurred trying to open the file {file}:", file_error)
        sys.exit(1)
    except Exception as e:
        print("An inexpected error has occurred in the main loop:", e)

    if empty_file:
        print("File has no entries, skipping")
        sys.exit(1)

    try:
        with open(file, 'w') as f:
            for deck_name in decks_list:
                f.write(deck_name + "\n")
    except (IOError, OSError) as file_error:
        print(f"An error has occurred trying to write to the file {file}:", file_error)
    except Exception as e:
        print(f"An inexpected error has occurred trying to write to the file {file}:", e)

