from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
import time
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

class PriceTracker:
    def __init__(self):
        self.client = Client("https://api.mainnet-beta.solana.com")
        self.last_prices = {}
        self.alert_thresholds = {
            "high": 1.1,  # Alert if price increases by 10%
            "low": 0.9    # Alert if price decreases by 10%
        }
        self.data_file = "price_history.json"
        
    def save_to_file(self, token_address, price_data):
        try:
            # Load existing data
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {}
                
            # Add new data
            if token_address not in data:
                data[token_address] = []
            data[token_address].append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'price': price_data,
                'slot': self.last_slot
            })
            
            # Save updated data
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
                
        except Exception as e:
            print(f"Error saving data: {e}")

    def check_alerts(self, token_address, current_price):
        if token_address in self.last_prices:
            change = current_price / self.last_prices[token_address]
            if change > self.alert_thresholds["high"]:
                print(f"\n🚨 ALERT: Price increased by {(change-1)*100:.2f}%!")
            elif change < self.alert_thresholds["low"]:
                print(f"\n🚨 ALERT: Price decreased by {(1-change)*100:.2f}%!")

    def check_price(self, token_addresses):
        try:
            for address in token_addresses:
                pubkey = Pubkey.from_string(address)
                account_info = self.client.get_account_info(pubkey)
                
                # Extract SOL amount
                lamports = account_info.value.lamports
                sol_amount = lamports / 1_000_000_000
                self.last_slot = account_info.context.slot
                
                # Calculate percentage change
                if address in self.last_prices:
                    change = ((sol_amount - self.last_prices[address]) / self.last_prices[address]) * 100
                    change_str = f"Change: {change:+.2f}%"
                else:
                    change_str = "Change: --"
                    
                # Get current time
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                print(f"\n[{current_time}]")
                print(f"Pool Address: {address}")
                print(f"SOL Amount: {sol_amount:.8f}")
                print(f"Slot: {self.last_slot}")
                print(change_str)
                print("-" * 50)
                
                # Check for price alerts
                self.check_alerts(address, sol_amount)
                
                # Save data
                self.save_to_file(address, sol_amount)
                
                self.last_prices[address] = sol_amount
                
        except Exception as e:
            print(f"Error: {e}")

    def run(self, token_addresses, update_frequency=60):
        print("Starting Solana Price Tracker...")
        print(f"Update frequency: {update_frequency} seconds")
        print("Press Ctrl+C to stop")
        print("-" * 50)
        while True:
            try:
                self.check_price(token_addresses)
                time.sleep(update_frequency)
            except KeyboardInterrupt:
                print("\nStopping tracker...")
                break

def main():
    tracker = PriceTracker()
    # Multiple pool addresses to track
    token_addresses = [
        "9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT",  # Original pool
        "8HoQnePLqPj4M7PUDzfw8e3Ymdwgc7NLGnaTUapubyvu",  # Another SOL pool
    ]
    # Update every 30 seconds
    tracker.run(token_addresses, update_frequency=30)

if __name__ == "__main__":
    main()
