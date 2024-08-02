import time
import requests
from solana.rpc.api import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Solana client
solana_client = Client("https://api.mainnet-beta.solana.com")

# Wallet address to monitor
wallet_address = os.getenv('69ngexW9UkgRp5KFjLpaK9XNSCxUFmps6jYmqhK3q6m9')

# Telegram bot details
telegram_bot_token = os.getenv('7455667006:AAF8ikJwtLU0jIouB1WJ9SWsXt7ZhKKIpTE')
public_trading_bot_username = os.getenv('@solana_trojanbot')  # e.g., '@PublicTradingBot'

# Function to get token accounts for a given wallet address
def get_token_accounts(wallet_address):
    response = solana_client.get_token_accounts_by_owner(wallet_address)
    return response['result']['value']

# Function to send a message to a public Telegram bot
def send_telegram_message_to_bot(bot_username, message):
    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
    payload = {
        'chat_id': bot_username,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()

# Function to check for new tokens and forward to the trading bot
def monitor_wallet():
    seen_tokens = set()

    while True:
        token_accounts = get_token_accounts(wallet_address)

        for account in token_accounts:
            token_address = account['pubkey']

            if token_address not in seen_tokens:
                print(f"New token detected: {token_address}")
                # Add the token to the seen set
                seen_tokens.add(token_address)
                
                # Forward token address to the public trading bot
                message = f"New token minted: {token_address}"
                send_telegram_message_to_bot(public_trading_bot_username, message)

        time.sleep(30)  # Adjust the sleep interval as needed

if __name__ == "__main__":
    monitor_wallet()
