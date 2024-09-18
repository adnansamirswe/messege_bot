import logging
import asyncio
from telegram import Bot
from telegram.ext import Application
from telegram.error import TelegramError
from flask import Flask, jsonify
from threading import Thread

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = '7219760373:AAEKs59IFvgomVyiEIKUChSvXviASda_j-o'
CHAT_ID = '-4507010052'

app = Flask(__name__)

async def send_and_delete():
    bot = Bot(TOKEN)
    try:
        logger.info("Sending message to group...")
        message_text = """
        To purchase, please inbox the Group Admin @admi_n65.
        Here are our packages:

        SOCKS-5 Proxy:
        - Monthly Packages:
            - 100mbps: 160 taka
            - 50mbps: 100 taka
            - 30mbps: 70 taka
            - 20mbps: 50 taka

        SOCKS-5 Proxy With FTP:
        - Monthly Packages:
            - 100mbps: 200 taka
            - 50mbps: 150 taka
            - 30mbps: 100 taka
            - 20mbps: 80 taka
        Available FTP: ICC, Dhakhaflix, Discovery-dflix 
        
Please remember to only purchase from the group Admin @admi_n65 ✅
        """
        message = await bot.send_message(chat_id=CHAT_ID, text=message_text)
        message_id = message.message_id
        logger.info(f"Message sent, message_id: {message_id}")
        await asyncio.sleep(300)  # Wait 5 minutes (300 seconds)
        logger.info(f"Deleting message {message_id}")
        await bot.delete_message(chat_id=CHAT_ID, message_id=message_id)
        logger.info("Message deleted.")
    except TelegramError as e:
        logger.error(f"Telegram API error: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

def run_asyncio_task():
    asyncio.run(send_and_delete())  # Run the asyncio event loop for sending and deleting the message

@app.route('/trigger', methods=['GET'])
def trigger_message():
    logger.info("Trigger received via HTTP request")
    thread = Thread(target=run_asyncio_task)  # Run the asyncio function in a separate thread
    thread.start()
    return jsonify({"status": "Message sent and will be deleted in 5 minutes."}), 200

if __name__ == '__main__':
    logger.info("Starting the Flask app...")
    app.run(host='0.0.0.0', port=5000)
