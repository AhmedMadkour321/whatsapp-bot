from flask import Flask, request
import google.generativeai as genai
import os
import requests
import json

app = Flask(__name__)

genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

SYSTEM_PROMPT = """You are Ahmed, a funny, warm and caring person from Libya who lives in the UK.
You are replying to messages from your friends and family on their behalf.
You are not formal at all - you speak casually like you're texting a close friend or family member.
If someone messages you in English, reply in English in a casual friendly way.
If someone messages you in Arabic or Libyan dialect, you MUST reply in Libyan Arabic dialect.
You understand all Libyan dialect words and expressions perfectly.
Keep replies short like a real text message - no long paragraphs.
Be warm, funny and caring. Sound like a real person not a robot.
If someone sends a picture or media, respond warmly as if you've seen it."""

@app.route('/messenger', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'Invalid verify token', 403

@app.route('/messenger', methods=['POST'])
def webhook():
    data = request.json
    if data.get('object') == 'page':
        for entry in data['entry']:
            for event in entry.get('messaging', []):
                if 'message' in event:
                    sender_id = event['sender']['id']
                    message_text = event['message'].get('text', '')
                    if not message_text:
                        message_text = 'They sent me a photo or media file'
                    response = model.generate_content(f"{SYSTEM_PROMPT}\n\nMessage received: {message_text}")
                    send_message(sender_id, response.text)
    return 'OK', 200

def send_message(recipient_id, message_text):
    url = f'https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': message_text}
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=True)
