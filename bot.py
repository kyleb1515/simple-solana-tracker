from solana.rpc.api import Client
from solana.publickey import PublicKey
import time
import os
from dotenv import load_dotenv

load_dotenv()

class PriceTracker:
    def __init__(self):
        self.client = Client("https://api.mainnet-beta.solana.com")
        
    def check_price(self, token_address):
        try:
            # Convert string address to Pubkey
            pubkey = PublicKey(token_address)
            account_info = self.client.get_account_info(pubkey)
            print(f"Price data: {account_info}")
            return account_info
        except Exception as e:
            print(f"Error: {e}")
            return None

    def run(self, token_address):
        while True:
            self.check_price(token_address)
            time.sleep(60)

def main():
    tracker = PriceTracker()
    # SOL/USDC pool address
    token_address = "9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT"
    tracker.run(token_address)

if __name__ == "__main__":
    main()
