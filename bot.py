from solders.pubkey import Pubkey
import requests
import time
from datetime import datetime

class PriceTracker:
    def __init__(self):
        self.endpoint = "https://api.mainnet-beta.solana.com"
        self.last_price = None
        # Raydium SOL/USDC pool
        self.price_pool = "58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2"

    def get_sol_price(self):
        try:
            response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT").json()
            return float(response['price'])
        except:
            return None

    def check_price(self, token_address):
        try:
            # Get SOL/USD price
            sol_price = self.get_sol_price()
            
            pubkey = Pubkey.from_string(token_address)
            response = requests.post(
                self.endpoint,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getAccountInfo",
                    "params": [str(pubkey), {"encoding": "jsonParsed"}]
                }
            ).json()
            
            if 'result' in response and response['result'] and 'value' in response['result']:
                lamports = response['result']['value']['lamports']
                sol_amount = lamports / 1_000_000_000  # Convert to SOL
                
                # Calculate change
                if self.last_price:
                    change = ((sol_amount - self.last_price) / self.last_price) * 100
                    change_str = f"Change: {change:+.2f}%"
                else:
                    change_str = "Change: --"

                # Print info with current time and SOL price
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}]")
                print(f"Pool SOL Amount: {sol_amount:.8f}")
                if sol_price:
                    print(f"SOL Price: ${sol_price:.2f}")
                    print(f"Pool Value: ${sol_amount * sol_price:.2f}")
                print(change_str)
                print("-" * 40)
                
                self.last_price = sol_amount

        except Exception as e:
            print(f"Error: {e}")

    def run(self):
        print("Starting Solana Price Tracker...")
        print("Press Ctrl+C to stop")
        print("-" * 40)
        
        # Using Raydium SOL/USDC pool
        token_address = self.price_pool
        
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