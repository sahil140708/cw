import telebot
import json
import os
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from flask import Flask, request
import logging

# Initialize Flask app for webhooks
app = Flask(__name__)

# Initialize bot with token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables")
bot = telebot.TeleBot(TOKEN, state_storage=StateMemoryStorage())

# Define states for conversation flow
class BotStates(StatesGroup):
    AWAITING_CHAT_ID = State()

# Sample function to load career will batches from a JSON file
def load_batches():
    try:
        with open("career_will_batches.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"batches": []}

# Command: /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Career Will Bot! Use /list to view batches or /upload to share batches to a chat.")

# Command: /list - Display available batches
@bot.message_handler(commands=['list'])
def list_batches(message):
    batches = load_batches().get("batches", [])
    if not batches:
        bot.reply_to(message, "No batches available.")
        return
    
    response = "Available Batches:\n"
    for batch in batches:
        response += (f"Course: {batch['course_name']}\n"
                     f"Batch ID: {batch['batch_id']}\n"
                     f"Start Date: {batch['start_date']}\n"
                     f"Details: {batch['details']}\n\n")
    bot.reply_to(message, response)

# Command: /upload - Start the upload process
@bot.message_handler(commands=['upload'])
def upload_batches(message):
    bot.reply_to(message, "Please provide the Chat ID of the group/channel where you want to upload the batches.")
    bot.set_state(message.from_user.id, BotStates.AWAITING_CHAT_ID, message.chat.id)

# Handle Chat ID input
@bot.message_handler(state=BotStates.AWAITING_CHAT_ID)
def process_chat_id(message):
    chat_id = message.text
    try:
        # Validate Chat ID by sending a test message
        bot.send_message(chat_id, "Test message to verify Chat ID.")
        
        # Load and send batches
        batches = load_batches().get("batches", [])
        if not batches:
            bot.reply_to(message, "No batches available to upload.")
            bot.delete_state(message.from_user.id, message.chat.id)
            return
        
        response = "Career Will Batches:\n"
        for batch in batches:
            response += (f"Course: {batch['course_name']}\n"
                         f"Batch ID: {batch['batch_id']}\n"
                         f"Start Date: {batch['start_date']}\n"
                         f"Details: {batch['details']}\n\n")
        
        bot.send_message(chat_id, response)
        bot.reply_to(message, f"Batches uploaded to chat {chat_id} successfully!")
    except telebot.apihelper.ApiTelegramException as e:
        bot.reply_to(message, f"Error: Invalid Chat ID or bot lacks permission. Please ensure the bot is an admin in the group/channel. Error: {str(e)}")
    finally:
        bot.delete_state(message.from_user.id, message.chat.id)

# Handle invalid commands
@bot.message_handler(func=lambda message: True)
def handle_invalid(message):
    bot.reply_to(message, "Unknown command. Use /start, /list, or /upload.")

# Flask route for webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "", 200
    return "", 403

# Main entry point
if __name__ == "__main__":
    # Remove existing webhook and set new one for Render
    bot.remove_webhook()
    # Use RENDER_EXTERNAL_URL from Render environment, or fallback to localhost for testing
    WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL", "http://localhost:5000") + f"/{TOKEN}"
    bot.set_webhook(url=WEBHOOK_URL)
    # Start Flask app
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)