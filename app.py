from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    try:
        user_id = data['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
        message_text = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']

        message_text = message_text.lower()

        if message_text == 'hello':
            send_message(user_id, "Hi there! How can I help?")
        elif message_text == 'help':
            send_message(user_id, "I can assist you with info or questions.")
        elif message_text == 'who made you':
            send_message(user_id, "My creator is Leslie Sarai.")
        else:
            send_message(user_id, "You said: " + message_text)

    except Exception as e:
        print(f"Error: {e}")

    return 'OK', 200

@app.route('/webhook', methods=['GET'])
def verify():
    verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN')
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == verify_token:
        return request.args.get("hub.challenge"), 200
    return "Verification failed", 403

def send_message(user_id, message):
    token = os.getenv('WHATSAPP_API_TOKEN')
    phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": user_id,
        "type": "text",
        "text": {
            "body": message
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code}, {response.text}")
    return response.status_code == 200

if __name__ == '__main__':
    app.run(debug=True)
