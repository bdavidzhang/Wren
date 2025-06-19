# main.py
# This is a simple backend server using Python and the Flask framework.
# It creates a webhook that listens for incoming messages from Twilio,
# forwards them to the OpenAI API, and sends the response back.

import os
import openai
import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

CONVERSATION_FILE = "conversation_history.json"

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY") 
base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
client = openai.OpenAI(api_key=api_key,base_url=base_url)
app = Flask(__name__)


def load_conversation_history():
    if os.path.exists(CONVERSATION_FILE):
        with open(CONVERSATION_FILE, "r") as f:
            return json.load(f)
    return {}

def save_conversation_history(history):
    with open(CONVERSATION_FILE, "w") as f:
        json.dump(history, f, indent=4)

conversation_history = load_conversation_history()

MOTIVATIONAL_COACH_PROMPT = {
    "role": "system",
    "content": (
        "You are 'Wren,' a compassionate and supportive motivational coach. "
        "Your purpose is to help users navigate feelings of stress and depression. "
        "Your tone should always be empathetic, patient, and encouraging. "
        "Never give medical advice, a diagnosis, or treatment plans. You are a supportive guide, not a clinician. "
        "If the user's situation sounds severe or they mention self-harm, gently guide them to seek professional help immediately by providing the number for a crisis hotline like the National Suicide Prevention Lifeline: 988. "
        "Start conversations by introducing yourself warmly. Ask open-ended questions to understand what's on their mind (e.g., 'What's been on your mind today?' or 'How are you feeling right now?'). "
        "Provide actionable, gentle advice, like suggesting mindfulness exercises, a short walk, journaling, or breaking down large tasks into smaller steps. "
        "Keep your responses concise but warm, and use formatting like new lines to make them easy to read on a phone."
        "You can only send messages up to 160 characters, so keep it concise."
    )
}



# --- Webhook Endpoint ---
@app.route("/webhook", methods=["POST"])
def webhook():
    """
    This function is triggered when Twilio sends a POST request to /webhook.
    It processes the incoming message, gets a response from OpenAI, and sends it back.
    """
    # Get the sender's phone number and the message body from the incoming request
    sender_id = request.values.get('From', None) # e.g., 'whatsapp:+14155238886'
    incoming_msg = request.values.get('Body', '')

    print(f"Received message from {sender_id}: {incoming_msg}")

    if not sender_id:
        # If we can't identify the sender, don't proceed.
        return "Failed to identify sender.", 400

    # Start or continue a conversation using the sender's phone number as a unique key
    if sender_id not in conversation_history:
        # Start a new conversation history for a new user with a system prompt
        conversation_history[sender_id] = [MOTIVATIONAL_COACH_PROMPT]
        print(f"Starting new coaching session for {sender_id}")

    # Add the new user message to their conversation history
    conversation_history[sender_id].append({"role": "user", "content": incoming_msg})
    save_conversation_history(conversation_history)

    try:
        # --- Get response from OpenAI API ---
        completion = client.chat.completions.create(
            model="deepseek-chat",  
            messages=conversation_history[sender_id],
            max_tokens = 100
        )
        
        # Extract the response text from the API result
        response_text = completion.choices[0].message.content
        print(f"AI Response: {response_text}")

        # Add the AI's response to the history to maintain context for the next turn
        conversation_history[sender_id].append({"role": "assistant", "content": response_text})
        save_conversation_history(conversation_history)


        # --- Send the response back to the user via Twilio ---
        # Create a TwiML response object
        twilio_resp = MessagingResponse()
        # Add the AI's message to the response
        twilio_resp.message(response_text)

        # Return the TwiML response as a string
        return str(twilio_resp)

    except Exception as e:
        print(f"An error occurred with OpenAI API: {e}")
        # If something goes wrong, send a generic error message to the user
        error_resp = MessagingResponse()
        error_resp.message("Sorry, I'm having trouble connecting to my brain right now. Please try again later.")
        return str(error_resp)


# --- Main Entry Point ---
if __name__ == "__main__":
    # The debug=True flag allows for hot-reloading when you save changes.
    # The host='0.0.0.0' makes the server accessible from your network.
    # The port can be any available port.
    app.run(host="0.0.0.0", port=5001, debug=True)
