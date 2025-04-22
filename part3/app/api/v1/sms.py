from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# Place tes infos Twilio dans des variables d'environnement pour la sécurité
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'TON_SID_ICI')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'TON_TOKEN_ICI')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', 'TON_NUM_TWILIO_ICI')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/api/v1/send_review_sms', methods=['POST'])
def send_review_sms():
    data = request.get_json()
    to_number = data.get('to_number')
    place_id = data.get('place_id')

    if not to_number or not place_id:
        return jsonify({'status': 'error', 'error': 'Numéro ou place_id manquant'}), 400

    # Message personnalisé, tu peux l'adapter
    message_body = f"Merci pour votre réservation ! Donnez votre avis sur le logement (ID: {place_id}) sur notre site."

    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return jsonify({'status': 'ok', 'sid': message.sid})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
