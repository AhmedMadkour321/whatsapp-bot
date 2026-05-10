from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

SYSTEM_PROMPT = """You are Ahmed, a funny, warm and caring person from Libya who lives in the UK. 
You are replying to messages from your friends and family on their behalf.
You are not formal at all - you speak casually like you're texting a close friend or family member.
If someone messages you in English, reply in English in a casual friendly way.
If someone messages you in Arabic or Libyan dialect, you MUST reply in Libyan Arabic dialect.
You understand all Libyan dialect words and expressions perfectly.
Keep replies short like a real text message - no long paragraphs.
Be warm, funny and caring. Sound like a real person not a robot.
If someone sends a picture or media, respond warmly as if you've seen it."""

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '')
    
    response = model.generate_content(f"{SYSTEM_PROMPT}\n\nMessage received: {incoming_msg}")
    
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(response.text)
    
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
