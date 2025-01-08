from solders.pubkey import Pubkey
from solders.rpc.config import RpcConfig
from solders.rpc.requests import GetAccountInfo
import requests
import time
from datetime import datetime

class PriceTracker:
    def __init__(self):
        self.endpoint = "https://api.mainnet-beta.solana.com"
        self.last_price = None

    def check_price(self, token_address):
        try:
            pubkey = Pubkey.from_string(token_address)
            response = requests.post(
                self.endpoint,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getAccountInfo",
                    "params": [str(pubkey)]
                }
            ).json()
            
            lamports = response['result']['value']['lamports']
            sol_amount = lamports / 1_000_000_000  # Convert to SOL
            
            # Calculate change
            if self.last_price:
                change = ((sol_amount - self.last_price) / self.last_price) * 100
                change_str = f"Change: {change:+.2f}%"
            else:
                change_str = "Change: --"

            # Print info
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}]")
            print(f"SOL Amount: {sol_amount:.8f}")
            print(change_str)
            print("-" * 30)
            
            self.last_price = sol_amount

        except Exception as e:
            print(f"Error: {e}")

    def run(self):
        print("Starting Solana Price Tracker...")
        print("Press Ctrl+C to stop")
        print("-" * 30)
        
        # SOL/USDC pool address
        token_address = "9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT"
        
        while True:
            try:
                self.check_price(token_address)
                time.sleep(30)  # Check every 30 seconds
            except KeyboardInterrupt:
                print("\nStopping tracker...")
                break

if __name__ == "__main__":
    tracker = PriceTracker()
    tracker.run()
